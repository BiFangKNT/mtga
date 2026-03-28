from __future__ import annotations

import importlib
import os
import ssl
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Literal, cast

import litellm
from litellm.exceptions import APIConnectionError

from modules.proxy.proxy_config import (
    ANTHROPIC_PROVIDER,
    DEFAULT_MIDDLE_ROUTE,
    GEMINI_DEFAULT_MIDDLE_ROUTE,
    GEMINI_NATIVE_X_GOOG_API_KEY_MODEL_DISCOVERY,
    GEMINI_PROVIDER,
    OPENAI_CHAT_COMPLETION_PROVIDER,
    OPENAI_COMPATIBLE_MODEL_DISCOVERY,
    OPENAI_PROVIDER_IDS,
    OPENAI_RESPONSE_PROVIDER,
    SUPPORTED_PROVIDER_IDS,
    ProxyConfig,
    normalize_middle_route,
    normalize_provider,
)

type LogFunc = Callable[[str], None]
type RequestApi = Literal["chat_completions", "responses"]

CHAT_COMPLETIONS_REQUEST_API: RequestApi = "chat_completions"
RESPONSES_REQUEST_API: RequestApi = "responses"
OPENAI_CHAT_COMPLETION_STANDARD_PARAMS: frozenset[str] = frozenset(
    {
        "model",
        "messages",
        "temperature",
        "top_p",
        "n",
        "stream",
        "stream_options",
        "stop",
        "max_tokens",
        "max_completion_tokens",
        "presence_penalty",
        "frequency_penalty",
        "logit_bias",
        "user",
        "response_format",
        "seed",
        "tools",
        "tool_choice",
        "functions",
        "function_call",
        "logprobs",
        "top_logprobs",
        "parallel_tool_calls",
        "service_tier",
        "reasoning_effort",
        "prediction",
        "modalities",
        "audio",
        "metadata",
        "store",
        "extra_body",
        "allowed_openai_params",
    }
)
NON_OPENAI_REQUIRED_CHAT_PARAMS: frozenset[str] = frozenset({"messages", "model"})
_litellm_compat_patch_state = {"applied": False}


@dataclass(frozen=True)
class UpstreamRoute:
    provider: str
    request_api: RequestApi
    litellm_model: str
    base_url: str
    api_key: str
    middle_route_applied: bool
    middle_route_ignored: bool
    litellm_base_url: str = ""
    model_discovery_strategy: str | None = None


@dataclass(frozen=True)
class UpstreamErrorInfo:
    status_code: int
    response_body: dict[str, Any]
    log_message: str


def _coerce_mapping_payload(payload: Any) -> dict[str, Any] | None:
    if isinstance(payload, dict):
        return dict(cast(dict[str, Any], payload))

    model_dump = getattr(payload, "model_dump", None)
    if callable(model_dump):
        dumped = model_dump(exclude_none=False)
        if isinstance(dumped, dict):
            return cast(dict[str, Any], dumped)

    return None


def _sanitize_empty_gemini_block_reason(payload: Any) -> Any:
    payload_dict = _coerce_mapping_payload(payload)
    if payload_dict is None:
        return payload

    prompt_feedback_obj = payload_dict.get("promptFeedback")
    if not isinstance(prompt_feedback_obj, dict):
        return payload_dict

    prompt_feedback = dict(cast(dict[str, Any], prompt_feedback_obj))
    block_reason = prompt_feedback.get("blockReason")
    if block_reason is not None and (
        not isinstance(block_reason, str) or block_reason.strip()
    ):
        return payload_dict

    # MTGA workaround:
    # 某些 Gemini 兼容反代会在成功响应里返回 `promptFeedback.blockReason=""`。
    # LiteLLM 1.82.x 只按“键是否存在”判断是否被 prompt-level content filter block，
    # 会把本来正常的 `STOP + text` 响应错误改写成 `content_filter + content=None`。
    # 这里在进入 LiteLLM Gemini transformer 之前，去掉空的 blockReason。
    # 等上游修复后，可删除这段兼容逻辑。
    prompt_feedback.pop("blockReason", None)
    block_reason_message = prompt_feedback.get("blockReasonMessage")
    if isinstance(block_reason_message, str) and not block_reason_message.strip():
        prompt_feedback.pop("blockReasonMessage", None)

    if prompt_feedback:
        payload_dict["promptFeedback"] = prompt_feedback
    else:
        payload_dict.pop("promptFeedback", None)
    return payload_dict


