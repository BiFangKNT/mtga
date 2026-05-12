# pyright: reportPrivateUsage=false, reportUnusedFunction=false
from __future__ import annotations

import json
import time
from collections.abc import Iterator
from typing import Any, cast

from .common import (
    _apply_request_body_patch,
    _as_str,
    _base_url,
    _chat_chunk,
    _ClosableIterator,
    _coerce_int,
    _collect_text_values,
    _content_to_text,
    _headers,
    _join_url,
    _json_request,
    _new_id,
    _normalize_finish_reason,
    _request_body_from_kwargs,
    _stream_json_request,
    _strip_model_prefix,
)


def _anthropic_completion(kwargs: dict[str, Any]) -> dict[str, Any] | Iterator[Any]:
    model = _strip_model_prefix(_as_str(kwargs.get("model")), "anthropic")
    body = _build_anthropic_body(kwargs, model=model)
    body = _apply_request_body_patch(body, kwargs, model=model, provider="anthropic")
    url = _join_url(_base_url(kwargs), "v1/messages")
    headers = _headers(
        api_key=_as_str(kwargs.get("api_key")),
        auth_header="x-api-key",
        auth_value_prefix="",
        extra_headers=kwargs.get("extra_headers"),
        defaults={"anthropic-version": "2023-06-01"},
    )
    if bool(body.get("stream")):
        return _stream_anthropic_messages(
            url,
            body=body,
            headers=headers,
            kwargs=kwargs,
            model=model,
        )
    response_json = _json_request(
        "POST",
        url,
        body=body,
        headers=headers,
        kwargs=kwargs,
        model=model,
        provider="anthropic",
    )
    return _anthropic_payload_to_chat_completion(response_json, fallback_model=model)

def _build_anthropic_body(kwargs: dict[str, Any], *, model: str) -> dict[str, Any]:
    source_body = _request_body_from_kwargs(kwargs, model=model)
    messages_obj = source_body.pop("messages", [])
    messages, system = _messages_to_anthropic(messages_obj)
    body: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "max_tokens": _coerce_int(
            source_body.pop("max_tokens", None)
            or source_body.pop("max_completion_tokens", None)
            or 4096
        ),
    }
    if system:
        body["system"] = system
    for key in (
        "metadata",
        "stop_sequences",
        "stream",
        "temperature",
        "thinking",
        "top_k",
        "top_p",
    ):
        if key in source_body:
            body[key] = source_body.pop(key)
    if "stop" in source_body:
        stop = source_body.pop("stop")
        body["stop_sequences"] = stop if isinstance(stop, list) else [stop]
    if "tools" in source_body:
        body["tools"] = _openai_tools_to_anthropic(source_body.pop("tools"))
    if "tool_choice" in source_body:
        body["tool_choice"] = _openai_tool_choice_to_anthropic(
            source_body.pop("tool_choice")
        )
    body.update(source_body)
    return body

def _stream_anthropic_messages(
    url: str,
    *,
    body: dict[str, Any],
    headers: dict[str, str],
    kwargs: dict[str, Any],
    model: str,
) -> Iterator[dict[str, Any] | str]:
    source = _stream_json_request(
        "POST",
        url,
        body=body,
        headers=headers,
        kwargs=kwargs,
        model=model,
        provider="anthropic",
    )
    return _ClosableIterator(source, _iter_anthropic_message_events(source, model=model))


def _iter_anthropic_message_events(
    events: Iterator[Any],
    *,
    model: str,
) -> Iterator[dict[str, Any] | str]:
    yield _chat_chunk(model=model, delta={"role": "assistant"})
    finish_reason: str | None = None
    for event in events:
        if isinstance(event, str):
            yield event
            continue
        if _has_openai_choices(event):
            yield event
            continue
        event_type = _as_str(event.get("type"))
        if event_type == "content_block_start":
            content_block = event.get("content_block")
            if isinstance(content_block, dict):
                yield from _anthropic_content_block_chunks(
                    cast(dict[str, Any], content_block),
                    model=model,
                )
        elif event_type == "content_block_delta":
            delta_obj = event.get("delta")
            if isinstance(delta_obj, dict):
                delta = cast(dict[str, Any], delta_obj)
                delta_type = _as_str(delta.get("type"))
                text = _as_str(delta.get("text") or delta.get("thinking"))
                if text:
                    key = "reasoning_content" if delta_type == "thinking_delta" else "content"
                    yield _chat_chunk(model=model, delta={key: text})
        elif event_type == "message_delta":
            delta_obj = event.get("delta")
            if isinstance(delta_obj, dict):
                delta = cast(dict[str, Any], delta_obj)
                finish_reason = _normalize_finish_reason(delta.get("stop_reason"))
        elif event_type == "message_stop":
            yield _chat_chunk(model=model, delta={}, finish_reason=finish_reason or "stop")


def _has_openai_choices(event: dict[str, Any]) -> bool:
    choices = event.get("choices")
    return isinstance(choices, list)


def _anthropic_content_block_chunks(
    content_block: dict[str, Any],
    *,
    model: str,
) -> Iterator[dict[str, Any]]:
    block_type = _as_str(content_block.get("type"))
    text = _as_str(content_block.get("text") or content_block.get("thinking"))
    if text:
        key = "reasoning_content" if block_type == "thinking" else "content"
        yield _chat_chunk(model=model, delta={key: text})

