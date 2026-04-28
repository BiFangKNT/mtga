from __future__ import annotations

import copy
import json
import threading
import time
import uuid
from collections import OrderedDict
from datetime import UTC, datetime
from typing import Any, Literal, NotRequired, TypedDict, cast

ProxyTraceStatus = Literal["active", "completed", "failed", "cancelled"]
ProxyTraceTruncatedReason = Literal["size_limit", "stream_limit", "unsupported_type"]

MAX_PROXY_TRACES = 500
MAX_BODY_CAPTURE_BYTES = 64 * 1024
MAX_EVENT_MESSAGE_BYTES = 8 * 1024
MAX_EVENT_DATA_BYTES = 8 * 1024
MAX_REDACT_DEPTH = 12

_SENSITIVE_KEY_PARTS = (
    "authorization",
    "api_key",
    "apikey",
    "access_token",
    "refresh_token",
    "secret",
    "password",
    "mtga_auth_key",
)


class ProxyTraceBodyCapture(TypedDict, total=False):
    value: Any
    bytes: int
    truncated: bool
    truncated_reason: ProxyTraceTruncatedReason
    redacted: bool


class ProxyTraceEvent(TypedDict, total=False):
    at: str
    kind: str
    message: str
    data: dict[str, Any]


class ProxyTrace(TypedDict):
    trace_id: str
    request_id: str
    status: ProxyTraceStatus
    method: str
    request_path: str
    is_stream: bool
    started_at: str
    events: list[ProxyTraceEvent]
    route_mode: NotRequired[str]
    provider: NotRequired[str]
    request_api: NotRequired[str]
    request_model: NotRequired[str]
    client_model: NotRequired[str]
    resolved_target_label: NotRequired[str]
    target_api_base_url: NotRequired[str]
    upstream_model: NotRequired[str]
    target_model: NotRequired[str]
    status_code: NotRequired[int]
    first_chunk_at: NotRequired[str]
    ended_at: NotRequired[str]
    duration_ms: NotRequired[int]
    chunk_count: NotRequired[int]
    finish_reason: NotRequired[str]
    request_body: NotRequired[ProxyTraceBodyCapture]
    response_body: NotRequired[ProxyTraceBodyCapture]
    error: NotRequired[str]


class ProxyTraceSummary(TypedDict, total=False):
    trace_id: str
    request_id: str
    status: ProxyTraceStatus
    method: str
    request_path: str
    request_model: str
    provider: str
    upstream_model: str
    is_stream: bool
    status_code: int
    started_at: str
    ended_at: str
    duration_ms: int
    chunk_count: int
    error: str
    events_count: int
    request_body_bytes: int
    response_body_bytes: int
    request_body_truncated: bool
    response_body_truncated: bool


def _now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _is_sensitive_key(key: str) -> bool:
    normalized = key.strip().lower().replace("-", "_")
    return any(part in normalized for part in _SENSITIVE_KEY_PARTS)


def _redact_value(value: Any, *, depth: int = 0) -> tuple[Any, bool]:
    if depth > MAX_REDACT_DEPTH:
        return "<max-depth>", True
    if isinstance(value, dict):
        redacted = False
        next_mapping: dict[str, Any] = {}
        for raw_key, raw_item in cast(dict[Any, Any], value).items():
            key = str(raw_key)
            if _is_sensitive_key(key):
                next_mapping[key] = "<redacted>"
                redacted = True
                continue
            next_value, child_redacted = _redact_value(raw_item, depth=depth + 1)
            next_mapping[key] = next_value
            redacted = redacted or child_redacted
        return next_mapping, redacted
    if isinstance(value, list):
        redacted = False
        next_items: list[Any] = []
        for item in cast(list[Any], value):
            next_value, child_redacted = _redact_value(item, depth=depth + 1)
            next_items.append(next_value)
            redacted = redacted or child_redacted
        return next_items, redacted
    if isinstance(value, tuple):
        redacted = False
        next_items: list[Any] = []
        for item in cast(tuple[Any, ...], value):
            next_value, child_redacted = _redact_value(item, depth=depth + 1)
            next_items.append(next_value)
            redacted = redacted or child_redacted
        return next_items, redacted
    if isinstance(value, bytes | bytearray):
        return bytes(value).decode("utf-8", errors="replace"), False
    return value, False


def _dump_json(value: Any) -> str:
    try:
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"), default=str)
    except Exception:  # noqa: BLE001
        return str(value)


def _trim_text_to_bytes(text: str, max_bytes: int) -> str:
    encoded = text.encode("utf-8", errors="replace")
    if len(encoded) <= max_bytes:
        return text
    return encoded[:max_bytes].decode("utf-8", errors="replace")


