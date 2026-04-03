from __future__ import annotations

import json
import time
from contextlib import suppress
from pathlib import Path
from typing import Any

from pydantic import BaseModel
from pytauri import Commands

from modules.runtime.log_bus import pull_logs, push_log
from modules.runtime.resource_manager import get_log_path


class LogPullPayload(BaseModel):
    after_id: int | None = None
    timeout_ms: int = 0
    max_items: int = 200


class FrontendReportPayload(BaseModel):
    kind: str
    message: str
    stack: str | None = None
    source: str | None = None
    url: str | None = None
    user_agent: str | None = None
    ready_state: str | None = None
    extra: dict[str, Any] | None = None


def _resolve_frontend_log_path() -> Path | None:
    try:
        return Path(get_log_path("mtga_frontend.log"))
    except Exception:
        return None


_FRONTEND_LOG_PATH = _resolve_frontend_log_path()


def _trim_text(value: str | None, limit: int = 4000) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    if len(text) <= limit:
        return text
    return text[: limit - 1] + "…"


def _append_frontend_log(message: str) -> None:
    if _FRONTEND_LOG_PATH is None:
        return
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S ")
    with suppress(Exception), _FRONTEND_LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(f"{timestamp}{message}\n")


def _format_frontend_report(body: FrontendReportPayload) -> str:
    title = _trim_text(body.kind, 80) or "unknown"
    message = _trim_text(body.message) or "unknown error"
    lines = [f"[frontend:{title}] {message}"]
    meta = {
        "source": _trim_text(body.source, 512),
        "url": _trim_text(body.url, 1024),
        "ready_state": _trim_text(body.ready_state, 64),
        "user_agent": _trim_text(body.user_agent, 1024),
    }
    compact_meta = {key: value for key, value in meta.items() if value}
    if compact_meta:
        lines.append(f"meta={json.dumps(compact_meta, ensure_ascii=False, sort_keys=True)}")
    if body.extra:
        lines.append(
            f"extra={json.dumps(body.extra, ensure_ascii=False, sort_keys=True, default=str)}"
        )
    stack = _trim_text(body.stack, 12000)
    if stack:
        lines.append(stack)
    return "\n".join(lines)


def register_log_commands(commands: Commands) -> None:
    @commands.command()
    async def pull_logs_command(body: LogPullPayload) -> dict[str, Any]:
        result = pull_logs(
            after_id=body.after_id,
            timeout_ms=body.timeout_ms,
            max_items=body.max_items,
        )
        return result

    @commands.command()
    async def frontend_report(body: FrontendReportPayload) -> bool:
        message = _format_frontend_report(body)
        push_log(message)
        _append_frontend_log(message)
        return True

    _ = pull_logs_command
    _ = frontend_report


__all__ = ["register_log_commands"]
