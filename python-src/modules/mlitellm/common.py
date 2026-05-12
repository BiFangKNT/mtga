# pyright: reportUnusedFunction=false
from __future__ import annotations

import contextlib
import copy
import json
import ssl
import sys
import time
import uuid
from collections.abc import Iterator
from typing import Any, NoReturn, cast

import httpx

from .exceptions import (
    APIConnectionError,
    APIError,
    AuthenticationError,
    BadRequestError,
    NotFoundError,
    RateLimitError,
)

HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_FORBIDDEN = 403
HTTP_NOT_FOUND = 404
HTTP_RATE_LIMITED = 429

_META_KWARGS: frozenset[str] = frozenset(
    {
        "api_base",
        "api_key",
        "base_url",
        "custom_llm_provider",
        "extra_headers",
        "max_retries",
        "num_retries",
        "ssl_verify",
        "timeout",
    }
)
_LOCAL_ONLY_KWARGS: frozenset[str] = frozenset(
    {
        "allowed_openai_params",
        "prompt_cache_key",
        "request_body_patch",
    }
)
ssl_verify: bool | str = True


class _PatchContext:
    def __init__(self, *, index: int, model: str, provider: str) -> None:
        self.index = index
        self.model = model
        self.provider = provider

    def fail(self, message: str) -> NoReturn:
        _raise_patch_error(message, model=self.model, provider=self.provider)


def _global_ssl_verify() -> bool | str:
    root_module = sys.modules.get("modules.mlitellm")
    if root_module is None:
        return ssl_verify
    verify = getattr(root_module, "ssl_verify", ssl_verify)
    return verify if isinstance(verify, (bool, str)) else ssl_verify


def _json_request(  # noqa: PLR0913
    method: str,
    url: str,
    *,
    body: dict[str, Any],
    headers: dict[str, str],
    kwargs: dict[str, Any],
    model: str,
    provider: str,
) -> dict[str, Any]:
    try:
        response = httpx.request(
            method,
            url,
            json=body,
            headers=headers,
            timeout=_timeout(kwargs),
            verify=_verify(kwargs),
        )
    except httpx.RequestError as exc:
        raise APIConnectionError(
            str(exc),
            llm_provider=provider,
            model=model,
            request=exc.request,
        ) from exc
    _raise_for_response(response, model=model, provider=provider)
    parsed = response.json()
    if isinstance(parsed, dict):
        return cast(dict[str, Any], parsed)
    return {"data": parsed}


class _SSEJsonStream:
    def __init__(  # noqa: PLR0913
        self,
        method: str,
        url: str,
        *,
        body: dict[str, Any],
        headers: dict[str, str],
        kwargs: dict[str, Any],
        model: str,
        provider: str,
    ) -> None:
        self._model = model
        self._provider = provider
        self._context: Any | None = httpx.stream(
            method,
            url,
            json=body,
            headers=headers,
            timeout=_timeout(kwargs),
            verify=_verify(kwargs),
        )
        self._response: httpx.Response | None = None
        self._lines: Iterator[str] | None = None
        self._data_lines: list[str] = []
        self._closed = False
        try:
            response = self._context.__enter__()
            self._response = response
            _raise_for_response(response, model=model, provider=provider)
            self._lines = iter(response.iter_lines())
        except httpx.RequestError as exc:
            self.close()
            raise APIConnectionError(
                str(exc),
                llm_provider=provider,
                model=model,
                request=exc.request,
            ) from exc
        except Exception:
            self.close()
            raise

    def __iter__(self) -> _SSEJsonStream:
        return self

    def __next__(self) -> dict[str, Any] | str:
        if self._lines is None:
            raise StopIteration
        try:
            for raw_line in self._lines:
                line = raw_line.strip()
                if not line:
                    if self._data_lines:
                        data = "\n".join(self._data_lines)
                        self._data_lines = []
                        return _parse_sse_data(data)
                    continue
                if line.startswith("data:"):
                    self._data_lines.append(line.removeprefix("data:").strip())
            if self._data_lines:
                data = "\n".join(self._data_lines)
                self._data_lines = []
                return _parse_sse_data(data)
        except httpx.RequestError as exc:
            self.close()
            raise APIConnectionError(
                str(exc),
                llm_provider=self._provider,
                model=self._model,
                request=exc.request,
            ) from exc
        self.close()
        raise StopIteration

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        if self._context is not None:
            self._context.__exit__(None, None, None)
            self._context = None