def capture_proxy_trace_body(
    value: Any,
    *,
    max_bytes: int = MAX_BODY_CAPTURE_BYTES,
    truncated_reason: ProxyTraceTruncatedReason = "size_limit",
) -> ProxyTraceBodyCapture:
    if value is None:
        return {"value": None, "bytes": 0, "truncated": False, "redacted": False}

    redacted_value, redacted = _redact_value(value)
    serialized = _dump_json(redacted_value)
    encoded_len = len(serialized.encode("utf-8", errors="replace"))
    if encoded_len <= max_bytes:
        return {
            "value": redacted_value,
            "bytes": encoded_len,
            "truncated": False,
            "redacted": redacted,
        }

    return {
        "value": _trim_text_to_bytes(serialized, max_bytes),
        "bytes": encoded_len,
        "truncated": True,
        "truncated_reason": truncated_reason,
        "redacted": redacted,
    }


class ProxyTraceBodyAccumulator:
    def __init__(self, *, max_bytes: int = MAX_BODY_CAPTURE_BYTES) -> None:
        self._max_bytes = max_bytes
        self._captured_parts: list[str] = []
        self._captured_bytes = 0
        self._total_bytes = 0
        self._truncated = False

    def append(self, value: Any) -> None:
        if isinstance(value, bytes | bytearray):
            text = bytes(value).decode("utf-8", errors="replace")
        elif isinstance(value, str):
            text = value
        else:
            text = _dump_json(value)

        encoded = text.encode("utf-8", errors="replace")
        self._total_bytes += len(encoded)
        remaining = self._max_bytes - self._captured_bytes
        if remaining <= 0:
            self._truncated = True
            return

        if len(encoded) <= remaining:
            self._captured_parts.append(text)
            self._captured_bytes += len(encoded)
            return

        self._captured_parts.append(encoded[:remaining].decode("utf-8", errors="replace"))
        self._captured_bytes = self._max_bytes
        self._truncated = True

    def capture(self) -> ProxyTraceBodyCapture:
        capture: ProxyTraceBodyCapture = {
            "value": "".join(self._captured_parts),
            "bytes": self._total_bytes,
            "truncated": self._truncated,
            "redacted": False,
        }
        if self._truncated:
            capture["truncated_reason"] = "stream_limit"
        return capture


class ProxyTraceStore:
    def __init__(self, *, max_traces: int = MAX_PROXY_TRACES) -> None:
        self._max_traces = max_traces
        self._lock = threading.RLock()
        self._items: OrderedDict[str, ProxyTrace] = OrderedDict()
        self._started_monotonic: dict[str, float] = {}

    def start_trace(
        self,
        *,
        request_id: str,
        method: str,
        request_path: str,
        is_stream: bool = False,
        route_mode: str | None = None,
    ) -> str:
        trace_id = uuid.uuid4().hex
        trace: ProxyTrace = {
            "trace_id": trace_id,
            "request_id": request_id,
            "status": "active",
            "method": method,
            "request_path": request_path,
            "is_stream": is_stream,
            "started_at": _now_iso(),
            "events": [],
        }
        if route_mode:
            trace["route_mode"] = route_mode

        with self._lock:
            self._items[trace_id] = trace
            self._started_monotonic[trace_id] = time.monotonic()
            self._prune_locked()
        return trace_id

    def update_trace(self, trace_id: str, **fields: Any) -> None:
        with self._lock:
            trace = self._items.get(trace_id)
            if trace is None:
                return
            for key, value in fields.items():
                if value is None:
                    continue
                trace[cast(Any, key)] = value

    def add_event(
        self,
        trace_id: str,
        *,
        kind: str,
        message: str | None = None,
        data: dict[str, Any] | None = None,
    ) -> None:
        event: ProxyTraceEvent = {
            "at": _now_iso(),
            "kind": kind,
        }
        if message:
            event["message"] = _trim_text_to_bytes(message, MAX_EVENT_MESSAGE_BYTES)
        if data:
            captured = capture_proxy_trace_body(
                data,
                max_bytes=MAX_EVENT_DATA_BYTES,
            )
            value = captured.get("value")
            event["data"] = value if isinstance(value, dict) else {"value": value}

        with self._lock:
            trace = self._items.get(trace_id)
            if trace is None:
                return
            trace["events"].append(event)

    def finish_trace(  # noqa: PLR0913
        self,
        trace_id: str,
        *,
        status: ProxyTraceStatus,
        status_code: int | None = None,
        response_body: ProxyTraceBodyCapture | None = None,
        error: str | None = None,
        chunk_count: int | None = None,
        finish_reason: str | None = None,
    ) -> None:
        with self._lock:
            trace = self._items.get(trace_id)
            if trace is None or trace["status"] != "active":
                return
            trace["status"] = status
            trace["ended_at"] = _now_iso()
            started = self._started_monotonic.pop(trace_id, None)
            if started is not None:
                trace["duration_ms"] = max(0, int((time.monotonic() - started) * 1000))
            if status_code is not None:
                trace["status_code"] = status_code
            if response_body is not None:
                trace["response_body"] = response_body
            if error:
                trace["error"] = error
            if chunk_count is not None:
                trace["chunk_count"] = chunk_count
            if finish_reason:
                trace["finish_reason"] = finish_reason
            self._prune_locked()

    def list_traces(self, *, limit: int = 200) -> list[ProxyTraceSummary]:
        normalized_limit = limit if limit > 0 else 200
        with self._lock:
            traces = list(reversed(self._items.values()))[:normalized_limit]
            return [self._build_summary(trace) for trace in traces]

    def get_trace(self, trace_id: str) -> ProxyTrace | None:
        with self._lock:
            trace = self._items.get(trace_id)
            if trace is None:
                return None
            return copy.deepcopy(trace)

    def clear_traces(self, *, include_active: bool = False) -> dict[str, int]:
        with self._lock:
            before = len(self._items)
            kept_items: OrderedDict[str, ProxyTrace] = OrderedDict()
            kept_started: dict[str, float] = {}
            for trace_id, trace in self._items.items():
                if not include_active and trace["status"] == "active":
                    kept_items[trace_id] = trace
                    if trace_id in self._started_monotonic:
                        kept_started[trace_id] = self._started_monotonic[trace_id]
            self._items = kept_items
            self._started_monotonic = kept_started
            kept = len(self._items)
            return {
                "deleted_count": before - kept,
                "kept_active_count": kept,
            }

    def _prune_locked(self) -> None:
        while len(self._items) > self._max_traces:
            removable_id: str | None = None
            for trace_id, trace in self._items.items():
                if trace["status"] != "active":
                    removable_id = trace_id
                    break
            if removable_id is None:
                return
            self._items.pop(removable_id, None)
            self._started_monotonic.pop(removable_id, None)

    @staticmethod
    def _build_summary(trace: ProxyTrace) -> ProxyTraceSummary:
        summary: ProxyTraceSummary = {
            "trace_id": trace["trace_id"],
            "request_id": trace["request_id"],
            "status": trace["status"],
            "method": trace["method"],
            "request_path": trace["request_path"],
            "is_stream": trace["is_stream"],
            "started_at": trace["started_at"],
            "events_count": len(trace["events"]),
        }
        optional_keys = (
            "request_model",
            "provider",
            "upstream_model",
            "status_code",
            "ended_at",
            "duration_ms",
            "chunk_count",
            "error",
        )
        for key in optional_keys:
            value = trace.get(key)
            if value is not None:
                summary[cast(Any, key)] = value

        request_body = trace.get("request_body")
        if request_body:
            summary["request_body_bytes"] = int(request_body.get("bytes") or 0)
            summary["request_body_truncated"] = request_body.get("truncated") is True
        response_body = trace.get("response_body")
        if response_body:
            summary["response_body_bytes"] = int(response_body.get("bytes") or 0)
            summary["response_body_truncated"] = response_body.get("truncated") is True
        return summary