def apply_litellm_compat_patches(*, log_func: LogFunc = print) -> None:
    if _litellm_compat_patch_state["applied"]:
        return

    vertex_gemini_module: Any = importlib.import_module(
        "litellm.llms.vertex_ai.gemini.vertex_and_google_ai_studio_gemini"
    )
    VertexGeminiConfig: Any = vertex_gemini_module.VertexGeminiConfig

    if getattr(VertexGeminiConfig, "_mtga_gemini_prompt_feedback_patch", False):
        _litellm_compat_patch_state["applied"] = True
        return

    original_transform: Any = (
        VertexGeminiConfig._transform_google_generate_content_to_openai_model_response
    )
    original_prompt_filter: Any = (
        VertexGeminiConfig._check_prompt_level_content_filter
    )

    def patched_transform(self: Any, *args: Any, **kwargs: Any) -> Any:
        if args:
            args = (
                _sanitize_empty_gemini_block_reason(args[0]),
                *args[1:],
            )
        elif "completion_response" in kwargs:
            kwargs = dict(kwargs)
            kwargs["completion_response"] = _sanitize_empty_gemini_block_reason(
                kwargs["completion_response"]
            )
        return original_transform(self, *args, **kwargs)

    def patched_prompt_filter(processed_chunk: Any, response_id: Any) -> Any:
        return original_prompt_filter(
            _sanitize_empty_gemini_block_reason(processed_chunk),
            response_id,
        )

    VertexGeminiConfig._transform_google_generate_content_to_openai_model_response = (
        patched_transform
    )
    VertexGeminiConfig._check_prompt_level_content_filter = staticmethod(
        patched_prompt_filter
    )
    VertexGeminiConfig._mtga_gemini_prompt_feedback_patch = True
    _litellm_compat_patch_state["applied"] = True
    log_func("已应用 LiteLLM Gemini promptFeedback 兼容补丁")


def build_upstream_route(
    proxy_config: ProxyConfig,
    *,
    fallback_api_key: str = "",
) -> UpstreamRoute:
    target_model_id = proxy_config.target_model_id.strip()
    if not target_model_id:
        raise ValueError("目标模型 ID 不能为空")

    provider = normalize_provider(proxy_config.provider)
    if _uses_openai_compatible_runtime_route(
        provider=provider,
        model_discovery_strategy=proxy_config.model_discovery_strategy,
    ):
        effective_provider = OPENAI_CHAT_COMPLETION_PROVIDER
        middle_route = _build_openai_compatible_middle_route(
            proxy_config.middle_route,
            provider=provider,
        )
    else:
        effective_provider = provider
        middle_route = normalize_middle_route(
            proxy_config.middle_route,
            provider=provider,
        )

    if effective_provider == OPENAI_CHAT_COMPLETION_PROVIDER:
        request_api = CHAT_COMPLETIONS_REQUEST_API
        litellm_model = target_model_id
    elif effective_provider == OPENAI_RESPONSE_PROVIDER:
        request_api = RESPONSES_REQUEST_API
        litellm_model = target_model_id
    else:
        request_api = CHAT_COMPLETIONS_REQUEST_API
        litellm_model = f"{effective_provider}/{target_model_id}"
    base_url = _build_chat_base_url(
        target_api_base_url=proxy_config.target_api_base_url,
        middle_route=middle_route,
    )
    litellm_base_url = _build_litellm_base_url(
        provider=effective_provider,
        chat_base_url=base_url,
        target_api_base_url=proxy_config.target_api_base_url,
        middle_route=middle_route,
    )

    return UpstreamRoute(
        provider=effective_provider,
        request_api=request_api,
        litellm_model=litellm_model,
        base_url=base_url,
        api_key=(proxy_config.api_key or fallback_api_key).strip(),
        middle_route_applied=True,
        middle_route_ignored=False,
        litellm_base_url=litellm_base_url,
        model_discovery_strategy=proxy_config.model_discovery_strategy,
    )


