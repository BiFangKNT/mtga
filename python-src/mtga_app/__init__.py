# ruff: noqa: E402
from __future__ import annotations

import json
import os
import sys
import time
import traceback
from contextlib import suppress
from functools import lru_cache
from importlib import import_module
from pathlib import Path
from threading import Lock, Thread
from typing import Any, cast

from platformdirs import user_data_dir

MTGA_PLATFORM = "tauri"
os.environ.setdefault("MTGA_PLATFORM", MTGA_PLATFORM)


def find_repo_root(start: Path) -> Path:
    p = start
    while True:
        if (p / "modules").exists() and (p / "mtga-tauri").exists():
            return p
        if p.parent == p:
            raise RuntimeError("Repo root not found (expected modules/ and mtga-tauri/).")
        p = p.parent


def _resolve_boot_log_path() -> Path:
    try:
        user_dir = user_data_dir("MTGA", appauthor=False, roaming=os.name == "nt")
    except Exception:
        user_dir = os.path.expanduser("~")
    with suppress(Exception):
        os.makedirs(user_dir, exist_ok=True)
    return Path(user_dir) / "mtga_tauri_boot.log"


_BOOT_LOG_PATH = _resolve_boot_log_path()
_INVOKE_LOCK = Lock()


def _boot_log(message: str) -> None:
    try:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S ")
        with _BOOT_LOG_PATH.open("a", encoding="utf-8") as fh:
            fh.write(f"{timestamp}{message}\n")
    except Exception:
        pass


def _try_push_log(message: str) -> None:
    with suppress(Exception):
        push_log = import_module("modules.runtime.log_bus").push_log
        push_log(message)


def _install_bootstrap_excepthook() -> None:
    original = sys.excepthook

    def handler(exc_type, exc_value, exc_traceback) -> None:
        _boot_log("Uncaught exception during startup:")
        for line in traceback.format_exception(exc_type, exc_value, exc_traceback):
            _boot_log(line.rstrip("\n"))
            _try_push_log(line.rstrip("\n"))
        original(exc_type, exc_value, exc_traceback)

    sys.excepthook = handler


_install_bootstrap_excepthook()
_boot_log("mtga_app init start")


# 统一 .env 入口（显眼开关）
# - MTGA_ENV_FILE=... 指定 env 文件路径（默认使用 mtga-tauri/.env）
# - 已存在的环境变量优先，不会被 .env 覆盖
TAURI_PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = Path(os.environ.get("MTGA_ENV_FILE", str(TAURI_PROJECT_ROOT / ".env")))


def _load_env_file(path: Path) -> None:
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return
    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("export "):
            stripped = stripped[7:].strip()
        if "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        key = key.strip()
        value = value.strip()
        if value and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        if key and key not in os.environ:
            os.environ[key] = value


_load_env_file(ENV_FILE)


def _load_tauri_config(path: Path) -> dict[str, Any] | None:
    try:
        raw = path.read_text(encoding="utf-8")
    except Exception as exc:
        _boot_log(f"tauri_config read failed: {exc}")
        return None
    try:
        return cast(dict[str, Any], json.loads(raw))
    except Exception as exc:
        _boot_log(f"tauri_config parse failed: {exc}")
        return None


# 模块来源控制（显眼开关）
# - MTGA_MODULES_SOURCE=auto|local|root
#   auto(默认): 优先 python-src/modules，找不到再回退仓库根
#   local: 强制使用 python-src/modules
#   root: 强制使用仓库根 modules
# - MTGA_PATH_STRICT=1
#   仅在 local/auto 时生效：要求 python-src/modules 必须存在，否则直接报错
MODULES_SOURCE = os.environ.get("MTGA_MODULES_SOURCE", "").strip().lower()
if not MODULES_SOURCE:
    raise RuntimeError("MTGA_MODULES_SOURCE 未设置（请在 .env 中配置）")

_strict_raw = os.environ.get("MTGA_PATH_STRICT")
if _strict_raw is None:
    raise RuntimeError("MTGA_PATH_STRICT 未设置（请在 .env 中配置）")
if _strict_raw not in {"0", "1"}:
    raise RuntimeError("MTGA_PATH_STRICT 仅支持 0/1")
STRICT_MODE = _strict_raw == "1"
LOCAL_ROOT = Path(__file__).resolve().parent.parent
LOCAL_MODULES = LOCAL_ROOT / "modules"


