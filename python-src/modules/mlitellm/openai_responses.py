# pyright: reportPrivateUsage=false, reportUnusedFunction=false
from __future__ import annotations

import time
from collections.abc import Iterator
from typing import Any, cast

from .common import (
    _as_str,
    _base_url,
    _chat_chunk,
    _ClosableIterator,
    _coerce_int,
    _collect_text_values,
    _headers,
    _join_url,
    _json_request,
    _new_id,
    _request_body_from_kwargs,
    _stream_json_request,
    _strip_model_prefix,
)


def _openai_responses_completion(kwargs: dict[str, Any]) -> dict[str, Any] | Iterator[Any]:
    model = _strip_model_prefix(_as_str(kwargs.get("model")), "responses")
    body = _build_openai_responses_body(kwargs, model=model)
    url = _join_url(_base_url(kwargs), "responses")
    headers = _headers(
        api_key=_as_str(kwargs.get("api_key")),
        auth_header="Authorization",
        auth_value_prefix="Bearer ",
        extra_headers=kwargs.get("extra_headers"),
    )
    if bool(body.get("stream")):
        return _stream_openai_responses(
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
        provider="openai",
    )
    return _responses_payload_to_chat_completion(response_json, fallback_model=model)

def _build_openai_responses_body(
    kwargs: dict[str, Any],
    *,
    model: str,
) -> dict[str, Any]:
    source_body = _request_body_from_kwargs(kwargs, model=model)
    body: dict[str, Any] = {"model": model}
    messages = source_body.pop("messages", None)
    if "input" in source_body:
        body["input"] = source_body.pop("input")
    elif messages is not None:
        body["input"] = _messages_to_responses_input(messages)
    for source_key, target_key in (
        ("max_completion_tokens", "max_output_tokens"),
        ("max_tokens", "max_output_tokens"),
        ("stream", "stream"),
        ("temperature", "temperature"),
        ("top_p", "top_p"),
        ("metadata", "metadata"),
        ("store", "store"),
        ("web_search_options", "web_search_options"),
    ):
        if source_key in source_body and target_key not in body:
            body[target_key] = source_body.pop(source_key)
    _move_openai_responses_tools(source_body, body)
    _move_openai_responses_tool_choice(source_body, body)
    if "reasoning" in source_body:
        body["reasoning"] = source_body.pop("reasoning")
    elif "reasoning_effort" in source_body:
        body["reasoning"] = {"effort": source_body.pop("reasoning_effort")}
    text_options: dict[str, Any] = {}
    if "verbosity" in source_body:
        text_options["verbosity"] = source_body.pop("verbosity")
    if "response_format" in source_body:
        text_options["format"] = source_body.pop("response_format")
    if text_options:
        body["text"] = text_options
    body.update(source_body)
    return body


def _move_openai_responses_tools(
    source_body: dict[str, Any],
    body: dict[str, Any],
) -> None:
    if "tools" in source_body:
        body["tools"] = _openai_tools_to_responses(source_body.pop("tools"))
        source_body.pop("functions", None)
        return
    if "functions" in source_body:
        body["tools"] = _openai_functions_to_responses_tools(
            source_body.pop("functions")
        )


def _move_openai_responses_tool_choice(
    source_body: dict[str, Any],
    body: dict[str, Any],
) -> None:
    if "tool_choice" in source_body:
        body["tool_choice"] = _openai_tool_choice_to_responses(
            source_body.pop("tool_choice")
        )
        source_body.pop("function_call", None)
        return
    if "function_call" in source_body:
        body["tool_choice"] = _openai_function_call_to_responses_tool_choice(
            source_body.pop("function_call")
        )

def _stream_openai_responses(
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
        provider="openai",
    )
    return _ClosableIterator(source, _iter_openai_response_chat_events(source, model=model))