_STORE = ProxyTraceStore()


def start_proxy_trace(
    *,
    request_id: str,
    method: str,
    request_path: str,
    is_stream: bool = False,
    route_mode: str | None = None,
) -> str:
    return _STORE.start_trace(
        request_id=request_id,
        method=method,
        request_path=request_path,
        is_stream=is_stream,
        route_mode=route_mode,
    )


def update_proxy_trace(trace_id: str, **fields: Any) -> None:
    _STORE.update_trace(trace_id, **fields)


def add_proxy_trace_event(
    trace_id: str,
    *,
    kind: str,
    message: str | None = None,
    data: dict[str, Any] | None = None,
) -> None:
    _STORE.add_event(trace_id, kind=kind, message=message, data=data)


def finish_proxy_trace(  # noqa: PLR0913
    trace_id: str,
    *,
    status: ProxyTraceStatus,
    status_code: int | None = None,
    response_body: ProxyTraceBodyCapture | None = None,
    error: str | None = None,
    chunk_count: int | None = None,
    finish_reason: str | None = None,
) -> None:
    _STORE.finish_trace(
        trace_id,
        status=status,
        status_code=status_code,
        response_body=response_body,
        error=error,
        chunk_count=chunk_count,
        finish_reason=finish_reason,
    )


def list_proxy_traces(*, limit: int = 200) -> list[ProxyTraceSummary]:
    return _STORE.list_traces(limit=limit)


def get_proxy_trace(trace_id: str) -> ProxyTrace | None:
    return _STORE.get_trace(trace_id)


def clear_proxy_traces(*, include_active: bool = False) -> dict[str, int]:
    return _STORE.clear_traces(include_active=include_active)


__all__ = [
    "ProxyTrace",
    "ProxyTraceBodyAccumulator",
    "ProxyTraceBodyCapture",
    "ProxyTraceEvent",
    "ProxyTraceStatus",
    "ProxyTraceStore",
    "MAX_EVENT_MESSAGE_BYTES",
    "capture_proxy_trace_body",
    "add_proxy_trace_event",
    "clear_proxy_traces",
    "finish_proxy_trace",
    "get_proxy_trace",
    "list_proxy_traces",
    "start_proxy_trace",
    "update_proxy_trace",
]