def _stream_json_request(  # noqa: PLR0913
    method: str,
    url: str,
    *,
    body: dict[str, Any],
    headers: dict[str, str],
    kwargs: dict[str, Any],
    model: str,
    provider: str,
) -> Iterator[Any]:
    return _SSEJsonStream(
        method,
        url,
        body=body,
        headers=headers,
        kwargs=kwargs,
        model=model,
        provider=provider,
    )


class _ClosableIterator:
    def __init__(self, source: Iterator[Any], iterator: Iterator[Any]) -> None:
        self._source = source
        self._iterator = iterator
        self._closed = False

    def __iter__(self) -> _ClosableIterator:
        return self

    def __next__(self) -> Any:
        try:
            return next(self._iterator)
        except StopIteration:
            self.close()
            raise
        except Exception:
            self.close()
            raise

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        iterator_close = getattr(self._iterator, "close", None)
        if callable(iterator_close):
            with contextlib.suppress(Exception):
                iterator_close()
        source_close = getattr(self._source, "close", None)
        if callable(source_close):
            with contextlib.suppress(Exception):
                source_close()


def _raise_for_response(response: httpx.Response, *, model: str, provider: str) -> None:
    if not response.is_error:
        return
    _ensure_response_content_loaded(response)
    body = _safe_response_json(response)
    message = (
        _extract_error_message(body)
        or _safe_response_text(response).strip()
        or response.reason_phrase
    )
    status_code = response.status_code
    error_kwargs: dict[str, Any] = {
        "model": model,
        "llm_provider": provider,
        "response": response,
        "body": body,
    }
    if status_code == HTTP_BAD_REQUEST:
        raise BadRequestError(message, **error_kwargs)
    if status_code in {HTTP_UNAUTHORIZED, HTTP_FORBIDDEN}:
        raise AuthenticationError(message, **error_kwargs)
    if status_code == HTTP_NOT_FOUND:
        raise NotFoundError(message, **error_kwargs)
    if status_code == HTTP_RATE_LIMITED:
        raise RateLimitError(message, **error_kwargs)
    raise APIError(message, **error_kwargs)


def _request_body_from_kwargs(kwargs: dict[str, Any], *, model: str) -> dict[str, Any]:
    body: dict[str, Any] = {"model": model}
    for key, value in kwargs.items():
        if key in _META_KWARGS or key in _LOCAL_ONLY_KWARGS or key == "model":
            continue
        if key == "extra_body":
            continue
        if value is not None:
            body[key] = value
    extra_body = kwargs.get("extra_body")
    if isinstance(extra_body, dict):
        body.update(cast(dict[str, Any], extra_body))
    return body


def _apply_request_body_patch(
    body: dict[str, Any],
    kwargs: dict[str, Any],
    *,
    model: str,
    provider: str,
) -> dict[str, Any]:
    patch_obj = kwargs.get("request_body_patch")
    if patch_obj in (None, "", ()):
        return body
    if not isinstance(patch_obj, list):
        _raise_patch_error(
            "request_body_patch must be a JSON Patch operation list",
            model=model,
            provider=provider,
        )

    patched_body = body
    for index, operation_obj in enumerate(cast(list[Any], patch_obj), start=1):
        context = _PatchContext(index=index, model=model, provider=provider)
        if not isinstance(operation_obj, dict):
            context.fail(f"request_body_patch[{index}] must be an object")
        operation = cast(dict[str, Any], operation_obj)
        _apply_request_body_patch_operation(patched_body, operation, context)
    return patched_body


def _apply_request_body_patch_operation(
    document: dict[str, Any],
    operation: dict[str, Any],
    context: _PatchContext,
) -> None:
    op = _as_str(operation.get("op")).strip()
    path = operation.get("path")
    if not isinstance(path, str):
        context.fail(f"request_body_patch[{context.index}].path must be a string")
    _ensure_patch_path_allowed(path, context)

    if op in {"add", "replace"}:
        _apply_value_patch_operation(document, op, path, operation, context)
        return
    if op == "remove":
        _json_pointer_remove(document, path, context)
        return
    if op == "copy":
        _apply_copy_patch_operation(document, path, operation, context)
        return
    if op == "move":
        _apply_move_patch_operation(document, path, operation, context)
        return
    if op == "test":
        _apply_test_patch_operation(document, path, operation, context)
        return
    context.fail(
        f"request_body_patch[{context.index}].op is unsupported: {op or '<empty>'}"
    )