def _iter_openai_response_chat_events(
    events: Iterator[Any],
    *,
    model: str,
) -> Iterator[dict[str, Any] | str]:
    yield _chat_chunk(model=model, delta={"role": "assistant"})
    for event in events:
        if isinstance(event, str):
            yield event
            continue
        event_type = _as_str(event.get("type"))
        if event_type in {
            "response.output_text.delta",
            "response.refusal.delta",
        }:
            delta = _as_str(event.get("delta"))
            if delta:
                yield _chat_chunk(model=model, delta={"content": delta})
        elif event_type in {
            "response.reasoning_summary_text.delta",
            "response.reasoning_text.delta",
        }:
            delta = _as_str(event.get("delta"))
            if delta:
                yield _chat_chunk(model=model, delta={"reasoning_content": delta})
        elif event_type == "response.completed":
            yield _chat_chunk(model=model, delta={}, finish_reason="stop")

def _messages_to_responses_input(messages: Any) -> list[dict[str, Any]]:
    if not isinstance(messages, list):
        return []
    items: list[dict[str, Any]] = []
    for message_obj in cast(list[object], messages):
        if not isinstance(message_obj, dict):
            continue
        message = cast(dict[str, Any], message_obj)
        role = _as_str(message.get("role")) or "user"
        items.append(
            {
                "role": role,
                "content": _content_to_responses_content(
                    message.get("content", ""),
                    role=role,
                ),
            }
        )
    return items


def _content_to_responses_content(content: Any, *, role: str) -> Any:
    if not isinstance(content, list):
        return content

    converted: list[Any] = []
    for part_obj in cast(list[object], content):
        if isinstance(part_obj, str):
            converted.append(
                {
                    "type": _responses_text_content_type(role),
                    "text": part_obj,
                }
            )
            continue
        if not isinstance(part_obj, dict):
            converted.append(part_obj)
            continue

        part = dict(cast(dict[str, Any], part_obj))
        part_type = _as_str(part.get("type"))
        if part_type == "text":
            part["type"] = _responses_text_content_type(role)
        elif part_type == "image_url":
            image_url = part.pop("image_url", None)
            part["type"] = "input_image"
            if isinstance(image_url, dict):
                url = cast(dict[str, Any], image_url).get("url")
                if isinstance(url, str):
                    part["image_url"] = url
            elif isinstance(image_url, str):
                part["image_url"] = image_url
        converted.append(part)
    return converted


def _responses_text_content_type(role: str) -> str:
    return "output_text" if role == "assistant" else "input_text"

def _openai_tools_to_responses(tools: Any) -> Any:
    if not isinstance(tools, list):
        return tools

    converted: list[Any] = []
    for tool_obj in cast(list[object], tools):
        if not isinstance(tool_obj, dict):
            converted.append(tool_obj)
            continue
        tool = cast(dict[str, Any], tool_obj)
        function_obj = tool.get("function")
        if tool.get("type") != "function" or not isinstance(function_obj, dict):
            converted.append(dict(tool))
            continue
        converted_tool = _openai_function_tool_to_responses_tool(
            cast(dict[str, Any], function_obj),
            fallback_strict=tool.get("strict"),
        )
        converted.append(converted_tool if converted_tool is not None else dict(tool))
    return converted


def _openai_functions_to_responses_tools(functions: Any) -> Any:
    if not isinstance(functions, list):
        return functions

    converted: list[Any] = []
    for function_obj in cast(list[object], functions):
        if not isinstance(function_obj, dict):
            converted.append(function_obj)
            continue
        function = cast(dict[str, Any], function_obj)
        converted_tool = _openai_function_tool_to_responses_tool(function)
        converted.append(converted_tool if converted_tool is not None else dict(function))
    return converted


def _openai_function_tool_to_responses_tool(
    function: dict[str, Any],
    *,
    fallback_strict: Any = None,
) -> dict[str, Any] | None:
    name = _as_str(function.get("name"))
    if not name:
        return None

    tool: dict[str, Any] = {"type": "function", "name": name}
    description = _as_str(function.get("description"))
    if description:
        tool["description"] = description
    parameters = function.get("parameters")
    tool["parameters"] = (
        parameters
        if isinstance(parameters, dict)
        else {"type": "object", "properties": {}}
    )
    strict = function.get("strict", fallback_strict)
    if isinstance(strict, bool):
        tool["strict"] = strict
    return tool


