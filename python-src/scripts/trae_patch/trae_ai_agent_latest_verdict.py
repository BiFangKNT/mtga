from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path

TRACE_ID_RE = re.compile(r'trace_id="([0-9a-f]+)"')
CONFIG_NAME_RE = re.compile(r'config_name: "([^"]+)"')
BASE_URL_RE = re.compile(r'base_url:\s*Some\("([^"]+)"\)')
STATUS_RE = re.compile(r"Status:\s*(\d+)")
UNKNOWN_EVENT_RE = re.compile(r'Unknown event: Event \{ event: "([^"]+)"')
REQUEST_URL_RE = re.compile(r"\[HTTPClient\] request url (\S+)")
FIRST_TOKEN_RE = re.compile(r'first token flushed thought, thought="([^"]*)"')
TASK_STATUS_RE = re.compile(r"TASK: .*status=([A-Za-z]+)")


@dataclass
class TraceSummary:
    trace_id: str
    model_info_line: str | None = None
    config_name: str | None = None
    base_url: str | None = None
    ak_present: bool | None = None
    llm_raw_chat_url: str | None = None
    llm_raw_chat_status: int | None = None
    create_agent_task_url: str | None = None
    create_agent_task_status: int | None = None
    unknown_events: list[str] = field(default_factory=list)
    provider_error_line: str | None = None
    first_token_text: str | None = None
    chat_finished: bool = False
    task_status: str | None = None
    main_routine_ok: bool = False
    latest_line_no: int = -1

    def verdict(self) -> str:
        result = "unknown"
        if self.base_url == "https://api.openai.com/v1" and self.provider_error_line:
            if "Incorrect API key provided: 111" in self.provider_error_line:
                result = "official_openai_route_invalid_key_111"
            else:
                result = "official_openai_route_provider_error"
        elif self.provider_error_line:
            result = "provider_error"
        elif self.task_status == "Completed" or self.main_routine_ok:
            result = "chat_completed"
        elif self.first_token_text is not None:
            result = "stream_consumed"
        elif self.base_url and "127.0.0.1" in self.base_url:
            result = "local_proxy_route"
        elif self.chat_finished:
            result = "chat_finished_without_success_marker"
        elif self.model_info_line:
            result = "model_info_only"
        return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="精简输出最新 Trae ai-agent 路由结论")
    parser.add_argument(
        "--log",
        type=Path,
        help="指定 ai-agent stdout 日志；默认自动选择最新文件",
    )
    parser.add_argument(
        "--trace-id",
        help="指定 trace_id；默认选择日志里最后一个 custom model trace",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="输出 JSON",
    )
    return parser.parse_args()


def find_latest_log(explicit_log: Path | None) -> Path:
    if explicit_log is not None:
        return explicit_log
    root = Path.home() / "AppData" / "Roaming" / "Trae" / "logs"
    candidates = sorted(
        root.rglob("ai-agent_*_stdout.log"),
        key=lambda item: item.stat().st_mtime,
        reverse=True,
    )
    if not candidates:
        raise FileNotFoundError("未找到 ai-agent stdout 日志")
    return candidates[0]


def get_trace(summary_map: dict[str, TraceSummary], trace_id: str) -> TraceSummary:
    summary = summary_map.get(trace_id)
    if summary is None:
        summary = TraceSummary(trace_id=trace_id)
        summary_map[trace_id] = summary
    return summary


def handle_model_info(raw_line: str, summary: TraceSummary) -> bool:
    if "model_info: CustomModel" not in raw_line:
        return False

    summary.model_info_line = raw_line
    config_match = CONFIG_NAME_RE.search(raw_line)
    if config_match:
        summary.config_name = config_match.group(1)
    base_url_match = BASE_URL_RE.search(raw_line)
    if base_url_match:
        summary.base_url = base_url_match.group(1)
    summary.ak_present = "ak: Some(" in raw_line
    return True


def handle_request_line(raw_line: str, summary: TraceSummary) -> bool:
    if "[HTTPClient] request url" not in raw_line:
        return False

    url_match = REQUEST_URL_RE.search(raw_line)
    if not url_match:
        return True

    url = url_match.group(1)
    if "llm_raw_chat" in raw_line:
        summary.llm_raw_chat_url = url
    elif "create_agent_task" in raw_line:
        summary.create_agent_task_url = url
    return True


