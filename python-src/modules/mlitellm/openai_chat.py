# pyright: reportPrivateUsage=false, reportUnusedFunction=false
from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from .common import (
    _as_str,
    _base_url,
    _headers,
    _join_url,
    _json_request,
    _request_body_from_kwargs,
    _stream_json_request,
    _strip_model_prefix,
)


def _openai_chat_completion(kwargs: dict[str, Any]) -> dict[str, Any] | Iterator[Any]:
    model = _strip_model_prefix(_as_str(kwargs.get("model")), "openai")
    body = _request_body_from_kwargs(kwargs, model=model)
    url = _join_url(_base_url(kwargs), "chat/completions")
    headers = _headers(
        api_key=_as_str(kwargs.get("api_key")),
        auth_header="Authorization",
        auth_value_prefix="Bearer ",
        extra_headers=kwargs.get("extra_headers"),
    )
    if bool(body.get("stream")):
        return _stream_json_request(
            "POST",
            url,
            body=body,
            headers=headers,
            kwargs=kwargs,
            model=model,
            provider="openai",
        )
    return _json_request(
        "POST",
        url,
        body=body,
        headers=headers,
        kwargs=kwargs,
        model=model,
        provider="openai",
    )
