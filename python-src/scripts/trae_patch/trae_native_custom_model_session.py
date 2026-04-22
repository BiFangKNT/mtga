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

DEFAULT_HOST = "127.0.0.1"
DEFAULT_LOOPBACK_PORT = 18083
DEFAULT_DURATION_SECONDS = 300
DEFAULT_LOOPBACK_WAIT_SECONDS = 20
DEFAULT_REWRITER_WAIT_SECONDS = 20
ARTIFACT_DIR = Path("python-src/artifacts")
DEFAULT_LOOPBACK_LOG = ARTIFACT_DIR / "trae_native_custom_model_session.loopback.log"
DEFAULT_REWRITER_LOG = ARTIFACT_DIR / "trae_native_custom_model_session.rewriter.log"
DEFAULT_REWRITER_EVENTS = ARTIFACT_DIR / "trae_native_custom_model_session.rewriter.jsonl"


def _script_path(name: str) -> Path:
    return Path(__file__).with_name(name)


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


def _start_loopback(args: argparse.Namespace) -> tuple[subprocess.Popen[bytes] | None, Any | None]:
    if args.no_start_loopback:
        return None, None
    if _is_port_open(args.loopback_host, args.loopback_port):
        return None, None

    args.loopback_log.parent.mkdir(parents=True, exist_ok=True)
    log_fp = args.loopback_log.open("w", encoding="utf-8", errors="replace")
    command = [
        sys.executable,
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


def _build_rewriter_command(args: argparse.Namespace, new_url: str) -> list[str]:
    command = [
        sys.executable,
        "-u",
        "-m",
        "modules.trae_patch.trae_native_sse_open_url_rewriter",
        "--new-url",
        new_url,
        "--duration-seconds",
        str(args.duration_seconds),
        "--output-path",
        str(args.rewriter_events),
        "--quiet",
    ]
    if args.pid is not None:
        command.extend(["--pid", str(args.pid)])
    if args.breakpoint_rva is not None:
        command.extend(["--breakpoint-rva", args.breakpoint_rva])
    if args.max_patches:
        command.extend(["--max-patches", str(args.max_patches)])

    return command


def _start_rewriter(
    args: argparse.Namespace,
    new_url: str,
) -> tuple[subprocess.Popen[bytes], Any]:
    args.rewriter_log.parent.mkdir(parents=True, exist_ok=True)
    args.rewriter_events.parent.mkdir(parents=True, exist_ok=True)
    args.rewriter_events.write_text("", encoding="utf-8")
    log_fp = args.rewriter_log.open("w", encoding="utf-8", errors="replace")
    process = subprocess.Popen(
        _build_rewriter_command(args, new_url),
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
            raise RuntimeError(
                f"native rewriter 提前退出 returncode={process.returncode}；"
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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="启动 MTGA local loopback，并在 native sse.open URL copy 点重写到该 loopback。"
    )
    parser.add_argument("--loopback-host", default=DEFAULT_HOST)
    parser.add_argument("--loopback-port", type=int, default=DEFAULT_LOOPBACK_PORT)
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
    parser.add_argument("--max-patches", type=int, default=0)
    parser.add_argument("--loopback-log", type=Path, default=DEFAULT_LOOPBACK_LOG)
    parser.add_argument("--rewriter-log", type=Path, default=DEFAULT_REWRITER_LOG)
    parser.add_argument("--rewriter-events", type=Path, default=DEFAULT_REWRITER_EVENTS)
    return parser


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    args = build_parser().parse_args()
    new_url = f"http://{args.loopback_host}:{args.loopback_port}/v1/chat/completions"
    loopback_process: subprocess.Popen[bytes] | None = None
    loopback_log_fp: Any | None = None
    rewriter_process: subprocess.Popen[bytes] | None = None
    rewriter_log_fp: Any | None = None
    try:
        loopback_process, loopback_log_fp = _start_loopback(args)
        rewriter_process, rewriter_log_fp = _start_rewriter(args, new_url)
        armed = _wait_rewriter_armed(args, rewriter_process)
        print(
            json.dumps(
                {
                    "status": "ready",
                    "new_url": new_url,
                    "rewriter_armed": armed,
                    "loopback_started_by_session": loopback_process is not None,
                    "loopback_log": str(args.loopback_log),
                    "rewriter_log": str(args.rewriter_log),
                    "rewriter_events": str(args.rewriter_events),
                },
                ensure_ascii=False,
            ),
            flush=True,
        )
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
        _stop_process(rewriter_process)
        if rewriter_log_fp is not None:
            rewriter_log_fp.close()
        _stop_process(loopback_process)
        if loopback_log_fp is not None:
            loopback_log_fp.close()


if __name__ == "__main__":
    raise SystemExit(main())
