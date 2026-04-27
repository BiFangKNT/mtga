from __future__ import annotations

import hashlib
import json
import shutil
import struct
import subprocess
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any, cast

MACHO_MAGIC_64_LE = 0xFEEDFACF
CPU_TYPE_ARM64 = 0x0100000C
LC_SEGMENT_64 = 0x19
MACHO_HEADER_SIZE = 32
MACHO_LOAD_COMMAND_HEADER_SIZE = 8
DEFAULT_OLD_URL = "https://api.openai.com/v1/chat/completions"
CHAT_COMPLETIONS_MARKER = b"/v1/chat/completions"
CUSTOM_MODEL_MARKER = b"CustomModelProxyManager"
SSE_OPEN_MARKER = b"SseOpenPayload"
NET_BRIDGE_CLIENT_MARKER = b"NetBridgeHttpClient"
LLDB_REWRITER_TARGET = "lldb:custom_model_proxy_client::handle_sse_open"
DEFAULT_MANIFEST_PATH = Path(__file__).with_name("url_patch_manifest.json")
MAX_RECORDED_OFFSETS = 20
DEFAULT_ATTACH_LOG_LOOKBACK = "5m"
MAX_ATTACH_LOG_LINES = 12


class CompatibilityStatus(StrEnum):
    SUPPORTED = "supported"
    COMPATIBLE_UNKNOWN = "compatible_unknown"
    BLOCKED = "blocked"


@dataclass(frozen=True)
class MachOSection:
    segment: str
    section: str
    address: int
    size: int
    offset: int

    def contains_file_offset(self, file_offset: int) -> bool:
        return self.offset <= file_offset < self.offset + self.size

    def file_offset_to_rva(self, file_offset: int) -> int:
        return self.address + (file_offset - self.offset)


@dataclass(frozen=True)
class MachOLayout:
    cpu_type: int
    sections: tuple[MachOSection, ...]

    def locate_file_offset(self, file_offset: int) -> dict[str, str]:
        for section in self.sections:
            if section.contains_file_offset(file_offset):
                rva = section.file_offset_to_rva(file_offset)
                return {
                    "segment": section.segment,
                    "section": section.section,
                    "file_offset": hex(file_offset),
                    "rva": hex(rva),
                }
        return {
            "segment": "<unknown>",
            "section": "<unknown>",
            "file_offset": hex(file_offset),
            "rva": "<unknown>",
        }


@dataclass(frozen=True)
class TraeNativeMacOSCompatibilityReport:
    status: CompatibilityStatus
    reason: str
    dll_path: str
    dll_size: int | None
    dll_mtime_ns: int | None
    dll_sha256: str | None
    pattern: str
    pattern_count: int | None
    pattern_offsets: tuple[str, ...]
    url_copy_call_offset: int
    url_copy_call_file_offset: str | None
    url_copy_call_rva: str | None
    old_url_present: bool | None
    manifest_hit: bool
    manifest_path: str | None
    manifest_error: str | None
    macho_cpu_type: str | None
    lldb_path: str | None
    codesign_runtime: bool | None
    get_task_allow: bool | None

    @property
    def blocked(self) -> bool:
        return self.status == CompatibilityStatus.BLOCKED

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status.value,
            "reason": self.reason,
            "dll_path": self.dll_path,
            "dll_size": self.dll_size,
            "dll_mtime_ns": self.dll_mtime_ns,
            "dll_sha256": self.dll_sha256,
            "pattern": self.pattern,
            "pattern_count": self.pattern_count,
            "pattern_offsets": list(self.pattern_offsets),
            "url_copy_call_offset": self.url_copy_call_offset,
            "url_copy_call_file_offset": self.url_copy_call_file_offset,
            "url_copy_call_rva": self.url_copy_call_rva,
            "old_url_present": self.old_url_present,
            "manifest_hit": self.manifest_hit,
            "manifest_path": self.manifest_path,
            "manifest_error": self.manifest_error,
            "macho_cpu_type": self.macho_cpu_type,
            "lldb_path": self.lldb_path,
            "codesign_runtime": self.codesign_runtime,
            "get_task_allow": self.get_task_allow,
        }


def _hash_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _find_all(data: bytes, needle: bytes) -> list[int]:
    offsets: list[int] = []
    start = 0
    while True:
        offset = data.find(needle, start)
        if offset < 0:
            return offsets
        offsets.append(offset)
        start = offset + 1


