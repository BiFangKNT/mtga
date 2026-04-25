from __future__ import annotations

import contextlib
import importlib.util
import json
import os
import subprocess
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

from modules.network.network_utils import (
    DEFAULT_PORT_SCAN_ATTEMPTS,
    get_process_name,
    get_tcp_listener_pids,
    get_tcp_listener_process_names,
    is_host_port_open,
    iter_port_candidates,
)
from modules.runtime.error_codes import ErrorCode
from modules.runtime.operation_result import OperationResult
from modules.runtime.resource_manager import ResourceManager
from modules.runtime.thread_manager import ThreadManager
from modules.services.trae_loopback import (
    DEFAULT_TRAE_LOOPBACK_HOST,
    DEFAULT_TRAE_LOOPBACK_PORT,
    TraeLoopbackConfig,
    TraeLoopbackManager,
)
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

DEFAULT_TRAE_CDP_HOST = "127.0.0.1"
DEFAULT_TRAE_CDP_PORT = 9330
DEFAULT_REWRITER_WAIT_SECONDS = 20.0
DEFAULT_CDP_PORT_SEARCH = DEFAULT_PORT_SCAN_ATTEMPTS
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
    cdp_port: int | None = None
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
        self._loopback = TraeLoopbackManager(
            thread_manager=thread_manager,
            resource_manager=resource_manager,
        )
        self._state = _TraeNativeRouteState()
        self._lock = threading.Lock()

    def is_running(self) -> bool:
        with self._lock:
            if self._state.running and not self._loopback.is_running():
                self._state.running = False
            return self._state.running

    def current_loopback_port(self) -> int | None:
        return self._loopback.current_selected_port()

    def apply_runtime_config(self, raw_config: dict[str, Any] | None) -> OperationResult:
        with self._lock:
            if self._state.running and not self._loopback.is_running():
                self._state.running = False
            if not self._state.running:
                return OperationResult.failure("Trae native 路线未运行")
        return self._loopback.apply_runtime_config(raw_config)

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
            loopback_result = self._loopback.start(
                TraeLoopbackConfig(
                    runtime_config=config.runtime_config,
                    loopback_host=config.loopback_host,
                    loopback_port=config.loopback_port,
                ),
                log_func=log_func,
                task_name="trae_native_loopback",
            )
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
                    "请关闭 Trae 后重试，或切回官方、反代路线。"
                )
                self._stop_locked(log_func=log_func, show_idle_message=False)
                return rewriter_result

            self._state.running = True
            self._start_rewriter_watcher_locked(log_func=log_func)
            log_func("✅ Trae native 路线已就绪")
            loopback_url = self._loopback.current_chat_url()
            return OperationResult.success(
                "Trae native 路线已就绪",
                loopback_url=loopback_url,
                cdp_port=self._state.cdp_port,
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

    def _launch_trae_locked(
        self,
        config: TraeNativeRouteConfig,
        *,
        log_func: LogFunc,
    ) -> OperationResult:
        validation_result = self._validate_trae_launch_locked(config, log_func=log_func)
        if not validation_result.ok:
            return validation_result

        trae_exe = cast(Path, validation_result.details.get("trae_exe"))

        cdp_port_result = self._resolve_cdp_port_locked(config, log_func=log_func)
        if not cdp_port_result.ok:
            return cdp_port_result

        cdp_port = int(cdp_port_result.details.get("cdp_port") or config.cdp_port)
        self._state.cdp_port = cdp_port
        spawn_result = self._spawn_trae_process_locked(
            trae_exe,
            cdp_port=cdp_port,
            log_func=log_func,
        )
        if not spawn_result.ok:
            return spawn_result

        log_func(
            "已拉起 Trae，并注入参数: "
            f"--remote-debugging-port={cdp_port}"
        )
        cdp_wait_result = self._wait_for_cdp_port_locked(
            host=config.cdp_host,
            port=cdp_port,
            timeout_seconds=8,
            log_func=log_func,
        )
        if not cdp_wait_result.ok:
            return cdp_wait_result
        return OperationResult.success()

    def _start_rewriter_locked(
        self,
        config: TraeNativeRouteConfig,
        *,
        log_func: LogFunc,
    ) -> OperationResult:
        prereq_result = self._resolve_rewriter_prerequisites_locked(config, log_func=log_func)
        if not prereq_result.ok:
            return prereq_result

        module_path = cast(Path, prereq_result.details.get("module_path"))
        loopback_url = str(prereq_result.details.get("loopback_url") or "")

        files = self._open_rewriter_files()
        task_result = self._start_rewriter_task_locked(
            module_path=module_path,
            loopback_url=loopback_url,
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
        *,
        module_path: Path,
        loopback_url: str,
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
                    new_url=loopback_url,
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
                self._loopback.is_running(),
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
        loopback_stopped = self._loopback.stop()
        clean = rewriter_stopped and loopback_stopped

        self._state.running = False
        self._state.stopping = False
        self._state.cdp_port = None
        if clean:
            self._state.native_backend = None
            self._state.compatibility_report = None
        log_func("Trae native 路线已停止；不会关闭 Trae 客户端进程")
        if clean:
            return OperationResult.success()
        return OperationResult.failure("Trae native 路线未完全停止", code=ErrorCode.UNKNOWN)

    def _validate_trae_launch_locked(
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

        return OperationResult.success(trae_exe=trae_exe)

    def _spawn_trae_process_locked(
        self,
        trae_exe: Path,
        *,
        cdp_port: int,
        log_func: LogFunc,
    ) -> OperationResult:
        command = [str(trae_exe), f"--remote-debugging-port={cdp_port}"]
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
        return OperationResult.success()

    def _resolve_rewriter_prerequisites_locked(
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
        loopback_url = self._loopback.current_chat_url()
        if not loopback_url:
            message = "Trae loopback URL 状态异常"
            log_func(f"❌ {message}")
            return OperationResult.failure(message, code=ErrorCode.UNKNOWN)

        return OperationResult.success(
            module_path=module_path,
            loopback_url=loopback_url,
        )

    def _resolve_cdp_port_locked(
        self,
        config: TraeNativeRouteConfig,
        *,
        log_func: LogFunc,
    ) -> OperationResult:
        preferred_port = config.cdp_port
        if is_host_port_open(config.cdp_host, preferred_port, timeout=0.5):
            owner_names = get_tcp_listener_process_names(preferred_port)
            owner_display = ", ".join(owner_names) if owner_names else "<unknown>"
            if any(name.lower() == "trae.exe" for name in owner_names):
                message = (
                    f"检测到已有 Trae CDP 端口 {config.cdp_host}:{preferred_port}。"
                    "为避免复用失效 custom model tunnel，请先完全关闭 Trae 后再启动。"
                )
                log_func(f"❌ {message}")
                return OperationResult.failure(message, code=ErrorCode.CONFIG_INVALID)

            for candidate_port in iter_port_candidates(
                preferred_port + 1,
                max_tries=DEFAULT_CDP_PORT_SEARCH - 1,
            ):
                if not is_host_port_open(config.cdp_host, candidate_port, timeout=0.5):
                    log_func(
                        "⚠️ Trae CDP 首选端口已被占用，"
                        f"owner={owner_display} "
                        f"preferred={preferred_port} "
                        f"selected={candidate_port}"
                    )
                    return OperationResult.success(
                        cdp_port=candidate_port,
                        preferred_cdp_port=preferred_port,
                        cdp_port_shifted=True,
                    )

            message = (
                "Trae CDP 未找到可用端口: "
                f"preferred={preferred_port} max_search={DEFAULT_CDP_PORT_SEARCH}"
            )
            log_func(f"❌ {message}")
            return OperationResult.failure(message, code=ErrorCode.PORT_IN_USE)

        return OperationResult.success(
            cdp_port=preferred_port,
            preferred_cdp_port=preferred_port,
            cdp_port_shifted=False,
        )

    def _wait_for_cdp_port_locked(
        self,
        *,
        host: str,
        port: int,
        timeout_seconds: float,
        log_func: LogFunc,
    ) -> OperationResult:
        trae_process = self._state.trae_process
        expected_pid = trae_process.pid if trae_process is not None else None
        deadline = time.monotonic() + timeout_seconds
        owner_resolution_seen = False

        while time.monotonic() < deadline:
            if not is_host_port_open(host, port, timeout=0.5):
                time.sleep(0.15)
                continue

            listener_pids = get_tcp_listener_pids(port)
            if listener_pids:
                owner_resolution_seen = True
                if expected_pid is None or expected_pid in listener_pids:
                    return OperationResult.success()
            else:
                time.sleep(0.15)
                continue

            time.sleep(0.15)

        if is_host_port_open(host, port, timeout=0.5):
            listener_pids = get_tcp_listener_pids(port)
            if expected_pid is not None and listener_pids:
                owner_names = [
                    name
                    for pid in listener_pids
                    if (name := get_process_name(pid))
                ]
                owner_display = ", ".join(owner_names) if owner_names else "<unknown>"
                message = (
                    "Trae CDP 端口已打开但不属于本次拉起的 Trae 进程: "
                    f"port={port} expected_pid={expected_pid} owner_pids={listener_pids} "
                    f"owner_names={owner_display}"
                )
                log_func(f"❌ {message}")
                return OperationResult.failure(message, code=ErrorCode.CONFIG_INVALID)
            if not owner_resolution_seen:
                log_func(
                    f"⚠️ CDP 端口 {host}:{port} 已打开，但未能解析监听 PID；继续等待 native rewriter"
                )
                return OperationResult.success()

        log_func(
            f"⚠️ 未检测到 CDP 端口 {host}:{port}，继续等待 native rewriter 挂载 ai_agent.dll"
        )
        return OperationResult.success()
