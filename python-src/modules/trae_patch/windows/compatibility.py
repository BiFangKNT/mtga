from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any, cast

from .string_offsets import find_all, parse_pe_layout

URL_COPY_PATTERN_HEX = "48 8b 52 08 4d 8b 46 10 48 8d 8d 20 01 00 00"
URL_COPY_PATTERN = bytes.fromhex(URL_COPY_PATTERN_HEX)
URL_COPY_CALL_OFFSET = 0x0F
DEFAULT_OLD_URL = "https://api.openai.com/v1/chat/completions"
DEFAULT_MANIFEST_PATH = Path(__file__).with_name("trae_native_compatibility_manifest.json")
MAX_RECORDED_OFFSETS = 20


class CompatibilityStatus(StrEnum):
    SUPPORTED = "supported"
    COMPATIBLE_UNKNOWN = "compatible_unknown"
    BLOCKED = "blocked"


@dataclass(frozen=True)
class TraeNativeCompatibilityReport:
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
        }


def _blocked_report(  # noqa: PLR0913
    *,
    dll_path: Path,
    reason: str,
    dll_size: int | None = None,
    dll_mtime_ns: int | None = None,
    dll_sha256: str | None = None,
    pattern_count: int | None = None,
    pattern_offsets: tuple[str, ...] = (),
    url_copy_call_file_offset: str | None = None,
    url_copy_call_rva: str | None = None,
    old_url_present: bool | None = None,
    manifest_path: Path | None = None,
    manifest_error: str | None = None,
) -> TraeNativeCompatibilityReport:
    return TraeNativeCompatibilityReport(
        status=CompatibilityStatus.BLOCKED,
        reason=reason,
        dll_path=str(dll_path),
        dll_size=dll_size,
        dll_mtime_ns=dll_mtime_ns,
        dll_sha256=dll_sha256,
        pattern=URL_COPY_PATTERN_HEX,
        pattern_count=pattern_count,
        pattern_offsets=pattern_offsets,
        url_copy_call_offset=URL_COPY_CALL_OFFSET,
        url_copy_call_file_offset=url_copy_call_file_offset,
        url_copy_call_rva=url_copy_call_rva,
        old_url_present=old_url_present,
        manifest_hit=False,
        manifest_path=str(manifest_path) if manifest_path is not None else None,
        manifest_error=manifest_error,
    )


def _hash_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _manifest_has_sha256(manifest_path: Path | None, dll_sha256: str) -> tuple[bool, str | None]:
    if manifest_path is None or not manifest_path.exists():
        return False, None
    try:
        raw_manifest = cast(object, json.loads(manifest_path.read_text(encoding="utf-8")))
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"

    if not isinstance(raw_manifest, dict):
        return False, "manifest root is not an object"
    manifest = cast(dict[str, object], raw_manifest)
    raw_entries = manifest.get("entries")
    if not isinstance(raw_entries, list):
        return False, "manifest entries is not a list"

    entries = cast(list[object], raw_entries)
    for raw_entry in entries:
        if not isinstance(raw_entry, dict):
            continue
        entry = cast(dict[str, object], raw_entry)
        if entry.get("ai_agent_sha256") == dll_sha256:
            return True, None
    return False, None


def build_compatibility_report(
    dll_path: Path,
    *,
    old_url: str = DEFAULT_OLD_URL,
    manifest_path: Path | None = DEFAULT_MANIFEST_PATH,
) -> TraeNativeCompatibilityReport:
    if not dll_path.is_file():
        return _blocked_report(
            dll_path=dll_path,
            reason="dll_not_found",
            manifest_path=manifest_path,
        )

    try:
        stat = dll_path.stat()
        data = dll_path.read_bytes()
    except Exception as exc:  # noqa: BLE001
        return _blocked_report(
            dll_path=dll_path,
            reason=f"dll_read_failed:{type(exc).__name__}: {exc}",
            manifest_path=manifest_path,
        )

    dll_sha256 = _hash_sha256(data)
    dll_size = stat.st_size
    dll_mtime_ns = stat.st_mtime_ns
    old_url_present = old_url.encode("utf-8") in data

    try:
        layout = parse_pe_layout(data)
    except Exception as exc:  # noqa: BLE001
        return _blocked_report(
            dll_path=dll_path,
            reason=f"pe_parse_failed:{type(exc).__name__}: {exc}",
            dll_size=dll_size,
            dll_mtime_ns=dll_mtime_ns,
            dll_sha256=dll_sha256,
            old_url_present=old_url_present,
            manifest_path=manifest_path,
        )

    offsets = find_all(data, URL_COPY_PATTERN)
    pattern_offsets = tuple(hex(offset) for offset in offsets[:MAX_RECORDED_OFFSETS])
    if len(offsets) != 1:
        return _blocked_report(
            dll_path=dll_path,
            reason=f"pattern_count_not_unique:{len(offsets)}",
            dll_size=dll_size,
            dll_mtime_ns=dll_mtime_ns,
            dll_sha256=dll_sha256,
            pattern_count=len(offsets),
            pattern_offsets=pattern_offsets,
            old_url_present=old_url_present,
            manifest_path=manifest_path,
        )

    call_file_offset = offsets[0] + URL_COPY_CALL_OFFSET
    location = layout.locate_file_offset(call_file_offset)
    raw_rva = location.get("rva")
    call_rva = raw_rva if isinstance(raw_rva, str) else None
    if call_rva in {None, "<unknown>"}:
        return _blocked_report(
            dll_path=dll_path,
            reason="call_rva_unknown",
            dll_size=dll_size,
            dll_mtime_ns=dll_mtime_ns,
            dll_sha256=dll_sha256,
            pattern_count=len(offsets),
            pattern_offsets=pattern_offsets,
            url_copy_call_file_offset=hex(call_file_offset),
            url_copy_call_rva=call_rva,
            old_url_present=old_url_present,
            manifest_path=manifest_path,
        )

    manifest_hit, manifest_error = _manifest_has_sha256(manifest_path, dll_sha256)
    status = (
        CompatibilityStatus.SUPPORTED
        if manifest_hit
        else CompatibilityStatus.COMPATIBLE_UNKNOWN
    )
    reason = "manifest_sha256_hit" if manifest_hit else "structure_compatible_unknown_version"
    return TraeNativeCompatibilityReport(
        status=status,
        reason=reason,
        dll_path=str(dll_path),
        dll_size=dll_size,
        dll_mtime_ns=dll_mtime_ns,
        dll_sha256=dll_sha256,
        pattern=URL_COPY_PATTERN_HEX,
        pattern_count=len(offsets),
        pattern_offsets=pattern_offsets,
        url_copy_call_offset=URL_COPY_CALL_OFFSET,
        url_copy_call_file_offset=hex(call_file_offset),
        url_copy_call_rva=call_rva,
        old_url_present=old_url_present,
        manifest_hit=manifest_hit,
        manifest_path=str(manifest_path) if manifest_path is not None else None,
        manifest_error=manifest_error,
    )


__all__ = [
    "CompatibilityStatus",
    "TraeNativeCompatibilityReport",
    "build_compatibility_report",
]
