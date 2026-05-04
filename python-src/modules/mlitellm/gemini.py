# pyright: reportPrivateUsage=false, reportUnusedFunction=false
from __future__ import annotations

import json
import time
from collections.abc import Iterator
from typing import Any, cast

from .common import (
    _as_str,
    _base_url,
    _chat_chunk,
    _ClosableIterator,
    _coerce_int,
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

_GEMINI_UNSUPPORTED_SCHEMA_KEYS: frozenset[str] = frozenset(
    {
        "additionalProperties",
    }
)


def _gemini_completion(kwargs: dict[str, Any]) -> dict[str, Any] | Iterator[Any]:
    model = _strip_model_prefix(_as_str(kwargs.get("model")), "gemini")
    body = _build_gemini_body(kwargs)
    headers = _headers(
        api_key=_as_str(kwargs.get("api_key")),
        auth_header="Authorization",
        auth_value_prefix="Bearer ",
        extra_headers=kwargs.get("extra_headers"),
    )
    endpoint = f"models/{model}:generateContent"
    if bool(kwargs.get("stream")):
        endpoint = f"models/{model}:streamGenerateContent?alt=sse"
        return _stream_gemini_content(
            _join_url(_base_url(kwargs), endpoint),
            body=body,
            headers=headers,
            kwargs=kwargs,
            model=model,
        )
    response_json = _json_request(
        "POST",
        _join_url(_base_url(kwargs), endpoint),
        body=body,
        headers=headers,
        kwargs=kwargs,
        model=model,
        provider="gemini",
    )
    response_json = _sanitize_empty_gemini_prompt_feedback(response_json)
    return _gemini_payload_to_chat_completion(response_json, fallback_model=model)

def _build_gemini_body(kwargs: dict[str, Any]) -> dict[str, Any]:
    source_body = _request_body_from_kwargs(
        kwargs,
        model=_strip_model_prefix(_as_str(kwargs.get("model")), "gemini"),
    )
    messages_obj = source_body.pop("messages", [])
    contents, system_instruction = _messages_to_gemini(messages_obj)
    body: dict[str, Any] = {"contents": contents}
    if system_instruction:
        body["systemInstruction"] = {"parts": [{"text": system_instruction}]}
    generation_config: dict[str, Any] = {}
    if "max_completion_tokens" in source_body:
        generation_config["maxOutputTokens"] = source_body.pop("max_completion_tokens")
    if "max_tokens" in source_body and "maxOutputTokens" not in generation_config:
        generation_config["maxOutputTokens"] = source_body.pop("max_tokens")
    if "temperature" in source_body:
        generation_config["temperature"] = source_body.pop("temperature")
    if "top_p" in source_body:
        generation_config["topP"] = source_body.pop("top_p")
    if "stop" in source_body:
        stop = source_body.pop("stop")
        generation_config["stopSequences"] = stop if isinstance(stop, list) else [stop]
    if "response_format" in source_body:
        mime_type = _gemini_response_mime_type(source_body.pop("response_format"))
        if mime_type:
            generation_config["responseMimeType"] = mime_type
    if "thinking" in source_body:
        generation_config["thinkingConfig"] = source_body.pop("thinking")
    if generation_config:
        body["generationConfig"] = generation_config
    if "tools" in source_body:
        body["tools"] = _openai_tools_to_gemini(source_body.pop("tools"))
    tool_config = _openai_tool_choice_to_gemini(source_body.pop("tool_choice", None))
    if tool_config:
        body["toolConfig"] = tool_config
    source_body.pop("stream", None)
    body.update(source_body)
    return body

def _stream_gemini_content(
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
        provider="gemini",
    )
    return _ClosableIterator(source, _iter_gemini_content_events(source, model=model))


def _iter_gemini_content_events(
    events: Iterator[Any],
    *,
    model: str,
) -> Iterator[dict[str, Any] | str]:
    yield _chat_chunk(model=model, delta={"role": "assistant"})
    for event in events:
        if isinstance(event, str):
            yield event
            continue
        sanitized_event = _sanitize_empty_gemini_prompt_feedback(event)
        candidate = _first_candidate(sanitized_event)
        if candidate is None:
            continue
        for part in _candidate_parts(candidate):
            text = _as_str(part.get("text"))
            if text:
                key = "reasoning_content" if _is_gemini_thought_part(part) else "content"
                yield _chat_chunk(model=model, delta={key: text})
            function_call = part.get("functionCall")
            if isinstance(function_call, dict):
                yield _chat_chunk(
                    model=model,
                    delta={
                        "tool_calls": [
                            _gemini_function_call_to_openai(
                                cast(dict[str, Any], function_call)
                            )
                        ]
                    },
                )
        finish_reason = _normalize_finish_reason(candidate.get("finishReason"))
        if finish_reason:
            yield _chat_chunk(model=model, delta={}, finish_reason=finish_reason)

def _messages_to_gemini(messages: Any) -> tuple[list[dict[str, Any]], str]:
    if not isinstance(messages, list):
        return [], ""
    contents: list[dict[str, Any]] = []
    system_parts: list[str] = []
    for message_obj in cast(list[object], messages):
        if not isinstance(message_obj, dict):
            continue
        message = cast(dict[str, Any], message_obj)
        role = _as_str(message.get("role"))
        text = _content_to_text(message.get("content"))
        if role == "system":
            if text:
                system_parts.append(text)
            continue
        contents.append(
            {
                "role": "model" if role == "assistant" else "user",
                "parts": [{"text": text}],
            }
        )
    return contents, "\n\n".join(system_parts)

def _openai_tools_to_gemini(tools: Any) -> list[dict[str, Any]]:
    if not isinstance(tools, list):
        return []
    declarations: list[dict[str, Any]] = []
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
        declaration: dict[str, Any] = {"name": name}
        description = _as_str(function.get("description"))
        if description:
            declaration["description"] = description
        parameters = function.get("parameters")
        if isinstance(parameters, dict):
            declaration["parameters"] = _sanitize_gemini_schema(parameters)
        declarations.append(declaration)
    return [{"functionDeclarations": declarations}] if declarations else []


def _sanitize_gemini_schema(schema: Any) -> Any:
    if isinstance(schema, list):
        return [_sanitize_gemini_schema(item) for item in cast(list[Any], schema)]
    if not isinstance(schema, dict):
        return schema

    sanitized: dict[str, Any] = {}
    for key, value in cast(dict[str, Any], schema).items():
        if key in _GEMINI_UNSUPPORTED_SCHEMA_KEYS:
            continue
        sanitized[key] = _sanitize_gemini_schema(value)
    return sanitized

def _openai_tool_choice_to_gemini(tool_choice: Any) -> dict[str, Any] | None:
    if tool_choice in (None, "none"):
        return None
    mode = "AUTO"
    allowed_names: list[str] = []
    if tool_choice == "required":
        mode = "ANY"
    elif isinstance(tool_choice, dict):
        function_obj = cast(dict[str, Any], tool_choice).get("function")
        if isinstance(function_obj, dict):
            name = _as_str(cast(dict[str, Any], function_obj).get("name"))
            if name:
                mode = "ANY"
                allowed_names.append(name)
    config: dict[str, Any] = {"mode": mode}
    if allowed_names:
        config["allowedFunctionNames"] = allowed_names
    return {"functionCallingConfig": config}

def _gemini_payload_to_chat_completion(
    payload: dict[str, Any],
    *,
    fallback_model: str,
) -> dict[str, Any]:
    candidate = _first_candidate(payload) or {}
    message = _message_from_gemini_candidate(candidate)
    return {
        "id": _new_id(),
        "object": "chat.completion",
        "created": _coerce_int(time.time()),
        "model": fallback_model,
        "choices": [
            {
                "index": 0,
                "message": message,
                "finish_reason": _normalize_finish_reason(candidate.get("finishReason")),
            }
        ],
        "usage": _gemini_usage_to_chat_usage(payload.get("usageMetadata")),
    }


def _message_from_gemini_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    message: dict[str, Any] = {"role": "assistant", "content": ""}
    content_parts: list[str] = []
    reasoning_parts: list[str] = []
    tool_calls: list[dict[str, Any]] = []
    for part in _candidate_parts(candidate):
        text = _as_str(part.get("text"))
        if text:
            if _is_gemini_thought_part(part):
                reasoning_parts.append(text)
            else:
                content_parts.append(text)
        function_call = part.get("functionCall")
        if isinstance(function_call, dict):
            tool_calls.append(
                _gemini_function_call_to_openai(cast(dict[str, Any], function_call))
            )
    message["content"] = "".join(content_parts)
    if reasoning_parts:
        message["reasoning_content"] = "".join(reasoning_parts)
    if tool_calls:
        message["tool_calls"] = tool_calls
    return message


def _is_gemini_thought_part(part: dict[str, Any]) -> bool:
    return part.get("thought") is True


def _gemini_function_call_to_openai(function_call: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": _new_id("call"),
        "type": "function",
        "function": {
            "name": _as_str(function_call.get("name")),
            "arguments": json.dumps(
                function_call.get("args") or {},
                ensure_ascii=False,
                separators=(",", ":"),
            ),
        },
    }


def _gemini_usage_to_chat_usage(usage: Any) -> dict[str, Any] | None:
    if not isinstance(usage, dict):
        return None
    usage_dict = cast(dict[str, Any], usage)
    return {
        "prompt_tokens": usage_dict.get("promptTokenCount"),
        "completion_tokens": usage_dict.get("candidatesTokenCount"),
        "total_tokens": usage_dict.get("totalTokenCount"),
    }


def _first_candidate(payload: dict[str, Any]) -> dict[str, Any] | None:
    candidates = payload.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        return None
    first = cast(list[Any], candidates)[0]
    if isinstance(first, dict):
        return cast(dict[str, Any], first)
    return None


def _candidate_parts(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    content = candidate.get("content")
    if not isinstance(content, dict):
        return []
    parts = cast(dict[str, Any], content).get("parts")
    if not isinstance(parts, list):
        return []
    return [
        cast(dict[str, Any], part)
        for part in cast(list[Any], parts)
        if isinstance(part, dict)
    ]


def _sanitize_empty_gemini_prompt_feedback(payload: Any) -> Any:
    if not isinstance(payload, dict):
        return payload

    payload_dict = dict(cast(dict[str, Any], payload))
    prompt_feedback_obj = payload_dict.get("promptFeedback")
    if not isinstance(prompt_feedback_obj, dict):
        return payload_dict

    prompt_feedback = dict(cast(dict[str, Any], prompt_feedback_obj))
    block_reason = prompt_feedback.get("blockReason")
    if block_reason is not None and (
        not isinstance(block_reason, str) or block_reason.strip()
    ):
        return payload_dict

    prompt_feedback.pop("blockReason", None)
    block_reason_message = prompt_feedback.get("blockReasonMessage")
    if isinstance(block_reason_message, str) and not block_reason_message.strip():
        prompt_feedback.pop("blockReasonMessage", None)

    if prompt_feedback:
        payload_dict["promptFeedback"] = prompt_feedback
    else:
        payload_dict.pop("promptFeedback", None)
    return payload_dict


def _gemini_response_mime_type(response_format: Any) -> str:
    if not isinstance(response_format, dict):
        return ""
    format_type = _as_str(cast(dict[str, Any], response_format).get("type"))
    if format_type in {"json_object", "json_schema"}:
        return "application/json"
    if format_type == "text":
        return "text/plain"
    return ""
