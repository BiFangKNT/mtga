from __future__ import annotations

import json
import os
import ssl
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Literal, cast

import httpx

from modules import mlitellm
from modules.mlitellm.exceptions import APIConnectionError
from modules.proxy.param_self_heal_signal import extract_param_self_heal_signal
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
from modules.proxy.upstream_param_self_heal import (
    TEMPORARY_SELF_HEAL_WARNING_PREFIX,
    UnsupportedParamRule,
    UpstreamParamSelfHealController,
)

type LogFunc = Callable[[str], None]
type RequestApi = Literal["chat_completions", "responses"]

CHAT_COMPLETIONS_REQUEST_API: RequestApi = "chat_completions"
RESPONSES_REQUEST_API: RequestApi = "responses"
MLITELLM_CONNECT_RETRY_COUNT = 2
UPSTREAM_PARAM_SELF_HEAL_MAX_ATTEMPTS = 3
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
OPENAI_COMPATIBLE_META_PARAMS: frozenset[str] = frozenset(
    {"messages", "model", "extra_body", "allowed_openai_params"}
)
@dataclass(frozen=True)
class UpstreamRoute:
    provider: str
    request_api: RequestApi
    mlitellm_model: str
    base_url: str
    api_key: str
    prompt_cache_enabled: bool
    middle_route_applied: bool
    middle_route_ignored: bool
    mlitellm_base_url: str = ""
    model_discovery_strategy: str | None = None
    prompt_cache_key: str = ""


@dataclass(frozen=True)
class UpstreamErrorInfo:
    status_code: int
    response_body: Any
    log_message: str
    detail_text: str
    raw_response_text: str | None = None
    parsed_response_body: dict[str, Any] | list[Any] | None = None


def _coerce_mapping_payload(payload: Any) -> dict[str, Any] | None:
    if isinstance(payload, dict):
        return dict(cast(dict[str, Any], payload))

    model_dump = getattr(payload, "model_dump", None)
    if callable(model_dump):
        dumped = model_dump(exclude_none=False)
        if isinstance(dumped, dict):
            return cast(dict[str, Any], dumped)

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


def _coerce_json_payload(payload: Any) -> dict[str, Any] | list[Any] | None:
    payload_dict = _coerce_mapping_payload(payload)
    if payload_dict is not None:
        return payload_dict
    if isinstance(payload, list):
        return list(cast(list[Any], payload))
    return None


def _serialize_json_payload(payload: dict[str, Any] | list[Any]) -> str:
    return json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        default=str,
    )


def _unwrap_exception_message(message: str) -> str:
    normalized = message.strip()
    if normalized.startswith("mlitellm.") and ": " in normalized:
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


def _extract_upstream_request_id(exc: Exception) -> str | None:
    request_id = getattr(exc, "request_id", None)
    if isinstance(request_id, str) and request_id.strip():
        return request_id.strip()

    response = getattr(exc, "response", None)
    headers = getattr(response, "headers", None)
    if headers is None:
        return None

    header_get = getattr(headers, "get", None)
    if not callable(header_get):
        return None

    for key in ("x-request-id", "request-id"):
        header_value = header_get(key)
        if isinstance(header_value, str) and header_value.strip():
            return header_value.strip()
    return None


def _attach_request_id(
    payload: dict[str, Any] | list[Any],
    exc: Exception,
) -> dict[str, Any] | list[Any]:
    if not isinstance(payload, dict):
        return payload
    if payload.get("request_id"):
        return payload

    request_id = _extract_upstream_request_id(exc)
    if not request_id:
        return payload

    payload_with_request_id = dict(payload)
    payload_with_request_id["request_id"] = request_id
    return payload_with_request_id


def _looks_like_openai_error_object(payload: dict[str, Any]) -> bool:
    payload_keys = set(payload)
    if "error" in payload_keys:
        return False
    if "message" not in payload_keys or "type" not in payload_keys:
        return False
    return payload_keys.issubset({"message", "type", "code", "param"})


