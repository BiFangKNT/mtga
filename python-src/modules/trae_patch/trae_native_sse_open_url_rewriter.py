from __future__ import annotations

import argparse
import contextlib
import ctypes
import json
import sys
import time
from ctypes import wintypes
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

from .trae_native_breakpoint_probe import (
    DBG_CONTINUE,
    DBG_EXCEPTION_NOT_HANDLED,
    DEBUG_EVENT,
    EFLAGS_OFFSET,
    EXCEPTION_BREAKPOINT,
    EXCEPTION_DEBUG_EVENT,
    EXCEPTION_SINGLE_STEP,
    EXIT_PROCESS_DEBUG_EVENT,
    REGISTER_OFFSETS,
    RIP_OFFSET,
    TRAP_FLAG,
    ContinueDebugEvent,
    DebugActiveProcess,
    DebugActiveProcessStop,
    WaitForDebugEvent,
    close_process_handle,
    format_registers,
    format_timeout_at,
    kernel32,
    last_windows_error,
    open_process_handle,
    open_thread_handle,
    put_u64,
    read_process_memory,
    read_thread_context,
    resolve_runtime_module,
    write_process_memory,
    write_thread_context,
)
from .trae_native_hook_candidates import AI_AGENT_DLL
from .trae_native_runtime_breakpoints import enable_debug_privilege
from .trae_native_string_offsets import find_all, parse_pe_layout

MEM_COMMIT = 0x1000
MEM_RESERVE = 0x2000
PAGE_READWRITE = 0x04

VirtualAllocEx = kernel32.VirtualAllocEx
VirtualAllocEx.argtypes = [
    wintypes.HANDLE,
    ctypes.c_void_p,
    ctypes.c_size_t,
    wintypes.DWORD,
    wintypes.DWORD,
]
VirtualAllocEx.restype = ctypes.c_void_p

URL_COPY_PATTERN = bytes.fromhex("48 8b 52 08 4d 8b 46 10 48 8d 8d 20 01 00 00")
URL_COPY_CALL_OFFSET = 0x0F
DEFAULT_OLD_URL = "https://api.openai.com/v1/chat/completions"
DEFAULT_NEW_URL = "http://127.0.0.1:18083/v1/chat/completions"
DEFAULT_DURATION_SECONDS = 300
DEFAULT_MAX_PATCHES = 0
DEFAULT_POLL_MILLISECONDS = 1000
DEFAULT_WAIT_FOR_MODULE_SECONDS = 300
MAX_URL_TEXT_LEN = 4096
MIN_USER_POINTER = 0x10000


@dataclass(frozen=True)
class RewriterConfig:
    pid: int | None = None
    module_path: Path = AI_AGENT_DLL
    breakpoint_rva: int | None = None
    old_url: str = DEFAULT_OLD_URL
    new_url: str = DEFAULT_NEW_URL
    duration_seconds: int = DEFAULT_DURATION_SECONDS
    max_patches: int = DEFAULT_MAX_PATCHES
    wait_for_module_seconds: int = DEFAULT_WAIT_FOR_MODULE_SECONDS
    poll_milliseconds: int = DEFAULT_POLL_MILLISECONDS
    output_path: Path | None = None
    stop_file: Path | None = None
    quiet: bool = False


def _now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")


def _read_u32(context: bytearray, offset: int) -> int:
    return int.from_bytes(context[offset : offset + 4], "little")


def _put_u32(context: bytearray, offset: int, value: int) -> None:
    context[offset : offset + 4] = int(value & 0xFFFFFFFF).to_bytes(4, "little")


def _read_utf8(process: ctypes.c_void_p, ptr: int, length: int) -> str | None:
    if ptr <= MIN_USER_POINTER or length <= 0 or length > MAX_URL_TEXT_LEN:
        return None
    data = read_process_memory(process, ptr, length)
    if len(data) != length:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None


def _record(output_path: Path | None, payload: dict[str, Any]) -> None:
    if output_path is None:
        return
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("a", encoding="utf-8") as fp:
        fp.write(json.dumps(payload, ensure_ascii=False) + "\n")


def _allocate_remote_utf8(process: wintypes.HANDLE, text: str) -> dict[str, Any]:
    payload = text.encode("utf-8")
    allocation_size = len(payload) + 1
    allocated = VirtualAllocEx(
        process,
        None,
        allocation_size,
        MEM_COMMIT | MEM_RESERVE,
        PAGE_READWRITE,
    )
    if not allocated:
        raise last_windows_error("VirtualAllocEx")
    allocated_address = int(ctypes.cast(allocated, ctypes.c_void_p).value or 0)
    if allocated_address <= MIN_USER_POINTER:
        raise RuntimeError(f"VirtualAllocEx 返回地址异常: {hex(allocated_address)}")
    write_process_memory(process, allocated_address, payload + b"\x00")
    return {
        "allocated_address": hex(allocated_address),
        "allocation_size": allocation_size,
        "payload_len": len(payload),
        "payload_preview": text,
    }