def _apply_value_patch_operation(
    document: dict[str, Any],
    op: str,
    path: str,
    operation: dict[str, Any],
    context: _PatchContext,
) -> None:
    if "value" not in operation:
        context.fail(f"request_body_patch[{context.index}].value is required for {op}")
    if op == "add":
        _json_pointer_add(document, path, operation["value"], context)
        return
    _json_pointer_replace(document, path, operation["value"], context)


def _apply_copy_patch_operation(
    document: dict[str, Any],
    path: str,
    operation: dict[str, Any],
    context: _PatchContext,
) -> None:
    from_path = _operation_from_path(operation, context)
    value = copy.deepcopy(_json_pointer_get(document, from_path, context))
    _json_pointer_add(document, path, value, context)


def _apply_move_patch_operation(
    document: dict[str, Any],
    path: str,
    operation: dict[str, Any],
    context: _PatchContext,
) -> None:
    from_path = _operation_from_path(operation, context)
    from_tokens = _decode_json_pointer(from_path, context)
    path_tokens = _decode_json_pointer(path, context)
    if (
        len(path_tokens) > len(from_tokens)
        and path_tokens[: len(from_tokens)] == from_tokens
    ):
        context.fail(
            f"request_body_patch[{context.index}] cannot move a value into its own child"
        )
    value = _json_pointer_get(document, from_path, context)
    _json_pointer_remove(document, from_path, context)
    _json_pointer_add(document, path, value, context)


def _apply_test_patch_operation(
    document: dict[str, Any],
    path: str,
    operation: dict[str, Any],
    context: _PatchContext,
) -> None:
    if "value" not in operation:
        context.fail(f"request_body_patch[{context.index}].value is required for test")
    current_value = _json_pointer_get(document, path, context)
    if current_value != operation["value"]:
        context.fail(f"request_body_patch[{context.index}] test operation failed")


def _operation_from_path(
    operation: dict[str, Any],
    context: _PatchContext,
) -> str:
    from_path = operation.get("from")
    if not isinstance(from_path, str):
        context.fail(f"request_body_patch[{context.index}].from must be a string")
    _ensure_patch_path_allowed(from_path, context)
    return from_path


def _ensure_patch_path_allowed(
    path: str,
    context: _PatchContext,
) -> None:
    if path in {"", "/stream"} or path.startswith("/stream/"):
        context.fail(
            f"request_body_patch[{context.index}] cannot patch stream or the document root"
        )


def _decode_json_pointer(
    path: str,
    context: _PatchContext,
) -> tuple[str, ...]:
    if not path.startswith("/"):
        context.fail(f"request_body_patch[{context.index}].path must be a JSON Pointer")
    decoded: list[str] = []
    for token in path.split("/")[1:]:
        decoded.append(_decode_json_pointer_token(token, context))
    return tuple(decoded)


def _decode_json_pointer_token(
    token: str,
    context: _PatchContext,
) -> str:
    chars: list[str] = []
    position = 0
    while position < len(token):
        char = token[position]
        if char != "~":
            chars.append(char)
            position += 1
            continue
        if position + 1 >= len(token):
            context.fail(
                f"request_body_patch[{context.index}].path has an invalid escape"
            )
        escape = token[position + 1]
        if escape == "0":
            chars.append("~")
        elif escape == "1":
            chars.append("/")
        else:
            context.fail(
                f"request_body_patch[{context.index}].path has an invalid escape"
            )
        position += 2
    return "".join(chars)


def _json_pointer_get(
    document: Any,
    path: str,
    context: _PatchContext,
) -> Any:
    current = document
    for token in _decode_json_pointer(path, context):
        current = _json_pointer_child(current, token, context)
    return current


def _json_pointer_parent(
    document: dict[str, Any],
    path: str,
    context: _PatchContext,
) -> tuple[Any, str]:
    tokens = _decode_json_pointer(path, context)
    if not tokens:
        context.fail(f"request_body_patch[{context.index}] cannot patch the document root")
    current: Any = document
    for token in tokens[:-1]:
        current = _json_pointer_child(current, token, context)
    return current, tokens[-1]