def _restore_error_root_payload(
    payload: dict[str, Any] | list[Any],
    exc: Exception,
) -> dict[str, Any] | list[Any]:
    if not isinstance(payload, dict):
        return payload
    if not _looks_like_openai_error_object(payload):
        return _attach_request_id(payload, exc)

    restored_payload: dict[str, Any] = {"error": dict(payload)}
    request_id = _extract_upstream_request_id(exc)
    if request_id:
        restored_payload["request_id"] = request_id
    return restored_payload


def _extract_fallback_response_body(exc: Exception) -> dict[str, Any] | list[Any] | None:
    body = getattr(exc, "body", None)
    if isinstance(body, str):
        parsed_body = _parse_json_payload_text(body)
        if parsed_body is not None:
            return _restore_error_root_payload(parsed_body, exc)
        return None

    coerced_body = _coerce_json_payload(body)
    if coerced_body is not None:
        return _restore_error_root_payload(coerced_body, exc)
    return None


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
        mlitellm_model = target_model_id
    elif effective_provider == OPENAI_RESPONSE_PROVIDER:
        request_api = RESPONSES_REQUEST_API
        mlitellm_model = target_model_id
    else:
        request_api = CHAT_COMPLETIONS_REQUEST_API
        mlitellm_model = f"{effective_provider}/{target_model_id}"
    base_url = _build_chat_base_url(
        target_api_base_url=proxy_config.target_api_base_url,
        middle_route=middle_route,
    )
    mlitellm_base_url = _build_mlitellm_base_url(
        provider=effective_provider,
        chat_base_url=base_url,
        target_api_base_url=proxy_config.target_api_base_url,
        middle_route=middle_route,
    )

    return UpstreamRoute(
        provider=effective_provider,
        request_api=request_api,
        mlitellm_model=mlitellm_model,
        base_url=base_url,
        api_key=(proxy_config.api_key or fallback_api_key).strip(),
        prompt_cache_enabled=proxy_config.prompt_cache_enabled,
        middle_route_applied=True,
        middle_route_ignored=False,
        mlitellm_base_url=mlitellm_base_url,
        model_discovery_strategy=proxy_config.model_discovery_strategy,
        prompt_cache_key=_build_prompt_cache_key(proxy_config.prompt_cache_bucket_id),
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


def _build_prompt_cache_key(prompt_cache_bucket_id: str) -> str:
    normalized_bucket_id = prompt_cache_bucket_id.strip().lower()
    if not normalized_bucket_id:
        return ""
    return f"mtga:pc:v1:b:{normalized_bucket_id}"


def _build_mlitellm_base_url(
    *,
    provider: str,
    chat_base_url: str,
    target_api_base_url: str,
    middle_route: str,
) -> str:
    if provider != ANTHROPIC_PROVIDER:
        return chat_base_url

    # 外部语义里，middle_route 表示聊天基路径前缀，`/messages` 由 provider 路由补。
    # 但 MLiteLLM 的 Anthropic adapter 会自行补 `/v1/messages`，因此内部基路径不能
    # 直接带尾部 `/v1`，否则会变成 `/v1/v1/messages`。
    if middle_route == DEFAULT_MIDDLE_ROUTE:
        return target_api_base_url.rstrip("/")
    if middle_route.endswith(DEFAULT_MIDDLE_ROUTE):
        prefix = middle_route[: -len(DEFAULT_MIDDLE_ROUTE)]
        return f"{target_api_base_url.rstrip('/')}{prefix}"
    return chat_base_url


def _extract_exception_detail(
    exc: Exception,
    *,
    raw_response_text: str | None,
    fallback_response_body: dict[str, Any] | list[Any] | None,
) -> str:
    if raw_response_text is not None:
        return raw_response_text
    if fallback_response_body is not None:
        return _serialize_json_payload(fallback_response_body)
    body = getattr(exc, "body", None)
    if isinstance(body, str) and body.strip():
        return body.strip()

    message = getattr(exc, "message", None)
    if isinstance(message, str) and message.strip():
        return _unwrap_exception_message(message)

    detail = _unwrap_exception_message(str(exc))
    return detail or exc.__class__.__name__


def normalize_upstream_error(exc: Exception) -> UpstreamErrorInfo:
    raw_response_text = _extract_raw_response_text(exc)
    parsed_response_body = (
        _parse_json_payload_text(raw_response_text)
        if raw_response_text is not None
        else None
    )
    fallback_response_body = (
        None if raw_response_text is not None else _extract_fallback_response_body(exc)
    )
    detail = _extract_exception_detail(
        exc,
        raw_response_text=raw_response_text,
        fallback_response_body=fallback_response_body,
    )

    if isinstance(exc, APIConnectionError):
        return UpstreamErrorInfo(
            status_code=503,
            response_body={"error": f"Error contacting target API: {detail}"},
            log_message=f"连接目标 API 时出错: {detail}",
            detail_text=detail,
            raw_response_text=raw_response_text,
            parsed_response_body=parsed_response_body,
        )

    status_code_obj = getattr(exc, "status_code", None)
    status_code = status_code_obj if isinstance(status_code_obj, int) else None
    if status_code is not None:
        return UpstreamErrorInfo(
            status_code=status_code,
            response_body=parsed_response_body
            if parsed_response_body is not None
            else fallback_response_body
            if fallback_response_body is not None
            else {
                "error": f"Target API error: {status_code}",
                "details": detail,
            },
            log_message=f"目标 API HTTP 错误: {status_code} - {detail}",
            detail_text=detail,
            raw_response_text=raw_response_text,
            parsed_response_body=parsed_response_body,
        )

    return UpstreamErrorInfo(
        status_code=500,
        response_body={"error": "An internal server error occurred"},
        log_message=f"发生意外错误: {detail}",
        detail_text=detail,
        raw_response_text=raw_response_text,
        parsed_response_body=parsed_response_body,
    )


class MLiteLLMUpstreamAdapter:
    """把 MTGA 运行时配置编译成 MLiteLLM 调用。"""

    def __init__(
        self,
        *,
        disable_ssl_strict_mode: bool,
        log_func: LogFunc = print,
    ) -> None:
        self._disable_ssl_strict_mode = disable_ssl_strict_mode
        self._log = log_func
        self._param_self_heal = UpstreamParamSelfHealController()

    def close(self) -> None:
        return

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
        top_level_params = set(OPENAI_COMPATIBLE_META_PARAMS)
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
        if supported_params is not None:
            self._drop_unsupported_standard_params(
                route=route,
                call_kwargs=call_kwargs,
                allowed_params=top_level_params,
            )

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

        self._drop_unsupported_standard_params(
            route=route,
            call_kwargs=call_kwargs,
            allowed_params=NON_OPENAI_REQUIRED_CHAT_PARAMS | supported_params,
        )
        return call_kwargs

    def _drop_unsupported_standard_params(
        self,
        *,
        route: UpstreamRoute,
        call_kwargs: dict[str, Any],
        allowed_params: set[str] | frozenset[str],
    ) -> None:
        dropped_params = [
            key
            for key in list(call_kwargs)
            if key in OPENAI_CHAT_COMPLETION_STANDARD_PARAMS and key not in allowed_params
        ]
        for key in dropped_params:
            call_kwargs.pop(key, None)
        if dropped_params:
            dropped_list = ", ".join(sorted(dropped_params))
            self._log(
                f"{self._format_route_log_context(route)} 已忽略不兼容参数: {dropped_list}"
            )

    @staticmethod
    def _format_route_log_context(
        route: UpstreamRoute,
        *,
        provider: str | None = None,
        model: str | None = None,
    ) -> str:
        return (
            f"provider={provider or route.provider} "
            f"request_api={route.request_api} "
            f"model={model or route.mlitellm_model}"
        )

    @staticmethod
    def _iter_exception_chain(exc: BaseException) -> list[BaseException]:
        seen: set[int] = set()
        pending: list[BaseException] = [exc]
        chain: list[BaseException] = []
        while pending:
            current = pending.pop()
            current_id = id(current)
            if current_id in seen:
                continue
            seen.add(current_id)
            chain.append(current)
            cause = getattr(current, "__cause__", None)
            context = getattr(current, "__context__", None)
            if isinstance(cause, BaseException):
                pending.append(cause)
            if isinstance(context, BaseException):
                pending.append(context)
        return chain

    @classmethod
    def _is_connect_stage_retryable(cls, exc: Exception) -> bool:
        connect_stage_errors = (
            httpx.ConnectError,
            httpx.ConnectTimeout,
            httpx.ProxyError,
        )
        return any(
            isinstance(candidate, connect_stage_errors)
            for candidate in cls._iter_exception_chain(exc)
        )

    def _call_completion_with_connect_retries(
        self,
        *,
        route: UpstreamRoute,
        call_kwargs: dict[str, Any],
        completion_func: Callable[..., Any],
    ) -> Any:
        route_log_context = self._format_route_log_context(route)
        total_attempts = MLITELLM_CONNECT_RETRY_COUNT + 1
        for attempt in range(1, total_attempts + 1):
            try:
                # 这里只覆盖拿到上游响应对象前、且异常链明确表明卡在建连阶段的失败，
                # 避免把可能已被上游受理的 POST 请求透明重放。
                return completion_func(**call_kwargs)
            except Exception as exc:  # noqa: BLE001
                if not self._is_connect_stage_retryable(exc):
                    raise
                if attempt >= total_attempts:
                    self._log(
                        f"{route_log_context} 建连阶段故障重试已耗尽: "
                        f"attempt={attempt}/{total_attempts} error={exc}"
                    )
                    raise
                self._log(
                    f"{route_log_context} 遇到建连阶段故障，准备重试: "
                    f"attempt={attempt + 1}/{total_attempts} error={exc}"
                )

    def _call_completion_with_param_self_heal(
        self,
        *,
        route: UpstreamRoute,
        call_kwargs: dict[str, Any],
        completion_func: Callable[..., Any],
    ) -> Any:
        route_log_context = self._format_route_log_context(route)
        cache_key = self._param_self_heal.build_cache_key(
            provider=route.provider,
            request_api=route.request_api,
            base_url=route.mlitellm_base_url or route.base_url,
            model=route.mlitellm_model,
            api_key=route.api_key,
        )
        effective_call_kwargs, cached_rules = self._param_self_heal.apply_cached_rules(
            cache_key=cache_key,
            call_kwargs=call_kwargs,
        )
        if cached_rules:
            cached_rule_labels = ", ".join(rule.label for rule in cached_rules)
            self._log(
                f"{TEMPORARY_SELF_HEAL_WARNING_PREFIX} "
                f"{route_log_context} 命中上游不兼容参数缓存，已跳过: "
                f"{cached_rule_labels}"
            )

        learned_rules: set[UnsupportedParamRule] = set()
        skipped_rules = set(cached_rules)
        current_call_kwargs = effective_call_kwargs
        for _attempt in range(UPSTREAM_PARAM_SELF_HEAL_MAX_ATTEMPTS):
            try:
                response = self._call_completion_with_connect_retries(
                    route=route,
                    call_kwargs=current_call_kwargs,
                    completion_func=completion_func,
                )
            except Exception as exc:  # noqa: BLE001
                param_self_heal_signal = extract_param_self_heal_signal(exc)
                if param_self_heal_signal is None:
                    raise
                selection = self._param_self_heal.select_rule(
                    call_kwargs=current_call_kwargs,
                    message=param_self_heal_signal.message,
                    param=param_self_heal_signal.param,
                    skipped_rules=skipped_rules,
                )
                if selection is None:
                    raise

                next_call_kwargs, changed = self._param_self_heal.apply_rule(
                    call_kwargs=current_call_kwargs,
                    rule=selection.rule,
                )
                if not changed:
                    raise

                skipped_rules.add(selection.rule)
                if selection.cacheable:
                    learned_rules.add(selection.rule)
                retry_action = (
                    "上游拒绝参数，自动剔除后重试"
                    if selection.cacheable
                    else "根据上游报错临时剔除参数后重试（本次不缓存）"
                )
                self._log(
                    f"{TEMPORARY_SELF_HEAL_WARNING_PREFIX} "
                    f"{route_log_context}"
                    + (
                        f"\nerror={param_self_heal_signal.message}"
                        if param_self_heal_signal.message
                        else ""
                    )
                    + f"\n{retry_action}: {selection.rule.label}"
                )
                current_call_kwargs = next_call_kwargs
                continue

            self._param_self_heal.remember_rules(
                cache_key=cache_key,
                rules=learned_rules,
            )
            return response

        response = self._call_completion_with_connect_retries(
            route=route,
            call_kwargs=current_call_kwargs,
            completion_func=completion_func,
        )
        self._param_self_heal.remember_rules(
            cache_key=cache_key,
            rules=learned_rules,
        )
        return response

    def _get_supported_openai_params(
        self,
        route: UpstreamRoute,
        *,
        custom_llm_provider: str | None = None,
    ) -> set[str] | None:
        mlitellm_sdk = cast(Any, mlitellm)
        supported_params_func = getattr(mlitellm_sdk, "get_supported_openai_params", None)
        if not callable(supported_params_func):
            return None

        provider_model = self._strip_provider_prefix(
            route.mlitellm_model,
            provider=route.provider,
        )
        effective_provider = custom_llm_provider or route.provider
        try:
            supported_params = supported_params_func(
                model=provider_model,
                custom_llm_provider=effective_provider,
            )
        except Exception as exc:  # noqa: BLE001
            route_log_context = self._format_route_log_context(
                route,
                provider=effective_provider,
                model=provider_model,
            )
            self._log(
                f"{route_log_context} 获取支持参数失败，保留原请求: {exc}"
            )
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
        """按 MLiteLLM 目标接口构造共享鉴权与地址参数。"""
        shared_kwargs: dict[str, Any] = {
            url_kwarg: route.mlitellm_base_url or route.base_url
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
        auth_header = MLiteLLMUpstreamAdapter._resolve_gemini_auth_header(route)
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
            return route.mlitellm_model
        if route.mlitellm_model.startswith("responses/"):
            return route.mlitellm_model
        return f"responses/{route.mlitellm_model}"

    def create_chat_completion(
        self,
        *,
        route: UpstreamRoute,
        request_data: dict[str, Any],
    ) -> Any:
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
        if (
            route.provider in OPENAI_PROVIDER_IDS
            and route.prompt_cache_enabled
            and route.prompt_cache_key
        ):
            call_kwargs.setdefault("prompt_cache_key", route.prompt_cache_key)
        # 关闭 MLiteLLM / OpenAI SDK 内层默认重试，避免和外层建连重试叠加。
        call_kwargs["max_retries"] = 0
        call_kwargs["num_retries"] = 0
        mlitellm_sdk = cast(Any, mlitellm)
        completion_func = cast(Callable[..., Any], mlitellm_sdk.completion)
        return self._call_completion_with_param_self_heal(
            route=route,
            call_kwargs=call_kwargs,
            completion_func=completion_func,
        )


__all__ = [
    "ANTHROPIC_PROVIDER",
    "CHAT_COMPLETIONS_REQUEST_API",
    "GEMINI_PROVIDER",
    "OPENAI_CHAT_COMPLETION_PROVIDER",
    "OPENAI_RESPONSE_PROVIDER",
    "RESPONSES_REQUEST_API",
    "SUPPORTED_PROVIDER_IDS",
    "MLiteLLMUpstreamAdapter",
    "UpstreamErrorInfo",
    "UpstreamRoute",
    "build_upstream_route",
    "normalize_upstream_error",
]
