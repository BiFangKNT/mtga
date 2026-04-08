from __future__ import annotations

import os
import secrets
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, cast

import yaml

from modules.runtime.resource_manager import ResourceManager

PLACEHOLDER_API_URL = "YOUR_REVERSE_ENGINEERED_API_ENDPOINT_BASE_URL"
DEFAULT_MIDDLE_ROUTE = "/v1"
GEMINI_DEFAULT_MIDDLE_ROUTE = "/v1beta"
OPENAI_CHAT_COMPLETION_PROVIDER = "openai_chat_completion"
OPENAI_RESPONSE_PROVIDER = "openai_response"
ANTHROPIC_PROVIDER = "anthropic"
GEMINI_PROVIDER = "gemini"
OPENAI_PROVIDER_ALIAS = "openai"
OPENAI_PROVIDER_IDS = (
    OPENAI_CHAT_COMPLETION_PROVIDER,
    OPENAI_RESPONSE_PROVIDER,
)
OPENAI_COMPATIBLE_MODEL_DISCOVERY = "openai_compatible_bearer"
ANTHROPIC_NATIVE_MODEL_DISCOVERY = "anthropic_native"
GEMINI_NATIVE_X_GOOG_API_KEY_MODEL_DISCOVERY = "gemini_native_x_goog_api_key"
GEMINI_NATIVE_BEARER_MODEL_DISCOVERY = "gemini_native_bearer"
SUPPORTED_MODEL_DISCOVERY_STRATEGY_IDS = (
    OPENAI_COMPATIBLE_MODEL_DISCOVERY,
    ANTHROPIC_NATIVE_MODEL_DISCOVERY,
    GEMINI_NATIVE_X_GOOG_API_KEY_MODEL_DISCOVERY,
    GEMINI_NATIVE_BEARER_MODEL_DISCOVERY,
)
SUPPORTED_PROVIDER_IDS = (
    *OPENAI_PROVIDER_IDS,
    ANTHROPIC_PROVIDER,
    GEMINI_PROVIDER,
)
PROMPT_CACHE_BUCKET_ID_KEY = "prompt_cache_bucket_id"
PROMPT_CACHE_BUCKET_ID_LENGTH = 16
type LogFunc = Callable[[str], None]


@dataclass(frozen=True)
class ProxyConfig:
    provider: str
    target_api_base_url: str
    middle_route: str
    custom_model_id: str
    target_model_id: str
    stream_mode: str | None
    debug_mode: bool
    disable_ssl_strict_mode: bool
    api_key: str
    mtga_auth_key: str
    model_discovery_strategy: str | None = None
    prompt_cache_bucket_id: str = ""
    prompt_cache_enabled: bool = True


@dataclass(frozen=True)
class GlobalConfigLoadResult:
    global_config: dict[str, Any]
    load_failed: bool


def _load_global_config_result(
    *, resource_manager: ResourceManager, log_func: LogFunc = print
) -> GlobalConfigLoadResult:
    config_file = resource_manager.get_user_config_file()
    if not os.path.exists(config_file):
        return GlobalConfigLoadResult(global_config={}, load_failed=False)

    try:
        with open(config_file, encoding="utf-8") as f:
            loaded: Any = yaml.safe_load(f)
    except Exception as exc:
        log_func(f"加载全局配置失败: {exc}")
        return GlobalConfigLoadResult(global_config={}, load_failed=True)

    if loaded is None:
        return GlobalConfigLoadResult(global_config={}, load_failed=False)
    if isinstance(loaded, dict):
        return GlobalConfigLoadResult(
            global_config=cast(dict[str, Any], loaded),
            load_failed=False,
        )

    log_func("加载全局配置失败: 配置根节点必须是对象")
    return GlobalConfigLoadResult(global_config={}, load_failed=True)


def load_global_config(
    *, resource_manager: ResourceManager, log_func: LogFunc = print
) -> dict[str, Any]:
    return _load_global_config_result(
        resource_manager=resource_manager,
        log_func=log_func,
    ).global_config