def _messages_to_anthropic(messages: Any) -> tuple[list[dict[str, Any]], str]:
    if not isinstance(messages, list):
        return [], ""
    converted: list[dict[str, Any]] = []
    system_parts: list[str] = []
    for message_obj in cast(list[object], messages):
        if not isinstance(message_obj, dict):
            continue
        message = cast(dict[str, Any], message_obj)
        role = _as_str(message.get("role"))
        content = message.get("content")
        if role == "system":
            system_text = _content_to_text(content)
            if system_text:
                system_parts.append(system_text)
            continue
        converted.append(
            {
                "role": "assistant" if role == "assistant" else "user",
                "content": _content_to_anthropic_blocks(content),
            }
        )
    return converted, "\n\n".join(system_parts)

def _content_to_anthropic_blocks(content: Any) -> list[dict[str, Any]]:
    if isinstance(content, list):
        blocks: list[dict[str, Any]] = []
        for part_obj in cast(list[object], content):
            if isinstance(part_obj, dict):
                part = cast(dict[str, Any], part_obj)
                if part.get("type") == "text" and isinstance(part.get("text"), str):
                    blocks.append({"type": "text", "text": part["text"]})
            elif isinstance(part_obj, str):
                blocks.append({"type": "text", "text": part_obj})
        return blocks
    return [{"type": "text", "text": _content_to_text(content)}]

def _openai_tools_to_anthropic(tools: Any) -> list[dict[str, Any]]:
    if not isinstance(tools, list):
        return []
    converted: list[dict[str, Any]] = []
    for tool_obj in cast(list[object], tools):
        if not isinstance(tool_obj, dict):
            continue
        tool = cast(dict[str, Any], tool_obj)
        function_obj = tool.get("function")
        if tool.get("type") != "function" or not isinstance(function_obj, dict):
            continue
        function = cast(dict[str, Any], function_obj)
        name = _as_str(function.get("name"))
        if not name:
            continue
        converted.append(
            {
                "name": name,
                "description": _as_str(function.get("description")),
                "input_schema": function.get("parameters") or {"type": "object"},
            }
        )
    return converted

def _openai_tool_choice_to_anthropic(tool_choice: Any) -> dict[str, Any] | None:
    if tool_choice in (None, "none"):
        return None
    if tool_choice == "auto":
        return {"type": "auto"}
    if tool_choice == "required":
        return {"type": "any"}
    if isinstance(tool_choice, dict):
        function_obj = cast(dict[str, Any], tool_choice).get("function")
        if isinstance(function_obj, dict):
            name = _as_str(cast(dict[str, Any], function_obj).get("name"))
            if name:
                return {"type": "tool", "name": name}
    return None

def _anthropic_payload_to_chat_completion(
    payload: dict[str, Any],
    *,
    fallback_model: str,
) -> dict[str, Any]:
    message = _message_from_anthropic_content(payload.get("content"))
    usage_obj = payload.get("usage")
    usage_dict = cast(dict[str, Any], usage_obj) if isinstance(usage_obj, dict) else {}
    input_tokens = usage_dict.get("input_tokens")
    output_tokens = usage_dict.get("output_tokens")
    total_tokens = (
        input_tokens + output_tokens
        if isinstance(input_tokens, int) and isinstance(output_tokens, int)
        else None
    )
    return {
        "id": _as_str(payload.get("id")) or _new_id(),
        "object": "chat.completion",
        "created": _coerce_int(time.time()),
        "model": _as_str(payload.get("model")) or fallback_model,
        "choices": [
            {
                "index": 0,
                "message": message,
                "finish_reason": _normalize_finish_reason(payload.get("stop_reason")),
            }
        ],
        "usage": {
            "prompt_tokens": input_tokens,
            "completion_tokens": output_tokens,
            "total_tokens": total_tokens,
        },
    }


def _message_from_anthropic_content(content: Any) -> dict[str, Any]:
    message: dict[str, Any] = {"role": "assistant", "content": ""}
    content_parts: list[str] = []
    reasoning_parts: list[str] = []
    tool_calls: list[dict[str, Any]] = []
    if isinstance(content, list):
        for part_obj in cast(list[object], content):
            if not isinstance(part_obj, dict):
                continue
            part = cast(dict[str, Any], part_obj)
            part_type = _as_str(part.get("type"))
            if part_type == "text":
                content_parts.append(_as_str(part.get("text")))
            elif part_type == "thinking":
                _collect_text_values(part.get("thinking") or part.get("text"), reasoning_parts)
            elif part_type == "tool_use":
                tool_calls.append(
                    {
                        "id": _as_str(part.get("id")) or _new_id("call"),
                        "type": "function",
                        "function": {
                            "name": _as_str(part.get("name")),
                            "arguments": json.dumps(
                                part.get("input") or {},
                                ensure_ascii=False,
                                separators=(",", ":"),
                            ),
                        },
                    }
                )
    message["content"] = "".join(content_parts)
    if reasoning_parts:
        message["reasoning_content"] = "".join(reasoning_parts)
    if tool_calls:
        message["tool_calls"] = tool_calls
    return message
