from __future__ import annotations

import contextlib
import importlib.util
import json
import os
import socket
import subprocess
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

from werkzeug.serving import WSGIRequestHandler

from modules.proxy.proxy_app import ProxyApp
from modules.proxy.proxy_runtime import StoppableWSGIServer
from modules.runtime.error_codes import ErrorCode
from modules.runtime.operation_result import OperationResult
from modules.runtime.resource_manager import ResourceManager
from modules.runtime.thread_manager import ThreadManager

type LogFunc = Callable[[str], None]

DEFAULT_TRAE_LOOPBACK_HOST = "127.0.0.1"
DEFAULT_TRAE_LOOPBACK_PORT = 18083
DEFAULT_TRAE_CDP_HOST = "127.0.0.1"
DEFAULT_TRAE_CDP_PORT = 9330
DEFAULT_REWRITER_WAIT_SECONDS = 20.0
DEFAULT_LOOPBACK_WAIT_SECONDS = 5.0
TRAE_REWRITER_MODULE = "modules.trae_patch.trae_native_sse_open_url_rewriter"
TRAE_AI_AGENT_DLL_RELATIVE_PATH = Path(
    "resources/app/modules/ai-agent/ai_agent.dll"
)
TASKLIST_MIN_COLUMNS = 2
TRAE_PID_LOG_LIMIT = 8


@dataclass(frozen=True)
class TraeNativeRouteConfig:
    runtime_config: dict[str, Any]
    trae_path: str
    debug_mode: bool = False
    disable_ssl_strict_mode: bool = False
    loopback_host: str = DEFAULT_TRAE_LOOPBACK_HOST
    loopback_port: int = DEFAULT_TRAE_LOOPBACK_PORT
    cdp_host: str = DEFAULT_TRAE_CDP_HOST
    cdp_port: int = DEFAULT_TRAE_CDP_PORT
    rewriter_wait_seconds: float = DEFAULT_REWRITER_WAIT_SECONDS


@dataclass
class _TraeNativeRouteState:
    proxy_app: ProxyApp | None = None
    server: StoppableWSGIServer | None = None
    server_task_id: str | None = None
    rewriter_task_id: str | None = None
    rewriter_error: str | None = None
    rewriter_summary: dict[str, Any] | None = None
    rewriter_log_fp: Any | None = None
    rewriter_events_path: Path | None = None
    rewriter_stop_path: Path | None = None
    trae_process: subprocess.Popen[bytes] | None = None
    running: bool = False


@dataclass(frozen=True)
class _RewriterFiles:
    log_path: Path
    events_path: Path
    stop_path: Path
    log_fp: Any


def resolve_trae_path(path: str) -> Path:
    return Path(os.path.expanduser(os.path.expandvars(path.strip()))).resolve()


def _resolve_ai_agent_dll_path(trae_exe: Path) -> Path:
    return trae_exe.parent / TRAE_AI_AGENT_DLL_RELATIVE_PATH


def _is_port_open(host: str, port: int) -> bool:
    with contextlib.suppress(OSError), socket.create_connection((host, port), timeout=0.5):
        return True
    return False


def _wait_port(host: str, port: int, timeout_seconds: float) -> bool:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        if _is_port_open(host, port):
            return True
        time.sleep(0.15)
    return _is_port_open(host, port)


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    records: list[dict[str, Any]] = []
    for raw_line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            records.append(cast(dict[str, Any], payload))
    return records


def _read_tail(path: Path, max_chars: int = 2000) -> str:
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8", errors="replace")
    return text[-max_chars:].strip()


def _list_existing_trae_pids() -> list[int]:
    if os.name != "nt":
        return []
    try:
        completed = subprocess.run(
            [
                "tasklist",
                "/FI",
                "IMAGENAME eq Trae.exe",
                "/FO",
                "CSV",
                "/NH",
            ],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=3,
        )
    except Exception:
        return []
    pids: list[int] = []
    for raw_line in completed.stdout.splitlines():
        line = raw_line.strip()
        if not line or "INFO:" in line:
            continue
        columns = [part.strip().strip('"') for part in line.split(",")]
        if len(columns) < TASKLIST_MIN_COLUMNS or columns[0].lower() != "trae.exe":
            continue
        with contextlib.suppress(ValueError):
            pids.append(int(columns[1]))
    return sorted(set(pids))