def _resolve_modules_root() -> Path:
    if MODULES_SOURCE in {"local", "python-src"}:
        if not LOCAL_MODULES.exists():
            raise RuntimeError("MTGA_MODULES_SOURCE=local 但未找到 python-src/modules")
        return LOCAL_ROOT

    if MODULES_SOURCE in {"root", "repo", "repo-root"}:
        return find_repo_root(Path(__file__).resolve())

    if LOCAL_MODULES.exists():
        return LOCAL_ROOT

    if STRICT_MODE:
        raise RuntimeError("MTGA_PATH_STRICT=1 但未找到 python-src/modules")
    return find_repo_root(Path(__file__).resolve())


modules_root = _resolve_modules_root()
if STRICT_MODE and modules_root != LOCAL_ROOT:
    raise RuntimeError("MTGA_PATH_STRICT=1 不允许回退到仓库根 modules")
sys.path.insert(0, str(modules_root))

try:
    from modules.platform.platform_context import get_platform

    get_platform()
except Exception as exc:
    _boot_log(f"Platform detection failed: {exc}")
    _try_push_log(f"平台识别失败: {exc}")
    raise


# 迁移期：仍需仓库根用于版本号读取
try:
    REPO_ROOT = find_repo_root(Path(__file__).resolve())
except RuntimeError:
    REPO_ROOT = TAURI_PROJECT_ROOT

from anyio.from_thread import start_blocking_portal
from pydantic import BaseModel
from pytauri import AppHandle, Commands, Emitter
from pytauri_wheel.lib import builder_factory, context_factory

from modules.runtime.log_bus import pull_logs
from modules.runtime.proxy_step_bus import pull_steps
from modules.runtime.resource_manager import ResourceManager
from modules.services.app_metadata import DEFAULT_METADATA
from modules.services.app_version import resolve_app_version
from modules.services.config_service import ConfigStore

from .commands import (
    register_cert_commands,
    register_hosts_commands,
    register_log_commands,
    register_model_test_commands,
    register_proxy_commands,
    register_startup_commands,
    register_update_commands,
    register_user_data_commands,
)

command_registry = Commands()
register_cert_commands(command_registry)
register_hosts_commands(command_registry)
register_log_commands(command_registry)
register_model_test_commands(command_registry)
register_proxy_commands(command_registry)
register_startup_commands(command_registry)
register_update_commands(command_registry)
register_user_data_commands(command_registry)

_invoke_state: dict[str, Any] = {
    "portal": None,
    "portal_context": None,
    "handler": None,
}


def get_py_invoke_handler() -> Any:
    handler = _invoke_state["handler"]
    if handler is not None:
        return handler
    with _INVOKE_LOCK:
        handler = _invoke_state["handler"]
        if handler is not None:
            return handler
        portal_context = start_blocking_portal("asyncio")
        portal = portal_context.__enter__()
        _invoke_state["portal_context"] = portal_context
        _invoke_state["portal"] = portal
        handler = command_registry.generate_handler(portal)
        _invoke_state["handler"] = handler
        return handler


class GreetPayload(BaseModel):
    name: str


class LogEventPayload(BaseModel):
    items: list[str]
    next_id: int


class SaveConfigPayload(BaseModel):
    config_groups: list[dict[str, Any]]
    current_config_index: int
    mapped_model_id: str | None = None
    mtga_auth_key: str | None = None
    outbound_proxy_enabled: bool | None = None
    outbound_proxy_type: str | None = None
    outbound_proxy_host: str | None = None
    outbound_proxy_port: int | None = None
    outbound_proxy_username: str | None = None
    outbound_proxy_password: str | None = None


@lru_cache(maxsize=1)
def _get_resource_manager() -> ResourceManager:
    return ResourceManager()


@lru_cache(maxsize=1)
def _get_config_store() -> ConfigStore:
    resource_manager = _get_resource_manager()
    return ConfigStore(resource_manager.get_user_config_file())


@command_registry.command()
async def greet(body: GreetPayload) -> str:
    return f"Hello, {body.name}! from Python {sys.version.split()[0]}"


@command_registry.command()
async def load_config() -> dict[str, Any]:
    config_store = _get_config_store()
    config_groups, current_index = config_store.load_config_groups()
    mapped_model_id, mtga_auth_key = config_store.load_global_config()
    outbound_proxy = config_store.load_outbound_proxy_config()
    return {
        "config_groups": config_groups,
        "current_config_index": current_index,
        "mapped_model_id": mapped_model_id,
        "mtga_auth_key": mtga_auth_key,
        **outbound_proxy,
    }


@command_registry.command()
async def save_config(body: SaveConfigPayload) -> bool:
    config_store = _get_config_store()
    return config_store.save_config_groups(
        body.config_groups,
        body.current_config_index,
        body.mapped_model_id,
        body.mtga_auth_key,
        {
            "outbound_proxy_enabled": body.outbound_proxy_enabled,
            "outbound_proxy_type": body.outbound_proxy_type,
            "outbound_proxy_host": body.outbound_proxy_host,
            "outbound_proxy_port": body.outbound_proxy_port,
            "outbound_proxy_username": body.outbound_proxy_username,
            "outbound_proxy_password": body.outbound_proxy_password,
        },
    )