def _read_c_string(data: bytes, offset: int, size: int) -> str:
    raw = data[offset : offset + size].split(b"\x00", 1)[0]
    return raw.decode("ascii", errors="replace")


def parse_macho_layout(data: bytes) -> MachOLayout:
    if len(data) < MACHO_HEADER_SIZE:
        raise ValueError("Mach-O 文件过小")
    magic, cpu_type, _cpu_subtype, _file_type, command_count, _command_size, _flags, _reserved = (
        struct.unpack_from("<IIIIIIII", data, 0)
    )
    if magic != MACHO_MAGIC_64_LE:
        raise ValueError(f"不支持的 Mach-O magic: {hex(magic)}")

    sections: list[MachOSection] = []
    offset = MACHO_HEADER_SIZE
    for _index in range(command_count):
        if offset + MACHO_LOAD_COMMAND_HEADER_SIZE > len(data):
            raise ValueError("Mach-O load command 越界")
        command, command_size = struct.unpack_from("<II", data, offset)
        if command_size < MACHO_LOAD_COMMAND_HEADER_SIZE or offset + command_size > len(data):
            raise ValueError("Mach-O load command size 异常")
        if command == LC_SEGMENT_64:
            segment = _read_c_string(data, offset + 8, 16)
            section_count = struct.unpack_from("<I", data, offset + 64)[0]
            section_offset = offset + 72
            for section_index in range(section_count):
                item_offset = section_offset + section_index * 80
                if item_offset + 80 > offset + command_size:
                    raise ValueError("Mach-O section 越界")
                section = _read_c_string(data, item_offset, 16)
                section_segment = _read_c_string(data, item_offset + 16, 16) or segment
                address, size = struct.unpack_from("<QQ", data, item_offset + 32)
                file_offset = struct.unpack_from("<I", data, item_offset + 48)[0]
                sections.append(
                    MachOSection(
                        segment=section_segment,
                        section=section,
                        address=address,
                        size=size,
                        offset=file_offset,
                    )
                )
        offset += command_size
    return MachOLayout(cpu_type=cpu_type, sections=tuple(sections))


def _resolve_lldb_path() -> str | None:
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
    return shutil.which("lldb")