def _openai_tool_choice_to_responses(tool_choice: Any) -> Any:
    if tool_choice in (None, "none", "auto", "required"):
        return tool_choice
    if not isinstance(tool_choice, dict):
        return tool_choice

    choice = dict(cast(dict[str, Any], tool_choice))
    function_obj = choice.get("function")
    if choice.get("type") == "function" and isinstance(function_obj, dict):
        name = _as_str(cast(dict[str, Any], function_obj).get("name"))
        if name:
            return {"type": "function", "name": name}
    return choice


def _openai_function_call_to_responses_tool_choice(function_call: Any) -> Any:
    if function_call in (None, "none", "auto"):
        return function_call
    if not isinstance(function_call, dict):
        return function_call

    name = _as_str(cast(dict[str, Any], function_call).get("name"))
    if name:
        return {"type": "function", "name": name}
    return dict(cast(dict[str, Any], function_call))

def _responses_payload_to_chat_completion(
    payload: dict[str, Any],
    *,
    fallback_model: str,
) -> dict[str, Any]:
    message = _message_from_responses_output(payload.get("output"))
    return {
        "id": _as_str(payload.get("id")) or _new_id(),
        "object": "chat.completion",
        "created": _coerce_int(payload.get("created_at") or time.time()),
        "model": _as_str(payload.get("model")) or fallback_model,
        "choices": [
            {
                "index": 0,
                "message": message,
                "finish_reason": "stop" if payload.get("status") == "completed" else None,
            }
        ],
        "usage": _responses_usage_to_chat_usage(payload.get("usage")),
    }


def _message_from_responses_output(output: Any) -> dict[str, Any]:
    message: dict[str, Any] = {"role": "assistant", "content": ""}
    content_parts: list[str] = []
    reasoning_parts: list[str] = []
    tool_calls: list[dict[str, Any]] = []
    if isinstance(output, list):
        for item_obj in cast(list[object], output):
            if not isinstance(item_obj, dict):
                continue
            item = cast(dict[str, Any], item_obj)
            item_type = _as_str(item.get("type"))
            if item_type == "message":
                _collect_responses_message_content(item.get("content"), content_parts)
            elif item_type == "reasoning":
                _collect_responses_reasoning(item, reasoning_parts)
            elif item_type == "function_call":
                tool_calls.append(_responses_function_call_to_openai(item))
    message["content"] = "".join(content_parts)
    if reasoning_parts:
        message["reasoning_content"] = "".join(reasoning_parts)
    if tool_calls:
        message["tool_calls"] = tool_calls
    return message


def _collect_responses_message_content(content: Any, parts: list[str]) -> None:
    if not isinstance(content, list):
        return
    for part_obj in cast(list[object], content):
        if not isinstance(part_obj, dict):
            continue
        part = cast(dict[str, Any], part_obj)
        text = part.get("text") or part.get("refusal")
        if isinstance(text, str):
            parts.append(text)


def _collect_responses_reasoning(item: dict[str, Any], parts: list[str]) -> None:
    for key in ("summary", "content"):
        _collect_text_values(item.get(key), parts)


def _responses_function_call_to_openai(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": _as_str(item.get("call_id")) or _as_str(item.get("id")) or _new_id("call"),
        "type": "function",
        "function": {
            "name": _as_str(item.get("name")),
            "arguments": _as_str(item.get("arguments")),
        },
    }


def _responses_usage_to_chat_usage(usage: Any) -> dict[str, Any] | None:
    if not isinstance(usage, dict):
        return None
    usage_dict = cast(dict[str, Any], usage)
    prompt_tokens = usage_dict.get("input_tokens")
    completion_tokens = usage_dict.get("output_tokens")
    return {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": usage_dict.get("total_tokens"),
    }
