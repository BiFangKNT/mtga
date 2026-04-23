from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import cast

AI_AGENT_DLL = Path(
    r"C:\Users\Administrator\AppData\Local\Programs\Trae\resources\app\modules\ai-agent\ai_agent.dll"
)
STRINGS_EXE = "strings.exe"


@dataclass
class CandidateGroup:
    name: str
    keywords: tuple[str, ...]
    matched_lines: list[str] = field(default_factory=lambda: cast(list[str], []))
    source_refs: list[str] = field(default_factory=lambda: cast(list[str], []))

    def add_line(self, line: str) -> None:
        if line not in self.matched_lines:
            self.matched_lines.append(line)

    def add_source_ref(self, source_ref: str) -> None:
        if source_ref not in self.source_refs:
            self.source_refs.append(source_ref)


GROUPS: tuple[CandidateGroup, ...] = (
    CandidateGroup(
        name="boot_config_ingress",
        keywords=(
            "AhaIPCSource",
            "BootService.getBootConfig",
            "start_boot_config_stream",
            "onDidBootConfigChanged",
            "update_boot_config",
            "ai_config::source::aha_ipc_source",
            "ai_config::source::async_builder",
            r"apps\icube_server_rs\crates\ai-config\src\source\aha_ipc_source.rs",
            r"apps\icube_server_rs\crates\ai-config\src\source\async_builder.rs",
        ),
    ),
    CandidateGroup(
        name="custom_model_manager",
        keywords=(
            "CustomModelProxyManager",
            "EnsureInitialized",
            "GetClient",
            "building new client",
            "build result",
        ),
    ),
    CandidateGroup(
        name="custom_model_transport",
        keywords=(
            "custom_model_proxy_client::connection",
            "custom_model_proxy_client::ws_transport",
            "custom_model_proxy_client::http_transport",
            "custom_model_proxy_client::stream_manager",
            "custom_model_proxy_client::message_handler",
            "custom_model_proxy_client::tunnel",
            "ws_connect_stream",
            "http_fallback",
            "Tunnel ID is required to build the WebSocket URL",
            "GetPending",
            "/custom_model/tunnel/",
        ),
    ),
)


def run_strings(dll_path: Path) -> list[str]:
    strings_path = shutil.which(STRINGS_EXE)
    if not strings_path:
        raise FileNotFoundError(f"未找到 {STRINGS_EXE}")

    result = subprocess.run(
        [strings_path, "-n", "8", str(dll_path)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=True,
    )
    return result.stdout.splitlines()


def extract_source_refs(line: str) -> list[str]:
    refs: list[str] = []
    marker = r"apps\icube_server_rs"
    if marker in line:
        start = line.index(marker)
        refs.append(line[start:].strip())
    return refs


def analyze_strings(lines: list[str]) -> list[CandidateGroup]:
    groups = tuple(
        CandidateGroup(name=group.name, keywords=group.keywords)
        for group in GROUPS
    )

    for line in lines:
        for group in groups:
            if any(keyword in line for keyword in group.keywords):
                group.add_line(line)
                for source_ref in extract_source_refs(line):
                    group.add_source_ref(source_ref)

    return list(groups)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="提取 Trae ai-agent native hook 候选点")
    parser.add_argument(
        "--dll-path",
        type=Path,
        default=AI_AGENT_DLL,
        help="ai_agent.dll 路径",
    )
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    groups = analyze_strings(run_strings(args.dll_path))
    payload = [
        {
            "name": group.name,
            "keywords": list(group.keywords),
            "source_refs": group.source_refs,
            "matched_lines": group.matched_lines,
        }
        for group in groups
    ]

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    print(f"dll_path: {args.dll_path}")
    for group in groups:
        print(f"[{group.name}]")
        print(f"keywords: {', '.join(group.keywords)}")
        print(f"source_refs: {group.source_refs or ['<empty>']}")
        if group.matched_lines:
            print("matched_lines:")
            for line in group.matched_lines:
                print(f"  {line}")
        else:
            print("matched_lines: ['<empty>']")
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