def _generate_prompt_cache_bucket_id() -> str:
    return secrets.token_hex(PROMPT_CACHE_BUCKET_ID_LENGTH // 2)


def _persist_global_config(
    *,
    resource_manager: ResourceManager,
    global_config: dict[str, Any],
    log_func: LogFunc = print,
) -> None:
    config_file = resource_manager.get_user_config_file()
    try:
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        with open(config_file, "w", encoding="utf-8") as f:
            yaml.dump(
                global_config,
                f,
                default_flow_style=False,
                allow_unicode=True,
                indent=2,
                sort_keys=False,
            )
    except Exception as exc:
        log_func(f"写入全局配置失败: {exc}")


def _resolve_prompt_cache_bucket_id(
    *,
    global_config: dict[str, Any],
    resource_manager: ResourceManager,
    log_func: LogFunc = print,
    allow_persist: bool = True,
) -> str:
    bucket_id_obj = global_config.get(PROMPT_CACHE_BUCKET_ID_KEY)
    if isinstance(bucket_id_obj, str):
        bucket_id = bucket_id_obj.strip().lower()
        if bucket_id:
            return bucket_id

    if not allow_persist:
        log_func("全局配置读取失败，跳过 prompt cache bucket id 自动持久化")
        return ""

    bucket_id = _generate_prompt_cache_bucket_id()
    next_global_config = dict(global_config)
    next_global_config[PROMPT_CACHE_BUCKET_ID_KEY] = bucket_id
    _persist_global_config(
        resource_manager=resource_manager,
        global_config=next_global_config,
        log_func=log_func,
    )
    return bucket_id


def _resolve_custom_model_id(*, global_config: dict[str, Any]) -> str:
    # 有意不兼容 legacy group 级 mapped_model_id：
    # 当前版本不会自动迁移或回退读取旧字段，映射模型ID必须只由全局配置提供。
    # 若全局字段缺失，交给上层全局配置校验链路直接报错，而不是继续兜底启动。
    global_mapped_model_id = (global_config.get("mapped_model_id") or "").strip()
    return global_mapped_model_id


def _resolve_target_model_id(*, raw_config: dict[str, Any], custom_model_id: str) -> str:
    target_model_id = (raw_config.get("model_id") or "").strip()
    return target_model_id if target_model_id else custom_model_id


def get_default_middle_route(provider: str | None = None) -> str:
    if normalize_provider(provider) == GEMINI_PROVIDER:
        return GEMINI_DEFAULT_MIDDLE_ROUTE
    return DEFAULT_MIDDLE_ROUTE


def normalize_middle_route(value: str | None, *, provider: str | None = None) -> str:
    raw_value = (value or "").strip()
    if not raw_value:
        raw_value = get_default_middle_route(provider)
    if not raw_value.startswith("/"):
        raw_value = f"/{raw_value}"
    if len(raw_value) > 1:
        raw_value = raw_value.rstrip("/")
        if not raw_value:
            raw_value = "/"
    return raw_value


def normalize_provider(value: str | None) -> str:
    normalized = (value or "").strip().lower()
    if normalized == OPENAI_PROVIDER_ALIAS:
        return OPENAI_CHAT_COMPLETION_PROVIDER
    if normalized in SUPPORTED_PROVIDER_IDS:
        return normalized
    return OPENAI_CHAT_COMPLETION_PROVIDER


def normalize_model_discovery_strategy(value: str | None) -> str | None:
    normalized = (value or "").strip().lower()
    if normalized in SUPPORTED_MODEL_DISCOVERY_STRATEGY_IDS:
        return normalized
    return None


def normalize_prompt_cache_enabled(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() not in {"false", "0", "off", "no"}
    return bool(value) if value is not None else False


def provider_supports_model_discovery(value: str | None) -> bool:
    return normalize_provider(value) in SUPPORTED_PROVIDER_IDS


def build_proxy_config(
    raw_config: dict[str, Any] | None,
    *,
    resource_manager: ResourceManager,
    log_func: LogFunc = print,
) -> ProxyConfig | None:
    raw_config = raw_config or {}
    global_config_result = _load_global_config_result(
        resource_manager=resource_manager,
        log_func=log_func,
    )
    global_config = global_config_result.global_config

    target_api_base_url = raw_config.get("api_url", PLACEHOLDER_API_URL)
    if target_api_base_url == PLACEHOLDER_API_URL:
        log_func("错误: 请在配置中设置正确的 API URL")
        return None

    custom_model_id = _resolve_custom_model_id(
        global_config=global_config,
    )
    target_model_id = _resolve_target_model_id(
        raw_config=raw_config,
        custom_model_id=custom_model_id,
    )
    provider = normalize_provider(raw_config.get("provider"))
    model_discovery_strategy = normalize_model_discovery_strategy(
        raw_config.get("model_discovery_strategy")
        if isinstance(raw_config.get("model_discovery_strategy"), str)
        else None
    )
    prompt_cache_bucket_id = _resolve_prompt_cache_bucket_id(
        global_config=global_config,
        resource_manager=resource_manager,
        log_func=log_func,
        allow_persist=not global_config_result.load_failed,
    )
    middle_route = normalize_middle_route(
        raw_config.get("middle_route"),
        provider=provider,
    )

    return ProxyConfig(
        provider=provider,
        target_api_base_url=target_api_base_url,
        middle_route=middle_route,
        custom_model_id=custom_model_id,
        target_model_id=target_model_id,
        stream_mode=raw_config.get("stream_mode"),
        debug_mode=bool(raw_config.get("debug_mode", False)),
        disable_ssl_strict_mode=bool(raw_config.get("disable_ssl_strict_mode", False)),
        api_key=(raw_config.get("api_key") or ""),
        mtga_auth_key=(global_config.get("mtga_auth_key") or ""),
        model_discovery_strategy=model_discovery_strategy,
        prompt_cache_bucket_id=prompt_cache_bucket_id,
        prompt_cache_enabled=normalize_prompt_cache_enabled(
            raw_config.get("prompt_cache_enabled")
        ),
    )


__all__ = [
    "ANTHROPIC_PROVIDER",
    "DEFAULT_MIDDLE_ROUTE",
    "GEMINI_DEFAULT_MIDDLE_ROUTE",
    "GEMINI_PROVIDER",
    "GEMINI_NATIVE_BEARER_MODEL_DISCOVERY",
    "GEMINI_NATIVE_X_GOOG_API_KEY_MODEL_DISCOVERY",
    "ANTHROPIC_NATIVE_MODEL_DISCOVERY",
    "OPENAI_CHAT_COMPLETION_PROVIDER",
    "OPENAI_COMPATIBLE_MODEL_DISCOVERY",
    "OPENAI_PROVIDER_ALIAS",
    "OPENAI_PROVIDER_IDS",
    "OPENAI_RESPONSE_PROVIDER",
    "ProxyConfig",
    "PLACEHOLDER_API_URL",
    "SUPPORTED_MODEL_DISCOVERY_STRATEGY_IDS",
    "SUPPORTED_PROVIDER_IDS",
    "build_proxy_config",
    "get_default_middle_route",
    "load_global_config",
    "normalize_middle_route",
    "normalize_model_discovery_strategy",
    "normalize_prompt_cache_enabled",
    "normalize_provider",
    "provider_supports_model_discovery",
]
