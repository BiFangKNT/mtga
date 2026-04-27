from __future__ import annotations

import argparse
import contextlib
import json
import socket
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

PYTHON_SRC_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(PYTHON_SRC_DIR))

from modules.trae_patch.backends import (  # noqa: E402
    UnsupportedNativeBackendError,
    get_native_backend,
)
from modules.trae_patch.common.types import NativeBackend  # noqa: E402

DEFAULT_HOST = "127.0.0.1"
DEFAULT_LOOPBACK_PORT = 18083
DEFAULT_CDP_PORT = 9330
DEFAULT_DURATION_SECONDS = 300
DEFAULT_LOOPBACK_WAIT_SECONDS = 20
DEFAULT_REWRITER_WAIT_SECONDS = 20
DEFAULT_CDP_WAIT_SECONDS = 20
DEFAULT_PATCH_WAIT_SECONDS = 20
DEFAULT_WAIT_AFTER_SEND_SECONDS = 0.5
DEFAULT_TARGET_URL_SUBSTRING = "workbench/workbench.html"
DEFAULT_TARGET_TITLE_SUBSTRING = ""
DEFAULT_CDP_MODE = "current"
DEFAULT_CDP_AGENT_NAME = "current"
DEFAULT_TEST_MESSAGE = "请简短回复：mtga-native-smoke"
ARTIFACT_DIR = Path("python-src/artifacts")
DEFAULT_LOOPBACK_LOG = ARTIFACT_DIR / "trae_native_custom_model_session.loopback.log"
DEFAULT_REWRITER_LOG = ARTIFACT_DIR / "trae_native_custom_model_session.rewriter.log"
DEFAULT_REWRITER_EVENTS = ARTIFACT_DIR / "trae_native_custom_model_session.rewriter.jsonl"
DEFAULT_REWRITER_STOP = ARTIFACT_DIR / "trae_native_custom_model_session.rewriter.stop"
DEFAULT_CDP_LOG = ARTIFACT_DIR / "trae_native_custom_model_session.cdp.log"
TRAE_PID_LOG_LIMIT = 8


def _script_path(name: str) -> Path:
    return Path(__file__).with_name(name)


def _project_python() -> str:
    candidates = [
        PYTHON_SRC_DIR / ".venv" / "bin" / "python",
        PYTHON_SRC_DIR / ".venv" / "Scripts" / "python.exe",
    ]
    for candidate in candidates:
        if candidate.is_file():
            return str(candidate)
    return sys.executable


def _is_port_open(host: str, port: int) -> bool:
    with contextlib.suppress(OSError), socket.create_connection((host, port), timeout=0.5):
        return True
    return False


def _wait_port(host: str, port: int, timeout_seconds: float) -> bool:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        if _is_port_open(host, port):
            return True
        time.sleep(0.2)
    return _is_port_open(host, port)


def _native_backend() -> NativeBackend:
    try:
        return get_native_backend()
    except UnsupportedNativeBackendError as exc:
        raise RuntimeError(str(exc)) from exc


def _start_loopback(args: argparse.Namespace) -> tuple[subprocess.Popen[bytes] | None, Any | None]:
    if args.no_start_loopback:
        return None, None
    if _is_port_open(args.loopback_host, args.loopback_port):
        return None, None

    args.loopback_log.parent.mkdir(parents=True, exist_ok=True)
    log_fp = args.loopback_log.open("w", encoding="utf-8", errors="replace")
    command = [
        _project_python(),
        "-u",
        str(_script_path("trae_local_model_loopback.py")),
        "--host",
        args.loopback_host,
        "--port",
        str(args.loopback_port),
        "--json",
    ]
    if args.debug_mode:
        command.append("--debug-mode")
    if args.disable_ssl_strict_mode:
        command.append("--disable-ssl-strict-mode")
    if args.current_config_index is not None:
        command.extend(["--current-config-index", str(args.current_config_index)])

    process = subprocess.Popen(command, stdout=log_fp, stderr=log_fp)
    if not _wait_port(args.loopback_host, args.loopback_port, args.loopback_wait_seconds):
        process.terminate()
        with contextlib.suppress(subprocess.TimeoutExpired):
            process.wait(timeout=3)
        log_fp.close()
        raise RuntimeError(
            f"loopback 未在 {args.loopback_wait_seconds}s 内监听 "
            f"{args.loopback_host}:{args.loopback_port}；详见 {args.loopback_log}"
        )
    return process, log_fp