def _json_pointer_child(
    container: Any,
    token: str,
    context: _PatchContext,
) -> Any:
    if isinstance(container, dict):
        container_dict = cast(dict[str, Any], container)
        if token in container_dict:
            return container_dict[token]
    elif isinstance(container, list):
        container_list = cast(list[Any], container)
        token_index = _json_pointer_array_index(
            token,
            max_index=len(container_list) - 1,
            allow_end=False,
            context=context,
        )
        return container_list[token_index]
    context.fail(f"request_body_patch[{context.index}] points to a missing path")


def _json_pointer_add(
    document: dict[str, Any],
    path: str,
    value: Any,
    context: _PatchContext,
) -> None:
    parent, token = _json_pointer_parent(document, path, context)
    next_value = copy.deepcopy(value)
    if isinstance(parent, dict):
        cast(dict[str, Any], parent)[token] = next_value
        return
    if isinstance(parent, list):
        parent_list = cast(list[Any], parent)
        if token == "-":
            parent_list.append(next_value)
            return
        token_index = _json_pointer_array_index(
            token,
            max_index=len(parent_list),
            allow_end=True,
            context=context,
        )
        parent_list.insert(token_index, next_value)
        return
    context.fail(f"request_body_patch[{context.index}] cannot add to this path")


def _json_pointer_replace(
    document: dict[str, Any],
    path: str,
    value: Any,
    context: _PatchContext,
) -> None:
    parent, token = _json_pointer_parent(document, path, context)
    next_value = copy.deepcopy(value)
    if isinstance(parent, dict):
        parent_dict = cast(dict[str, Any], parent)
        if token in parent_dict:
            parent_dict[token] = next_value
            return
    elif isinstance(parent, list):
        parent_list = cast(list[Any], parent)
        token_index = _json_pointer_array_index(
            token,
            max_index=len(parent_list) - 1,
            allow_end=False,
            context=context,
        )
        parent_list[token_index] = next_value
        return
    context.fail(f"request_body_patch[{context.index}] cannot replace a missing path")


def _json_pointer_remove(
    document: dict[str, Any],
    path: str,
    context: _PatchContext,
) -> None:
    parent, token = _json_pointer_parent(document, path, context)
    if isinstance(parent, dict):
        parent_dict = cast(dict[str, Any], parent)
        if token in parent_dict:
            del parent_dict[token]
            return
    elif isinstance(parent, list):
        parent_list = cast(list[Any], parent)
        token_index = _json_pointer_array_index(
            token,
            max_index=len(parent_list) - 1,
            allow_end=False,
            context=context,
        )
        del parent_list[token_index]
        return
    context.fail(f"request_body_patch[{context.index}] cannot remove a missing path")


def _json_pointer_array_index(
    token: str,
    *,
    max_index: int,
    allow_end: bool,
    context: _PatchContext,
) -> int:
    if token == "-":
        if allow_end:
            return max_index
        context.fail(f"request_body_patch[{context.index}] cannot use '-' here")
    try:
        token_index = int(token)
    except ValueError:
        context.fail(
            f"request_body_patch[{context.index}] has an invalid array index"
        )
    if str(token_index) != token or token_index < 0 or token_index > max_index:
        context.fail(
            f"request_body_patch[{context.index}] array index is out of range"
        )
    return token_index


def _raise_patch_error(message: str, *, model: str, provider: str) -> NoReturn:
    raise BadRequestError(
        message,
        model=model,
        llm_provider=provider,
        body={"error": {"message": message, "type": "invalid_request_error"}},
        status_code=HTTP_BAD_REQUEST,
    )


def _parse_sse_data(data: str) -> dict[str, Any] | str:
    if data == "[DONE]":
        return data
    parsed = json.loads(data)
    if isinstance(parsed, dict):
        return cast(dict[str, Any], parsed)
    return {"data": parsed}

def _content_to_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for part_obj in cast(list[object], content):
            if isinstance(part_obj, str):
                parts.append(part_obj)
            elif isinstance(part_obj, dict):
                part = cast(dict[str, Any], part_obj)
                text = part.get("text")
                if isinstance(text, str):
                    parts.append(text)
        return "\n".join(parts)
    return "" if content is None else str(content)


