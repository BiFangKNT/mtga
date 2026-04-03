from __future__ import annotations

import contextlib
import copy
import json
import os
import time
import uuid
from collections.abc import Callable
from typing import Any, cast

from modules.proxy.upstream_adapter import LiteLLMUpstreamAdapter
from modules.runtime.resource_manager import ResourceManager

type LogFunc = Callable[[str], None]


class ProxyTransport:
    """代理传输层：LiteLLM 上游调用与响应归一化。"""

    def __init__(
        self,
        *,
        resource_manager: ResourceManager,
        disable_ssl_strict_mode: bool,
        log_func: LogFunc = print,
    ) -> None:
        self._resource_manager = resource_manager
        self._log = log_func
        self._adapter = LiteLLMUpstreamAdapter(
            disable_ssl_strict_mode=disable_ssl_strict_mode,
            log_func=log_func,
        )

    @property
    def adapter(self) -> LiteLLMUpstreamAdapter:
        return self._adapter

    def close(self) -> None:
        with contextlib.suppress(Exception):
            self._adapter.close()

    def prepare_sse_log_path(self) -> str:
        log_dir = os.path.join(self._resource_manager.user_data_dir, "logs", "SSE")
        os.makedirs(log_dir, exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"sse_{timestamp}_{int(time.time() * 1000)}.log"
        return os.path.join(log_dir, filename)

    def coerce_payload_dict(self, payload: Any) -> dict[str, Any] | None:
        if isinstance(payload, dict):
            return cast(dict[str, Any], payload)

        model_dump = getattr(payload, "model_dump", None)
        if callable(model_dump):
            dumped = model_dump(exclude_none=False)
            if isinstance(dumped, dict):
                return cast(dict[str, Any], dumped)

        dict_method = getattr(payload, "dict", None)
        if callable(dict_method):
            dumped = dict_method(exclude_none=False)
            if isinstance(dumped, dict):
                return cast(dict[str, Any], dumped)

        json_method = getattr(payload, "json", None)
        if callable(json_method):
            try:
                raw_json = json_method()
                dumped = json.loads(raw_json) if isinstance(raw_json, str) else None
            except Exception:  # noqa: BLE001
                dumped = None
            if isinstance(dumped, dict):
                return cast(dict[str, Any], dumped)

        return None

    def dump_payload_json(self, payload: Any) -> str:
        payload_dict = self.coerce_payload_dict(payload)
        if payload_dict is not None:
            return json.dumps(payload_dict, ensure_ascii=False)
        if isinstance(payload, str):
            return payload
        return repr(payload)

    @staticmethod
    def normalize_provider_model_name(model_name: str, *, provider: str) -> str:
        prefix = f"{provider}/"
        if model_name.startswith(prefix):
            return model_name[len(prefix) :]
        return model_name

    def normalize_chat_completion_payload(
        self,
        payload: Any,
        *,
        provider: str,
        fallback_model: str,
    ) -> dict[str, Any] | None:
        payload_dict = self.coerce_payload_dict(payload)
        if payload_dict is None:
            return None

        normalized = copy.deepcopy(payload_dict)
        model_obj = normalized.get("model")
        if isinstance(model_obj, str):
            normalized["model"] = self.normalize_provider_model_name(
                model_obj,
                provider=provider,
            )
        elif fallback_model:
            normalized["model"] = self.normalize_provider_model_name(
                fallback_model,
                provider=provider,
            )
        return normalized

    def normalize_openai_event(
        self, payload_input: Any, event_index: int, *, model_name: str, log: LogFunc
    ) -> tuple[bytes, str | None]:
        if isinstance(payload_input, str) and payload_input.strip() == "[DONE]":
            return b"data: [DONE]\n\n", None

        payload = self.coerce_payload_dict(payload_input)
        if payload is None:
            payload_str = self.dump_payload_json(payload_input)
            try:
                payload_obj = json.loads(payload_str)
            except Exception as exc:  # noqa: BLE001
                log(f"chunk#{event_index} JSON 解析失败，原样透传: {exc}")
                return f"data: {payload_str}\n\n".encode(), None
            if not isinstance(payload_obj, dict):
                return f"data: {payload_str}\n\n".encode(), None
            payload = cast(dict[str, Any], payload_obj)

        chunk_obj = copy.deepcopy(payload)
        chunk_obj["id"] = payload.get("id") or self._new_request_id("chatcmpl")
        chunk_obj["object"] = "chat.completion.chunk"
        chunk_obj["created"] = int(payload.get("created") or time.time())
        chunk_obj["model"] = model_name or payload.get("model") or ""

        choices_obj = payload.get("choices")
        normalized_choices: list[dict[str, Any]] = []
        finish_reason: str | None = None
        if isinstance(choices_obj, list):
            choices_list = cast(list[object], choices_obj)
            for choice_index, item in enumerate(choices_list):
                if not isinstance(item, dict):
                    continue
                normalized_choice = self._normalize_openai_choice_chunk(
                    cast(dict[str, Any], item),
                    event_index=event_index,
                    choice_index=choice_index,
                )
                normalized_choices.append(normalized_choice)
                if finish_reason is None:
                    finish_reason_obj = normalized_choice.get("finish_reason")
                    if isinstance(finish_reason_obj, str) and finish_reason_obj:
                        finish_reason = finish_reason_obj
        chunk_obj["choices"] = normalized_choices

        chunk_json = json.dumps(chunk_obj, ensure_ascii=False)
        return f"data: {chunk_json}\n\n".encode(), finish_reason

    @staticmethod
    def _normalize_openai_choice_chunk(
        choice: dict[str, Any],
        *,
        event_index: int,
        choice_index: int,
    ) -> dict[str, Any]:
        normalized_choice = copy.deepcopy(choice)

        raw_delta_obj = normalized_choice.get("delta")
        has_raw_delta = isinstance(raw_delta_obj, dict)
        raw_delta: dict[str, Any] = (
            cast(dict[str, Any], raw_delta_obj) if has_raw_delta else {}
        )
        message_obj = normalized_choice.pop("message", None)
        message: dict[str, Any] = (
            cast(dict[str, Any], message_obj) if isinstance(message_obj, dict) else {}
        )

        if has_raw_delta or message:
            delta = copy.deepcopy(raw_delta)
            role = delta.get("role") or message.get("role")
            if role or event_index == 1:
                delta.setdefault("role", role or "assistant")

            if "content" not in delta:
                content = message.get("content")
                if content:
                    delta["content"] = content

            for key in ("tool_calls", "function_calls", "reasoning_content"):
                if key not in delta:
                    value = message.get(key)
                    if value not in (None, []):
                        delta[key] = value

            normalized_choice["delta"] = delta

        normalized_choice.setdefault("index", choice_index)
        if "finish_reason" not in normalized_choice:
            normalized_choice["finish_reason"] = None
        return normalized_choice

    @staticmethod
    def _new_request_id(prefix: str = "resp") -> str:
        return f"{prefix}_{uuid.uuid4().hex}"

    @staticmethod
    def _split_text_chunks(text: str, *, chunk_size: int = 10) -> list[str]:
        if not text:
            return []
        return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]

    def normalize_response_payload(self, payload: Any) -> dict[str, Any] | None:
        payload_dict = self.coerce_payload_dict(payload)
        if payload_dict is None:
            return None

        normalized = copy.deepcopy(payload_dict)
        response_id = normalized.get("id")
        if not isinstance(response_id, str) or not response_id.strip():
            normalized["id"] = self._new_request_id()

        created_at = normalized.get("created_at")
        if not isinstance(created_at, int):
            created = normalized.pop("created", None)
            if isinstance(created, (int, float)):
                normalized["created_at"] = int(created)
            else:
                normalized["created_at"] = int(time.time())
        else:
            normalized.pop("created", None)

        normalized["object"] = "response"
        if not isinstance(normalized.get("status"), str):
            normalized["status"] = "completed"

        output = normalized.get("output")
        if not isinstance(output, list):
            normalized["output"] = []

        return normalized

    def serialize_response_event(
        self,
        payload_input: Any,
        *,
        log: LogFunc,
    ) -> tuple[bytes, str | None]:
        if isinstance(payload_input, str) and payload_input.strip() == "[DONE]":
            return b"data: [DONE]\n\n", None

        payload = self.coerce_payload_dict(payload_input)
        if payload is None:
            payload_str = self.dump_payload_json(payload_input)
            try:
                payload_obj = json.loads(payload_str)
            except Exception as exc:  # noqa: BLE001
                log(f"响应事件 JSON 解析失败，原样透传: {exc}")
                return f"data: {payload_str}\n\n".encode(), None
            if not isinstance(payload_obj, dict):
                return f"data: {payload_str}\n\n".encode(), None
            payload = cast(dict[str, Any], payload_obj)

        event_type_obj = payload.get("type")
        event_type = event_type_obj if isinstance(event_type_obj, str) else None
        payload_json = json.dumps(payload, ensure_ascii=False)
        if event_type:
            return f"event: {event_type}\ndata: {payload_json}\n\n".encode(), event_type
        return f"data: {payload_json}\n\n".encode(), None

    @staticmethod
    def _new_output_item_id(item_type: str | None) -> str:
        prefix = "msg"
        if item_type == "reasoning":
            prefix = "rs"
        elif item_type == "function_call":
            prefix = "fc"
        return f"{prefix}_{uuid.uuid4().hex}"

    def _build_content_part_stream_events(
        self,
        *,
        item_id: str,
        output_index: int,
        content_index: int,
        part: dict[str, Any],
    ) -> list[dict[str, Any]]:
        part_type = part.get("type")
        if part_type == "output_text":
            text_obj = part.get("text")
            text = text_obj if isinstance(text_obj, str) else ""
            annotations_obj = part.get("annotations")
            annotations: list[Any] = (
                cast(list[Any], annotations_obj) if isinstance(annotations_obj, list) else []
            )
            events: list[dict[str, Any]] = [
                {
                    "type": "response.content_part.added",
                    "item_id": item_id,
                    "output_index": output_index,
                    "content_index": content_index,
                    "part": {
                        "type": "output_text",
                        "text": "",
                        "annotations": annotations,
                    },
                }
            ]
            for chunk in self._split_text_chunks(text):
                events.append(
                    {
                        "type": "response.output_text.delta",
                        "item_id": item_id,
                        "output_index": output_index,
                        "content_index": content_index,
                        "delta": chunk,
                    }
                )
            events.append(
                {
                    "type": "response.output_text.done",
                    "item_id": item_id,
                    "output_index": output_index,
                    "content_index": content_index,
                    "text": text,
                }
            )
            done_part = copy.deepcopy(part)
            done_part["annotations"] = annotations
            events.append(
                {
                    "type": "response.content_part.done",
                    "item_id": item_id,
                    "output_index": output_index,
                    "content_index": content_index,
                    "part": done_part,
                }
            )
            return events

        if part_type == "refusal":
            refusal_obj = part.get("refusal")
            refusal = refusal_obj if isinstance(refusal_obj, str) else ""
            events = [
                {
                    "type": "response.content_part.added",
                    "item_id": item_id,
                    "output_index": output_index,
                    "content_index": content_index,
                    "part": {"type": "refusal", "refusal": ""},
                }
            ]
            for chunk in self._split_text_chunks(refusal):
                events.append(
                    {
                        "type": "response.refusal.delta",
                        "item_id": item_id,
                        "output_index": output_index,
                        "content_index": content_index,
                        "delta": chunk,
                    }
                )
            events.append(
                {
                    "type": "response.refusal.done",
                    "item_id": item_id,
                    "output_index": output_index,
                    "content_index": content_index,
                    "refusal": refusal,
                }
            )
            events.append(
                {
                    "type": "response.content_part.done",
                    "item_id": item_id,
                    "output_index": output_index,
                    "content_index": content_index,
                    "part": {"type": "refusal", "refusal": refusal},
                }
            )
            return events

        return [
            {
                "type": "response.content_part.added",
                "item_id": item_id,
                "output_index": output_index,
                "content_index": content_index,
                "part": copy.deepcopy(part),
            },
            {
                "type": "response.content_part.done",
                "item_id": item_id,
                "output_index": output_index,
                "content_index": content_index,
                "part": copy.deepcopy(part),
            },
        ]

    def _build_output_item_stream_events(
        self,
        *,
        item: dict[str, Any],
        output_index: int,
        sequence_number: int,
    ) -> tuple[list[dict[str, Any]], int]:
        item_copy = copy.deepcopy(item)
        item_type_obj = item_copy.get("type")
        item_type = item_type_obj if isinstance(item_type_obj, str) else None
        item_id_obj = item_copy.get("id")
        item_id = (
            item_id_obj
            if isinstance(item_id_obj, str) and item_id_obj.strip()
            else self._new_output_item_id(item_type)
        )
        item_copy["id"] = item_id

        added_item = copy.deepcopy(item_copy)
        if item_type == "message":
            added_item["status"] = "in_progress"
            added_item["content"] = []
        elif item_type == "reasoning" and not isinstance(added_item.get("status"), str):
            added_item["status"] = "in_progress"

        events: list[dict[str, Any]] = [
            {
                "type": "response.output_item.added",
                "output_index": output_index,
                "item": added_item,
            }
        ]

        content_obj = item_copy.get("content")
        if item_type == "message" and isinstance(content_obj, list):
            content_list = cast(list[object], content_obj)
            for content_index, part_obj in enumerate(content_list):
                if not isinstance(part_obj, dict):
                    continue
                events.extend(
                    self._build_content_part_stream_events(
                        item_id=item_id,
                        output_index=output_index,
                        content_index=content_index,
                        part=cast(dict[str, Any], part_obj),
                    )
                )

        next_sequence_number = sequence_number + 1
        completed_item = copy.deepcopy(item_copy)
        if item_type == "message" and not isinstance(completed_item.get("status"), str):
            completed_item["status"] = "completed"
        events.append(
            {
                "type": "response.output_item.done",
                "output_index": output_index,
                "sequence_number": next_sequence_number,
                "item": completed_item,
            }
        )
        return events, next_sequence_number

    def build_response_stream_events(
        self,
        response_payload: dict[str, Any],
    ) -> list[dict[str, Any]]:
        normalized = self.normalize_response_payload(response_payload)
        if normalized is None:
            return []

        in_progress_response = copy.deepcopy(normalized)
        in_progress_response["status"] = "in_progress"
        in_progress_response["output"] = []

        events: list[dict[str, Any]] = [
            {
                "type": "response.created",
                "response": copy.deepcopy(in_progress_response),
            },
            {
                "type": "response.in_progress",
                "response": copy.deepcopy(in_progress_response),
            },
        ]

        output_obj = normalized.get("output")
        output_items = cast(list[object], output_obj) if isinstance(output_obj, list) else []
        sequence_number = 0
        for output_index, item_obj in enumerate(output_items):
            if not isinstance(item_obj, dict):
                continue
            item_events, sequence_number = self._build_output_item_stream_events(
                item=cast(dict[str, Any], item_obj),
                output_index=output_index,
                sequence_number=sequence_number,
            )
            events.extend(item_events)

        events.append({"type": "response.completed", "response": normalized})
        return events

    def build_chat_completion_stream_chunks(
        self,
        response_payload: dict[str, Any],
    ) -> list[dict[str, Any]]:
        response = copy.deepcopy(response_payload)
        choices_obj = response.get("choices")
        if not isinstance(choices_obj, list) or not choices_obj:
            return []
        choices = cast(list[object], choices_obj)

        simulated_choices: list[dict[str, Any]] = []
        for fallback_index, choice_obj in enumerate(choices):
            if not isinstance(choice_obj, dict):
                continue
            choice = cast(dict[str, Any], choice_obj)
            choice_index_obj = choice.get("index")
            choice_index = (
                choice_index_obj if isinstance(choice_index_obj, int) else fallback_index
            )
            message_obj = choice.get("message")
            message = (
                cast(dict[str, Any], message_obj) if isinstance(message_obj, dict) else {}
            )
            finish_reason_obj = choice.get("finish_reason")
            finish_reason = (
                finish_reason_obj if isinstance(finish_reason_obj, str) else "stop"
            )
            simulated_choices.append(
                {
                    "index": choice_index,
                    "message": message,
                    "finish_reason": finish_reason,
                }
            )
        if not simulated_choices:
            return []

        model = response.get("model")
        model_name = model if isinstance(model, str) else ""
        created = response.get("created")
        created_at = created if isinstance(created, int) else int(time.time())
        response_id = response.get("id")
        chunk_id = (
            response_id
            if isinstance(response_id, str) and response_id
            else self._new_request_id("chatcmpl")
        )

        base_chunk = {
            "id": chunk_id,
            "object": "chat.completion.chunk",
            "created": created_at,
            "model": model_name,
        }

        chunks: list[dict[str, Any]] = [
            {
                **base_chunk,
                "choices": [
                    {
                        "index": cast(int, choice["index"]),
                        "delta": {
                            "role": (
                                choice["message"].get("role")
                                if isinstance(choice["message"].get("role"), str)
                                else "assistant"
                            )
                        },
                        "finish_reason": None,
                    }
                    for choice in simulated_choices
                ],
            }
        ]

        for choice in simulated_choices:
            choice_index = cast(int, choice["index"])
            message = cast(dict[str, Any], choice["message"])

            reasoning_obj = message.get("reasoning_content")
            reasoning_content = reasoning_obj if isinstance(reasoning_obj, str) else ""
            for chunk_text in self._split_text_chunks(reasoning_content):
                chunks.append(
                    {
                        **base_chunk,
                        "choices": [
                            {
                                "index": choice_index,
                                "delta": {"reasoning_content": chunk_text},
                                "finish_reason": None,
                            }
                        ],
                    }
                )

            content_obj = message.get("content")
            content = content_obj if isinstance(content_obj, str) else ""
            for chunk_text in self._split_text_chunks(content):
                chunks.append(
                    {
                        **base_chunk,
                        "choices": [
                            {
                                "index": choice_index,
                                "delta": {"content": chunk_text},
                                "finish_reason": None,
                            }
                        ],
                    }
                )

            tool_calls_obj = message.get("tool_calls")
            if isinstance(tool_calls_obj, list) and tool_calls_obj:
                tool_calls: list[Any] = []
                for tool_call_index, tool_call_obj in enumerate(cast(list[Any], tool_calls_obj)):
                    if isinstance(tool_call_obj, dict):
                        tool_call = copy.deepcopy(cast(dict[str, Any], tool_call_obj))
                        tool_call.setdefault("index", tool_call_index)
                        tool_calls.append(tool_call)
                    else:
                        tool_calls.append(tool_call_obj)
                chunks.append(
                    {
                        **base_chunk,
                        "choices": [
                            {
                                "index": choice_index,
                                "delta": {"tool_calls": tool_calls},
                                "finish_reason": None,
                            }
                        ],
                    }
                )

        chunks.append(
            {
                **base_chunk,
                "choices": [
                    {
                        "index": cast(int, choice["index"]),
                        "delta": {},
                        "finish_reason": cast(str, choice["finish_reason"]),
                    }
                    for choice in simulated_choices
                ],
            }
        )
        return chunks


__all__ = ["ProxyTransport"]