def _stop_process(process: subprocess.Popen[bytes] | None) -> None:
    if process is None or process.poll() is not None:
        return
    process.terminate()
    with contextlib.suppress(subprocess.TimeoutExpired):
        process.wait(timeout=5)
    if process.poll() is None:
        process.kill()
        with contextlib.suppress(subprocess.TimeoutExpired):
            process.wait(timeout=3)


def _start_trae(
    args: argparse.Namespace,
    backend: NativeBackend,
) -> subprocess.Popen[bytes] | None:
    if not args.trae_path:
        return None

    trae_executable = backend.resolve_trae_executable(args.trae_path)
    if not trae_executable.is_file():
        raise RuntimeError(f"Trae 路径无效: {trae_executable}")
    if _is_port_open(args.cdp_host, args.cdp_port):
        raise RuntimeError(
            f"CDP 端口已被占用: {args.cdp_host}:{args.cdp_port}；请先关闭已有 Trae"
        )

    existing_processes = backend.list_existing_trae_processes()
    if existing_processes:
        preview = ", ".join(
            str(process.pid) for process in existing_processes[:TRAE_PID_LOG_LIMIT]
        )
        suffix = "..." if len(existing_processes) > TRAE_PID_LOG_LIMIT else ""
        raise RuntimeError(
            f"检测到 Trae 已在运行 pid={preview}{suffix}；"
            "请先完全关闭 Trae，再跑自动化会话"
        )

    command, cwd = backend.build_launch_command(trae_executable, cdp_port=args.cdp_port)
    process = subprocess.Popen(
        command,
        cwd=str(cwd),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if not _wait_port(args.cdp_host, args.cdp_port, args.cdp_wait_seconds):
        raise RuntimeError(
            f"Trae 未在 {args.cdp_wait_seconds}s 内开放 CDP "
            f"{args.cdp_host}:{args.cdp_port}"
    )
    return process


def _resolve_rewriter_module_path(
    args: argparse.Namespace,
    backend: NativeBackend,
) -> Path | None:
    raw_module_path = getattr(args, "module_path", None)
    if raw_module_path is not None:
        return Path(raw_module_path)
    trae_path = getattr(args, "trae_path", None)
    if not trae_path or backend.name != "macos":
        return None

    trae_executable = backend.resolve_trae_executable(trae_path)
    return backend.resolve_module_path(trae_executable)


def _build_rewriter_command(
    args: argparse.Namespace,
    new_url: str,
    backend: NativeBackend,
) -> list[str]:
    command = [
        _project_python(),
        "-u",
        "-m",
        backend.rewriter_module,
        "--new-url",
        new_url,
        "--duration-seconds",
        str(args.duration_seconds),
        "--output-path",
        str(args.rewriter_events),
        "--stop-file",
        str(args.rewriter_stop),
        "--quiet",
    ]
    if args.pid is not None:
        command.extend(["--pid", str(args.pid)])
    if args.breakpoint_rva is not None and backend.name == "windows":
        command.extend(["--breakpoint-rva", args.breakpoint_rva])
    if args.max_patches and backend.name == "windows":
        command.extend(["--max-patches", str(args.max_patches)])
    if backend.name == "macos" and getattr(args, "module_path", None) is not None:
        command.extend(["--module-path", str(args.module_path)])

    return command


def _start_rewriter(
    args: argparse.Namespace,
    new_url: str,
    backend: NativeBackend,
) -> tuple[subprocess.Popen[bytes], Any]:
    args.rewriter_log.parent.mkdir(parents=True, exist_ok=True)
    args.rewriter_events.parent.mkdir(parents=True, exist_ok=True)
    args.rewriter_stop.parent.mkdir(parents=True, exist_ok=True)
    args.rewriter_events.write_text("", encoding="utf-8")
    with contextlib.suppress(FileNotFoundError):
        args.rewriter_stop.unlink()
    log_fp = args.rewriter_log.open("w", encoding="utf-8", errors="replace")
    process = subprocess.Popen(
        _build_rewriter_command(args, new_url, backend),
        stdout=log_fp,
        stderr=log_fp,
    )
    return process, log_fp


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
            records.append(payload)
    return records


def _wait_rewriter_armed(
    args: argparse.Namespace,
    process: subprocess.Popen[bytes],
) -> dict[str, Any]:
    deadline = time.monotonic() + args.rewriter_wait_seconds
    while time.monotonic() < deadline:
        for record in _read_jsonl(args.rewriter_events):
            if record.get("kind") == "armed":
                return record
        if process.poll() is not None:
            summary = _read_rewriter_summary(args.rewriter_log)
            summary_status = summary.get("status") if isinstance(summary, dict) else None
            summary_error = summary.get("error") if isinstance(summary, dict) else None
            raise RuntimeError(
                f"native rewriter 提前退出 returncode={process.returncode}；"
                f"summary_status={summary_status or '<empty>'} "
                f"summary_error={summary_error or '<empty>'}"
                f"{_format_attach_diagnostics(summary)}；"
                f"详见 {args.rewriter_log}"
            )
        time.sleep(0.2)
    raise RuntimeError(
        f"native rewriter 未在 {args.rewriter_wait_seconds}s 内 armed；"
        f"详见 {args.rewriter_log}"
    )


def _read_rewriter_summary(log_path: Path) -> dict[str, Any] | None:
    if not log_path.exists():
        return None
    text = log_path.read_text(encoding="utf-8", errors="replace").strip()
    if not text:
        return None
    start = text.rfind("\n{")
    candidate = text[start + 1 :] if start >= 0 else text
    try:
        payload = json.loads(candidate)
    except json.JSONDecodeError:
        return None
    return payload if isinstance(payload, dict) else None


def _format_attach_diagnostics(summary: dict[str, Any] | None) -> str:
    if not isinstance(summary, dict):
        return ""
    diagnostics = summary.get("attach_diagnostics")
    if not isinstance(diagnostics, dict):
        return ""
    signals = diagnostics.get("signals")
    signal_text = (
        ",".join(str(item) for item in signals)
        if isinstance(signals, list)
        else "<empty>"
    )
    return (
        "; attach_reason="
        f"{diagnostics.get('reason') or '<empty>'}"
        "; developer_mode="
        f"{diagnostics.get('developer_mode_enabled')}"
        "; target_runtime="
        f"{diagnostics.get('target_codesign_runtime')}"
        "; target_get_task_allow="
        f"{diagnostics.get('target_get_task_allow')}"
        "; signals="
        f"{signal_text}"
    )


def _wait_rewriter_event(
    args: argparse.Namespace,
    process: subprocess.Popen[bytes],
    *,
    event_kinds: set[str],
    timeout_seconds: float,
) -> dict[str, Any] | None:
    deadline = time.monotonic() + timeout_seconds
    record_count = 0
    while time.monotonic() < deadline:
        records = _read_jsonl(args.rewriter_events)
        for record in records[record_count:]:
            if str(record.get("kind") or "") in event_kinds:
                return record
        record_count = len(records)
        if process.poll() is not None:
            return None
        time.sleep(0.2)
    return None


def _touch_stop_file(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("stop\n", encoding="utf-8")


def _run_cdp_send_chat(args: argparse.Namespace) -> dict[str, Any]:
    args.cdp_log.parent.mkdir(parents=True, exist_ok=True)
    command = [
        _project_python(),
        str(_script_path("trae_cdp_send_chat.py")),
        "--message",
        args.message,
        "--host",
        args.cdp_host,
        "--port",
        str(args.cdp_port),
        "--target-url-substring",
        args.target_url_substring,
        "--target-title-substring",
        args.target_title_substring,
        "--wait-after-send-seconds",
        str(args.wait_after_send_seconds),
        "--mode",
        args.cdp_mode,
        "--agent-name",
        args.cdp_agent_name,
        "--json",
    ]
    completed = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    output_text = completed.stdout
    if completed.stdout and completed.stderr:
        output_text += "\n"
    output_text += completed.stderr
    args.cdp_log.write_text(
        output_text,
        encoding="utf-8",
    )
    if completed.returncode != 0:
        message = completed.stderr.strip() or completed.stdout.strip() or "cdp_send_chat failed"
        raise RuntimeError(message)
    payload = json.loads(completed.stdout or "{}")
    if not isinstance(payload, dict):
        raise RuntimeError("CDP send 返回格式无效")
    return payload


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="启动 MTGA local loopback，并在 native sse.open URL copy 点重写到该 loopback。"
    )
    parser.add_argument("--loopback-host", default=DEFAULT_HOST)
    parser.add_argument("--loopback-port", type=int, default=DEFAULT_LOOPBACK_PORT)
    parser.add_argument("--cdp-host", default=DEFAULT_HOST)
    parser.add_argument("--cdp-port", type=int, default=DEFAULT_CDP_PORT)
    parser.add_argument("--trae-path", help="可选：自动拉起 Trae，支持 .app/.exe/可执行文件")
    parser.add_argument("--no-start-loopback", action="store_true", help="只使用已有 loopback")
    parser.add_argument(
        "--loopback-wait-seconds",
        type=float,
        default=DEFAULT_LOOPBACK_WAIT_SECONDS,
    )
    parser.add_argument("--current-config-index", type=int)
    parser.add_argument("--debug-mode", action="store_true")
    parser.add_argument("--disable-ssl-strict-mode", action="store_true")
    parser.add_argument("--pid", type=int, help="可选：指定 ai_agent.dll 所在 Trae PID")
    parser.add_argument(
        "--breakpoint-rva",
        help="可选：覆盖 native URL copy call RVA；默认由 rewriter 自动定位",
    )
    parser.add_argument("--duration-seconds", type=int, default=DEFAULT_DURATION_SECONDS)
    parser.add_argument(
        "--rewriter-wait-seconds",
        type=float,
        default=DEFAULT_REWRITER_WAIT_SECONDS,
    )
    parser.add_argument(
        "--cdp-wait-seconds",
        type=float,
        default=DEFAULT_CDP_WAIT_SECONDS,
        help="等待 Trae CDP 端口可用的秒数",
    )
    parser.add_argument(
        "--patch-wait-seconds",
        type=float,
        default=DEFAULT_PATCH_WAIT_SECONDS,
        help="CDP 发消息后等待 rewriter 命中/改写的秒数",
    )
    parser.add_argument("--max-patches", type=int, default=0)
    parser.add_argument(
        "--send-chat",
        action="store_true",
        help="armed 后通过 CDP 自动发一条测试消息",
    )
    parser.add_argument("--message", default=DEFAULT_TEST_MESSAGE, help="CDP 自动发送的测试消息")
    parser.add_argument(
        "--target-url-substring",
        default=DEFAULT_TARGET_URL_SUBSTRING,
        help="CDP 目标 page URL 子串",
    )
    parser.add_argument(
        "--target-title-substring",
        default=DEFAULT_TARGET_TITLE_SUBSTRING,
        help="CDP 目标 page 标题子串",
    )
    parser.add_argument(
        "--wait-after-send-seconds",
        type=float,
        default=DEFAULT_WAIT_AFTER_SEND_SECONDS,
        help="CDP 发消息后额外等待秒数",
    )
    parser.add_argument(
        "--cdp-mode",
        choices=("ide", "solo", "current"),
        default=DEFAULT_CDP_MODE,
        help="CDP 发消息前优先切换的模式；主线默认保持 current",
    )
    parser.add_argument(
        "--cdp-agent-name",
        default=DEFAULT_CDP_AGENT_NAME,
        help="CDP 发消息前要求的已选 agent；传 current 跳过校验",
    )
    parser.add_argument("--loopback-log", type=Path, default=DEFAULT_LOOPBACK_LOG)
    parser.add_argument("--rewriter-log", type=Path, default=DEFAULT_REWRITER_LOG)
    parser.add_argument("--rewriter-events", type=Path, default=DEFAULT_REWRITER_EVENTS)
    parser.add_argument("--rewriter-stop", type=Path, default=DEFAULT_REWRITER_STOP)
    parser.add_argument("--cdp-log", type=Path, default=DEFAULT_CDP_LOG)
    parser.add_argument(
        "--module-path",
        type=Path,
        help="可选：覆盖 native rewriter 目标模块路径；macOS 下默认根据 --trae-path 推导",
    )
    return parser


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    args = build_parser().parse_args()
    backend = _native_backend()
    new_url = f"http://{args.loopback_host}:{args.loopback_port}/v1/chat/completions"
    loopback_process: subprocess.Popen[bytes] | None = None
    loopback_log_fp: Any | None = None
    trae_process: subprocess.Popen[bytes] | None = None
    rewriter_process: subprocess.Popen[bytes] | None = None
    rewriter_log_fp: Any | None = None
    try:
        loopback_process, loopback_log_fp = _start_loopback(args)
        trae_process = _start_trae(args, backend)
        args.module_path = _resolve_rewriter_module_path(args, backend)
        rewriter_process, rewriter_log_fp = _start_rewriter(args, new_url, backend)
        armed = _wait_rewriter_armed(args, rewriter_process)
        ready_payload: dict[str, Any] = {
            "status": "ready",
            "backend": backend.name,
            "new_url": new_url,
            "module_path": str(args.module_path) if args.module_path is not None else None,
            "rewriter_armed": armed,
            "loopback_started_by_session": loopback_process is not None,
            "trae_started_by_session": trae_process is not None,
            "loopback_log": str(args.loopback_log),
            "rewriter_log": str(args.rewriter_log),
            "rewriter_events": str(args.rewriter_events),
            "rewriter_stop": str(args.rewriter_stop),
        }
        if args.send_chat:
            if not _wait_port(args.cdp_host, args.cdp_port, args.cdp_wait_seconds):
                raise RuntimeError(
                    f"CDP 未在 {args.cdp_wait_seconds}s 内就绪: {args.cdp_host}:{args.cdp_port}"
                )
            ready_payload["cdp_send"] = _run_cdp_send_chat(args)
            ready_payload["cdp_mode"] = args.cdp_mode
            ready_payload["cdp_agent_name"] = args.cdp_agent_name
            ready_payload["patch_event"] = _wait_rewriter_event(
                args,
                rewriter_process,
                event_kinds={"patched", "already_patched", "patch_failed"},
                timeout_seconds=args.patch_wait_seconds,
            )
            _touch_stop_file(args.rewriter_stop)

        print(json.dumps(ready_payload, ensure_ascii=False), flush=True)
        return_code = int(rewriter_process.wait())
        summary = _read_rewriter_summary(args.rewriter_log)
        print(
            json.dumps(
                {
                    "status": "stopped",
                    "return_code": return_code,
                    "rewriter_summary": summary,
                },
                ensure_ascii=False,
                indent=2,
            ),
            flush=True,
        )
        return return_code
    finally:
        _touch_stop_file(args.rewriter_stop)
        _stop_process(rewriter_process)
        if rewriter_log_fp is not None:
            rewriter_log_fp.close()
        _stop_process(trae_process)
        _stop_process(loopback_process)
        if loopback_log_fp is not None:
            loopback_log_fp.close()


if __name__ == "__main__":
    raise SystemExit(main())
