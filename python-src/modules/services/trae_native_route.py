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
from modules.trae_patch.backends import (
    UnsupportedNativeBackendError,
    get_native_backend,
)
from modules.trae_patch.common.types import (
    CompatibilityReport,
    NativeBackend,
    RewriterConfigRequest,
)

type LogFunc = Callable[[str], None]

DEFAULT_TRAE_LOOPBACK_HOST = "127.0.0.1"
DEFAULT_TRAE_LOOPBACK_PORT = 18083
DEFAULT_TRAE_CDP_HOST = "127.0.0.1"
DEFAULT_TRAE_CDP_PORT = 9330
DEFAULT_REWRITER_WAIT_SECONDS = 20.0
DEFAULT_LOOPBACK_WAIT_SECONDS = 5.0
REWRITER_WATCH_INTERVAL_SECONDS = 1.0
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
    rewriter_watcher_task_id: str | None = None
    native_backend: NativeBackend | None = None
    compatibility_report: CompatibilityReport | None = None
    trae_process: subprocess.Popen[bytes] | None = None
    running: bool = False
    stopping: bool = False


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


def _summary_value(summary: dict[str, Any] | None, key: str) -> str:
    if summary is None:
        return "<empty>"
    value = summary.get(key)
    return str(value) if value is not None else "<empty>"


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
            self._state.stopping = False

            compatibility_result = self._check_static_compatibility_locked(
                config,
                log_func=log_func,
            )
            if not compatibility_result.ok:
                return compatibility_result

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
            self._start_rewriter_watcher_locked(log_func=log_func)
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

    def _check_static_compatibility_locked(
        self,
        config: TraeNativeRouteConfig,
        *,
        log_func: LogFunc,
    ) -> OperationResult:
        self._state.native_backend = None
        self._state.compatibility_report = None
        try:
            backend = get_native_backend()
        except UnsupportedNativeBackendError as exc:
            message = str(exc)
            log_func(f"❌ {message}")
            return OperationResult.failure(message, code=ErrorCode.CONFIG_INVALID)

        if not config.trae_path.strip():
            message = "trae_path_missing"
            log_func("❌ Trae 路径为空，请先在设置中选择 Trae.exe")
            return OperationResult.failure(message, code=ErrorCode.CONFIG_INVALID)

        trae_exe = resolve_trae_path(config.trae_path)
        if not trae_exe.is_file():
            message = "trae_path_invalid"
            log_func(f"❌ Trae 路径无效: {trae_exe}")
            return OperationResult.failure(message, code=ErrorCode.FILE_NOT_FOUND)

        module_path = _resolve_ai_agent_dll_path(trae_exe)
        report = backend.build_compatibility_report(module_path)
        self._state.native_backend = backend
        self._state.compatibility_report = report
        details = report.to_dict()
        sha_preview = (report.dll_sha256 or "<empty>")[:12]
        if report.blocked:
            log_func(
                "❌ Trae native 兼容性检查失败: "
                f"reason={report.reason} "
                f"pattern_count={report.pattern_count} "
                f"sha={sha_preview} "
                f"dll={module_path}"
            )
            return OperationResult.failure(
                "Trae native 兼容性检查失败",
                code=ErrorCode.CONFIG_INVALID,
                **details,
            )

        log_func(
            "Trae native 兼容性检查通过: "
            f"status={report.status.value} "
            f"reason={report.reason} "
            f"breakpoint_rva={report.url_copy_call_rva} "
            f"sha={sha_preview}"
        )
        if report.manifest_error:
            log_func(f"⚠️ Trae native manifest 读取异常，按未知版本处理: {report.manifest_error}")
        return OperationResult.success("Trae native 兼容性检查通过", **details)

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
        backend = self._state.native_backend
        if backend is None:
            try:
                backend = get_native_backend()
            except UnsupportedNativeBackendError as exc:
                message = str(exc)
                log_func(f"❌ {message}")
                return OperationResult.failure(message, code=ErrorCode.CONFIG_INVALID)
            self._state.native_backend = backend

        if importlib.util.find_spec(backend.rewriter_module) is None:
            message = f"未找到 native rewriter 模块: {backend.rewriter_module}"
            log_func(f"❌ {message}")
            return OperationResult.failure(message, code=ErrorCode.FILE_NOT_FOUND)

        trae_exe = resolve_trae_path(config.trae_path)
        module_path = _resolve_ai_agent_dll_path(trae_exe)

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
        dll_sha = str(armed.get("dll_sha256") or "<empty>")[:12]
        if armed.get("compatibility_changed_since_preflight") is True:
            log_func(
                "⚠️ Trae ai_agent.dll 在启动期间发生变化，"
                "已使用 rewriter attach 前重新定位的 RVA"
            )
        log_func(
            "Trae native rewriter 已就绪: "
            f"breakpoint_rva={breakpoint_rva} "
            f"dll_sha={dll_sha}"
        )
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
        backend = self._state.native_backend
        if backend is None:
            message = "native backend 状态异常"
            log_func(f"❌ {message}")
            return OperationResult.failure(message, code=ErrorCode.UNKNOWN)

        compatibility_report = self._state.compatibility_report
        try:
            rewriter_config = backend.create_rewriter_config(
                RewriterConfigRequest(
                    module_path=module_path,
                    new_url=self._loopback_url(config),
                    compatibility_report=(
                        compatibility_report.to_dict()
                        if compatibility_report is not None
                        else None
                    ),
                    duration_seconds=0,
                    output_path=files.events_path,
                    stop_file=files.stop_path,
                    quiet=True,
                )
            )
        except Exception as exc:  # noqa: BLE001
            files.log_fp.close()
            message = f"native rewriter 配置创建失败: {exc}"
            log_func(f"❌ {message}")
            return OperationResult.failure(message, code=ErrorCode.UNKNOWN)

        def run_rewriter() -> None:
            try:
                summary = backend.run_rewriter_config(rewriter_config)
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

    def _start_rewriter_watcher_locked(self, *, log_func: LogFunc) -> None:
        task_id = self._state.rewriter_task_id
        events_path = self._state.rewriter_events_path
        if task_id is None or events_path is None:
            return

        def watch_rewriter() -> None:
            first_request_event_logged = False
            while True:
                with self._lock:
                    active = (
                        self._state.rewriter_task_id == task_id
                        and self._state.running
                        and not self._state.stopping
                    )
                if not active:
                    return

                if not first_request_event_logged:
                    first_request_event_logged = self._log_first_rewrite_event(
                        events_path,
                        log_func=log_func,
                    )

                status = self._thread_manager.get_status(task_id=task_id)
                if status is not None and status.get("status") in {"failed", "finished"}:
                    with self._lock:
                        still_active = (
                            self._state.rewriter_task_id == task_id
                            and self._state.running
                            and not self._state.stopping
                        )
                        if not still_active:
                            return
                        self._state.running = False
                        summary = self._state.rewriter_summary
                        error = self._state.rewriter_error

                    log_func(
                        "❌ native rewriter 运行中退出，Trae native 路线已失效；"
                        "请重启 Trae native 路线。"
                        f"status={status.get('status')} "
                        f"error={error or status.get('error') or '<empty>'} "
                        f"summary_status={_summary_value(summary, 'status')}"
                    )
                    return

                time.sleep(REWRITER_WATCH_INTERVAL_SECONDS)

        self._state.rewriter_watcher_task_id = self._thread_manager.run(
            "trae_native_rewriter_watcher",
            watch_rewriter,
            allow_parallel=False,
        )

    @staticmethod
    def _log_first_rewrite_event(events_path: Path, *, log_func: LogFunc) -> bool:
        for record in _read_jsonl(events_path):
            kind = record.get("kind")
            if kind == "patched":
                log_func(f"Trae native URL rewrite 已命中: count={record.get('count')}")
                return True
            if kind == "already_patched":
                log_func(
                    "Trae native URL rewrite 观察到已改写 URL: "
                    f"count={record.get('count')}"
                )
                return True
            if kind == "unexpected_url":
                current_text = str(record.get("current_text") or "")
                preview = current_text[:200] if current_text else "<empty>"
                log_func(
                    "⚠️ Trae native URL copy 点命中非目标 URL: "
                    f"count={record.get('count')} preview={preview}"
                )
                return True
        return False

    def _stop_rewriter_locked(self, *, log_func: LogFunc) -> bool:
        task_id = self._state.rewriter_task_id
        if task_id is None:
            return True

        if self._state.rewriter_stop_path is not None:
            with contextlib.suppress(Exception):
                self._state.rewriter_stop_path.write_text("stop", encoding="utf-8")

        rewriter_stopped = self._thread_manager.wait(task_id, timeout=5)
        if not rewriter_stopped:
            log_func("⚠️ native rewriter 未能在 5 秒内停止，保留停止状态以便后续重试")
            return False

        self._log_rewriter_stop_summary_locked(log_func=log_func)
        self._clear_rewriter_state_locked()
        return True

    def _log_rewriter_stop_summary_locked(self, *, log_func: LogFunc) -> None:
        summary = self._state.rewriter_summary
        if summary is None:
            return
        log_func(
            "Trae native rewriter 停止摘要: "
            f"status={_summary_value(summary, 'status')} "
            f"breakpoint_restored={_summary_value(summary, 'breakpoint_restored')} "
            f"debug_detached={_summary_value(summary, 'debug_detached')}"
        )

    def _clear_rewriter_state_locked(self) -> None:
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
        self._state.rewriter_watcher_task_id = None

    def _stop_loopback_locked(self) -> bool:
        clean = True
        server = self._state.server
        if server is not None:
            with contextlib.suppress(Exception):
                server.server_close()
        if self._state.server_task_id:
            clean = self._thread_manager.wait(self._state.server_task_id, timeout=5)
        self._state.server = None
        self._state.server_task_id = None

        if self._state.proxy_app is not None:
            with contextlib.suppress(Exception):
                self._state.proxy_app.close()
            self._state.proxy_app = None
        return clean

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
            self._state.native_backend = None
            self._state.compatibility_report = None
            self._state.stopping = False
            if show_idle_message:
                log_func("Trae native 路线未运行")
            return OperationResult.success()

        log_func("正在停止 Trae native 路线...")
        self._state.stopping = True
        rewriter_stopped = self._stop_rewriter_locked(log_func=log_func)
        loopback_stopped = self._stop_loopback_locked()
        clean = rewriter_stopped and loopback_stopped

        self._state.running = False
        self._state.stopping = False
        if clean:
            self._state.native_backend = None
            self._state.compatibility_report = None
        log_func("Trae native 路线已停止；不会关闭 Trae 客户端进程")
        if clean:
            return OperationResult.success()
        return OperationResult.failure("Trae native 路线未完全停止", code=ErrorCode.UNKNOWN)

    @staticmethod
    def _loopback_base_url(config: TraeNativeRouteConfig) -> str:
        return f"http://{config.loopback_host}:{config.loopback_port}"

    def _loopback_url(self, config: TraeNativeRouteConfig) -> str:
        return f"{self._loopback_base_url(config)}/v1/chat/completions"
