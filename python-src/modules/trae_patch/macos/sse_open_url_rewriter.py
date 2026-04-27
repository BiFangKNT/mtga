from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

from .compatibility import (
    DEFAULT_OLD_URL,
    build_compatibility_report,
    diagnose_lldb_attach_failure,
)

DEFAULT_NEW_URL = "http://127.0.0.1:18083/v1/chat/completions"
DEFAULT_DURATION_SECONDS = 300
DEFAULT_WAIT_FOR_MODULE_SECONDS = 300
DEFAULT_POLL_SECONDS = 1.0
DEFAULT_LSOF_TIMEOUT_SECONDS = 3
LLDB_STDIO_TAIL_CHARS = 6000
LLDB_ENV_VARS_TO_CLEAR = (
    "PYTHONHOME",
    "PYTHONPATH",
    "PYTHONEXECUTABLE",
    "PYTHONPLATLIBDIR",
    "__PYVENV_LAUNCHER__",
    "VIRTUAL_ENV",
    "CONDA_PREFIX",
)
DEFAULT_MODULE_PATH = Path(
    "/Applications/Trae.app/Contents/Resources/app/modules/ai-agent/libai_agent.dylib"
)


@dataclass(frozen=True)
class RewriterConfig:
    pid: int | None = None
    module_path: Path = DEFAULT_MODULE_PATH
    old_url: str = DEFAULT_OLD_URL
    new_url: str = DEFAULT_NEW_URL
    compatibility_report: dict[str, Any] | None = None
    duration_seconds: int = DEFAULT_DURATION_SECONDS
    wait_for_module_seconds: int = DEFAULT_WAIT_FOR_MODULE_SECONDS
    output_path: Path | None = None
    stop_file: Path | None = None
    quiet: bool = False


