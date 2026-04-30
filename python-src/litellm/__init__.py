from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import httpx as httpx

from litellm.anthropic import _anthropic_completion
from litellm.exceptions import (
    APIConnectionError,
    APIError,
    AuthenticationError,
    BadRequestError,
    NotFoundError,
    RateLimitError,
)
from litellm.gemini import _gemini_completion
from litellm.openai_chat import _openai_chat_completion
from litellm.openai_responses import _openai_responses_completion

ssl_verify: bool | str = True
drop_params = False
__version__ = "mtga-slim"

_OPENAI_CHAT_PARAMS: tuple[str, ...] = (
    "audio",
    "frequency_penalty",
    "function_call",
    "functions",
    "logit_bias",
    "logprobs",
    "max_completion_tokens",
    "max_tokens",
    "messages",
    "metadata",
    "modalities",
    "n",
    "parallel_tool_calls",
    "prediction",
    "presence_penalty",
    "prompt_cache_key",
    "reasoning_effort",
    "response_format",
    "seed",
    "service_tier",
    "stop",
    "store",
    "stream",
    "stream_options",
    "temperature",
    "tool_choice",
    "tools",
    "top_logprobs",
    "top_p",
    "user",
    "verbosity",
    "web_search_options",
)
_ANTHROPIC_PARAMS: tuple[str, ...] = (
    "max_tokens",
    "messages",
    "metadata",
    "stop",
    "stream",
    "temperature",
    "thinking",
    "tool_choice",
    "tools",
    "top_k",
    "top_p",
)
_GEMINI_PARAMS: tuple[str, ...] = (
    "max_completion_tokens",
    "max_tokens",
    "messages",
    "response_format",
    "stop",
    "stream",
    "temperature",
    "thinking",
    "tool_choice",
    "tools",
    "top_p",
)


def get_supported_openai_params(
    *,
    model: str,
    custom_llm_provider: str | None = None,
    request_type: str = "chat_completion",
) -> list[str]:
    del model, request_type
    provider = (custom_llm_provider or "openai").strip().lower()
    if provider == "anthropic":
        return list(_ANTHROPIC_PARAMS)
    if provider == "gemini":
        return list(_GEMINI_PARAMS)
    return list(_OPENAI_CHAT_PARAMS)


def completion(**kwargs: Any) -> dict[str, Any] | Iterator[Any]:
    provider = _resolve_provider(kwargs)
    if provider == "anthropic":
        return _anthropic_completion(kwargs)
    if provider == "gemini":
        return _gemini_completion(kwargs)
    if provider == "responses":
        return _openai_responses_completion(kwargs)
    return _openai_chat_completion(kwargs)


def _resolve_provider(kwargs: dict[str, Any]) -> str:
    model = kwargs.get("model") if isinstance(kwargs.get("model"), str) else ""
    explicit_provider = (
        kwargs.get("custom_llm_provider")
        if isinstance(kwargs.get("custom_llm_provider"), str)
        else ""
    ).lower()
    if model.startswith("responses/"):
        return "responses"
    if model.startswith("anthropic/"):
        return "anthropic"
    if model.startswith("gemini/"):
        return "gemini"
    if explicit_provider in {"anthropic", "gemini"}:
        return explicit_provider
    return "openai"


__all__ = [
    "APIConnectionError",
    "APIError",
    "AuthenticationError",
    "BadRequestError",
    "NotFoundError",
    "RateLimitError",
    "completion",
    "drop_params",
    "get_supported_openai_params",
    "ssl_verify",
]
