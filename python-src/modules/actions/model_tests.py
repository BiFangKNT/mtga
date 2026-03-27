from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Protocol, cast

import requests

from modules.proxy.proxy_config import (
    ANTHROPIC_NATIVE_MODEL_DISCOVERY,
    ANTHROPIC_PROVIDER,
    DEFAULT_MIDDLE_ROUTE,
    GEMINI_DEFAULT_MIDDLE_ROUTE,
    GEMINI_NATIVE_BEARER_MODEL_DISCOVERY,
    GEMINI_NATIVE_X_GOOG_API_KEY_MODEL_DISCOVERY,
    GEMINI_PROVIDER,
    OPENAI_CHAT_COMPLETION_PROVIDER,
    OPENAI_COMPATIBLE_MODEL_DISCOVERY,
    OPENAI_PROVIDER_IDS,
    OPENAI_RESPONSE_PROVIDER,
    ProxyConfig,
    normalize_middle_route,
    normalize_model_discovery_strategy,
    normalize_provider,
    provider_supports_model_discovery,
)
from modules.proxy.upstream_adapter import LiteLLMUpstreamAdapter, normalize_upstream_error

HTTP_OK = 200
CONTENT_PREVIEW_LEN = 50
HTTP_SERVER_ERROR_STATUS_MIN = 500
HTTP_SERVER_ERROR_STATUS_MAX = 600
RETRYABLE_MODEL_DISCOVERY_STATUS_CODES = frozenset(
    {400, 401, 403, 404, 405, 406, 415, 422, 501}
)


@dataclass(frozen=True)
class ModelDiscoveryStrategy:
    id: str
    label: str
    path: str
    headers: dict[str, str]


@dataclass(frozen=True)
class ModelDiscoveryResult:
    model_ids: list[str]
    ok: bool
    strategy_id: str | None = None


class ThreadRunner(Protocol):
    def run(  # noqa: PLR0913
        self,
        name: str,
        target: Callable[..., None],
        *,
        args: tuple[Any, ...] | None = None,
        kwargs: dict[str, Any] | None = None,
        wait_for: list[str] | None = None,
        allow_parallel: bool = False,
        daemon: bool = True,
    ) -> str: ...


def _extract_model_items(payload: Any) -> list[dict[str, Any]]:
    if not isinstance(payload, dict):
        return []
    payload_dict = cast(dict[str, Any], payload)

    data = payload_dict.get("data")
    if isinstance(data, list):
        items: list[dict[str, Any]] = []
        data_list = cast(list[object], data)
        for item in data_list:
            if isinstance(item, dict):
                items.append(cast(dict[str, Any], item))
        return items

    result = payload_dict.get("result")
    if isinstance(result, dict):
        result_dict = cast(dict[str, Any], result)
        result_data = result_dict.get("data")
        if isinstance(result_data, list):
            items: list[dict[str, Any]] = []
            result_data_list = cast(list[object], result_data)
            for item in result_data_list:
                if isinstance(item, dict):
                    items.append(cast(dict[str, Any], item))
            return items

    alt = payload_dict.get("models")
    if isinstance(alt, list):
        items: list[dict[str, Any]] = []
        alt_list = cast(list[object], alt)
        for item in alt_list:
            if isinstance(item, dict):
                items.append(cast(dict[str, Any], item))
        return items

    return []


def _collect_model_ids(model_items: list[dict[str, Any]]) -> set[str]:
    model_ids: set[str] = set()
    for item in model_items:
        model_id = item.get("id")
        if not isinstance(model_id, str):
            model_id = item.get("name")
        if isinstance(model_id, str):
            normalized_model_id = _normalize_discovered_model_id(model_id)
            if normalized_model_id:
                model_ids.add(normalized_model_id)
    return model_ids


def _normalize_discovered_model_id(model_id: str) -> str:
    normalized = model_id.strip()
    if normalized.startswith("models/"):
        return normalized[len("models/") :]
    return normalized