@command_registry.command()
async def get_app_info() -> dict[str, Any]:
    metadata = DEFAULT_METADATA
    version = resolve_app_version(project_root=REPO_ROOT)
    resource_manager = _get_resource_manager()
    default_user_data_dir = user_data_dir(
        "MTGA",
        appauthor=False,
        roaming=os.name == "nt",
    )
    return {
        "display_name": metadata.display_name,
        "version": version,
        "github_repo": metadata.github_repo,
        "ca_common_name": metadata.ca_common_name,
        "api_key_visible_chars": metadata.api_key_visible_chars,
        "user_data_dir": resource_manager.user_data_dir,
        "default_user_data_dir": default_user_data_dir,
    }


def _start_log_event_stream(app_handle: AppHandle) -> None:
    def run() -> None:
        after_id: int | None = None
        while True:
            try:
                result = pull_logs(
                    after_id=after_id,
                    timeout_ms=1000,
                    max_items=200,
                )
            except Exception as exc:
                _boot_log(f"log stream pull failed: {exc}")
                time.sleep(0.2)
                continue

            if not isinstance(result, dict):
                time.sleep(0.2)
                continue

            items = result.get("items")
            next_id = result.get("next_id")
            if isinstance(next_id, int):
                after_id = next_id
            if isinstance(items, list) and items:
                try:
                    payload = LogEventPayload(
                        items=[str(item) for item in items],
                        next_id=after_id or 0,
                    )
                    Emitter.emit(app_handle, "mtga:logs", payload)
                except Exception as exc:
                    _boot_log(f"log stream emit failed: {exc}")
                    time.sleep(0.2)

    Thread(target=run, name="mtga-log-stream", daemon=True).start()


def _start_proxy_step_event_stream(app_handle: AppHandle) -> None:
    def run() -> None:
        after_id: int | None = None
        while True:
            try:
                result = pull_steps(
                    after_id=after_id,
                    timeout_ms=1000,
                    max_items=200,
                )
            except Exception as exc:
                _boot_log(f"proxy step pull failed: {exc}")
                time.sleep(0.2)
                continue

            if not isinstance(result, dict):
                time.sleep(0.2)
                continue

            items = result.get("items")
            next_id = result.get("next_id")
            if isinstance(next_id, int):
                after_id = next_id
            if isinstance(items, list) and items:
                for item in items:
                    try:
                        Emitter.emit_str(app_handle, "mtga:proxy-step", str(item))
                    except Exception as exc:
                        _boot_log(f"proxy step emit failed: {exc}")
                        time.sleep(0.2)

    Thread(target=run, name="mtga-proxy-step-stream", daemon=True).start()


def main() -> int:
    # 开发期：让 Tauri 加载 Nuxt dev server
    dev_server = os.environ.get("DEV_SERVER")
    src_tauri_dir = os.environ.get("MTGA_SRC_TAURI_DIR")
    src_tauri_path = (
        Path(src_tauri_dir).expanduser().resolve()
        if src_tauri_dir
        else Path(__file__).resolve().parent.parent
    )
    tauri_config: dict[str, Any] | None = None
    if dev_server:
        base_config = _load_tauri_config(src_tauri_path / "tauri.conf.json") or {}
        build_config = dict(base_config.get("build", {}))
        build_config["devUrl"] = dev_server
        build_config["frontendDist"] = dev_server
        base_config["build"] = build_config

        app_config = dict(base_config.get("app", {}))
        windows = app_config.get("windows")
        if isinstance(windows, list):
            new_windows: list[dict[str, Any]] = []
            for window in windows:
                if not isinstance(window, dict):
                    continue
                label = window.get("label")
                if label == "splash":
                    continue
                updated_window = (
                    {**window, "visible": True} if label == "main" else window
                )
                new_windows.append(updated_window)
            if new_windows:
                app_config["windows"] = new_windows
        base_config["app"] = app_config
        tauri_config = base_config

    with start_blocking_portal("asyncio") as portal:
        context_factory_any = cast(Any, context_factory)
        context = context_factory_any(
            # ✅ v2：context 根通常用 src-tauri 目录
            src_tauri_path,
            tauri_config=tauri_config,
        )
        app = builder_factory().build(
            context=context,
            invoke_handler=command_registry.generate_handler(portal),
        )
        _start_log_event_stream(app.handle())
        _start_proxy_step_event_stream(app.handle())
        return app.run_return()
