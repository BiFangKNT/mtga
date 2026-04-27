from __future__ import annotations

import argparse
import bisect
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

PYTHON_SRC_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(PYTHON_SRC_DIR))

from modules.trae_patch.backends import MacOSNativeBackend  # noqa: E402
from modules.trae_patch.macos.compatibility import (  # noqa: E402
    build_compatibility_report,
    parse_macho_layout,
)

DEFAULT_ARTIFACT_ROOT = Path("python-src/artifacts/trae_macos_native_symbol_report")
DEFAULT_TRAE_PATH = "/Applications/Trae.app"
DEFAULT_MAX_DISASM_LINES = 220
DEFAULT_MAX_MARKER_HITS = 20
DEFAULT_MAX_CAVES = 12
DEFAULT_MIN_TEXT_ZERO_CAVE_BYTES = 32
DEFAULT_MIN_TEXT_NOP_CAVE_BYTES = 16
DEFAULT_MIN_TRAMPOLINE_BYTES = 64
ARM64_BL_RANGE_BYTES = 128 * 1024 * 1024
ARM64_BRANCH_OPCODE_MASK = 0xFC000000
ARM64_B_OPCODE = 0x14000000
ARM64_BL_OPCODE = 0x94000000
ARM64_BRANCH_IMM_MASK = 0x03FFFFFF
NM_MIN_COLUMNS = 3
ASCII_PRINTABLE_MIN = 32
ASCII_PRINTABLE_MAX = 127
ARM64_NOP = b"\x1f\x20\x03\xd5"
MAX_DIRECT_XREF_CALLERS = 32

SYMBOL_TARGETS: tuple[tuple[str, str], ...] = (
    (
        "handle_sse_open_closure",
        "__ZN25custom_model_proxy_client15message_handler14MessageHandler15handle_sse_open28_$u7b$$u7b$closure$u7d$$u7d$17hdb481d17e266a2cdE",
    ),
    (
        "net_bridge_http_send",
        "__ZN149_$LT$ai_agent..infrastructure..adapter..net_bridge_http_client..NetBridgeHttpClient$u20$as$u20$custom_model_proxy_client..http_client..HttpClient$GT$4send17h05912d8ccc606d3eE",
    ),
    (
        "net_bridge_http_send_closure",
        "__ZN149_$LT$ai_agent..infrastructure..adapter..net_bridge_http_client..NetBridgeHttpClient$u20$as$u20$custom_model_proxy_client..http_client..HttpClient$GT$4send28_$u7b$$u7b$closure$u7d$$u7d$17h6570596625bdffabE",
    ),
    (
        "request_builder_new",
        "__ZN10net_bridge15request_builder14RequestBuilder3new17h426821ce7468a4fbE",
    ),
    (
        "request_builder_backend_auto",
        "__ZN10net_bridge15request_builder14RequestBuilder12backend_auto17hc73cac76f75638a6E",
    ),
    (
        "request_builder_header",
        "__ZN10net_bridge15request_builder14RequestBuilder6header17hcd619ba215cd95a4E",
    ),
    (
        "request_builder_body",
        "__ZN10net_bridge15request_builder14RequestBuilder4body17h86c17ff0ddfe2708E",
    ),
    (
        "request_builder_send_closure",
        "__ZN10net_bridge15request_builder14RequestBuilder4send28_$u7b$$u7b$closure$u7d$$u7d$17hdbe1edab16e09c52E",
    ),
    (
        "reqwest_client_build",
        "__ZN10net_bridge4http6client7reqwest19ReqwestClientBridge10new_shared5build17h2fb513e37125ecbbE",
    ),
    (
        "reqwest_post_configured",
        "__ZN122_$LT$net_bridge..http..client..reqwest..ReqwestClientBridge$u20$as$u20$net_bridge..http..types..BlockingResponseClient$GT$15post_configured17hffda2916dc033ff4E",
    ),
    (
        "reqwest_post_configured_closure",
        "__ZN122_$LT$net_bridge..http..client..reqwest..ReqwestClientBridge$u20$as$u20$net_bridge..http..types..BlockingResponseClient$GT$15post_configured28_$u7b$$u7b$closure$u7d$$u7d$17ha9158265d818ca8eE",
    ),
)
MARKER_TARGETS: tuple[str, ...] = (
    "/v1/chat/completions",
    "CustomModelProxyManager",
    "SseOpenPayload",
    "NetBridgeHttpClient",
    "icube_ai_custom_model_request_builder",
    "?http_fallback=true",
)
DIRECT_XREF_TARGETS: tuple[tuple[str, str], ...] = (
    (
        "handle_sse_open_closure",
        "__ZN25custom_model_proxy_client15message_handler14MessageHandler15handle_sse_open28_$u7b$$u7b$closure$u7d$$u7d$17hdb481d17e266a2cdE",
    ),
    (
        "net_bridge_http_send",
        "__ZN149_$LT$ai_agent..infrastructure..adapter..net_bridge_http_client..NetBridgeHttpClient$u20$as$u20$custom_model_proxy_client..http_client..HttpClient$GT$4send17h05912d8ccc606d3eE",
    ),
    (
        "reqwest_post_configured",
        "__ZN122_$LT$net_bridge..http..client..reqwest..ReqwestClientBridge$u20$as$u20$net_bridge..http..types..BlockingResponseClient$GT$15post_configured17hffda2916dc033ff4E",
    ),
    (
        "tunnel_handle_http_poll_closure",
        "__ZN25custom_model_proxy_client6tunnel13TunnelManager16handle_http_poll28_$u7b$$u7b$closure$u7d$$u7d$17h42dabc7962b8b84aE",
    ),
    (
        "tunnel_handle_command_closure",
        "__ZN25custom_model_proxy_client6tunnel13TunnelManager14handle_command28_$u7b$$u7b$closure$u7d$$u7d$17hfc90cbd94d73bd5eE",
    ),
    (
        "http_transport_queue_message",
        "__ZN25custom_model_proxy_client14http_transport13HttpTransport13queue_message28_$u7b$$u7b$closure$u7d$$u7d$17h4b6824cac3acc8cbE",
    ),
    (
        "http_transport_send_response",
        "__ZN25custom_model_proxy_client14http_transport13HttpTransport13send_response28_$u7b$$u7b$closure$u7d$$u7d$17h9b57439869c8093dE",
    ),
    (
        "http_transport_send_system_error",
        "__ZN25custom_model_proxy_client14http_transport13HttpTransport17send_system_error28_$u7b$$u7b$closure$u7d$$u7d$17h0ee15bf8555172f0E",
    ),
    (
        "http_transport_send_sse_error",
        "__ZN25custom_model_proxy_client14http_transport13HttpTransport14send_sse_error28_$u7b$$u7b$closure$u7d$$u7d$17hd5e29c7e62eedcb7E",
    ),
    (
        "http_transport_send_sse_delta",
        "__ZN25custom_model_proxy_client14http_transport13HttpTransport14send_sse_delta28_$u7b$$u7b$closure$u7d$$u7d$17hf9abe204cf3d46c3E",
    ),
    (
        "http_transport_send_sse_end",
        "__ZN25custom_model_proxy_client14http_transport13HttpTransport12send_sse_end28_$u7b$$u7b$closure$u7d$$u7d$17h1fa5929d687a3af0E",
    ),
    (
        "default_handler_handle_sse_closure",
        "__ZN139_$LT$custom_model_proxy_client..default_handler..DefaultSseProxyHandler$u20$as$u20$custom_model_proxy_client..messages..SseProxyHandler$GT$10handle_sse28_$u7b$$u7b$closure$u7d$$u7d$17h0271e1eca3661b45E",
    ),
    (
        "aws_handler_handle_sse_closure",
        "__ZN128_$LT$custom_model_proxy_client..aws_handler..AWSProxyHandler$u20$as$u20$custom_model_proxy_client..messages..SseProxyHandler$GT$10handle_sse28_$u7b$$u7b$closure$u7d$$u7d$17hba805c3224dd8b75E",
    ),
    (
        "reqwest_client_request",
        "__ZN7reqwest10async_impl6client6Client7request17h067074143593adacE",
    ),
    (
        "reqwest_client_get",
        "__ZN7reqwest10async_impl6client6Client3get",
    ),
    (
        "reqwest_client_post",
        "__ZN7reqwest10async_impl6client6Client4post17h8b5e56b0aeea9972E",
    ),
    (
        "reqwest_client_put",
        "__ZN7reqwest10async_impl6client6Client3put",
    ),
)