LLDB_REWRITER_SCRIPT = r'''
from __future__ import annotations

import json
import shlex
import struct
import time
import traceback
from pathlib import Path

import lldb

MAX_SCAN_BYTES = 2048
MAX_STACK_SCAN_BYTES = 4096
MAX_TEXT_LEN = 4096
MIN_USER_POINTER = 0x10000
URL_SUFFIX = "/v1/chat/completions"
BREAKPOINT_REGEXES = (
    "custom_model_proxy_client.*message_handler.*handle_sse_open.*closure",
    "NetBridgeHttpClient.*custom_model_proxy_client.*HttpClient.*send",
)


def _now_iso():
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")


def _record(path, payload):
    if not path:
        return
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("a", encoding="utf-8") as fp:
        fp.write(json.dumps(payload, ensure_ascii=False) + "\n")


def _plausible_ptr(value):
    return isinstance(value, int) and value >= MIN_USER_POINTER


def _read_memory(process, address, size):
    if not _plausible_ptr(address) or size <= 0:
        return None
    error = lldb.SBError()
    data = process.ReadMemory(address, size, error)
    if not error.Success() or not data:
        return None
    return bytes(data)


def _write_memory(process, address, data):
    error = lldb.SBError()
    written = process.WriteMemory(address, data, error)
    return error.Success() and written == len(data)


def _read_text(process, pointer, length):
    if not _plausible_ptr(pointer) or length <= 0 or length > MAX_TEXT_LEN:
        return None
    data = _read_memory(process, pointer, length)
    if data is None or len(data) != length:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None


def _register_value(frame, name):
    value = frame.FindRegister(name)
    if not value.IsValid():
        return None
    raw = value.GetValue()
    if not raw:
        return None
    try:
        return int(raw, 0)
    except ValueError:
        return None


def _malloc(process, frame, size):
    value = frame.EvaluateExpression(f"(void*)malloc({size})")
    if not value.IsValid() or value.GetError().Fail():
        return None
    raw = value.GetValue()
    if not raw:
        return None
    try:
        pointer = int(raw, 0)
    except ValueError:
        return None
    if not _plausible_ptr(pointer):
        return None
    if not _write_memory(process, pointer, b"\x00" * size):
        return None
    return pointer


def _matches_target(text, old_url, new_url):
    if text == new_url:
        return "already_patched"
    if text == old_url:
        return "target"
    if text.startswith(("http://", "https://")) and text.endswith(URL_SUFFIX):
        return "target"
    return None


def _patch_string(process, frame, base, offset, layout, pointer, length, capacity, new_url):
    payload = new_url.encode("utf-8")
    pointer_field = base + offset
    if layout == "ptr_len_cap":
        length_field = base + offset + 8
        capacity_field = base + offset + 16
    else:
        capacity_field = base + offset + 8
        length_field = base + offset + 16

    if len(payload) <= capacity and _write_memory(process, pointer, payload):
        return {
            "patch_mode": "in_place",
            "old_ptr": hex(pointer),
            "new_ptr": hex(pointer),
            "old_len": length,
            "new_len": len(payload),
            "capacity": capacity,
            "write_fields": _write_memory(process, length_field, struct.pack("<Q", len(payload))),
        }

    allocated = _malloc(process, frame, len(payload) + 1)
    if allocated is None:
        return None
    if not _write_memory(process, allocated, payload + b"\x00"):
        return None
    ok = (
        _write_memory(process, pointer_field, struct.pack("<Q", allocated))
        and _write_memory(process, length_field, struct.pack("<Q", len(payload)))
        and _write_memory(process, capacity_field, struct.pack("<Q", len(payload)))
    )
    if not ok:
        return None
    return {
        "patch_mode": "allocated",
        "old_ptr": hex(pointer),
        "new_ptr": hex(allocated),
        "old_len": length,
        "new_len": len(payload),
        "capacity": len(payload),
    }


def _scan_region(process, frame, base, label, old_url, new_url):
    size = MAX_STACK_SCAN_BYTES if label == "sp" else MAX_SCAN_BYTES
    data = _read_memory(process, base, size)
    if data is None:
        return []
    results = []
    for offset in range(0, max(0, len(data) - 24), 8):
        first, second, third = struct.unpack_from("<QQQ", data, offset)
        variants = (
            ("ptr_len_cap", first, second, third),
            ("ptr_cap_len", first, third, second),
        )
        for layout, pointer, length, capacity in variants:
            if (
                length <= 0
                or length > MAX_TEXT_LEN
                or capacity < length
                or capacity > MAX_TEXT_LEN * 4
            ):
                continue
            text = _read_text(process, pointer, length)
            if text is None:
                continue
            match = _matches_target(text, old_url, new_url)
            if match == "already_patched":
                results.append(
                    {
                        "kind": "already_patched",
                        "label": label,
                        "base": hex(base),
                        "offset": hex(offset),
                        "layout": layout,
                        "current_text": text,
                    }
                )
                continue
            if match != "target":
                continue
            patch = _patch_string(
                process,
                frame,
                base,
                offset,
                layout,
                pointer,
                length,
                capacity,
                new_url,
            )
            if patch is None:
                results.append(
                    {
                        "kind": "patch_failed",
                        "label": label,
                        "base": hex(base),
                        "offset": hex(offset),
                        "layout": layout,
                        "current_text": text,
                    }
                )
                continue
            patch.update(
                {
                    "kind": "patched",
                    "label": label,
                    "base": hex(base),
                    "offset": hex(offset),
                    "layout": layout,
                    "old_url": text,
                    "new_url": new_url,
                }
            )
            results.append(patch)
    return results


def _scan_frame(process, frame, old_url, new_url):
    results = []
    seen = set()
    for index in range(29):
        label = f"x{index}"
        value = _register_value(frame, label)
        if value is None or value in seen:
            continue
        seen.add(value)
        results.extend(_scan_region(process, frame, value, label, old_url, new_url))
    for label in ("fp", "sp"):
        value = _register_value(frame, label)
        if value is None or value in seen:
            continue
        seen.add(value)
        results.extend(_scan_region(process, frame, value, label, old_url, new_url))
    return results


def _configure_breakpoints(target):
    breakpoints = []
    for regex in BREAKPOINT_REGEXES:
        breakpoint = target.BreakpointCreateByRegex(regex)
        if breakpoint.IsValid():
            breakpoint.SetAutoContinue(False)
            breakpoints.append({"regex": regex, "locations": breakpoint.GetNumLocations()})
    return breakpoints


def _run_rewriter(debugger, config):
    debugger.SetAsync(True)
    listener = lldb.SBListener("mtga-trae-url-rewriter")
    target = debugger.CreateTarget(str(config["module_path"]))
    if not target.IsValid():
        target = debugger.CreateTarget("")
    error = lldb.SBError()
    process = target.AttachToProcessWithID(listener, int(config["pid"]), error)
    if not error.Success() or not process.IsValid():
        raise RuntimeError(f"lldb_attach_failed: {error.GetCString()}")

    breakpoints = _configure_breakpoints(target)
    if not any(item["locations"] > 0 for item in breakpoints):
        process.Detach()
        raise RuntimeError(f"lldb_breakpoint_not_found: {breakpoints}")

    stats = {
        "pid": int(config["pid"]),
        "module_path": str(config["module_path"]),
        "old_url": config["old_url"],
        "new_url": config["new_url"],
        "breakpoints": breakpoints,
        "hit_count": 0,
        "patched_count": 0,
        "already_patched_count": 0,
        "patch_failed_count": 0,
        "events": [],
        "status": "running",
        "debug_detached": False,
    }
    armed = {
        "ts": _now_iso(),
        "kind": "armed",
        "pid": stats["pid"],
        "breakpoint": "lldb:function-regex",
        "breakpoint_rva": "lldb:function-regex",
        "dll_sha256": config.get("dll_sha256"),
        "pattern_count": config.get("pattern_count"),
        "old_url": config["old_url"],
        "new_url": config["new_url"],
        "breakpoints": breakpoints,
        "compatibility_changed_since_preflight": None,
    }
    stats["events"].append(armed)
    _record(config.get("output_path"), armed)

    started = time.monotonic()
    process.Continue()
    try:
        while True:
            if config.get("stop_file") and Path(config["stop_file"]).exists():
                stats["status"] = "stop_requested"
                return stats
            duration = int(config.get("duration_seconds") or 0)
            if duration > 0 and time.monotonic() - started > duration:
                stats["status"] = "timeout"
                return stats

            event = lldb.SBEvent()
            if not listener.WaitForEvent(1, event):
                continue
            if not lldb.SBProcess.EventIsProcessEvent(event):
                continue
            state = lldb.SBProcess.GetStateFromEvent(event)
            if state == lldb.eStateExited:
                stats["status"] = "process_exited"
                return stats
            if state not in (lldb.eStateStopped, lldb.eStateCrashed, lldb.eStateSuspended):
                continue
            if state == lldb.eStateCrashed:
                stats["status"] = "process_crashed"
                return stats

            for thread in process:
                if thread.GetStopReason() != lldb.eStopReasonBreakpoint:
                    continue
                frame = thread.GetFrameAtIndex(0)
                if not frame.IsValid():
                    continue
                stats["hit_count"] += 1
                for item in _scan_frame(process, frame, config["old_url"], config["new_url"]):
                    item["ts"] = _now_iso()
                    item["thread_id"] = thread.GetThreadID()
                    if item["kind"] == "patched":
                        stats["patched_count"] += 1
                        item["count"] = stats["patched_count"]
                    elif item["kind"] == "already_patched":
                        stats["already_patched_count"] += 1
                        item["count"] = stats["already_patched_count"]
                    elif item["kind"] == "patch_failed":
                        stats["patch_failed_count"] += 1
                        item["count"] = stats["patch_failed_count"]
                    stats["events"].append(item)
                    _record(config.get("output_path"), item)
            process.Continue()
    finally:
        detached = process.Detach()
        stats["debug_detached"] = bool(detached.Success())
        if not detached.Success():
            stats["debug_detach_error"] = detached.GetCString()


def mtga_trae_url_rewriter(debugger, command, _exe_ctx, result, _internal_dict):
    try:
        parts = shlex.split(command)
        if not parts:
            raise ValueError("missing config path")
        config_path = Path(parts[0])
        config = json.loads(config_path.read_text(encoding="utf-8"))
        summary = _run_rewriter(debugger, config)
    except Exception as exc:
        summary = {
            "status": "error",
            "error": f"{type(exc).__name__}: {exc}",
            "traceback": traceback.format_exc(),
        }
    summary_path = None
    try:
        summary_path = config.get("summary_path")
    except Exception:
        summary_path = None
    if summary_path:
        Path(summary_path).write_text(
            json.dumps(summary, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    print(json.dumps(summary, ensure_ascii=False), flush=True)
    if summary.get("status") == "error":
        result.SetError(summary.get("error") or "mtga-trae-url-rewriter failed")


def __lldb_init_module(debugger, _internal_dict):
    debugger.HandleCommand(
        "command script add -f "
        + __name__
        + ".mtga_trae_url_rewriter "
        + "mtga-trae-url-rewriter"
    )
'''


