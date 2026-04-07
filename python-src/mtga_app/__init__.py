# ruff: noqa: E402
from __future__ import annotations

import json
import os
import sys
import time
import traceback
from collections.abc import Callable
from contextlib import suppress
from functools import lru_cache
from importlib import import_module
from pathlib import Path
from threading import Lock, Thread
from types import TracebackType
from typing import TYPE_CHECKING, Any, Literal, cast

from platformdirs import user_data_dir

from modules.runtime.resource_manager import get_log_path

MTGA_PLATFORM = "tauri"
os.environ.setdefault("MTGA_PLATFORM", MTGA_PLATFORM)


def _resolve_boot_log_path() -> Path | None:
    try:
        return Path(get_log_path("mtga_tauri_boot.log"))
    except Exception:
        return None


_BOOT_LOG_PATH = _resolve_boot_log_path()
_INVOKE_LOCK = Lock()


def _boot_log(message: str) -> None:
    if _BOOT_LOG_PATH is None:
        return
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

    def handler(
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_traceback: TracebackType | None,
    ) -> None:
        _boot_log("Uncaught exception during startup:")
        for line in traceback.format_exception(exc_type, exc_value, exc_traceback):
            _boot_log(line.rstrip("\n"))
            _try_push_log(line.rstrip("\n"))
        original(exc_type, exc_value, exc_traceback)

    sys.excepthook = handler


_install_bootstrap_excepthook()
_boot_log("mtga_app init start")


# 统一 .env 入口（显眼开关）
# - MTGA_ENV_FILE=... 指定 env 文件路径（默认使用项目根 .env）
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


def _sanitize_sslkeylogfile() -> None:
    if os.name != "nt":
        return
    removed = os.environ.pop("SSLKEYLOGFILE", None)
    if removed:
        _boot_log("Removed SSLKEYLOGFILE to avoid Windows OpenSSL_Applink crash")


_load_env_file(ENV_FILE)
_sanitize_sslkeylogfile()


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


# 当前仓库固定从 python-src/modules 导入 modules 包。
LOCAL_ROOT = Path(__file__).resolve().parent.parent
LOCAL_MODULES = LOCAL_ROOT / "modules"
if not LOCAL_MODULES.exists():
    raise RuntimeError("未找到 python-src/modules")
sys.path.insert(0, str(LOCAL_ROOT))

try:
    from modules.platform.platform_context import get_platform

    get_platform()
except Exception as exc:
    _boot_log(f"Platform detection failed: {exc}")
    _try_push_log(f"平台识别失败: {exc}")
    raise


# 仓库根仍用于版本号读取。
REPO_ROOT = TAURI_PROJECT_ROOT

from anyio.from_thread import start_blocking_portal
from pydantic import BaseModel
from pytauri import AppHandle, Commands, Emitter

from .commands import register_eager_command_groups, register_lazy_command_groups

if TYPE_CHECKING:
    from modules.runtime.resource_manager import ResourceManager
    from modules.services.config_service import ConfigStore

command_registry = Commands()
register_eager_command_groups(command_registry)
register_lazy_command_groups(command_registry)

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


class LazyWarmupEventPayload(BaseModel):
    phase: Literal["start", "progress", "done", "error"]
    stage: str | None = None
    label: str | None = None
    detail: str | None = None
    completed: int
    total: int
    error_message: str | None = None


class SaveConfigPayload(BaseModel):
    config_groups: list[dict[str, Any]]
    current_config_index: int
    mapped_model_id: str | None = None
    mtga_auth_key: str | None = None


@lru_cache(maxsize=1)
def _get_resource_manager() -> ResourceManager:
    resource_manager_cls = import_module("modules.runtime.resource_manager").ResourceManager
    return resource_manager_cls()


@lru_cache(maxsize=1)
def _get_config_store() -> ConfigStore:
    config_store_cls = import_module("modules.services.config_service").ConfigStore
    resource_manager = _get_resource_manager()
    return config_store_cls(resource_manager.get_user_config_file())


@command_registry.command()
async def greet(body: GreetPayload) -> str:
    return f"Hello, {body.name}! from Python {sys.version.split()[0]}"


@command_registry.command()
async def load_config() -> dict[str, Any]:
    config_store = _get_config_store()
    config_groups, current_index = config_store.load_config_groups()
    mapped_model_id, mtga_auth_key = config_store.load_global_config()
    warnings = config_store.load_config_warnings()
    return {
        "config_groups": config_groups,
        "current_config_index": current_index,
        "mapped_model_id": mapped_model_id,
        "mtga_auth_key": mtga_auth_key,
        "warnings": warnings,
    }