class TraeNativeRouteManager:
    def __init__(
        self,
        *,
        thread_manager: ThreadManager,
        resource_manager: ResourceManager,
    ) -> None:
        self._thread_manager = thread_manager
        self._resource_manager = resource_manager
        self._state = _TraeNativeRouteState()
        self._lock = threading.Lock()

    def is_running(self) -> bool:
        return self._state.running

    def apply_runtime_config(self, raw_config: dict[str, Any] | None) -> OperationResult:
        with self._lock:
            proxy_app = self._state.proxy_app
            if not self._state.running or proxy_app is None:
                return OperationResult.failure("Trae native 路线未运行")
            return proxy_app.apply_runtime_config(raw_config)

    def start(self, config: TraeNativeRouteConfig, *, log_func: LogFunc) -> OperationResult:
        with self._lock:
            stop_result = self._stop_locked(log_func=log_func, show_idle_message=False)
            if not stop_result.ok:
                return stop_result

            log_func("Trae native 路线：启动本地 custom model loopback")
            loopback_result = self._start_loopback_locked(config, log_func=log_func)
            if not loopback_result.ok:
                self._stop_locked(log_func=log_func, show_idle_message=False)
                return loopback_result

            launch_result = self._launch_trae_locked(config, log_func=log_func)
            if not launch_result.ok:
                self._stop_locked(log_func=log_func, show_idle_message=False)
                return launch_result

            rewriter_result = self._start_rewriter_locked(config, log_func=log_func)
            if not rewriter_result.ok:
                log_func(
                    "⚠️ native rewriter 启动失败；Trae 已由 MTGA 拉起但不会自动关闭，"
                    "请关闭 Trae 后重试，或切回默认反代路线。"
                )
                self._stop_locked(log_func=log_func, show_idle_message=False)
                return rewriter_result

            self._state.running = True
            log_func("✅ Trae native 路线已就绪")
            return OperationResult.success(
                "Trae native 路线已就绪",
                loopback_url=self._loopback_url(config),
            )

    def stop(
        self,
        *,
        log_func: LogFunc,
        show_idle_message: bool = False,
    ) -> OperationResult:
        with self._lock:
            return self._stop_locked(
                log_func=log_func,
                show_idle_message=show_idle_message,
            )

    def _start_loopback_locked(
        self,
        config: TraeNativeRouteConfig,
        *,
        log_func: LogFunc,
    ) -> OperationResult:
        if _is_port_open(config.loopback_host, config.loopback_port):
            message = f"Trae loopback 端口已被占用: {config.loopback_host}:{config.loopback_port}"
            log_func(f"❌ {message}")
            return OperationResult.failure(message, code=ErrorCode.PORT_IN_USE)

        proxy_app = ProxyApp(
            config.runtime_config,
            log_func,
            resource_manager=self._resource_manager,
        )
        if not proxy_app.valid or proxy_app.app is None:
            proxy_app.close()
            return OperationResult.failure("Trae loopback 初始化失败", code=ErrorCode.UNKNOWN)

        try:
            server = StoppableWSGIServer(
                config.loopback_host,
                config.loopback_port,
                proxy_app.app,
            )
            server.RequestHandlerClass = WSGIRequestHandler
        except OSError as exc:
            proxy_app.close()
            message = f"Trae loopback 监听失败: {exc}"
            log_func(f"❌ {message}")
            return OperationResult.failure(message, code=ErrorCode.PORT_IN_USE)
        except Exception as exc:  # noqa: BLE001
            proxy_app.close()
            message = f"Trae loopback 创建失败: {exc}"
            log_func(f"❌ {message}")
            return OperationResult.failure(message, code=ErrorCode.UNKNOWN)

        ready_event = threading.Event()

        def run_server() -> None:
            ready_event.set()
            try:
                server.serve_forever()
            except Exception as exc:  # noqa: BLE001
                log_func(f"Trae loopback 运行异常: {exc}")

        task_id = self._thread_manager.run(
            "trae_native_loopback",
            run_server,
            allow_parallel=False,
        )
        self._state.proxy_app = proxy_app
        self._state.server = server
        self._state.server_task_id = task_id

        if not ready_event.wait(timeout=DEFAULT_LOOPBACK_WAIT_SECONDS):
            return OperationResult.failure("Trae loopback 启动超时", code=ErrorCode.UNKNOWN)

        log_func(f"Trae custom model loopback 已启动: {self._loopback_base_url(config)}/v1")
        log_func(f"Trae custom model loopback chat 入口: {self._loopback_url(config)}")
        return OperationResult.success()

    def _launch_trae_locked(
        self,
        config: TraeNativeRouteConfig,
        *,
        log_func: LogFunc,
    ) -> OperationResult:
        if not config.trae_path.strip():
            message = "trae_path_missing"
            log_func("❌ Trae 路径为空，请先在设置中选择 Trae.exe")
            return OperationResult.failure(message, code=ErrorCode.CONFIG_INVALID)

        trae_exe = resolve_trae_path(config.trae_path)
        if not trae_exe.is_file():
            message = "trae_path_invalid"
            log_func(f"❌ Trae 路径无效: {trae_exe}")
            return OperationResult.failure(message, code=ErrorCode.FILE_NOT_FOUND)

        if _is_port_open(config.cdp_host, config.cdp_port):
            message = (
                f"检测到已有 Trae CDP 端口 {config.cdp_host}:{config.cdp_port}。"
                "为避免复用失效 custom model tunnel，请先完全关闭 Trae 后再启动。"
            )
            log_func(f"❌ {message}")
            return OperationResult.failure(message, code=ErrorCode.CONFIG_INVALID)

        existing_pids = _list_existing_trae_pids()
        if existing_pids:
            preview = ", ".join(str(pid) for pid in existing_pids[:TRAE_PID_LOG_LIMIT])
            suffix = "..." if len(existing_pids) > TRAE_PID_LOG_LIMIT else ""
            message = (
                f"检测到 Trae 已在运行 pid={preview}{suffix}。"
                "请先完全关闭 Trae，再由 MTGA 拉起干净实例。"
            )
            log_func(f"❌ {message}")
            return OperationResult.failure(message, code=ErrorCode.CONFIG_INVALID)

        command = [str(trae_exe), f"--remote-debugging-port={config.cdp_port}"]
        try:
            self._state.trae_process = subprocess.Popen(
                command,
                cwd=str(trae_exe.parent),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except Exception as exc:  # noqa: BLE001
            message = f"Trae 拉起失败: {exc}"
            log_func(f"❌ {message}")
            return OperationResult.failure(message, code=ErrorCode.UNKNOWN)

        log_func(
            "已拉起 Trae，并注入参数: "
            f"--remote-debugging-port={config.cdp_port}"
        )
        if not _wait_port(config.cdp_host, config.cdp_port, timeout_seconds=8):
            log_func(
                f"⚠️ 未检测到 CDP 端口 {config.cdp_host}:{config.cdp_port}，"
                "继续等待 native rewriter 挂载 ai_agent.dll"
            )
        return OperationResult.success()

    def _start_rewriter_locked(
        self,
        config: TraeNativeRouteConfig,
        *,
        log_func: LogFunc,
    ) -> OperationResult:
        if importlib.util.find_spec(TRAE_REWRITER_MODULE) is None:
            message = f"未找到 native rewriter 模块: {TRAE_REWRITER_MODULE}"
            log_func(f"❌ {message}")
            return OperationResult.failure(message, code=ErrorCode.FILE_NOT_FOUND)

        trae_exe = resolve_trae_path(config.trae_path)
        module_path = _resolve_ai_agent_dll_path(trae_exe)
        if not module_path.is_file():
            message = f"未找到 Trae ai_agent.dll: {module_path}"
            log_func(f"❌ {message}")
            return OperationResult.failure(message, code=ErrorCode.FILE_NOT_FOUND)

        files = self._open_rewriter_files()
        task_result = self._start_rewriter_task_locked(
            config,
            module_path=module_path,
            files=files,
            log_func=log_func,
        )
        if not task_result.ok:
            return task_result

        task_id = self._state.rewriter_task_id
        if task_id is None:
            message = "native rewriter 启动状态异常"
            log_func(f"❌ {message}")
            return OperationResult.failure(message, code=ErrorCode.UNKNOWN)

        armed = self._wait_rewriter_armed(
            task_id,
            events_path=files.events_path,
            log_path=files.log_path,
            timeout_seconds=config.rewriter_wait_seconds,
            log_func=log_func,
        )
        if armed is None:
            return OperationResult.failure("native rewriter 未就绪", code=ErrorCode.UNKNOWN)

        breakpoint_rva = str(armed.get("breakpoint_rva") or "")
        log_func(f"Trae native rewriter 已就绪: breakpoint_rva={breakpoint_rva}")
        return OperationResult.success()

    def _open_rewriter_files(self) -> _RewriterFiles:
        log_path = Path(self._resource_manager.get_log_file("trae_native_rewriter.log"))
        events_path = Path(
            self._resource_manager.get_log_file("trae_native_rewriter.events.jsonl")
        )
        stop_path = Path(self._resource_manager.get_log_file("trae_native_rewriter.stop"))
        log_path.parent.mkdir(parents=True, exist_ok=True)
        events_path.write_text("", encoding="utf-8")
        with contextlib.suppress(FileNotFoundError):
            stop_path.unlink()

        log_fp = log_path.open("w", encoding="utf-8", errors="replace")
        return _RewriterFiles(
            log_path=log_path,
            events_path=events_path,
            stop_path=stop_path,
            log_fp=log_fp,
        )

    def _start_rewriter_task_locked(
        self,
        config: TraeNativeRouteConfig,
        *,
        module_path: Path,
        files: _RewriterFiles,
        log_func: LogFunc,
    ) -> OperationResult:
        try:
            from modules.trae_patch.trae_native_sse_open_url_rewriter import (  # noqa: PLC0415
                RewriterConfig,
                run_rewriter_config,
            )
        except Exception as exc:  # noqa: BLE001
            files.log_fp.close()
            message = f"native rewriter 模块导入失败: {exc}"
            log_func(f"❌ {message}")
            return OperationResult.failure(message, code=ErrorCode.UNKNOWN)

        rewriter_config = RewriterConfig(
            module_path=module_path,
            new_url=self._loopback_url(config),
            duration_seconds=0,
            output_path=files.events_path,
            stop_file=files.stop_path,
            quiet=True,
        )

        def run_rewriter() -> None:
            try:
                summary = run_rewriter_config(rewriter_config)
            except Exception as exc:  # noqa: BLE001
                self._state.rewriter_error = f"{type(exc).__name__}: {exc}"
                files.log_fp.write(f"{self._state.rewriter_error}\n")
                files.log_fp.flush()
                raise
            else:
                self._state.rewriter_summary = summary
                files.log_fp.write(json.dumps(summary, ensure_ascii=False, indent=2))
                files.log_fp.write("\n")
                files.log_fp.flush()

        try:
            self._state.rewriter_error = None
            self._state.rewriter_summary = None
            self._state.rewriter_log_fp = files.log_fp
            self._state.rewriter_events_path = files.events_path
            self._state.rewriter_stop_path = files.stop_path
            task_id = self._thread_manager.run(
                "trae_native_rewriter",
                run_rewriter,
                allow_parallel=False,
            )
        except Exception as exc:  # noqa: BLE001
            files.log_fp.close()
            self._state.rewriter_log_fp = None
            self._state.rewriter_events_path = None
            self._state.rewriter_stop_path = None
            message = f"native rewriter 启动失败: {exc}"
            log_func(f"❌ {message}")
            return OperationResult.failure(message, code=ErrorCode.UNKNOWN)

        self._state.rewriter_task_id = task_id
        return OperationResult.success()

    def _wait_rewriter_armed(
        self,
        task_id: str,
        *,
        events_path: Path,
        log_path: Path,
        timeout_seconds: float,
        log_func: LogFunc,
    ) -> dict[str, Any] | None:
        deadline = time.monotonic() + timeout_seconds
        while time.monotonic() < deadline:
            for record in _read_jsonl(events_path):
                if record.get("kind") == "armed":
                    return record
            status = self._thread_manager.get_status(task_id=task_id)
            if status is not None and status.get("status") in {"failed", "finished"}:
                tail = _read_tail(log_path)
                log_func(
                    "❌ native rewriter 提前退出 "
                    f"status={status.get('status')}; "
                    f"error={self._state.rewriter_error or status.get('error') or '<empty>'}; "
                    f"log_tail={tail or '<empty>'}"
                )
                return None
            time.sleep(0.2)

        tail = _read_tail(log_path)
        log_func(f"❌ native rewriter 等待超时; log_tail={tail or '<empty>'}")
        return None

    def _stop_locked(
        self,
        *,
        log_func: LogFunc,
        show_idle_message: bool,
    ) -> OperationResult:
        had_runtime = any(
            (
                self._state.running,
                self._state.rewriter_task_id is not None,
                self._state.server is not None,
                self._state.proxy_app is not None,
            )
        )
        if not had_runtime:
            if show_idle_message:
                log_func("Trae native 路线未运行")
            return OperationResult.success()

        log_func("正在停止 Trae native 路线...")
        clean = True

        task_id = self._state.rewriter_task_id
        rewriter_stopped = task_id is None
        if task_id is not None:
            if self._state.rewriter_stop_path is not None:
                with contextlib.suppress(Exception):
                    self._state.rewriter_stop_path.write_text("stop", encoding="utf-8")
            rewriter_stopped = self._thread_manager.wait(task_id, timeout=5)
            clean = clean and rewriter_stopped
            if not rewriter_stopped:
                log_func("⚠️ native rewriter 未能在 5 秒内停止，保留停止状态以便后续重试")

        if rewriter_stopped:
            self._state.rewriter_task_id = None
            self._state.rewriter_error = None
            self._state.rewriter_summary = None

            if self._state.rewriter_log_fp is not None:
                with contextlib.suppress(Exception):
                    self._state.rewriter_log_fp.close()
                self._state.rewriter_log_fp = None
            if self._state.rewriter_stop_path is not None:
                with contextlib.suppress(FileNotFoundError):
                    self._state.rewriter_stop_path.unlink()
                self._state.rewriter_stop_path = None
            self._state.rewriter_events_path = None

        server = self._state.server
        if server is not None:
            with contextlib.suppress(Exception):
                server.server_close()
        if self._state.server_task_id:
            finished = self._thread_manager.wait(self._state.server_task_id, timeout=5)
            clean = clean and finished
        self._state.server = None
        self._state.server_task_id = None

        if self._state.proxy_app is not None:
            with contextlib.suppress(Exception):
                self._state.proxy_app.close()
            self._state.proxy_app = None

        self._state.running = False
        log_func("Trae native 路线已停止；不会关闭 Trae 客户端进程")
        if clean:
            return OperationResult.success()
        return OperationResult.failure("Trae native 路线未完全停止", code=ErrorCode.UNKNOWN)

    @staticmethod
    def _loopback_base_url(config: TraeNativeRouteConfig) -> str:
        return f"http://{config.loopback_host}:{config.loopback_port}"

    def _loopback_url(self, config: TraeNativeRouteConfig) -> str:
        return f"{self._loopback_base_url(config)}/v1/chat/completions"
