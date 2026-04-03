from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any, cast

INVALID_REQUEST_STATUS_CODE = 400
LITELLM_UNSUPPORTED_PARAMS_PATTERN = re.compile(
    r"\bdoes\s+not\s+support\s+parameters?\s*:\s*\[([^\]]*)\]",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class ParamSelfHealSignal:
    message: str | None
    param: str | None


def extract_param_self_heal_signal(exc: Exception) -> ParamSelfHealSignal | None:
    upstream_signal = _extract_upstream_invalid_request_signal(exc)
    if upstream_signal is not None:
        return upstream_signal
    return _extract_litellm_validation_signal(exc)


def extract_litellm_unsupported_params_from_message(message: str) -> tuple[str, ...]:
    listed_params: list[str] = []
    for raw_list in LITELLM_UNSUPPORTED_PARAMS_PATTERN.findall(message):
        for raw_item in raw_list.split(","):
            normalized_item = raw_item.strip().strip("\"'`")
            if normalized_item:
                listed_params.append(normalized_item)
    return tuple(dict.fromkeys(listed_params))


def _extract_upstream_invalid_request_signal(
    exc: Exception,
) -> ParamSelfHealSignal | None:
    if _extract_status_code(exc) != INVALID_REQUEST_STATUS_CODE:
        return None

    error_payload = _extract_upstream_error_payload(exc)
    error_type = None
    message = None
    param = None
    if error_payload is not None:
        error_type_obj = error_payload.get("type")
        if isinstance(error_type_obj, str):
            error_type = error_type_obj.strip()
        message_obj = error_payload.get("message")
        if isinstance(message_obj, str) and message_obj.strip():
            message = message_obj.strip()
        param_obj = error_payload.get("param")
        if isinstance(param_obj, str) and param_obj.strip():
            param = param_obj.strip()

    if error_type and error_type != "invalid_request_error":
        return None

    if message is None:
        normalized_message = _unwrap_exception_message(str(exc))
        message = normalized_message if normalized_message else None

    if message is None and param is None:
        return None
    return ParamSelfHealSignal(message=message, param=param)


def _extract_litellm_validation_signal(
    exc: Exception,
) -> ParamSelfHealSignal | None:
    normalized_message = _unwrap_exception_message(str(exc))
    if not normalized_message:
        return None

    unsupported_params = extract_litellm_unsupported_params_from_message(
        normalized_message
    )
    if not unsupported_params:
        return None

    return ParamSelfHealSignal(
        message=normalized_message,
        param=unsupported_params[0],
    )


def _extract_status_code(exc: Exception) -> int | None:
    status_code_obj = getattr(exc, "status_code", None)
    if isinstance(status_code_obj, int):
        return status_code_obj

    response = getattr(exc, "response", None)
    response_status_code = getattr(response, "status_code", None)
    if isinstance(response_status_code, int):
        return response_status_code
    return None


def _extract_upstream_error_payload(exc: Exception) -> dict[str, Any] | None:
    raw_response_text = _extract_raw_response_text(exc)
    payload: dict[str, Any] | list[Any] | None = (
        _parse_json_payload_text(raw_response_text)
        if raw_response_text is not None
        else _extract_fallback_response_body(exc)
    )
    if not isinstance(payload, dict):
        return None

    error_obj = payload.get("error")
    if isinstance(error_obj, dict):
        return dict(cast(dict[str, Any], error_obj))
    if _looks_like_openai_error_object(payload):
        return dict(payload)
    return None


def _parse_json_payload_text(text: str) -> dict[str, Any] | list[Any] | None:
    stripped = text.strip()
    if not stripped:
        return None
    try:
        parsed = json.loads(stripped)
    except json.JSONDecodeError:
        return None
    payload_dict = _coerce_mapping_payload(parsed)
    if payload_dict is not None:
        return payload_dict
    if isinstance(parsed, list):
        return list(cast(list[Any], parsed))
    return None


def _coerce_mapping_payload(payload: Any) -> dict[str, Any] | None:
    if isinstance(payload, dict):
        return cast(dict[str, Any], payload)
    return None


def _coerce_json_payload(payload: Any) -> dict[str, Any] | list[Any] | None:
    payload_dict = _coerce_mapping_payload(payload)
    if payload_dict is not None:
        return payload_dict
    if isinstance(payload, list):
        return list(cast(list[Any], payload))
    return None


def _unwrap_exception_message(message: str) -> str:
    normalized = message.strip()
    if normalized.startswith("litellm.") and ": " in normalized:
        normalized = normalized.split(": ", 1)[1].strip()
    if normalized.startswith("OpenAIException - "):
        normalized = normalized.removeprefix("OpenAIException - ").strip()
    return normalized


def _extract_raw_response_text(exc: Exception) -> str | None:
    response = getattr(exc, "response", None)
    response_text = getattr(response, "text", None)
    if isinstance(response_text, str):
        stripped = response_text.strip()
        if stripped:
            return stripped
    return None


def _looks_like_openai_error_object(payload: dict[str, Any]) -> bool:
    payload_keys = set(payload)
    if "error" in payload_keys:
        return False
    if "message" not in payload_keys or "type" not in payload_keys:
        return False
    return payload_keys.issubset({"message", "type", "code", "param"})


def _extract_fallback_response_body(exc: Exception) -> dict[str, Any] | list[Any] | None:
    body = getattr(exc, "body", None)
    if isinstance(body, str):
        return _parse_json_payload_text(body)

    return _coerce_json_payload(body)


__all__ = [
    "ParamSelfHealSignal",
    "extract_litellm_unsupported_params_from_message",
    "extract_param_self_heal_signal",
]
