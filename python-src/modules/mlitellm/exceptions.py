from __future__ import annotations

from typing import Any

import httpx


class MLiteLLMException(Exception):
    def __init__(  # noqa: PLR0913
        self,
        message: str,
        *,
        model: str | None = None,
        llm_provider: str | None = None,
        response: httpx.Response | None = None,
        request: httpx.Request | None = None,
        body: Any | None = None,
        status_code: int | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.model = model
        self.llm_provider = llm_provider
        self.request = request
        self.body = body
        self.status_code = status_code if status_code is not None else _status_code(response)
        self.request_id = _request_id(response)
        self.response = response

    def __str__(self) -> str:
        return f"mlitellm.{self.__class__.__name__}: {self.message}"


class APIConnectionError(MLiteLLMException):
    pass


class APIError(MLiteLLMException):
    pass


class AuthenticationError(MLiteLLMException):
    pass


class BadRequestError(MLiteLLMException):
    pass


class NotFoundError(MLiteLLMException):
    pass


class RateLimitError(MLiteLLMException):
    pass


def _status_code(response: httpx.Response | None) -> int | None:
    if response is None:
        return None
    return response.status_code


def _request_id(response: httpx.Response | None) -> str | None:
    if response is None:
        return None
    for key in ("x-request-id", "request-id"):
        value = response.headers.get(key)
        if value:
            return value
    return None


__all__ = [
    "APIConnectionError",
    "APIError",
    "AuthenticationError",
    "BadRequestError",
    "MLiteLLMException",
    "NotFoundError",
    "RateLimitError",
]