def _collect_text_values(value: Any, parts: list[str]) -> None:
    if isinstance(value, str):
        parts.append(value)
    elif isinstance(value, list):
        for item in cast(list[Any], value):
            _collect_text_values(item, parts)
    elif isinstance(value, dict):
        value_dict = cast(dict[str, Any], value)
        for key in (
            "text",
            "content",
            "summary",
            "summary_text",
            "reasoning_text",
            "thinking",
        ):
            _collect_text_values(value_dict.get(key), parts)


def _chat_chunk(
    *,
    model: str,
    delta: dict[str, Any],
    finish_reason: str | None = None,
) -> dict[str, Any]:
    return {
        "id": _new_id("chatcmpl"),
        "object": "chat.completion.chunk",
        "created": _coerce_int(time.time()),
        "model": model,
        "choices": [{"index": 0, "delta": delta, "finish_reason": finish_reason}],
    }


def _headers(
    *,
    api_key: str,
    auth_header: str,
    auth_value_prefix: str,
    extra_headers: Any,
    defaults: dict[str, str] | None = None,
) -> dict[str, str]:
    headers: dict[str, str] = {"Content-Type": "application/json"}
    if defaults:
        headers.update(defaults)
    if api_key:
        headers[auth_header] = f"{auth_value_prefix}{api_key}"
    if isinstance(extra_headers, dict):
        for key, value in cast(dict[Any, Any], extra_headers).items():
            if isinstance(key, str) and value is not None:
                headers[key] = str(value)
    return headers


def _base_url(kwargs: dict[str, Any]) -> str:
    base_url = _as_str(kwargs.get("base_url") or kwargs.get("api_base")).strip()
    if not base_url:
        return "https://api.openai.com/v1"
    return base_url


def _join_url(base_url: str, suffix: str) -> str:
    clean_suffix = suffix.lstrip("/")
    if "?" in clean_suffix:
        path, query = clean_suffix.split("?", 1)
        return f"{base_url.rstrip('/')}/{path}?{query}"
    return f"{base_url.rstrip('/')}/{clean_suffix}"


def _verify(kwargs: dict[str, Any]) -> bool | str | ssl.SSLContext:
    verify = kwargs.get("ssl_verify", _global_ssl_verify())
    if isinstance(verify, (bool, str, ssl.SSLContext)):
        return verify
    return _global_ssl_verify()


def _timeout(kwargs: dict[str, Any]) -> float | httpx.Timeout | None:
    timeout = kwargs.get("timeout")
    if isinstance(timeout, (int, float)):
        return float(timeout)
    if isinstance(timeout, httpx.Timeout):
        return timeout
    return None


def _safe_response_json(response: httpx.Response) -> Any | None:
    _ensure_response_content_loaded(response)
    try:
        return response.json()
    except Exception:  # noqa: BLE001
        return None


def _safe_response_text(response: httpx.Response) -> str:
    _ensure_response_content_loaded(response)
    try:
        return response.text
    except Exception:  # noqa: BLE001
        return ""


def _ensure_response_content_loaded(response: httpx.Response) -> None:
    with contextlib.suppress(Exception):
        response.read()


def _extract_error_message(body: Any | None) -> str:
    if isinstance(body, dict):
        body_dict = cast(dict[str, Any], body)
        error = body_dict.get("error")
        if isinstance(error, dict):
            message = cast(dict[str, Any], error).get("message")
            if isinstance(message, str):
                return message
        message = body_dict.get("message")
        if isinstance(message, str):
            return message
    return ""


def _strip_model_prefix(model: str, provider: str) -> str:
    prefix = f"{provider}/"
    if model.startswith(prefix):
        return model[len(prefix) :]
    return model


def _as_str(value: Any) -> str:
    return value if isinstance(value, str) else ""


def _coerce_int(value: Any) -> int:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, (int, float)):
        return int(value)
    return 0


def _new_id(prefix: str = "resp") -> str:
    return f"{prefix}_{uuid.uuid4().hex}"


def _normalize_finish_reason(value: Any) -> str | None:
    reason = _as_str(value)
    if not reason:
        return None
    normalized = reason.lower()
    if normalized in {"end_turn", "stop", "stop_sequence"}:
        return "stop"
    if normalized in {"max_tokens", "length"}:
        return "length"
    if normalized in {"tool_use", "tool_calls"}:
        return "tool_calls"
    if normalized in {"safety", "content_filter", "recitation"}:
        return "content_filter"
    return normalized
