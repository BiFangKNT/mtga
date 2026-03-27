from __future__ import annotations

import os
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

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


def load_global_config(
    *, resource_manager: ResourceManager, log_func: LogFunc = print
) -> dict[str, Any]:
    try:
        config_file = resource_manager.get_user_config_file()
        if os.path.exists(config_file):
            with open(config_file, encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
    except Exception as exc:
        log_func(f"加载全局配置失败: {exc}")
    return {}


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


def provider_supports_model_discovery(value: str | None) -> bool:
    return normalize_provider(value) in SUPPORTED_PROVIDER_IDS


def build_proxy_config(
    raw_config: dict[str, Any] | None,
    *,
    resource_manager: ResourceManager,
    log_func: LogFunc = print,
) -> ProxyConfig | None:
    raw_config = raw_config or {}
    global_config = load_global_config(resource_manager=resource_manager, log_func=log_func)

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
    "normalize_provider",
    "provider_supports_model_discovery",
]