def _should_continue_model_discovery(status_code: int) -> bool:
    return (
        status_code in RETRYABLE_MODEL_DISCOVERY_STATUS_CODES
        or HTTP_SERVER_ERROR_STATUS_MIN <= status_code < HTTP_SERVER_ERROR_STATUS_MAX
    )


def _build_model_discovery_path(middle_route: str, suffix: str) -> str:
    normalized = normalize_middle_route(middle_route)
    if normalized == "/":
        return f"/{suffix.lstrip('/')}"
    return f"{normalized.rstrip('/')}/{suffix.lstrip('/')}"


def _build_gemini_native_models_path(middle_route: str) -> str:
    normalized = normalize_middle_route(middle_route)
    return _build_model_discovery_path(normalized, "models")


def _build_openai_compatible_headers(api_key: str) -> dict[str, str]:
    headers: dict[str, str] = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    return headers


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


def _build_anthropic_native_headers(api_key: str) -> dict[str, str]:
    headers: dict[str, str] = {"anthropic-version": "2023-06-01"}
    if api_key:
        headers["x-api-key"] = api_key
    return headers


def _build_gemini_x_goog_api_key_headers(api_key: str) -> dict[str, str]:
    headers: dict[str, str] = {}
    if api_key:
        headers["x-goog-api-key"] = api_key
    return headers


def _build_model_discovery_strategies(
    config_group: dict[str, Any],
) -> list[ModelDiscoveryStrategy]:
    provider = normalize_provider(config_group.get("provider"))
    api_key = (config_group.get("api_key") or "").strip()
    raw_middle_route = config_group.get("middle_route")
    middle_route = normalize_middle_route(
        raw_middle_route,
        provider=provider,
    )
    compatible_middle_route = _build_openai_compatible_middle_route(
        raw_middle_route,
        provider=provider,
    )
    strategies: list[ModelDiscoveryStrategy]

    if provider in OPENAI_PROVIDER_IDS:
        strategies = [
            ModelDiscoveryStrategy(
                id=OPENAI_COMPATIBLE_MODEL_DISCOVERY,
                label="OpenAI-compatible /models",
                path=_build_model_discovery_path(compatible_middle_route, "models"),
                headers=_build_openai_compatible_headers(api_key),
            )
        ]
    elif provider == ANTHROPIC_PROVIDER:
        strategies = [
            ModelDiscoveryStrategy(
                id=ANTHROPIC_NATIVE_MODEL_DISCOVERY,
                label="Anthropic native /v1/models",
                path=_build_model_discovery_path(middle_route, "models"),
                headers=_build_anthropic_native_headers(api_key),
            ),
            ModelDiscoveryStrategy(
                id=OPENAI_COMPATIBLE_MODEL_DISCOVERY,
                label="OpenAI-compatible /models",
                path=_build_model_discovery_path(compatible_middle_route, "models"),
                headers=_build_openai_compatible_headers(api_key),
            ),
        ]
    elif provider == GEMINI_PROVIDER:
        native_path = _build_gemini_native_models_path(middle_route)
        strategies = [
            ModelDiscoveryStrategy(
                id=GEMINI_NATIVE_X_GOOG_API_KEY_MODEL_DISCOVERY,
                label="Gemini native /models (x-goog-api-key)",
                path=native_path,
                headers=_build_gemini_x_goog_api_key_headers(api_key),
            ),
            ModelDiscoveryStrategy(
                id=GEMINI_NATIVE_BEARER_MODEL_DISCOVERY,
                label="Gemini native /models (Bearer)",
                path=native_path,
                headers=_build_openai_compatible_headers(api_key),
            ),
            ModelDiscoveryStrategy(
                id=OPENAI_COMPATIBLE_MODEL_DISCOVERY,
                label="OpenAI-compatible /models",
                path=_build_model_discovery_path(compatible_middle_route, "models"),
                headers=_build_openai_compatible_headers(api_key),
            ),
        ]
    else:
        strategies = []

    cached_strategy_id = normalize_model_discovery_strategy(
        config_group.get("model_discovery_strategy")
        if isinstance(config_group.get("model_discovery_strategy"), str)
        else None
    )
    if not cached_strategy_id:
        return strategies

    prioritized: list[ModelDiscoveryStrategy] = []
    for strategy in strategies:
        if strategy.id == cached_strategy_id:
            prioritized.append(strategy)
            break
    prioritized.extend(strategy for strategy in strategies if strategy.id != cached_strategy_id)
    return prioritized