def _uses_openai_compatible_runtime_route(
    *,
    provider: str,
    model_discovery_strategy: str | None,
) -> bool:
    return (
        provider in {ANTHROPIC_PROVIDER, GEMINI_PROVIDER}
        and model_discovery_strategy == OPENAI_COMPATIBLE_MODEL_DISCOVERY
    )


def _build_openai_compatible_middle_route(
    raw_middle_route: str | None,
    *,
    provider: str,
) -> str:
    normalized_provider = normalize_provider(provider)
    normalized_middle_route = normalize_middle_route(
        raw_middle_route,
        provider=normalized_provider,
    )
    if normalized_provider == GEMINI_PROVIDER:
        if normalized_middle_route == GEMINI_DEFAULT_MIDDLE_ROUTE:
            return DEFAULT_MIDDLE_ROUTE
        if normalized_middle_route.endswith(GEMINI_DEFAULT_MIDDLE_ROUTE):
            prefix = normalized_middle_route[: -len(GEMINI_DEFAULT_MIDDLE_ROUTE)]
            if prefix:
                return f"{prefix}{DEFAULT_MIDDLE_ROUTE}"
    return normalize_middle_route(
        raw_middle_route,
        provider=OPENAI_CHAT_COMPLETION_PROVIDER,
    )


def _build_chat_base_url(*, target_api_base_url: str, middle_route: str) -> str:
    base_url = target_api_base_url.rstrip("/")
    return f"{base_url}{middle_route}"


def _build_litellm_base_url(
    *,
    provider: str,
    chat_base_url: str,
    target_api_base_url: str,
    middle_route: str,
) -> str:
    if provider != ANTHROPIC_PROVIDER:
        return chat_base_url

    # 外部语义里，middle_route 表示聊天基路径前缀，`/messages` 由 provider 路由补。
    # 但 LiteLLM 的 Anthropic adapter 会自行补 `/v1/messages`，因此内部基路径不能
    # 直接带尾部 `/v1`，否则会变成 `/v1/v1/messages`。
    if middle_route == DEFAULT_MIDDLE_ROUTE:
        return target_api_base_url.rstrip("/")
    if middle_route.endswith(DEFAULT_MIDDLE_ROUTE):
        prefix = middle_route[: -len(DEFAULT_MIDDLE_ROUTE)]
        return f"{target_api_base_url.rstrip('/')}{prefix}"
    return chat_base_url


def _extract_exception_detail(exc: Exception) -> str:
    response = getattr(exc, "response", None)
    response_text = getattr(response, "text", None)
    if isinstance(response_text, str) and response_text.strip():
        return response_text.strip()

    body = getattr(exc, "body", None)
    if isinstance(body, str) and body.strip():
        return body.strip()

    message = getattr(exc, "message", None)
    if isinstance(message, str) and message.strip():
        return message.strip()

    detail = str(exc).strip()
    return detail or exc.__class__.__name__


def normalize_upstream_error(exc: Exception) -> UpstreamErrorInfo:
    detail = _extract_exception_detail(exc)

    if isinstance(exc, APIConnectionError):
        return UpstreamErrorInfo(
            status_code=503,
            response_body={"error": f"Error contacting target API: {detail}"},
            log_message=f"连接目标 API 时出错: {detail}",
        )

    status_code_obj = getattr(exc, "status_code", None)
    status_code = status_code_obj if isinstance(status_code_obj, int) else None
    if status_code is not None:
        return UpstreamErrorInfo(
            status_code=status_code,
            response_body={
                "error": f"Target API error: {status_code}",
                "details": detail,
            },
            log_message=f"目标 API HTTP 错误: {status_code} - {detail}",
        )

    return UpstreamErrorInfo(
        status_code=500,
        response_body={"error": "An internal server error occurred"},
        log_message=f"发生意外错误: {detail}",
    )


