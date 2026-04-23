from __future__ import annotations

import argparse
import json
from pathlib import Path

from modules.trae_patch.windows.hook_candidates import AI_AGENT_DLL
from modules.trae_patch.windows.string_offsets import find_all, parse_pe_layout


def _normalize_hex(value: str) -> bytes:
    normalized = "".join(value.split()).replace("0x", "")
    if len(normalized) % 2 != 0:
        raise ValueError("hex pattern 长度必须是偶数")
    return bytes.fromhex(normalized)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="在 ai_agent.dll 中搜索十六进制字节模式")
    parser.add_argument("--dll-path", type=Path, default=AI_AGENT_DLL)
    parser.add_argument(
        "--pattern",
        action="append",
        required=True,
        help="hex bytes；可重复。格式示例: '48 8b 52 08'",
    )
    parser.add_argument("--json", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    data = args.dll_path.read_bytes()
    layout = parse_pe_layout(data)
    results = []
    for raw_pattern in args.pattern:
        pattern = _normalize_hex(raw_pattern)
        offsets = find_all(data, pattern)
        results.append(
            {
                "pattern": raw_pattern,
                "count": len(offsets),
                "locations": [
                    layout.locate_file_offset(offset)
                    for offset in offsets[:50]
                ],
            }
        )

    if args.json:
        print(json.dumps({"dll_path": str(args.dll_path), "results": results}, indent=2))
    else:
        for item in results:
            print(f"pattern={item['pattern']} count={item['count']}")
            for location in item["locations"]:
                print(
                    "  "
                    f"section={location['section']} "
                    f"file_offset={location['file_offset']} "
                    f"rva={location['rva']}"
                )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
