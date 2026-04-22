from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass

import httpx

DEFAULT_REMOTE_DEBUGGING_HOST = "127.0.0.1"
DEFAULT_REMOTE_DEBUGGING_PORT = 9330


@dataclass(slots=True)
class CdpTarget:
    id: str
    type: str
    title: str
    url: str
    web_socket_debugger_url: str | None


def target_to_dict(target: CdpTarget) -> dict[str, str | None]:
    return {
        "id": target.id,
        "type": target.type,
        "title": target.title,
        "url": target.url,
        "web_socket_debugger_url": target.web_socket_debugger_url,
    }


def fetch_targets(host: str, port: int) -> list[CdpTarget]:
    url = f"http://{host}:{port}/json/list"
    with httpx.Client(timeout=5.0) as client:
        response = client.get(url)
        response.raise_for_status()
        payload = response.json()

    if not isinstance(payload, list):
        raise RuntimeError("CDP /json/list 返回格式无效")

    targets: list[CdpTarget] = []
    for item in payload:
        if not isinstance(item, dict):
            continue
        target_id = item.get("id")
        target_type = item.get("type")
        title = item.get("title", "")
        target_url = item.get("url", "")
        websocket_url = item.get("webSocketDebuggerUrl")
        if not isinstance(target_id, str) or not isinstance(target_type, str):
            continue
        targets.append(
            CdpTarget(
                id=target_id,
                type=target_type,
                title=title if isinstance(title, str) else "",
                url=target_url if isinstance(target_url, str) else "",
                web_socket_debugger_url=(
                    websocket_url if isinstance(websocket_url, str) else None
                ),
            )
        )
    return targets


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="枚举 Trae 当前 remote-debugging 端口暴露的所有 CDP targets。"
    )
    parser.add_argument(
        "--host",
        default=DEFAULT_REMOTE_DEBUGGING_HOST,
        help="CDP 主机，默认 127.0.0.1",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_REMOTE_DEBUGGING_PORT,
        help="CDP 端口，默认 9330",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="输出 JSON",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        targets = fetch_targets(args.host, args.port)
    except httpx.HTTPError as exc:
        print(f"error: 无法连接 CDP {args.host}:{args.port} ({exc})", file=sys.stderr)
        return 1

    if args.json:
        print(
            json.dumps(
                [target_to_dict(target) for target in targets],
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    print(f"target_count: {len(targets)}")
    for target in targets:
        print(
            json.dumps(
                {
                    "id": target.id,
                    "type": target.type,
                    "title": target.title,
                    "url": target.url,
                    "ws": target.web_socket_debugger_url,
                },
                ensure_ascii=False,
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