def handle_status_line(raw_line: str, summary: TraceSummary) -> bool:
    if "Status:" not in raw_line or "[AhaNetHTTPClient/Stream][Error]" in raw_line:
        return False

    status_match = STATUS_RE.search(raw_line)
    if not status_match:
        return True

    status = int(status_match.group(1))
    if "llm_raw_chat" in raw_line:
        summary.llm_raw_chat_status = status
    elif "create_agent_task" in raw_line:
        summary.create_agent_task_status = status
    return True


def handle_event_or_error(raw_line: str, summary: TraceSummary) -> None:
    if "Unknown event:" in raw_line:
        event_match = UNKNOWN_EVENT_RE.search(raw_line)
        if event_match:
            summary.unknown_events.append(event_match.group(1))
        return

    if "[AhaNetHTTPClient/Stream][Error]" in raw_line or "send error to frontend" in raw_line:
        summary.provider_error_line = raw_line


def handle_completion_line(raw_line: str, summary: TraceSummary) -> bool:
    first_token_match = FIRST_TOKEN_RE.search(raw_line)
    if first_token_match:
        summary.first_token_text = first_token_match.group(1)
        return True

    if "[ChatContextEntity] chat finished" in raw_line:
        summary.chat_finished = True
        return True

    task_status_match = TASK_STATUS_RE.search(raw_line)
    if task_status_match:
        summary.task_status = task_status_match.group(1)
        return True

    if "main_routine resp: Ok(())" in raw_line:
        summary.main_routine_ok = True
        return True

    return False


def parse_log(log_path: Path) -> tuple[dict[str, TraceSummary], list[str]]:
    summary_map: dict[str, TraceSummary] = {}
    custom_model_trace_ids: list[str] = []
    content = log_path.read_text(encoding="utf-8", errors="ignore").splitlines()

    for line_no, raw_line in enumerate(content, start=1):
        trace_match = TRACE_ID_RE.search(raw_line)
        if not trace_match:
            continue
        trace_id = trace_match.group(1)
        summary = get_trace(summary_map, trace_id)
        summary.latest_line_no = line_no

        if handle_model_info(raw_line, summary):
            custom_model_trace_ids.append(trace_id)
            continue

        if "[create_agent_task]" in raw_line:
            continue

        if handle_request_line(raw_line, summary):
            continue

        if handle_status_line(raw_line, summary):
            continue

        if handle_completion_line(raw_line, summary):
            continue

        handle_event_or_error(raw_line, summary)

    return summary_map, custom_model_trace_ids


def render_text(log_path: Path, summary: TraceSummary) -> str:
    unknown_events = ",".join(summary.unknown_events) if summary.unknown_events else "<none>"
    return "\n".join(
        [
            f"log={log_path}",
            f"trace_id={summary.trace_id}",
            f"verdict={summary.verdict()}",
            f"config_name={summary.config_name or '<none>'}",
            f"base_url={summary.base_url or '<none>'}",
            f"ak_present={summary.ak_present}",
            f"create_agent_task_url={summary.create_agent_task_url or '<none>'}",
            f"create_agent_task_status={summary.create_agent_task_status}",
            f"llm_raw_chat_url={summary.llm_raw_chat_url or '<none>'}",
            f"llm_raw_chat_status={summary.llm_raw_chat_status}",
            f"unknown_events={unknown_events}",
            f"first_token_text={summary.first_token_text or '<none>'}",
            f"chat_finished={summary.chat_finished}",
            f"task_status={summary.task_status or '<none>'}",
            f"main_routine_ok={summary.main_routine_ok}",
            f"provider_error={summary.provider_error_line or '<none>'}",
        ]
    )


def main() -> int:
    args = parse_args()
    log_path = find_latest_log(args.log)
    summary_map, custom_model_trace_ids = parse_log(log_path)

    if args.trace_id:
        trace_id = args.trace_id
    elif custom_model_trace_ids:
        trace_id = custom_model_trace_ids[-1]
    else:
        raise RuntimeError("日志里未找到 custom model trace_id")

    summary = summary_map.get(trace_id)
    if summary is None:
        raise RuntimeError(f"未在日志中找到 trace_id={trace_id}")

    if args.json:
        payload = {
            "log": str(log_path),
            "summary": asdict(summary),
            "verdict": summary.verdict(),
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(render_text(log_path, summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
