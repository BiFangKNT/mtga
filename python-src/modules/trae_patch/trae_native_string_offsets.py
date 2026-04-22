from __future__ import annotations

import argparse
import json
import struct
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .trae_native_hook_candidates import AI_AGENT_DLL

DEFAULT_KEYWORDS = (
    "[AhaIPCSource] start_boot_config_stream",
    "[AhaIPCSource] onDidBootConfigChanged",
    "[AhaIPCSource] update_boot_config",
    "BootService.getBootConfig",
    "BootService.onDidBootConfigChanged",
    "TRAE_CONFIG_CHANNEL",
    "trae-config-channel",
    "CustomModelProxyManager] EnsureInitialized start",
    "CustomModelProxyManager] building new client",
    "ws_connect_stream: connecting id=",
    "/custom_model/tunnel/",
    "?http_fallback=true",
    "Tunnel ID is required to build the WebSocket URL",
    "custom_model_proxy_client::connection",
    "custom_model_proxy_client::ws_transport",
    "custom_model_proxy_client::tunnel",
    "custom_model_proxy_client::http_transport",
)
PE32_MAGIC = 0x10B
PE32_PLUS_MAGIC = 0x20B


@dataclass(frozen=True)
class Section:
    name: str
    virtual_address: int
    virtual_size: int
    raw_pointer: int
    raw_size: int

    def contains_file_offset(self, offset: int) -> bool:
        return self.raw_pointer <= offset < self.raw_pointer + self.raw_size

    def file_offset_to_rva(self, offset: int) -> int:
        return self.virtual_address + (offset - self.raw_pointer)


@dataclass(frozen=True)
class PeLayout:
    image_base: int
    sections: tuple[Section, ...]

    def locate_file_offset(self, offset: int) -> dict[str, Any]:
        for section in self.sections:
            if section.contains_file_offset(offset):
                rva = section.file_offset_to_rva(offset)
                return {
                    "section": section.name,
                    "file_offset": hex(offset),
                    "rva": hex(rva),
                    "va": hex(self.image_base + rva),
                }
        return {
            "section": "<unknown>",
            "file_offset": hex(offset),
            "rva": "<unknown>",
            "va": "<unknown>",
        }


def parse_pe_layout(data: bytes) -> PeLayout:
    if data[:2] != b"MZ":
        raise ValueError("不是有效 PE 文件：缺少 MZ 头")

    pe_offset = struct.unpack_from("<I", data, 0x3C)[0]
    if data[pe_offset : pe_offset + 4] != b"PE\x00\x00":
        raise ValueError("不是有效 PE 文件：缺少 PE 签名")

    coff_offset = pe_offset + 4
    section_count = struct.unpack_from("<H", data, coff_offset + 2)[0]
    optional_header_size = struct.unpack_from("<H", data, coff_offset + 16)[0]
    optional_offset = coff_offset + 20
    magic = struct.unpack_from("<H", data, optional_offset)[0]
    if magic == PE32_PLUS_MAGIC:
        image_base = struct.unpack_from("<Q", data, optional_offset + 24)[0]
    elif magic == PE32_MAGIC:
        image_base = struct.unpack_from("<I", data, optional_offset + 28)[0]
    else:
        raise ValueError(f"不支持的 PE optional header magic: {hex(magic)}")

    section_offset = optional_offset + optional_header_size
    sections: list[Section] = []
    for index in range(section_count):
        item_offset = section_offset + index * 40
        raw_name = data[item_offset : item_offset + 8]
        name = raw_name.split(b"\x00", 1)[0].decode("ascii", errors="replace")
        virtual_size, virtual_address, raw_size, raw_pointer = struct.unpack_from(
            "<IIII",
            data,
            item_offset + 8,
        )
        sections.append(
            Section(
                name=name,
                virtual_address=virtual_address,
                virtual_size=virtual_size,
                raw_pointer=raw_pointer,
                raw_size=raw_size,
            )
        )
    return PeLayout(image_base=image_base, sections=tuple(sections))


def find_all(data: bytes, needle: bytes) -> list[int]:
    offsets: list[int] = []
    start = 0
    while True:
        offset = data.find(needle, start)
        if offset < 0:
            return offsets
        offsets.append(offset)
        start = offset + 1


def build_report(dll_path: Path, keywords: tuple[str, ...]) -> dict[str, Any]:
    data = dll_path.read_bytes()
    layout = parse_pe_layout(data)

    matches: list[dict[str, Any]] = []
    for keyword in keywords:
        keyword_bytes = keyword.encode("utf-8")
        offsets = find_all(data, keyword_bytes)
        matches.append(
            {
                "keyword": keyword,
                "count": len(offsets),
                "locations": [
                    layout.locate_file_offset(offset)
                    for offset in offsets[:20]
                ],
            }
        )

    return {
        "dll_path": str(dll_path),
        "image_base": hex(layout.image_base),
        "matches": matches,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="定位 ai_agent.dll 关键字符串的 offset/RVA/section"
    )
    parser.add_argument("--dll-path", type=Path, default=AI_AGENT_DLL, help="目标 DLL")
    parser.add_argument(
        "--keyword",
        action="append",
        dest="keywords",
        help="追加自定义关键字；不传则使用默认 native 切点关键字",
    )
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    keywords = tuple(args.keywords) if args.keywords else DEFAULT_KEYWORDS
    report = build_report(args.dll_path, keywords)

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    print(f"dll_path: {report['dll_path']}")
    print(f"image_base: {report['image_base']}")
    print("matches:")
    for item in report["matches"]:
        print(f"  - {item['keyword']}: count={item['count']}")
        for location in item["locations"]:
            print(
                "      "
                f"section={location['section']} "
                f"file_offset={location['file_offset']} "
                f"rva={location['rva']} "
                f"va={location['va']}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