def _read_codesign_flags(module_path: Path) -> tuple[bool | None, bool | None]:
    codesign_path = shutil.which("codesign")
    if not codesign_path:
        return None, None
    try:
        details = subprocess.run(
            [codesign_path, "-dv", "--verbose=4", str(module_path)],
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
        entitlements = subprocess.run(
            [codesign_path, "-d", "--entitlements", ":-", str(module_path)],
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except Exception:
        return None, None

    combined_details = f"{details.stdout}\n{details.stderr}"
    combined_entitlements = f"{entitlements.stdout}\n{entitlements.stderr}"
    runtime = "flags=0x10000(runtime)" in combined_details
    get_task_allow = "com.apple.security.get-task-allow" in combined_entitlements
    return runtime, get_task_allow


def _run_text_command(
    command: list[str],
    *,
    timeout: int = 5,
) -> subprocess.CompletedProcess[str] | None:
    try:
        return subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
    except Exception:
        return None


def _read_developer_mode_status() -> tuple[bool | None, str | None]:
    tool_path = shutil.which("DevToolsSecurity")
    if not tool_path:
        return None, None
    completed = _run_text_command([tool_path, "-status"])
    if completed is None:
        return None, None
    combined = f"{completed.stdout}\n{completed.stderr}".strip()
    lowered = combined.lower()
    if "disabled" in lowered:
        return False, combined or None
    if "enabled" in lowered:
        return True, combined or None
    return None, combined or None


def _manifest_has_sha256(
    manifest_path: Path | None,
    dylib_sha256: str,
) -> tuple[bool, str | None]:
    if manifest_path is None or not manifest_path.exists():
        return False, None
    try:
        raw_manifest = cast(
            object,
            json.loads(manifest_path.read_text(encoding="utf-8")),
        )
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"
    if not isinstance(raw_manifest, dict):
        return False, "manifest root is not an object"
    manifest = cast(dict[str, Any], raw_manifest)
    raw_entries = manifest.get("entries")
    if not isinstance(raw_entries, list):
        return False, "manifest entries is not a list"
    entries = cast(list[object], raw_entries)
    for raw_entry in entries:
        if not isinstance(raw_entry, dict):
            continue
        entry = cast(dict[str, Any], raw_entry)
        entry_sha256 = entry.get("module_sha256")
        if isinstance(entry_sha256, str) and entry_sha256 == dylib_sha256:
            return True, None
    return False, None


def _resolve_pid_executable(pid: int) -> Path | None:
    completed = _run_text_command(["ps", "-p", str(pid), "-o", "comm="])
    if completed is None or completed.returncode != 0:
        return None
    executable = completed.stdout.strip()
    if not executable:
        return None
    path = Path(executable)
    return path if path.is_file() else None


def _read_attach_log_excerpt(
    pid: int,
    *,
    lookback: str = DEFAULT_ATTACH_LOG_LOOKBACK,
    limit: int = MAX_ATTACH_LOG_LINES,
) -> list[str]:
    log_path = shutil.which("log")
    if not log_path:
        return []
    completed = _run_text_command(
        [
            log_path,
            "show",
            "--style",
            "compact",
            "--last",
            lookback,
            "--predicate",
            '(process == "taskgated" || process == "taskgated-helper" || '
            'process == "debugserver" || process == "lldb")',
        ],
        timeout=10,
    )
    if completed is None or completed.returncode != 0:
        return []
    pid_markers = (
        f"task_for_pid({pid})",
        f"process {pid}",
        f"pid {pid}",
        f"({pid})",
        str(pid),
    )
    lines: list[str] = []
    for raw_line in completed.stdout.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if any(marker in line for marker in pid_markers) or any(
            token in line
            for token in (
                "Not allowed to attach to process",
                "Attach failed",
                "task_for_pid",
            )
        ):
            lines.append(line)
    return lines[-limit:]


def diagnose_lldb_attach_failure(
    pid: int,
    *,
    module_path: Path | None = None,
) -> dict[str, Any]:
    developer_mode_enabled, developer_mode_status = _read_developer_mode_status()
    target_executable = _resolve_pid_executable(pid)
    target_codesign_runtime, target_get_task_allow = (
        _read_codesign_flags(target_executable)
        if target_executable is not None
        else (None, None)
    )
    module_codesign_runtime, module_get_task_allow = (
        _read_codesign_flags(module_path)
        if module_path is not None and module_path.is_file()
        else (None, None)
    )
    attach_log_excerpt = _read_attach_log_excerpt(pid)

    signals: list[str] = []
    if developer_mode_enabled is False:
        signals.append("developer_mode_disabled")
    if target_codesign_runtime and target_get_task_allow is False:
        signals.append("target_hardened_runtime_without_get_task_allow")
    if any("task_for_pid" in line and "err = 0x00000005" in line for line in attach_log_excerpt):
        signals.append("task_for_pid_denied")
    if any("Not allowed to attach to process" in line for line in attach_log_excerpt):
        signals.append("debugserver_attach_denied")

    reason = "attach_diagnostics_collected"
    hint = "已采集 LLDB attach 失败诊断。"
    if (
        "task_for_pid_denied" in signals
        and "target_hardened_runtime_without_get_task_allow" in signals
    ):
        reason = "likely_hardened_runtime_attach_denied"
        hint = (
            "目标进程启用了 hardened runtime 且未授予 get-task-allow，"
            "debugserver/task_for_pid 很可能被 macOS 直接拒绝。"
        )
    elif "task_for_pid_denied" in signals and "developer_mode_disabled" in signals:
        reason = "likely_developer_mode_disabled"
        hint = "本机 Developer Mode 处于 disabled，先启用后再重试 LLDB attach。"
    elif "task_for_pid_denied" in signals or "debugserver_attach_denied" in signals:
        reason = "attach_denied_by_macos"
        hint = "macOS 已拒绝本次 debugserver/task_for_pid attach 请求。"

    return {
        "reason": reason,
        "hint": hint,
        "signals": signals,
        "developer_mode_enabled": developer_mode_enabled,
        "developer_mode_status": developer_mode_status,
        "target_executable": str(target_executable) if target_executable is not None else None,
        "target_codesign_runtime": target_codesign_runtime,
        "target_get_task_allow": target_get_task_allow,
        "module_path": str(module_path) if module_path is not None else None,
        "module_codesign_runtime": module_codesign_runtime,
        "module_get_task_allow": module_get_task_allow,
        "taskgated_excerpt": attach_log_excerpt,
    }


def _blocked_report(  # noqa: PLR0913
    *,
    dylib_path: Path,
    reason: str,
    dylib_size: int | None = None,
    dylib_mtime_ns: int | None = None,
    dylib_sha256: str | None = None,
    marker_count: int | None = None,
    marker_offsets: tuple[str, ...] = (),
    old_url_present: bool | None = None,
    manifest_path: Path | None = DEFAULT_MANIFEST_PATH,
    manifest_error: str | None = None,
    macho_cpu_type: str | None = None,
    lldb_path: str | None = None,
    codesign_runtime: bool | None = None,
    get_task_allow: bool | None = None,
) -> TraeNativeMacOSCompatibilityReport:
    return TraeNativeMacOSCompatibilityReport(
        status=CompatibilityStatus.BLOCKED,
        reason=reason,
        dll_path=str(dylib_path),
        dll_size=dylib_size,
        dll_mtime_ns=dylib_mtime_ns,
        dll_sha256=dylib_sha256,
        pattern=CHAT_COMPLETIONS_MARKER.decode("ascii"),
        pattern_count=marker_count,
        pattern_offsets=marker_offsets,
        url_copy_call_offset=0,
        url_copy_call_file_offset=None,
        url_copy_call_rva=None,
        old_url_present=old_url_present,
        manifest_hit=False,
        manifest_path=str(manifest_path) if manifest_path is not None else None,
        manifest_error=manifest_error,
        macho_cpu_type=macho_cpu_type,
        lldb_path=lldb_path,
        codesign_runtime=codesign_runtime,
        get_task_allow=get_task_allow,
    )


def build_compatibility_report(  # noqa: PLR0911
    dylib_path: Path,
    *,
    old_url: str = DEFAULT_OLD_URL,
    manifest_path: Path | None = DEFAULT_MANIFEST_PATH,
) -> TraeNativeMacOSCompatibilityReport:
    lldb_path = _resolve_lldb_path()
    if not dylib_path.is_file():
        return _blocked_report(
            dylib_path=dylib_path,
            reason="dylib_not_found",
            manifest_path=manifest_path,
            lldb_path=lldb_path,
        )

    try:
        stat = dylib_path.stat()
        data = dylib_path.read_bytes()
    except Exception as exc:  # noqa: BLE001
        return _blocked_report(
            dylib_path=dylib_path,
            reason=f"dylib_read_failed:{type(exc).__name__}: {exc}",
            manifest_path=manifest_path,
            lldb_path=lldb_path,
        )

    dylib_sha256 = _hash_sha256(data)
    dylib_size = stat.st_size
    dylib_mtime_ns = stat.st_mtime_ns
    old_url_present = old_url.encode("utf-8") in data
    marker_offsets_raw = _find_all(data, CHAT_COMPLETIONS_MARKER)
    marker_offsets = tuple(hex(offset) for offset in marker_offsets_raw[:MAX_RECORDED_OFFSETS])

    try:
        layout = parse_macho_layout(data)
    except Exception as exc:  # noqa: BLE001
        return _blocked_report(
            dylib_path=dylib_path,
            reason=f"macho_parse_failed:{type(exc).__name__}: {exc}",
            dylib_size=dylib_size,
            dylib_mtime_ns=dylib_mtime_ns,
            dylib_sha256=dylib_sha256,
            marker_count=len(marker_offsets_raw),
            marker_offsets=marker_offsets,
            old_url_present=old_url_present,
            manifest_path=manifest_path,
            lldb_path=lldb_path,
        )

    macho_cpu_type = hex(layout.cpu_type)
    codesign_runtime, get_task_allow = _read_codesign_flags(dylib_path)
    if layout.cpu_type != CPU_TYPE_ARM64:
        return _blocked_report(
            dylib_path=dylib_path,
            reason=f"unsupported_macho_cpu:{macho_cpu_type}",
            dylib_size=dylib_size,
            dylib_mtime_ns=dylib_mtime_ns,
            dylib_sha256=dylib_sha256,
            marker_count=len(marker_offsets_raw),
            marker_offsets=marker_offsets,
            old_url_present=old_url_present,
            manifest_path=manifest_path,
            macho_cpu_type=macho_cpu_type,
            lldb_path=lldb_path,
            codesign_runtime=codesign_runtime,
            get_task_allow=get_task_allow,
        )
    if lldb_path is None:
        return _blocked_report(
            dylib_path=dylib_path,
            reason="lldb_not_found",
            dylib_size=dylib_size,
            dylib_mtime_ns=dylib_mtime_ns,
            dylib_sha256=dylib_sha256,
            marker_count=len(marker_offsets_raw),
            marker_offsets=marker_offsets,
            old_url_present=old_url_present,
            manifest_path=manifest_path,
            macho_cpu_type=macho_cpu_type,
            lldb_path=lldb_path,
            codesign_runtime=codesign_runtime,
            get_task_allow=get_task_allow,
        )
    if not marker_offsets_raw:
        return _blocked_report(
            dylib_path=dylib_path,
            reason="chat_completions_marker_missing",
            dylib_size=dylib_size,
            dylib_mtime_ns=dylib_mtime_ns,
            dylib_sha256=dylib_sha256,
            marker_count=0,
            marker_offsets=(),
            old_url_present=old_url_present,
            manifest_path=manifest_path,
            macho_cpu_type=macho_cpu_type,
            lldb_path=lldb_path,
            codesign_runtime=codesign_runtime,
            get_task_allow=get_task_allow,
        )
    if CUSTOM_MODEL_MARKER not in data or SSE_OPEN_MARKER not in data:
        return _blocked_report(
            dylib_path=dylib_path,
            reason="custom_model_sse_markers_missing",
            dylib_size=dylib_size,
            dylib_mtime_ns=dylib_mtime_ns,
            dylib_sha256=dylib_sha256,
            marker_count=len(marker_offsets_raw),
            marker_offsets=marker_offsets,
            old_url_present=old_url_present,
            manifest_path=manifest_path,
            macho_cpu_type=macho_cpu_type,
            lldb_path=lldb_path,
            codesign_runtime=codesign_runtime,
            get_task_allow=get_task_allow,
        )
    if NET_BRIDGE_CLIENT_MARKER not in data:
        return _blocked_report(
            dylib_path=dylib_path,
            reason="net_bridge_http_client_marker_missing",
            dylib_size=dylib_size,
            dylib_mtime_ns=dylib_mtime_ns,
            dylib_sha256=dylib_sha256,
            marker_count=len(marker_offsets_raw),
            marker_offsets=marker_offsets,
            old_url_present=old_url_present,
            manifest_path=manifest_path,
            macho_cpu_type=macho_cpu_type,
            lldb_path=lldb_path,
            codesign_runtime=codesign_runtime,
            get_task_allow=get_task_allow,
        )

    marker_location = layout.locate_file_offset(marker_offsets_raw[0])
    marker_rva = marker_location.get("rva")
    manifest_hit, manifest_error = _manifest_has_sha256(manifest_path, dylib_sha256)
    if manifest_hit:
        status = CompatibilityStatus.SUPPORTED
        reason = "manifest_sha256_hit"
    else:
        status = CompatibilityStatus.COMPATIBLE_UNKNOWN
        reason = "structure_compatible_lldb_required"
        if codesign_runtime and not get_task_allow:
            reason = "structure_compatible_hardened_runtime_lldb_may_fail"
    return TraeNativeMacOSCompatibilityReport(
        status=status,
        reason=reason,
        dll_path=str(dylib_path),
        dll_size=dylib_size,
        dll_mtime_ns=dylib_mtime_ns,
        dll_sha256=dylib_sha256,
        pattern=CHAT_COMPLETIONS_MARKER.decode("ascii"),
        pattern_count=len(marker_offsets_raw),
        pattern_offsets=marker_offsets,
        url_copy_call_offset=0,
        url_copy_call_file_offset=marker_location.get("file_offset"),
        url_copy_call_rva=marker_rva if marker_rva != "<unknown>" else LLDB_REWRITER_TARGET,
        old_url_present=old_url_present,
        manifest_hit=manifest_hit,
        manifest_path=str(manifest_path) if manifest_path is not None else None,
        manifest_error=manifest_error,
        macho_cpu_type=macho_cpu_type,
        lldb_path=lldb_path,
        codesign_runtime=codesign_runtime,
        get_task_allow=get_task_allow,
    )


__all__ = [
    "CompatibilityStatus",
    "TraeNativeMacOSCompatibilityReport",
    "build_compatibility_report",
    "diagnose_lldb_attach_failure",
    "parse_macho_layout",
]