def _locate_url_copy_call_rva(module_path: Path) -> int:
    data = module_path.read_bytes()
    layout = parse_pe_layout(data)
    offsets = find_all(data, URL_COPY_PATTERN)
    if len(offsets) != 1:
        raise RuntimeError(
            "无法唯一定位 SseOpenPayload URL copy call；"
            f"pattern_count={len(offsets)}"
        )
    location = layout.locate_file_offset(offsets[0] + URL_COPY_CALL_OFFSET)
    rva = location.get("rva")
    if not isinstance(rva, str) or rva == "<unknown>":
        raise RuntimeError(f"无法把 URL copy call file offset 转换为 RVA: {location}")
    return int(rva, 0)


def run_rewriter_config(config: RewriterConfig) -> dict[str, Any]:
    return run_rewriter(argparse.Namespace(**config.__dict__))


def run_rewriter(args: argparse.Namespace) -> dict[str, Any]:  # noqa: PLR0912, PLR0915
    breakpoint_rva = (
        args.breakpoint_rva
        if args.breakpoint_rva is not None
        else _locate_url_copy_call_rva(args.module_path)
    )
    target_pid, module_base, module_size = resolve_runtime_module(
        args.pid,
        args.module_path,
        wait_for_module_seconds=args.wait_for_module_seconds,
    )
    breakpoint_address = module_base + breakpoint_rva
    privilege = enable_debug_privilege()
    if not DebugActiveProcess(target_pid):
        error = last_windows_error(f"DebugActiveProcess({target_pid})")
        error.add_note(f"debug_privilege={privilege}")
        raise error

    process: wintypes.HANDLE | None = None
    original = b""
    started = time.monotonic()
    stats: dict[str, Any] = {
        "pid": target_pid,
        "module_base": hex(module_base),
        "module_size": hex(module_size),
        "breakpoint": hex(breakpoint_address),
        "breakpoint_rva": hex(breakpoint_rva),
        "old_url": args.old_url,
        "new_url": args.new_url,
        "duration_seconds": args.duration_seconds,
        "max_patches": args.max_patches,
        "hit_count": 0,
        "patched_count": 0,
        "already_patched_count": 0,
        "unexpected_count": 0,
        "single_step_count": 0,
        "events": [],
        "status": "running",
    }
    pending_rearm_threads: set[int] = set()
    try:
        process = open_process_handle(target_pid)
        original = read_process_memory(process, breakpoint_address, 1)
        if len(original) != 1:
            raise RuntimeError(f"读取断点原字节失败: {hex(breakpoint_address)}")

        allocation = _allocate_remote_utf8(process, args.new_url)
        new_ptr = int(str(allocation["allocated_address"]), 16)
        new_len = len(args.new_url.encode("utf-8"))
        stats["allocation"] = allocation
        write_process_memory(process, breakpoint_address, b"\xCC")
        armed_payload = {
            "ts": _now_iso(),
            "kind": "armed",
            "pid": target_pid,
            "breakpoint": hex(breakpoint_address),
            "breakpoint_rva": hex(breakpoint_rva),
            "new_url": args.new_url,
        }
        stats["events"].append(armed_payload)
        _record(args.output_path, armed_payload)
        if not args.quiet:
            print(json.dumps(armed_payload, ensure_ascii=False), flush=True)

        while True:
            can_exit = not pending_rearm_threads
            if can_exit and args.stop_file is not None and args.stop_file.exists():
                stats["status"] = "stop_requested"
                return stats
            elapsed = time.monotonic() - started
            if can_exit and args.duration_seconds > 0 and elapsed > args.duration_seconds:
                stats["status"] = "timeout"
                stats["timeout_at"] = format_timeout_at(0)
                return stats
            if can_exit and args.max_patches > 0 and stats["patched_count"] >= args.max_patches:
                stats["status"] = "max_patches_reached"
                return stats

            event = DEBUG_EVENT()
            if not WaitForDebugEvent(ctypes.byref(event), args.poll_milliseconds):
                continue

            status = DBG_CONTINUE
            thread_id = int(event.dwThreadId)
            if event.dwDebugEventCode == EXCEPTION_DEBUG_EVENT:
                record = event.u.Exception.ExceptionRecord
                exception_code = int(record.ExceptionCode)
                exception_address = int(record.ExceptionAddress)

                if (
                    exception_code == EXCEPTION_BREAKPOINT
                    and exception_address == breakpoint_address
                ):
                    stats["hit_count"] += 1
                    thread = open_thread_handle(thread_id)
                    try:
                        context = read_thread_context(thread)
                        put_u64(context, RIP_OFFSET, breakpoint_address)
                        registers = format_registers(context)
                        old_ptr = int(registers["rdx"], 16)
                        old_len = int(registers["r8"], 16)
                        current_text = _read_utf8(process, old_ptr, old_len)

                        write_process_memory(process, breakpoint_address, original)
                        if current_text == args.old_url:
                            put_u64(context, REGISTER_OFFSETS["rdx"], new_ptr)
                            put_u64(context, REGISTER_OFFSETS["r8"], new_len)
                            stats["patched_count"] += 1
                            event_payload = {
                                "ts": _now_iso(),
                                "kind": "patched",
                                "count": stats["patched_count"],
                                "thread_id": thread_id,
                                "old_ptr": hex(old_ptr),
                                "old_len": old_len,
                                "new_ptr": hex(new_ptr),
                                "new_len": new_len,
                            }
                            stats["events"].append(event_payload)
                            _record(args.output_path, event_payload)
                            if not args.quiet:
                                print(
                                    json.dumps(event_payload, ensure_ascii=False),
                                    flush=True,
                                )
                        else:
                            kind = (
                                "already_patched"
                                if current_text == args.new_url
                                else "unexpected_url"
                            )
                            if kind == "already_patched":
                                stats["already_patched_count"] += 1
                                count = stats["already_patched_count"]
                            else:
                                stats["unexpected_count"] += 1
                                count = stats["unexpected_count"]
                            event_payload = {
                                "ts": _now_iso(),
                                "kind": kind,
                                "count": count,
                                "thread_id": thread_id,
                                "registers": {
                                    "rdx": registers["rdx"],
                                    "r8": registers["r8"],
                                },
                                "current_text": current_text,
                            }
                            stats["events"].append(event_payload)
                            _record(args.output_path, event_payload)

                        eflags = _read_u32(context, EFLAGS_OFFSET)
                        _put_u32(context, EFLAGS_OFFSET, eflags | TRAP_FLAG)
                        write_thread_context(thread, context)
                        pending_rearm_threads.add(thread_id)
                    finally:
                        close_process_handle(thread)

                elif exception_code == EXCEPTION_SINGLE_STEP and thread_id in pending_rearm_threads:
                    thread = open_thread_handle(thread_id)
                    try:
                        context = read_thread_context(thread)
                        eflags = _read_u32(context, EFLAGS_OFFSET)
                        _put_u32(context, EFLAGS_OFFSET, eflags & ~TRAP_FLAG)
                        write_thread_context(thread, context)
                        write_process_memory(process, breakpoint_address, b"\xCC")
                        pending_rearm_threads.remove(thread_id)
                        stats["single_step_count"] += 1
                    finally:
                        close_process_handle(thread)
                else:
                    status = DBG_EXCEPTION_NOT_HANDLED

            elif event.dwDebugEventCode == EXIT_PROCESS_DEBUG_EVENT:
                stats["status"] = "process_exited"
                return stats

            ContinueDebugEvent(event.dwProcessId, event.dwThreadId, status)
    finally:
        if process is not None and original:
            with contextlib.suppress(Exception):
                write_process_memory(process, breakpoint_address, original)
        DebugActiveProcessStop(target_pid)
        if process is not None:
            close_process_handle(process)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="持续在 native SseOpenPayload URL copy call 前重写 reqwest 目标 URL。"
    )
    parser.add_argument("--pid", type=int, help="可选：指定已加载 ai_agent.dll 的 Trae PID")
    parser.add_argument("--module-path", type=Path, default=AI_AGENT_DLL, help="ai_agent.dll 路径")
    parser.add_argument(
        "--breakpoint-rva",
        type=lambda value: int(value, 0),
        help="SseOpenPayload URL copy call RVA；不传则按字节模式自动定位",
    )
    parser.add_argument("--old-url", default=DEFAULT_OLD_URL, help="要匹配的原 URL")
    parser.add_argument("--new-url", default=DEFAULT_NEW_URL, help="要改写成的新 URL")
    parser.add_argument(
        "--duration-seconds",
        type=int,
        default=DEFAULT_DURATION_SECONDS,
        help="运行时长；<=0 表示一直运行到进程退出或 Ctrl+C",
    )
    parser.add_argument(
        "--max-patches",
        type=int,
        default=DEFAULT_MAX_PATCHES,
        help="成功改写次数上限；0 表示不限",
    )
    parser.add_argument(
        "--wait-for-module-seconds",
        type=int,
        default=DEFAULT_WAIT_FOR_MODULE_SECONDS,
    )
    parser.add_argument(
        "--poll-milliseconds",
        type=int,
        default=DEFAULT_POLL_MILLISECONDS,
        help="WaitForDebugEvent 轮询间隔",
    )
    parser.add_argument("--output-path", type=Path, help="可选 JSONL 事件输出")
    parser.add_argument("--stop-file", type=Path, help="文件存在时主动退出并恢复断点")
    parser.add_argument("--quiet", action="store_true", help="只输出最终 summary")
    return parser


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        cast(Any, sys.stdout).reconfigure(encoding="utf-8", errors="backslashreplace")
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