def _now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")


def _record(output_path: Path | None, payload: dict[str, Any]) -> None:
    if output_path is None:
        return
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("a", encoding="utf-8") as fp:
        fp.write(json.dumps(payload, ensure_ascii=False) + "\n")


def _resolve_lldb_path() -> str:
    xcrun_path = shutil.which("xcrun")
    if xcrun_path:
        try:
            completed = subprocess.run(
                [xcrun_path, "--find", "lldb"],
                check=False,
                capture_output=True,
                text=True,
                timeout=3,
            )
        except Exception:
            completed = None
        if completed is not None and completed.returncode == 0:
            lldb_path = completed.stdout.strip()
            if lldb_path:
                return lldb_path
    lldb_path = shutil.which("lldb")
    if lldb_path:
        return lldb_path
    raise RuntimeError("lldb_not_found")


def _build_lldb_env() -> dict[str, str]:
    env = dict(os.environ)
    for key in LLDB_ENV_VARS_TO_CLEAR:
        env.pop(key, None)
    return env


def _quote_lldb_arg(value: str | Path) -> str:
    return json.dumps(str(value), ensure_ascii=False)


def _find_pid_with_module(module_path: Path, *, timeout_seconds: int) -> int:
    deadline = time.monotonic() + timeout_seconds
    while True:
        try:
            completed = subprocess.run(
                ["lsof", "-t", str(module_path)],
                check=False,
                capture_output=True,
                text=True,
                timeout=DEFAULT_LSOF_TIMEOUT_SECONDS,
            )
        except Exception:
            completed = None
        if completed is not None and completed.returncode == 0:
            pids: list[int] = []
            for raw_line in completed.stdout.splitlines():
                line = raw_line.strip()
                if not line:
                    continue
                try:
                    pids.append(int(line))
                except ValueError:
                    continue
            if pids:
                return sorted(set(pids))[0]
        if time.monotonic() >= deadline:
            raise RuntimeError(f"module_not_loaded: {module_path}")
        time.sleep(DEFAULT_POLL_SECONDS)