def _extract_response_output_text(payload: Any) -> str:
    if not isinstance(payload, dict):
        return ""

    payload_dict = cast(dict[str, Any], payload)
    output_obj = payload_dict.get("output")
    if not isinstance(output_obj, list):
        return ""

    texts: list[str] = []
    output_items = cast(list[object], output_obj)
    for item in output_items:
        if not isinstance(item, dict):
            continue
        item_map = cast(dict[str, Any], item)
        if item_map.get("type") != "message":
            continue
        content_obj = item_map.get("content")
        if not isinstance(content_obj, list):
            continue
        content_items = cast(list[object], content_obj)
        for content_item in content_items:
            if not isinstance(content_item, dict):
                continue
            content_map = cast(dict[str, Any], content_item)
            if content_map.get("type") != "output_text":
                continue
            text = content_map.get("text")
            if isinstance(text, str) and text.strip():
                texts.append(text.strip())
    return "".join(texts).strip()


def _extract_generation_preview(payload: Any, provider: str) -> str:
    if not isinstance(payload, dict):
        return ""
    payload_dict = cast(dict[str, Any], payload)
    if provider == OPENAI_RESPONSE_PROVIDER:
        return _extract_response_output_text(payload_dict)
    choices_obj = payload_dict.get("choices")
    if not isinstance(choices_obj, list) or not choices_obj:
        return ""
    choices = cast(list[object], choices_obj)
    first_choice_obj = choices[0]
    if not isinstance(first_choice_obj, dict):
        return ""
    first_choice = cast(dict[str, Any], first_choice_obj)
    message_obj = first_choice.get("message")
    if not isinstance(message_obj, dict):
        return ""
    message = cast(dict[str, Any], message_obj)
    content = message.get("content")
    return content.strip() if isinstance(content, str) else ""


def _log_model_list(
    payload: Any,
    model_id: str,
    log_func: Callable[[str], None],
) -> None:
    model_ids = _parse_model_ids(payload, log_func)
    if not model_ids:
        return
    if model_id in model_ids:
        log_func(f"✅ 发现模型: {model_id}")
    else:
        log_func(f"❌ 未找到模型: {model_id}")


def _log_response_error(
    response: requests.Response,
    log_func: Callable[[str], None],
) -> None:
    log_func(f"❌ 模型列表获取失败: HTTP {response.status_code}")
    try:
        error_info = response.text[:200]
        log_func(f"   错误信息: {error_info}")
    except Exception:
        log_func("   (无法获取错误详情)")


def _parse_response_json(
    response: requests.Response,
    log_func: Callable[[str], None],
) -> Any | None:
    try:
        return response.json()
    except Exception:
        log_func("   (响应成功，但无法解析详细信息)")
        return None


def _parse_model_ids(
    payload: Any,
    log_func: Callable[[str], None],
) -> list[str]:
    if isinstance(payload, dict):
        payload_dict = cast(dict[str, Any], payload)
        if payload_dict.get("object"):
            log_func(f"   对象类型: {payload_dict['object']}")

    model_items = _extract_model_items(payload)
    if not model_items:
        log_func("❌ 响应中未发现模型列表")
        return []

    model_ids = sorted(_collect_model_ids(model_items))
    log_func(f"   模型数量: {len(model_ids)}")
    return model_ids


def _coerce_payload_dict(payload: Any) -> dict[str, Any] | None:
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

    return None