class LiteLLMUpstreamAdapter:
    """把 MTGA 运行时配置编译成 LiteLLM 调用。"""

    def __init__(
        self,
        *,
        disable_ssl_strict_mode: bool,
        log_func: LogFunc = print,
    ) -> None:
        self._disable_ssl_strict_mode = disable_ssl_strict_mode
        self._log = log_func

    def close(self) -> None:
        return

    def _apply_route_compat_patches(self, route: UpstreamRoute) -> None:
        if route.provider != GEMINI_PROVIDER:
            return
        if _litellm_compat_patch_state["applied"]:
            return
        apply_litellm_compat_patches(log_func=self._log)

    @staticmethod
    def _coerce_payload_dict(payload: Any) -> dict[str, Any] | None:
        if isinstance(payload, dict):
            return cast(dict[str, Any], payload)

        model_dump = getattr(payload, "model_dump", None)
        if callable(model_dump):
            dumped = model_dump(exclude_none=False)
            if isinstance(dumped, dict):
                return cast(dict[str, Any], dumped)

        return None

    def _normalize_openai_compatible_request(
        self,
        *,
        route: UpstreamRoute,
        request_data: dict[str, Any],
    ) -> dict[str, Any]:
        call_kwargs: dict[str, Any] = dict(request_data)
        extra_body_obj = call_kwargs.get("extra_body")
        extra_body: dict[str, Any] = (
            dict(cast(dict[str, Any], extra_body_obj))
            if isinstance(extra_body_obj, dict)
            else {}
        )
        top_level_params = set(OPENAI_CHAT_COMPLETION_STANDARD_PARAMS)
        supported_params = self._get_supported_openai_params(
            route,
            custom_llm_provider="openai",
        )
        if supported_params is not None:
            top_level_params.update(supported_params)
        allowed_openai_params_obj = call_kwargs.get("allowed_openai_params")
        if isinstance(allowed_openai_params_obj, list):
            for allowed_param in cast(list[object], allowed_openai_params_obj):
                if isinstance(allowed_param, str) and allowed_param.strip():
                    top_level_params.add(allowed_param)

        passthrough_keys = [
            key
            for key in list(call_kwargs)
            if key not in top_level_params
        ]
        for key in passthrough_keys:
            extra_body[key] = call_kwargs.pop(key)

        if extra_body:
            call_kwargs["extra_body"] = extra_body
        return call_kwargs

    def _normalize_provider_chat_request(
        self,
        *,
        route: UpstreamRoute,
        request_data: dict[str, Any],
    ) -> dict[str, Any]:
        """按 provider 清洗 chat/completions 请求参数。"""
        if route.provider in OPENAI_PROVIDER_IDS:
            return self._normalize_openai_compatible_request(
                route=route,
                request_data=request_data,
            )
        call_kwargs = dict(request_data)
        supported_params = self._get_supported_openai_params(route)
        if supported_params is None:
            return call_kwargs

        dropped_params = [
            key
            for key in list(call_kwargs)
            if key in OPENAI_CHAT_COMPLETION_STANDARD_PARAMS
            and key not in NON_OPENAI_REQUIRED_CHAT_PARAMS
            and key not in supported_params
        ]
        for key in dropped_params:
            call_kwargs.pop(key, None)
        if dropped_params:
            dropped_list = ", ".join(sorted(dropped_params))
            self._log(f"{route.provider} 已忽略不兼容参数: {dropped_list}")
        return call_kwargs

    def _get_supported_openai_params(
        self,
        route: UpstreamRoute,
        *,
        custom_llm_provider: str | None = None,
    ) -> set[str] | None:
        litellm_sdk = cast(Any, litellm)
        supported_params_func = getattr(litellm_sdk, "get_supported_openai_params", None)
        if not callable(supported_params_func):
            return None

        provider_model = self._strip_provider_prefix(
            route.litellm_model,
            provider=route.provider,
        )
        effective_provider = custom_llm_provider or route.provider
        try:
            supported_params = supported_params_func(
                model=provider_model,
                custom_llm_provider=effective_provider,
            )
        except Exception as exc:  # noqa: BLE001
            self._log(f"获取 {effective_provider} 支持参数失败，保留原请求: {exc}")
            return None
        if not isinstance(supported_params, list):
            return None
        normalized_supported_params: set[str] = set()
        for supported_param in cast(list[object], supported_params):
            if isinstance(supported_param, str) and supported_param.strip():
                normalized_supported_params.add(supported_param)
        return normalized_supported_params

    @staticmethod
    def _strip_provider_prefix(model_name: str, *, provider: str) -> str:
        prefix = f"{provider}/"
        if model_name.startswith(prefix):
            return model_name[len(prefix) :]
        return model_name

    @staticmethod
    def _build_shared_kwargs(
        route: UpstreamRoute,
        *,
        url_kwarg: Literal["api_base", "base_url"],
    ) -> dict[str, Any]:
        """按 LiteLLM 目标接口构造共享鉴权与地址参数。"""
        shared_kwargs: dict[str, Any] = {
            url_kwarg: route.litellm_base_url or route.base_url
        }
        if route.api_key:
            shared_kwargs["api_key"] = route.api_key
        if route.provider in OPENAI_PROVIDER_IDS:
            shared_kwargs["custom_llm_provider"] = "openai"
        return shared_kwargs

    @staticmethod
    def _resolve_gemini_auth_header(route: UpstreamRoute) -> tuple[str, str] | None:
        if route.provider != GEMINI_PROVIDER or not route.api_key:
            return None
        if (
            route.model_discovery_strategy
            == GEMINI_NATIVE_X_GOOG_API_KEY_MODEL_DISCOVERY
        ):
            return "x-goog-api-key", route.api_key
        return "Authorization", f"Bearer {route.api_key}"

    @staticmethod
    def _merge_provider_extra_headers(
        route: UpstreamRoute,
        call_kwargs: dict[str, Any],
    ) -> dict[str, Any]:
        """为兼容代理补充 provider 级别的额外请求头。"""
        auth_header = LiteLLMUpstreamAdapter._resolve_gemini_auth_header(route)
        if auth_header is None:
            return call_kwargs

        extra_headers_obj = call_kwargs.get("extra_headers")
        extra_headers: dict[str, Any] = (
            dict(cast(dict[str, Any], extra_headers_obj))
            if isinstance(extra_headers_obj, dict)
            else {}
        )
        header_name, header_value = auth_header
        extra_headers.setdefault(header_name, header_value)
        call_kwargs["extra_headers"] = extra_headers
        return call_kwargs

    @staticmethod
    def _build_request_ssl_verify(disable_ssl_strict_mode: bool) -> bool | ssl.SSLContext:
        if not disable_ssl_strict_mode:
            return True

        cafile = os.getenv("SSL_CERT_FILE") or None
        ssl_context = ssl.create_default_context(cafile=cafile)
        strict_flag = getattr(ssl, "VERIFY_X509_STRICT", 0)
        if strict_flag and hasattr(ssl_context, "verify_flags"):
            ssl_context.verify_flags &= ~strict_flag
        return ssl_context

    def build_route(
        self,
        proxy_config: ProxyConfig,
        *,
        fallback_api_key: str = "",
    ) -> UpstreamRoute:
        return build_upstream_route(proxy_config, fallback_api_key=fallback_api_key)

    @staticmethod
    def _resolve_chat_completion_model(route: UpstreamRoute) -> str:
        if route.request_api != RESPONSES_REQUEST_API:
            return route.litellm_model
        if route.litellm_model.startswith("responses/"):
            return route.litellm_model
        return f"responses/{route.litellm_model}"

    def create_chat_completion(
        self,
        *,
        route: UpstreamRoute,
        request_data: dict[str, Any],
    ) -> Any:
        self._apply_route_compat_patches(route)
        call_kwargs = self._normalize_provider_chat_request(
            route=route,
            request_data=request_data,
        )
        call_kwargs["model"] = self._resolve_chat_completion_model(route)
        call_kwargs.update(self._build_shared_kwargs(route, url_kwarg="base_url"))
        call_kwargs["ssl_verify"] = self._build_request_ssl_verify(
            self._disable_ssl_strict_mode
        )
        call_kwargs = self._merge_provider_extra_headers(route, call_kwargs)
        litellm_sdk = cast(Any, litellm)
        completion_func = cast(Callable[..., Any], litellm_sdk.completion)
        return completion_func(**call_kwargs)


__all__ = [
    "ANTHROPIC_PROVIDER",
    "CHAT_COMPLETIONS_REQUEST_API",
    "GEMINI_PROVIDER",
    "OPENAI_CHAT_COMPLETION_PROVIDER",
    "OPENAI_RESPONSE_PROVIDER",
    "RESPONSES_REQUEST_API",
    "SUPPORTED_PROVIDER_IDS",
    "LiteLLMUpstreamAdapter",
    "UpstreamErrorInfo",
    "UpstreamRoute",
    "build_upstream_route",
    "normalize_upstream_error",
]