def _coerce_report(raw_report: object) -> dict[str, Any]:
    if isinstance(raw_report, dict):
        return cast("dict[str, Any]", raw_report)
    return {}


def _runtime_report(config: RewriterConfig) -> dict[str, Any]:
    report = build_compatibility_report(config.module_path, old_url=config.old_url)
    if report.blocked:
        raise RuntimeError(
            "Trae native macOS runtime compatibility blocked before attach: "
            f"reason={report.reason} "
            f"pattern_count={report.pattern_count} "
            f"sha={report.dll_sha256 or '<empty>'} "
            f"dylib={report.dll_path}"
        )
    return report.to_dict()


def _tail(value: str, max_chars: int = LLDB_STDIO_TAIL_CHARS) -> str:
    return value[-max_chars:].strip()


def run_rewriter_config(config: RewriterConfig) -> dict[str, Any]:
    return run_rewriter(argparse.Namespace(**config.__dict__))


def run_rewriter(args: argparse.Namespace) -> dict[str, Any]:
    module_path = Path(args.module_path)
    raw_preflight_report = getattr(args, "compatibility_report", None)
    preflight_report = _coerce_report(raw_preflight_report)
    runtime_report = _runtime_report(
        RewriterConfig(
            pid=getattr(args, "pid", None),
            module_path=module_path,
            old_url=str(getattr(args, "old_url", DEFAULT_OLD_URL)),
            new_url=str(getattr(args, "new_url", DEFAULT_NEW_URL)),
            duration_seconds=int(getattr(args, "duration_seconds", DEFAULT_DURATION_SECONDS)),
            output_path=getattr(args, "output_path", None),
            stop_file=getattr(args, "stop_file", None),
            quiet=bool(getattr(args, "quiet", False)),
        )
    )
    compatibility_report = runtime_report or preflight_report
    target_pid = getattr(args, "pid", None)
    if target_pid is None:
        target_pid = _find_pid_with_module(
            module_path,
            timeout_seconds=int(
                getattr(args, "wait_for_module_seconds", DEFAULT_WAIT_FOR_MODULE_SECONDS)
            ),
        )

    output_path = getattr(args, "output_path", None)
    output_path = Path(output_path) if output_path is not None else None
    stop_file = getattr(args, "stop_file", None)
    stop_file = Path(stop_file) if stop_file is not None else None
    work_dir = (output_path.parent if output_path is not None else Path.cwd()).resolve()
    work_dir.mkdir(parents=True, exist_ok=True)

    script_path = work_dir / "trae_native_lldb_url_rewriter.py"
    config_path = work_dir / "trae_native_lldb_url_rewriter.config.json"
    summary_path = work_dir / "trae_native_lldb_url_rewriter.summary.json"
    stdout_path = work_dir / "trae_native_lldb_url_rewriter.stdout.log"
    stderr_path = work_dir / "trae_native_lldb_url_rewriter.stderr.log"
    script_path.write_text(LLDB_REWRITER_SCRIPT, encoding="utf-8")
    summary_path.write_text("", encoding="utf-8")
    config_payload = {
        "pid": target_pid,
        "module_path": str(module_path),
        "old_url": str(getattr(args, "old_url", DEFAULT_OLD_URL)),
        "new_url": str(getattr(args, "new_url", DEFAULT_NEW_URL)),
        "duration_seconds": int(getattr(args, "duration_seconds", DEFAULT_DURATION_SECONDS)),
        "output_path": str(output_path) if output_path is not None else None,
        "stop_file": str(stop_file) if stop_file is not None else None,
        "summary_path": str(summary_path),
        "dll_sha256": compatibility_report.get("dll_sha256"),
        "pattern_count": compatibility_report.get("pattern_count"),
    }
    config_path.write_text(
        json.dumps(config_payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    lldb_path = _resolve_lldb_path()
    command = [
        lldb_path,
        "--batch",
        "-o",
        f"command script import {_quote_lldb_arg(script_path)}",
        "-o",
        f"mtga-trae-url-rewriter {_quote_lldb_arg(config_path)}",
    ]
    completed = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=_build_lldb_env(),
    )
    stdout_path.write_text(completed.stdout, encoding="utf-8")
    stderr_path.write_text(completed.stderr, encoding="utf-8")

    summary: dict[str, Any]
    try:
        raw_summary = json.loads(summary_path.read_text(encoding="utf-8") or "{}")
    except Exception:
        raw_summary = {}
    summary = cast("dict[str, Any]", raw_summary) if isinstance(raw_summary, dict) else {}
    if not summary:
        summary = {
            "status": "error",
            "error": "lldb_summary_missing",
        }
    summary["pid"] = target_pid
    summary["module_path"] = str(module_path)
    summary["lldb_returncode"] = completed.returncode
    summary["lldb_stdout_tail"] = _tail(completed.stdout)
    summary["lldb_stderr_tail"] = _tail(completed.stderr)
    error_text = str(summary.get("error") or "")
    if "lldb_attach_failed" in error_text:
        summary["attach_diagnostics"] = diagnose_lldb_attach_failure(
            int(target_pid),
            module_path=module_path,
        )
    if completed.returncode != 0 and summary.get("status") != "error":
        summary["status"] = "error"
        summary["error"] = f"lldb_returncode:{completed.returncode}"
    if output_path is not None and summary.get("status") == "error":
        attach_diagnostics = summary.get("attach_diagnostics")
        _record(
            output_path,
            {
                "ts": _now_iso(),
                "kind": "error",
                "error": summary.get("error"),
                "lldb_returncode": completed.returncode,
                "attach_diagnostics": (
                    attach_diagnostics if isinstance(attach_diagnostics, dict) else None
                ),
            },
        )
    return summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="macOS LLDB-backed Trae native SseOpenPayload URL rewriter."
    )
    parser.add_argument(
        "--pid",
        type=int,
        help="optional Trae helper PID that loaded libai_agent.dylib",
    )
    parser.add_argument("--module-path", type=Path, default=RewriterConfig.module_path)
    parser.add_argument("--old-url", default=DEFAULT_OLD_URL)
    parser.add_argument("--new-url", default=DEFAULT_NEW_URL)
    parser.add_argument("--duration-seconds", type=int, default=DEFAULT_DURATION_SECONDS)
    parser.add_argument(
        "--wait-for-module-seconds",
        type=int,
        default=DEFAULT_WAIT_FOR_MODULE_SECONDS,
    )
    parser.add_argument("--output-path", type=Path)
    parser.add_argument("--stop-file", type=Path)
    parser.add_argument("--quiet", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.output_path:
        args.output_path.parent.mkdir(parents=True, exist_ok=True)
        args.output_path.write_text("", encoding="utf-8")
    try:
        summary = run_rewriter(args)
    except KeyboardInterrupt:
        summary = {"status": "interrupted"}
    except Exception as exc:  # noqa: BLE001
        summary = {"status": "error", "error": f"{type(exc).__name__}: {exc}"}

    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)
    return 1 if summary.get("status") == "error" else 0


if __name__ == "__main__":
    raise SystemExit(main())