def _build_generation_test_proxy_config(config_group: dict[str, Any]) -> ProxyConfig:
    provider = normalize_provider(config_group.get("provider"))
    model_id = (config_group.get("model_id") or "").strip()
    model_discovery_strategy = normalize_model_discovery_strategy(
        config_group.get("model_discovery_strategy")
        if isinstance(config_group.get("model_discovery_strategy"), str)
        else None
    )
    return ProxyConfig(
        provider=provider,
        target_api_base_url=(config_group.get("api_url") or "").rstrip("/"),
        middle_route=normalize_middle_route(
            config_group.get("middle_route"),
            provider=provider,
        ),
        custom_model_id=model_id or "test-model",
        target_model_id=model_id or "test-model",
        stream_mode=None,
        debug_mode=False,
        disable_ssl_strict_mode=bool(config_group.get("disable_ssl_strict_mode", False)),
        api_key=(config_group.get("api_key") or ""),
        mtga_auth_key="",
        model_discovery_strategy=model_discovery_strategy,
    )


def _run_generation_test_with_litellm(
    config_group: dict[str, Any],
    log_func: Callable[[str], None],
) -> None:
    provider = normalize_provider(config_group.get("provider"))
    model_id = (config_group.get("model_id") or "").strip()
    api_url = (config_group.get("api_url") or "").rstrip("/")
    if not api_url or not model_id:
        log_func("测活失败: API URL或模型ID为空")
        return

    proxy_config = _build_generation_test_proxy_config(config_group)
    adapter = LiteLLMUpstreamAdapter(
        disable_ssl_strict_mode=proxy_config.disable_ssl_strict_mode,
        log_func=log_func,
    )
    try:
        route = adapter.build_route(proxy_config)
        test_data = {
            "model": model_id,
            "messages": [{"role": "user", "content": "1"}],
            "max_tokens": 1,
            "temperature": 0,
        }
        log_func(
            "正在测活模型: "
            f"{model_id} (provider={provider}, request_api={route.request_api}, 会消耗少量tokens)"
        )

        response_payload = adapter.create_chat_completion(
            route=route,
            request_data=test_data,
        )
        response_json = _coerce_payload_dict(response_payload)
        if response_json is None:
            log_func("✅ 模型测活成功")
            return

        log_func(f"✅ 模型测活成功: {model_id}")
        content = _extract_generation_preview(response_json, OPENAI_CHAT_COMPLETION_PROVIDER)
        if content:
            preview = content[:CONTENT_PREVIEW_LEN]
            suffix = "..." if len(content) > CONTENT_PREVIEW_LEN else ""
            log_func(f"   响应内容: {preview}{suffix}")
        usage_obj = response_json.get("usage")
        if isinstance(usage_obj, dict):
            usage = cast(dict[str, Any], usage_obj)
            log_func(f"   消耗tokens: {usage.get('total_tokens', '未知')}")
    except Exception as exc:  # noqa: BLE001
        error_info = normalize_upstream_error(exc)
        log_func(f"❌ 模型测活失败: HTTP {error_info.status_code}")
        detail_obj = error_info.response_body.get("details")
        if not isinstance(detail_obj, str):
            detail_obj = error_info.response_body.get("error")
        detail = detail_obj if isinstance(detail_obj, str) else None
        if isinstance(detail, str):
            log_func(f"   错误信息: {detail[:200]}")
    finally:
        adapter.close()


def _try_fetch_model_payload(
    *,
    api_url: str,
    strategy: ModelDiscoveryStrategy,
    log_func: Callable[[str], None],
    model_id: str | None = None,
) -> tuple[Any | None, bool]:
    test_url = f"{api_url}{strategy.path}"
    suffix = f": {model_id}" if model_id else ""
    log_func(f"正在获取模型列表 ({strategy.label}): {test_url}")

    try:
        response = requests.get(test_url, headers=strategy.headers, timeout=10)
    except requests.exceptions.Timeout:
        log_func(f"❌ 模型列表获取超时{suffix}")
        payload = None
        should_continue = True
    except requests.exceptions.RequestException as exc:
        log_func(f"❌ 模型列表获取网络错误{suffix}: {str(exc)}")
        payload = None
        should_continue = True
    except Exception as exc:
        log_func(f"❌ 模型列表获取意外错误{suffix}: {str(exc)}")
        payload = None
        should_continue = False
    else:
        if response.status_code != HTTP_OK:
            _log_response_error(response, log_func)
            payload = None
            should_continue = _should_continue_model_discovery(response.status_code)
        else:
            log_func("✅ 模型列表获取成功")
            payload = _parse_response_json(response, log_func)
            if payload is None:
                should_continue = True
            elif not _extract_model_items(payload):
                log_func("❌ 响应中未发现模型列表")
                payload = None
                should_continue = True
            else:
                should_continue = False

    return payload, should_continue