def _now_stamp() -> str:
    return time.strftime("%Y%m%dT%H%M%S")


def _ascii_preview(data: bytes) -> str:
    return "".join(
        chr(byte) if ASCII_PRINTABLE_MIN <= byte < ASCII_PRINTABLE_MAX else "."
        for byte in data
    )


def _run_command(command: list[str], *, timeout: float = 15) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )


def _find_app_bundle(path: Path) -> Path | None:
    candidates = (path, *path.parents)
    for candidate in candidates:
        if candidate.suffix.lower() == ".app" and candidate.is_dir():
            return candidate
    return None


def _resolve_paths(raw_trae_path: str, raw_module_path: str | None) -> dict[str, Path]:
    backend = MacOSNativeBackend()
    executable = backend.resolve_trae_executable(raw_trae_path)
    if not executable.is_file():
        raise RuntimeError(f"Trae 可执行文件不存在: {executable}")
    app_bundle = _find_app_bundle(executable)
    if app_bundle is None:
        raise RuntimeError(f"无法从路径推导 Trae.app: {executable}")

    if raw_module_path is not None:
        module_path = Path(raw_module_path).expanduser().resolve()
    else:
        module_path = backend.resolve_module_path(executable)
    if not module_path.is_file():
        raise RuntimeError(f"libai_agent.dylib 不存在: {module_path}")

    return {
        "app_bundle": app_bundle,
        "executable": executable,
        "module_path": module_path,
    }


def _load_nm_symbols(module_path: Path) -> dict[str, dict[str, Any]]:
    completed = _run_command(["nm", "-a", str(module_path)], timeout=30)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip() or "nm 执行失败")

    symbols: dict[str, dict[str, Any]] = {}
    for raw_line in completed.stdout.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) < NM_MIN_COLUMNS:
            continue
        address, symbol_type, name = parts[0], parts[1], parts[-1]
        if not address or not all(ch in "0123456789abcdefABCDEF" for ch in address):
            continue
        if name not in symbols:
            symbols[name] = {
                "address": f"0x{address.lower()}",
                "symbol_type": symbol_type,
                "raw_line": line,
            }
    return symbols