@command_registry.command()
async def save_config(body: SaveConfigPayload) -> bool:
    config_store = _get_config_store()
    return config_store.save_config_groups(
        body.config_groups,
        body.current_config_index,
        body.mapped_model_id,
        body.mtga_auth_key,
    )


@command_registry.command()
async def get_app_info() -> dict[str, Any]:
    metadata_module = import_module("modules.services.app_metadata")
    version_module = import_module("modules.services.app_version")
    metadata = metadata_module.DEFAULT_METADATA
    resolve_app_version = version_module.resolve_app_version
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


@command_registry.command("start_lazy_warmup")
async def start_lazy_warmup_command() -> bool:
    start_lazy_warmup = import_module("mtga_app.lazy_warmup").start_lazy_warmup
    result = start_lazy_warmup(
        command_registry,
        log_func=_boot_log,
    )
    return result in {"started", "running", "completed"}


@command_registry.command("get_lazy_warmup_status")
async def get_lazy_warmup_status_command() -> dict[str, Any] | None:
    get_lazy_warmup_status = cast(
        Callable[[], dict[str, Any] | None],
        import_module("mtga_app.lazy_warmup").get_lazy_warmup_status,
    )
    return get_lazy_warmup_status()


def _start_log_event_stream(app_handle: AppHandle) -> None:
    def run() -> None:
        pull_logs = import_module("modules.runtime.log_bus").pull_logs
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

            items = result.get("items")
            next_id = result.get("next_id")
            if isinstance(next_id, int):
                after_id = next_id
            if isinstance(items, list) and items:
                safe_items = cast(list[object], items)
                try:
                    payload = LogEventPayload(
                        items=[str(item) for item in safe_items],
                        next_id=after_id or 0,
                    )
                    Emitter.emit(app_handle, "mtga:logs", payload)
                except Exception as exc:
                    _boot_log(f"log stream emit failed: {exc}")
                    time.sleep(0.2)

    Thread(target=run, name="mtga-log-stream", daemon=True).start()


def _start_proxy_step_event_stream(app_handle: AppHandle) -> None:
    def run() -> None:
        pull_steps = import_module("modules.runtime.proxy_step_bus").pull_steps
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

            items = result.get("items")
            next_id = result.get("next_id")
            if isinstance(next_id, int):
                after_id = next_id
            if isinstance(items, list) and items:
                safe_items = cast(list[object], items)
                for item in safe_items:
                    try:
                        Emitter.emit_str(app_handle, "mtga:proxy-step", str(item))
                    except Exception as exc:
                        _boot_log(f"proxy step emit failed: {exc}")
                        time.sleep(0.2)

    Thread(target=run, name="mtga-proxy-step-stream", daemon=True).start()


def _start_lazy_warmup_event_stream(app_handle: AppHandle) -> None:
    def run() -> None:
        pull_events = import_module("modules.runtime.lazy_warmup_bus").pull_events
        after_id: int | None = None
        while True:
            try:
                result = pull_events(
                    after_id=after_id,
                    timeout_ms=1000,
                    max_items=100,
                )
            except Exception as exc:
                _boot_log(f"lazy warmup pull failed: {exc}")
                time.sleep(0.2)
                continue

            items = result.get("items")
            next_id = result.get("next_id")
            if isinstance(next_id, int):
                after_id = next_id
            if isinstance(items, list) and items:
                safe_items = cast(list[object], items)
                for item in safe_items:
                    try:
                        payload = LazyWarmupEventPayload.model_validate_json(str(item))
                        Emitter.emit(app_handle, "mtga:lazy-warmup", payload)
                    except Exception as exc:
                        _boot_log(f"lazy warmup emit failed: {exc}")
                        time.sleep(0.2)

    Thread(target=run, name="mtga-lazy-warmup-stream", daemon=True).start()


def main() -> int:
    pytauri_wheel_lib = import_module("pytauri_wheel.lib")
    builder_factory = pytauri_wheel_lib.builder_factory
    context_factory = pytauri_wheel_lib.context_factory

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
        windows_obj = app_config.get("windows")
        if isinstance(windows_obj, list):
            windows_list = cast(list[object], windows_obj)
            new_windows: list[dict[str, Any]] = []
            for window_obj in windows_list:
                if not isinstance(window_obj, dict):
                    continue
                window = cast(dict[str, Any], window_obj)
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
        context = context_factory(
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
        _start_lazy_warmup_event_stream(app.handle())
        return app.run_return()