def _fetch_model_payload(  # noqa: PLR0911
    config_group: dict[str, Any],
    log_func: Callable[[str], None],
    *,
    model_id: str | None = None,
) -> tuple[Any | None, str | None]:
    provider = normalize_provider(config_group.get("provider"))
    api_url = config_group.get("api_url", "").rstrip("/")
    if not api_url:
        log_func("检查失败: API URL为空")
        return None, None
    if not provider_supports_model_discovery(provider):
        log_func("当前提供商不支持通过 /models 自动发现模型，请直接手填实际模型ID")
        return None, None

    strategies = _build_model_discovery_strategies(config_group)
    if not strategies:
        log_func("当前提供商没有可用的模型发现策略")
        return None, None

    cached_strategy_id = normalize_model_discovery_strategy(
        config_group.get("model_discovery_strategy")
        if isinstance(config_group.get("model_discovery_strategy"), str)
        else None
    )
    if cached_strategy_id:
        log_func(f"优先使用缓存模型发现策略: {cached_strategy_id}")

    for strategy in strategies:
        payload, should_continue = _try_fetch_model_payload(
            api_url=api_url,
            strategy=strategy,
            log_func=log_func,
            model_id=model_id,
        )
        if payload is not None:
            if strategy.id != cached_strategy_id:
                log_func(f"已选定模型发现策略: {strategy.id}")
            else:
                log_func(f"缓存模型发现策略命中: {strategy.id}")
            return payload, strategy.id
        if not should_continue:
            break
        log_func(f"当前策略失败，尝试降级到下一种模型发现策略: {strategy.id}")

    return None, None


def _run_model_connection_test(
    config_group: dict[str, Any],
    log_func: Callable[[str], None],
) -> None:
    model_id = "未知模型"
    model_id = config_group.get("model_id", "")
    if not config_group.get("api_url") or not model_id:
        log_func("检查失败: API URL或模型ID为空")
        return

    payload, _strategy_id = _fetch_model_payload(
        config_group,
        log_func,
        model_id=model_id,
    )
    if payload is None:
        return
    _log_model_list(payload, model_id, log_func)


def fetch_model_list_result(
    config_group: dict[str, Any],
    *,
    log_func: Callable[[str], None] = print,
) -> ModelDiscoveryResult:
    payload, strategy_id = _fetch_model_payload(config_group, log_func)
    if payload is None:
        return ModelDiscoveryResult(model_ids=[], ok=False, strategy_id=None)
    model_ids = _parse_model_ids(payload, log_func)
    if not model_ids:
        return ModelDiscoveryResult(model_ids=[], ok=False, strategy_id=None)
    return ModelDiscoveryResult(model_ids=model_ids, ok=True, strategy_id=strategy_id)


def fetch_model_list(
    config_group: dict[str, Any],
    *,
    log_func: Callable[[str], None] = print,
) -> tuple[list[str], bool]:
    result = fetch_model_list_result(config_group, log_func=log_func)
    return result.model_ids, result.ok


def test_model_in_list(
    config_group: dict[str, Any],
    *,
    log_func: Callable[[str], None] = print,
    thread_manager: ThreadRunner,
) -> None:
    """测试模型是否在列表中（GET /v1/models）。"""
    thread_manager.run(
        "test_model_in_list",
        lambda: _run_model_connection_test(config_group, log_func),
    )


def test_chat_completion(
    config_group: dict[str, Any],
    *,
    log_func: Callable[[str], None] = print,
    thread_manager: ThreadRunner,
) -> None:
    """测试上游生成接口连接。"""

    def run_test():
        try:
            _run_generation_test_with_litellm(config_group, log_func)
        except Exception as exc:
            log_func(f"❌ 模型测活意外错误: {str(exc)}")

    thread_manager.run("test_chat_completion", run_test)