def _resolve_direct_xref_targets(
    nm_symbols: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    resolved: list[dict[str, Any]] = []
    for label, needle in DIRECT_XREF_TARGETS:
        matches = [
            (name, meta)
            for name, meta in nm_symbols.items()
            if name == needle or needle in name
        ]
        if len(matches) != 1:
            resolved.append(
                {
                    "label": label,
                    "needle": needle,
                    "resolved": False,
                    "match_count": len(matches),
                    "callers": [],
                }
            )
            continue
        symbol_name, symbol_meta = matches[0]
        resolved.append(
            {
                "label": label,
                "needle": needle,
                "resolved": True,
                "symbol_name": symbol_name,
                "address": symbol_meta["address"],
                "callers": [],
            }
        )
    return resolved


def _locate_section_by_rva(layout: Any, rva: int) -> Any | None:
    for section in layout.sections:
        if section.address <= rva < section.address + section.size:
            return section
    return None


def _text_function_symbols(
    layout: Any,
    nm_symbols: dict[str, dict[str, Any]],
) -> tuple[list[int], list[dict[str, Any]]]:
    records: list[dict[str, Any]] = []
    for name, meta in nm_symbols.items():
        symbol_type = str(meta.get("symbol_type") or "")
        raw_line = str(meta.get("raw_line") or "")
        if symbol_type.lower() != "t" and " FUN " not in raw_line:
            continue
        try:
            address = int(str(meta["address"]), 16)
        except (KeyError, TypeError, ValueError):
            continue
        section = _locate_section_by_rva(layout, address)
        if section is None or section.segment != "__TEXT" or section.section != "__text":
            continue
        records.append(
            {
                "symbol_name": name,
                "address": address,
            }
        )
    records.sort(key=lambda item: int(item["address"]))
    return [int(item["address"]) for item in records], records


def _find_enclosing_text_symbol(
    text_symbol_addresses: list[int],
    text_symbols: list[dict[str, Any]],
    rva: int,
) -> dict[str, Any] | None:
    index = bisect.bisect_right(text_symbol_addresses, rva) - 1
    if index < 0:
        return None
    record = text_symbols[index]
    start = int(record["address"])
    end = text_symbol_addresses[index + 1] if index + 1 < len(text_symbol_addresses) else None
    if rva < start:
        return None
    if end is not None and rva >= end:
        return None
    return record


def _sign_extend(value: int, bits: int) -> int:
    sign_bit = 1 << (bits - 1)
    return (value & (sign_bit - 1)) - (value & sign_bit)


def _branch_target_rva(current_rva: int, instruction: int) -> tuple[str, int] | None:
    opcode = instruction & ARM64_BRANCH_OPCODE_MASK
    if opcode not in (ARM64_B_OPCODE, ARM64_BL_OPCODE):
        return None
    imm26 = instruction & ARM64_BRANCH_IMM_MASK
    offset = _sign_extend(imm26, 26) << 2
    kind = "bl" if opcode == ARM64_BL_OPCODE else "b"
    return kind, current_rva + offset


def _direct_call_xrefs(
    module_path: Path,
    *,
    nm_symbols: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    module_data = module_path.read_bytes()
    layout = parse_macho_layout(module_data)
    text_symbol_addresses, text_symbols = _text_function_symbols(layout, nm_symbols)
    target_reports = _resolve_direct_xref_targets(nm_symbols)
    target_by_rva = {
        int(str(item["address"]), 16): item
        for item in target_reports
        if item.get("resolved") and item.get("address") is not None
    }
    if not target_by_rva:
        return target_reports

    for section in layout.sections:
        if section.segment != "__TEXT" or section.section != "__text":
            continue
        section_data = module_data[section.offset : section.offset + section.size]
        for index in range(0, len(section_data) - 3, 4):
            instruction = int.from_bytes(section_data[index : index + 4], "little")
            current_rva = section.address + index
            branch = _branch_target_rva(current_rva, instruction)
            if branch is None:
                continue
            kind, target_rva = branch
            target = target_by_rva.get(target_rva)
            if target is None:
                continue
            caller = _find_enclosing_text_symbol(text_symbol_addresses, text_symbols, current_rva)
            target["callers"].append(
                {
                    "kind": kind,
                    "site_address": hex(current_rva),
                    "caller_symbol": caller["symbol_name"] if caller is not None else None,
                    "caller_address": hex(int(caller["address"])) if caller is not None else None,
                }
            )

    for item in target_reports:
        callers = item.get("callers")
        if isinstance(callers, list):
            callers.sort(
                key=lambda record: (
                    record.get("caller_symbol") or "",
                    record.get("site_address") or "",
                )
            )
            item["caller_count"] = len(callers)
            item["callers"] = callers[:MAX_DIRECT_XREF_CALLERS]
    return target_reports


def _disassemble_symbol(
    module_path: Path,
    *,
    symbol_name: str,
    artifact_root: Path,
    max_lines: int,
) -> dict[str, Any]:
    completed = _run_command(
        [
            "xcrun",
            "llvm-objdump",
            "--macho",
            "-d",
            "--dis-symname",
            symbol_name,
            str(module_path),
        ],
        timeout=30,
    )
    if completed.returncode != 0:
        return {
            "ok": False,
            "error": completed.stderr.strip() or completed.stdout.strip() or "objdump 执行失败",
        }

    lines = completed.stdout.splitlines()
    trimmed_lines = lines[:max_lines]
    if len(lines) > max_lines:
        trimmed_lines.append(f"... <truncated after {max_lines} lines>")
    text = "\n".join(trimmed_lines).rstrip() + "\n"
    out_path = artifact_root / "disasm" / f"{symbol_name}.txt"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")
    return {
        "ok": True,
        "line_count": len(lines),
        "saved_line_count": len(trimmed_lines),
        "path": str(out_path),
    }


def _find_all(data: bytes, needle: bytes) -> list[int]:
    offsets: list[int] = []
    start = 0
    while True:
        offset = data.find(needle, start)
        if offset < 0:
            return offsets
        offsets.append(offset)
        start = offset + 1


def _marker_hits(
    module_path: Path,
    *,
    markers: tuple[str, ...],
    max_hits: int,
    window_bytes: int = 40,
) -> list[dict[str, Any]]:
    data = module_path.read_bytes()
    layout = parse_macho_layout(data)
    records: list[dict[str, Any]] = []
    for marker in markers:
        needle = marker.encode("utf-8")
        offsets = _find_all(data, needle)
        contexts: list[dict[str, Any]] = []
        for offset in offsets[:max_hits]:
            start = max(0, offset - window_bytes)
            end = min(len(data), offset + len(needle) + window_bytes)
            window = data[start:end]
            contexts.append(
                {
                    "file_offset": hex(offset),
                    "location": layout.locate_file_offset(offset),
                    "window_hex": window.hex(" "),
                    "window_ascii": _ascii_preview(window),
                }
            )
        records.append(
            {
                "marker": marker,
                "count": len(offsets),
                "contexts": contexts,
            }
        )
    return records


def _align_up(value: int, alignment: int) -> int:
    remainder = value % alignment
    return value if remainder == 0 else value + (alignment - remainder)


def _scan_pattern_runs(
    section_data: bytes,
    *,
    pattern: bytes,
    min_run_bytes: int,
) -> list[tuple[int, int]]:
    if not pattern:
        return []
    runs: list[tuple[int, int]] = []
    pattern_len = len(pattern)
    index = 0
    data_len = len(section_data)
    while index <= data_len - pattern_len:
        if section_data[index : index + pattern_len] != pattern:
            index += 1
            continue
        start = index
        index += pattern_len
        while (
            index <= data_len - pattern_len
            and section_data[index : index + pattern_len] == pattern
        ):
            index += pattern_len
        length = index - start
        if length >= min_run_bytes:
            runs.append((start, length))
    return runs


def _text_code_caves(
    module_path: Path,
    *,
    max_results: int = DEFAULT_MAX_CAVES,
    min_zero_run_bytes: int = DEFAULT_MIN_TEXT_ZERO_CAVE_BYTES,
    min_nop_run_bytes: int = DEFAULT_MIN_TEXT_NOP_CAVE_BYTES,
) -> list[dict[str, Any]]:
    data = module_path.read_bytes()
    layout = parse_macho_layout(data)
    records: list[dict[str, Any]] = []
    for section in layout.sections:
        if section.segment != "__TEXT" or section.section != "__text":
            continue
        section_data = data[section.offset : section.offset + section.size]
        zero_runs = _scan_pattern_runs(
            section_data,
            pattern=b"\x00",
            min_run_bytes=min_zero_run_bytes,
        )
        nop_runs = _scan_pattern_runs(
            section_data,
            pattern=ARM64_NOP,
            min_run_bytes=min_nop_run_bytes,
        )
        for start, length in zero_runs:
            file_offset = section.offset + start
            aligned_file_offset = _align_up(file_offset, 4)
            alignment_padding = aligned_file_offset - file_offset
            records.append(
                {
                    "kind": "zero_fill",
                    "length_bytes": length,
                    "aligned_file_offset": hex(aligned_file_offset),
                    "usable_length_bytes": max(0, length - alignment_padding),
                    "location": layout.locate_file_offset(file_offset),
                }
            )
        for start, length in nop_runs:
            file_offset = section.offset + start
            aligned_file_offset = _align_up(file_offset, 4)
            alignment_padding = aligned_file_offset - file_offset
            records.append(
                {
                    "kind": "arm64_nop_fill",
                    "length_bytes": length,
                    "aligned_file_offset": hex(aligned_file_offset),
                    "usable_length_bytes": max(0, length - alignment_padding),
                    "location": layout.locate_file_offset(file_offset),
                }
            )
        break
    records.sort(
        key=lambda item: (
            -int(item["usable_length_bytes"]),
            -int(item["length_bytes"]),
            item["location"]["file_offset"],
        )
    )
    return records[:max_results]


def _build_observations(
    symbols: list[dict[str, Any]],
    markers: list[dict[str, Any]],
    *,
    direct_xrefs: list[dict[str, Any]],
) -> list[str]:
    symbol_labels = {item["label"] for item in symbols if item.get("present")}
    marker_counts = {item["marker"]: item["count"] for item in markers}
    observations: list[str] = []
    if {
        "net_bridge_http_send",
        "net_bridge_http_send_closure",
        "request_builder_new",
        "reqwest_post_configured_closure",
        "request_builder_send_closure",
    }.issubset(symbol_labels):
        observations.append(
            "存在完整的 NetBridgeHttpClient -> RequestBuilder native 调用链，"
            "macOS 侧应继续把 patch 点收敛在 Rust 请求构造/发送边界，"
            "而不是 UI/数据库层。"
        )
        observations.append(
            "当前已确认至少存在 DefaultSseProxyHandler 直达 reqwest "
            "和 NetBridge -> RequestBuilder 两类 native 请求边界；"
            "primary site 需要优先参考 direct xref，而不是只看局部符号名字。"
        )
    if "handle_sse_open_closure" in symbol_labels:
        observations.append(
            "custom_model_proxy_client::handle_sse_open closure 符号可见，"
            "说明 SSE 打开后的 native 路径仍可作为上游入口锚点。"
        )
    if marker_counts.get("/v1/chat/completions", 0) > 0:
        observations.append(
            "dylib 内存在 /v1/chat/completions 字符串锚点，"
            "但是否能直接静态替换仍需结合 RequestBuilder/HttpRequest 布局判断。"
        )
    if marker_counts.get("icube_ai_custom_model_request_builder", 0) > 0:
        observations.append(
            "存在 icube_ai_custom_model_request_builder 埋点字符串，"
            "可作为后续进一步缩小 request builder 调用区间的辅助锚点。"
        )
    observations.extend(_build_xref_observations(direct_xrefs))
    if not observations:
        observations.append("未生成明确结论，请检查符号和 marker 是否因版本变化漂移。")
    return observations


def _build_xref_observations(direct_xrefs: list[dict[str, Any]]) -> list[str]:
    xref_by_label = {item["label"]: item for item in direct_xrefs if item.get("resolved")}
    observations: list[str] = []

    handle_sse_open_xref = xref_by_label.get("handle_sse_open_closure")
    if isinstance(handle_sse_open_xref, dict):
        callers = handle_sse_open_xref.get("callers") or []
        if any(
            "TunnelManager16handle_http_poll" in str(item.get("caller_symbol") or "")
            for item in callers
        ):
            observations.append(
                "direct xref 已确认 TunnelManager::handle_http_poll 会直接调用 "
                "MessageHandler::handle_sse_open；HTTP fallback 的 pending "
                "sse.open 请求会进入这条消息处理链。"
            )

    if _has_tunnel_http_transport_xref(xref_by_label):
        observations.append(
            "direct xref 已确认 HTTP fallback 的 GetPending/response/error/delta/end "
            "回包逻辑停留在 HttpTransport，和 handle_sse_open 之后的上游模型请求"
            "不是同一批 direct caller。"
        )

    default_reqwest_methods = _default_handler_reqwest_methods(xref_by_label)
    if default_reqwest_methods:
        observations.append(
            "direct xref 已确认 DefaultSseProxyHandler 会直接调用 "
            f"reqwest::Client::{'/'.join(sorted(default_reqwest_methods))}；"
            "0x5dbd48 不能再被视为覆盖全部 custom-model 上游请求的唯一入口。"
        )

    net_bridge_send_xref = xref_by_label.get("net_bridge_http_send")
    if (
        isinstance(net_bridge_send_xref, dict)
        and int(net_bridge_send_xref.get("caller_count", 0)) == 0
    ):
        observations.append(
            "direct xref 目前没有发现 NetBridgeHttpClient::send 的直接 caller；"
            "它更像是某条特定 adapter 路径，而不是所有 custom-model "
            "handler 的统一出口。"
        )
    return observations


def _has_tunnel_http_transport_xref(xref_by_label: dict[str, dict[str, Any]]) -> bool:
    for label in (
        "http_transport_queue_message",
        "http_transport_send_response",
        "http_transport_send_system_error",
        "http_transport_send_sse_error",
        "http_transport_send_sse_delta",
        "http_transport_send_sse_end",
    ):
        record = xref_by_label.get(label)
        if not isinstance(record, dict):
            continue
        for caller in record.get("callers") or []:
            caller_symbol = str(caller.get("caller_symbol") or "")
            if (
                "TunnelManager16handle_http_poll" in caller_symbol
                or "TunnelManager14handle_command" in caller_symbol
            ):
                return True
    return False


def _default_handler_reqwest_methods(
    xref_by_label: dict[str, dict[str, Any]],
) -> list[str]:
    methods: list[str] = []
    for label in ("reqwest_client_get", "reqwest_client_post", "reqwest_client_put"):
        record = xref_by_label.get(label)
        if not isinstance(record, dict):
            continue
        if any(
            "DefaultSseProxyHandler" in str(item.get("caller_symbol") or "")
            for item in record.get("callers") or []
        ):
            methods.append(label.removeprefix("reqwest_client_"))
    return methods


def _layout_hypotheses() -> list[dict[str, str]]:
    return [
        {
            "structure": "custom_model_http_request",
            "field": "url",
            "offset": "0x88",
            "source_symbol": "net_bridge_http_send_closure",
            "evidence": "0x5dbd48: ldp x1, x2, [x19, #0x88] 后立即调用 RequestBuilder::new",
        },
        {
            "structure": "custom_model_http_request",
            "field": "method_bytes",
            "offset": "0xa0",
            "source_symbol": "net_bridge_http_send_closure",
            "evidence": "0x5dbcb8: ldp x1, x2, [x19, #0xa0] 后立即调用 http::Method::from_bytes",
        },
        {
            "structure": "request_builder",
            "field": "headers_map",
            "offset": "0x18",
            "source_symbol": "request_builder_header / ensure_bridge_transport",
            "evidence": "header/ensure_bridge_transport 都对 x19 + 0x18 做 HeaderMap 操作",
        },
        {
            "structure": "default_handler_request_args",
            "field": "url",
            "offset": "0x8",
            "source_symbol": "default_handler_handle_sse_closure",
            "evidence": (
                "0x1204b3c: ldp x3, x4, [x28, #0x8] 后在 0x1204b44 "
                "调用 reqwest::Client::request；"
                "reqwest::Client::get/post 包装器会把原始 x2/x3 前移到 x3/x4 再 tailcall request。"
            ),
        },
        {
            "structure": "request_builder",
            "field": "url",
            "offset": "0x80",
            "source_symbol": "reqwest_post_configured_closure",
            "evidence": (
                "0x1352e60: ldp x3, x4, [x25, #0x80] 后在 0x1352e6c "
                "调用 reqwest::Client::request"
            ),
        },
        {
            "structure": "request_builder",
            "field": "body",
            "offset": "0x98",
            "source_symbol": "reqwest_post_configured_closure",
            "evidence": (
                "0x1352e70: ldp x1, x2, [x25, #0x98] 后转成 Vec 再传给 "
                "reqwest::RequestBuilder::body"
            ),
        },
        {
            "structure": "request_builder",
            "field": "method_tag",
            "offset": "0xb0",
            "source_symbol": "reqwest_post_configured_closure",
            "evidence": "0x1352cfc: ldrb w8, [x25, #0xb0] 用于 method 分支选择",
        },
        {
            "structure": "request_builder",
            "field": "method_extension_or_inline_storage",
            "offset": "0xb8",
            "source_symbol": "reqwest_post_configured_closure",
            "evidence": "0x1352d98: ldp x23, x24, [x25, #0xb8] 用于自定义 method 路径",
        },
        {
            "structure": "request_builder",
            "field": "reqwest_client_ptr",
            "offset": "0xc8",
            "source_symbol": "reqwest_post_configured_closure",
            "evidence": "0x1352e5c: ldr x1, [x26]，其中 x26 = x19 + 0xc8",
        },
    ]


def _candidate_patch_sites() -> list[dict[str, str]]:
    return [
        {
            "label": "default_handler_final_request_url_load",
            "symbol": "default_handler_handle_sse_closure",
            "address": "0x1204b3c",
            "kind": "reqwest_request_url_pair_load",
            "why": "DefaultSseProxyHandler 在 reqwest::Client::request 前最后一次装入 URL 对。",
        },
        {
            "label": "default_handler_final_request_call",
            "symbol": "default_handler_handle_sse_closure",
            "address": "0x1204b44",
            "kind": "reqwest_request_call",
            "why": "DefaultSseProxyHandler 直达 reqwest::Client::request 的调用点。",
        },
        {
            "label": "final_reqwest_url_load",
            "symbol": "reqwest_post_configured_closure",
            "address": "0x1352e60",
            "kind": "url_pair_load",
            "why": "调用 reqwest::Client::request 前最后一次从 builder 读取 URL 对。",
        },
        {
            "label": "final_reqwest_request_call",
            "symbol": "reqwest_post_configured_closure",
            "address": "0x1352e6c",
            "kind": "reqwest_request_call",
            "why": "最接近 Windows 端最终 URL 进入 reqwest 的 native 调用点。",
        },
        {
            "label": "http_request_url_to_builder",
            "symbol": "net_bridge_http_send_closure",
            "address": "0x5dbd48",
            "kind": "builder_url_source_load",
            "why": "custom_model HttpRequest 的 URL 在这里被装入 RequestBuilder::new。",
        },
        {
            "label": "http_request_method_to_builder",
            "symbol": "net_bridge_http_send_closure",
            "address": "0x5dbcb8",
            "kind": "builder_method_source_load",
            "why": "custom_model HttpRequest 的 method bytes 在这里进入 http::Method::from_bytes。",
        },
    ]


def _rejected_patch_sites() -> list[dict[str, Any]]:
    return [
        {
            "label": "request_builder_new_to_vec_call",
            "symbol": "request_builder_new",
            "address": "0x13565ec",
            "kind": "shared_constructor_to_vec_call",
            "why_rejected": [
                "该位点位于共享 RequestBuilder::new 内部，不是 custom-model 专用路径。",
                (
                    "它会影响所有进入 RequestBuilder::new 的 URL 拷贝流程，"
                    "而不是只影响 custom-model 请求。"
                ),
                "本地验证里该位点的 patch 已经触发过 AI/服务启动异常，因此只能作为反例保留。",
            ],
            "risk_profile": "high_relative",
        }
    ]


def _site_flow_analysis() -> list[dict[str, Any]]:
    return [
        {
            "label": "http_request_url_to_builder",
            "scope": "custom_model_only",
            "register_flow": {
                "load_instruction": "0x5dbd48: ldp x1, x2, [x19, #0x88]",
                "consumer_setup": [
                    "0x5dbd4c: add x0, sp, #0x230",
                    "0x5dbd50: bl RequestBuilder::new",
                ],
            },
            "structure_binding": {
                "base_register": "x19",
                "field_offset": "0x88",
                "field_name": "custom_model_http_request.url",
            },
            "why_narrow": [
                (
                    "位点位于 ai_agent..net_bridge_http_client::NetBridgeHttpClient "
                    "as custom_model_proxy_client::http_client::HttpClient::send "
                    "的 closure 内。"
                ),
                (
                    "同一 closure 紧邻的 0x5dbcb8 还从 x19 + 0xa0 取 method bytes "
                    "交给 http::Method::from_bytes，说明这里处理的是 "
                    "custom-model HttpRequest 对象。"
                ),
                (
                    "该位点只改 RequestBuilder::new 的 URL 入参，不碰共享 "
                    "RequestBuilder::new 内部实现。"
                ),
            ],
            "expected_patch_effect": (
                "只覆盖 custom-model HttpRequest -> RequestBuilder 的 URL 装载路径。"
            ),
            "risk_profile": "low_relative",
        },
        {
            "label": "default_handler_final_request_url_load",
            "scope": "custom_model_default_handler",
            "register_flow": {
                "load_instruction": "0x1204b3c: ldp x3, x4, [x28, #0x8]",
                "consumer_setup": [
                    "0x1204b34: ldr x1, [x8]",
                    "0x1204b40: bl _OUTLINED_FUNCTION_40351",
                    "0x1204b44: bl reqwest::Client::request",
                ],
            },
            "structure_binding": {
                "base_register": "x28",
                "field_offset": "0x8",
                "field_name": "default_handler_request.url",
            },
            "why_narrow": [
                (
                    "位点位于 DefaultSseProxyHandler 的 handle_sse closure 内，"
                    "属于 custom-model 默认 handler 的真实上游请求路径。"
                ),
                (
                    "reqwest::Client::get/post/put 包装器会把原始 x2/x3 前移到 x3/x4，"
                    "然后 tailcall reqwest::Client::request，说明这里的 x3/x4 就是 URL 对。"
                ),
                (
                    "相比 NetBridgeHttpClient::send，这个点已有 direct xref 证明会被 "
                    "DefaultSseProxyHandler 直接命中。"
                ),
            ],
            "expected_patch_effect": (
                "覆盖 DefaultSseProxyHandler 走 reqwest::Client::request 的 "
                "custom-model URL 装载路径。"
            ),
            "risk_profile": "lowest_relative",
        },
        {
            "label": "final_reqwest_url_load",
            "scope": "generic_reqwest_bridge",
            "register_flow": {
                "load_instruction": "0x1352e60: ldp x3, x4, [x25, #0x80]",
                "consumer_setup": [
                    "0x1352e5c: ldr x1, [x26]",
                    "0x1352e64: add x0, sp, #0x318",
                    "0x1352e68: add x2, sp, #0x178",
                    "0x1352e6c: bl reqwest::Client::request",
                ],
            },
            "structure_binding": {
                "base_register": "x25",
                "field_offset": "0x80",
                "field_name": "request_builder.url",
            },
            "why_narrow": [
                "它确实是最终 URL 进入 reqwest::Client::request 之前的最后一次 builder.url 读取。",
                (
                    "但 enclosing symbol 是 net_bridge::http::client::reqwest::"
                    "BlockingResponseClient::post_configured closure，不是 "
                    "custom-model 专用实现。"
                ),
                "这里更贴近 Windows 端最终 reqwest 边界，但覆盖面比 primary 更宽。",
            ],
            "expected_patch_effect": (
                "覆盖所有走 post_configured 的 RequestBuilder.url -> reqwest 请求路径。"
            ),
            "risk_profile": "medium_relative",
        },
    ]


def _recommended_patch_plan(
    candidate_patch_sites: list[dict[str, str]],
    text_code_caves: list[dict[str, Any]],
) -> dict[str, Any]:
    site_by_label = {item["label"]: item for item in candidate_patch_sites}

    def _attach_cave(site: dict[str, str] | None) -> dict[str, Any] | None:
        if site is None:
            return None
        site_rva = int(site["address"], 16)
        suitable_caves: list[dict[str, Any]] = []
        for cave in text_code_caves:
            usable_length = int(cave.get("usable_length_bytes", 0))
            aligned_file_offset = int(cave.get("aligned_file_offset", "0x0"), 16)
            distance = aligned_file_offset - site_rva
            if usable_length < DEFAULT_MIN_TRAMPOLINE_BYTES:
                continue
            if abs(distance) >= ARM64_BL_RANGE_BYTES:
                continue
            suitable_caves.append(
                {
                    **cave,
                    "branch_distance_bytes": distance,
                }
            )
        suitable_caves.sort(
            key=lambda item: (
                -int(item["usable_length_bytes"]),
                abs(int(item["branch_distance_bytes"])),
            )
        )
        return {
            "site": site,
            "trampoline_cave": suitable_caves[0] if suitable_caves else None,
        }

    primary = _attach_cave(site_by_label.get("default_handler_final_request_url_load"))
    secondary = _attach_cave(site_by_label.get("final_reqwest_url_load"))
    return {
        "strategy": "static_branch_trampoline",
        "primary": primary,
        "secondary": secondary,
        "notes": [
            "第一版更建议从 DefaultSseProxyHandler -> reqwest::Client::request "
            "前的 URL 装载点入手，静态 patch 只需改 x3/x4。",
            "final_reqwest_url_load 仍可作为更通用的次选点，用于对齐更宽的 reqwest bridge。",
            "当前 __TEXT,__text 内存在可达的填充空洞，可直接承载 ARM64 trampoline "
            "和内联 URL 常量。"
            if primary is not None and primary.get("trampoline_cave") is not None
            else "当前报告里还没找到满足长度和分支范围要求的 trampoline 空洞。",
        ],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="生成 macOS Trae native Rust 请求链的离线符号与反汇编报告。"
    )
    parser.add_argument(
        "--trae-path",
        default=DEFAULT_TRAE_PATH,
        help="Trae.app 或其可执行文件路径",
    )
    parser.add_argument("--module-path", help="可选：直接指定 libai_agent.dylib 路径")
    parser.add_argument("--artifact-root", type=Path, default=DEFAULT_ARTIFACT_ROOT)
    parser.add_argument("--max-disasm-lines", type=int, default=DEFAULT_MAX_DISASM_LINES)
    parser.add_argument("--max-marker-hits", type=int, default=DEFAULT_MAX_MARKER_HITS)
    parser.add_argument("--json", action="store_true", help="只输出 JSON summary")
    return parser


def main() -> int:  # noqa: PLR0912, PLR0915
    if sys.platform != "darwin":
        raise SystemExit("该脚本仅支持 macOS")

    args = build_parser().parse_args()
    artifact_root = args.artifact_root.resolve()
    artifact_root.mkdir(parents=True, exist_ok=True)
    paths = _resolve_paths(args.trae_path, args.module_path)
    compatibility = build_compatibility_report(paths["module_path"])
    nm_symbols = _load_nm_symbols(paths["module_path"])

    symbol_reports: list[dict[str, Any]] = []
    for label, symbol_name in SYMBOL_TARGETS:
        symbol_meta = nm_symbols.get(symbol_name)
        record: dict[str, Any] = {
            "label": label,
            "symbol_name": symbol_name,
            "present": symbol_meta is not None,
        }
        if symbol_meta is not None:
            record.update(symbol_meta)
            record["disassembly"] = _disassemble_symbol(
                paths["module_path"],
                symbol_name=symbol_name,
                artifact_root=artifact_root,
                max_lines=args.max_disasm_lines,
            )
        symbol_reports.append(record)

    markers = _marker_hits(
        paths["module_path"],
        markers=MARKER_TARGETS,
        max_hits=args.max_marker_hits,
    )
    direct_xrefs = _direct_call_xrefs(
        paths["module_path"],
        nm_symbols=nm_symbols,
    )
    text_code_caves = _text_code_caves(paths["module_path"])
    candidate_patch_sites = _candidate_patch_sites()
    summary = {
        "ts": _now_stamp(),
        "paths": {
            "app_bundle": str(paths["app_bundle"]),
            "executable": str(paths["executable"]),
            "module_path": str(paths["module_path"]),
        },
        "compatibility_report": compatibility.to_dict(),
        "symbols": symbol_reports,
        "markers": markers,
        "direct_xrefs": direct_xrefs,
        "layout_hypotheses": _layout_hypotheses(),
        "candidate_patch_sites": candidate_patch_sites,
        "rejected_patch_sites": _rejected_patch_sites(),
        "site_flow_analysis": _site_flow_analysis(),
        "text_code_caves": text_code_caves,
        "recommended_patch_plan": _recommended_patch_plan(
            candidate_patch_sites,
            text_code_caves,
        ),
        "observations": _build_observations(
            symbol_reports,
            markers,
            direct_xrefs=direct_xrefs,
        ),
    }

    summary_path = artifact_root / "summary.json"
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0

    print(f"summary: {summary_path}")
    print(f"module_path: {paths['module_path']}")
    print(f"compatibility: {compatibility.status.value} reason={compatibility.reason}")
    print("observations:")
    for item in summary["observations"]:
        print(f"  - {item}")
    print("symbols:")
    for item in symbol_reports:
        status = "present" if item["present"] else "missing"
        address = item.get("address", "<unknown>")
        print(f"  - {item['label']}: {status} {address}")
    print("candidate_patch_sites:")
    for item in summary["candidate_patch_sites"]:
        print(
            "  - "
            f"{item['label']}: {item['symbol']} {item['address']} "
            f"({item['kind']})"
        )
    print("rejected_patch_sites:")
    for item in summary["rejected_patch_sites"]:
        print(
            "  - "
            f"{item['label']}: {item['symbol']} {item['address']} "
            f"({item['kind']})"
        )
    print("site_flow_analysis:")
    for item in summary["site_flow_analysis"]:
        print(
            "  - "
            f"{item['label']}: scope={item['scope']} "
            f"effect={item['expected_patch_effect']}"
        )
    print("direct_xrefs:")
    for item in summary["direct_xrefs"]:
        if not item.get("resolved"):
            print(
                "  - "
                f"{item['label']}: unresolved match_count={item.get('match_count', 0)}"
            )
            continue
        print(
            "  - "
            f"{item['label']}: {item.get('address')} callers={item.get('caller_count', 0)}"
        )
    print("text_code_caves:")
    for item in summary["text_code_caves"]:
        location = item["location"]
        print(
            "  - "
            f"{item['kind']}: len={item['length_bytes']} usable={item['usable_length_bytes']} "
            f"file={location['file_offset']} aligned={item['aligned_file_offset']} "
            f"rva={location['rva']}"
        )
    recommended = summary["recommended_patch_plan"]
    print(f"recommended_patch_strategy: {recommended['strategy']}")
    primary = recommended.get("primary")
    if isinstance(primary, dict) and primary.get("site") is not None:
        site = primary["site"]
        print(f"recommended_primary_site: {site['label']} {site['address']}")
        cave = primary.get("trampoline_cave")
        if isinstance(cave, dict):
            location = cave["location"]
            print(
                "recommended_primary_cave: "
                f"{location['file_offset']} aligned={cave['aligned_file_offset']} "
                f"usable={cave['usable_length_bytes']} "
                f"branch_distance={cave['branch_distance_bytes']}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
