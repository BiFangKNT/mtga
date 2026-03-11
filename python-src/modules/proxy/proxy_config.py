from __future__ import annotations

import os
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, cast

import yaml

from modules.runtime.resource_manager import ResourceManager

PLACEHOLDER_API_URL = "YOUR_REVERSE_ENGINEERED_API_ENDPOINT_BASE_URL"
DEFAULT_MIDDLE_ROUTE = "/v1"
type LogFunc = Callable[[str], None]


@dataclass(frozen=True)
class ProxyApiEndpoint:
    api_url: str
    api_key: str


@dataclass(frozen=True)
class ProxyConfig:
    target_api_base_url: str
    api_endpoints: tuple[ProxyApiEndpoint, ...]
    middle_route: str
    custom_model_id: str
    target_model_id: str
    stream_mode: str | None
    debug_mode: bool
    disable_ssl_strict_mode: bool
    api_key: str
    mtga_auth_key: str


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


def _resolve_custom_model_id(
    *, global_config: dict[str, Any], raw_config: dict[str, Any]
) -> str:
    global_mapped_model_id = (global_config.get("mapped_model_id") or "").strip()
    legacy_group_mapped_model_id = (raw_config.get("mapped_model_id") or "").strip()
    return global_mapped_model_id or legacy_group_mapped_model_id or "CUSTOM_MODEL_ID"


def _resolve_target_model_id(*, raw_config: dict[str, Any], custom_model_id: str) -> str:
    target_model_id = (raw_config.get("model_id") or "").strip()
    return target_model_id if target_model_id else custom_model_id


def _parse_api_endpoints(*, raw_config: dict[str, Any]) -> tuple[ProxyApiEndpoint, ...]:
    raw_list = raw_config.get("api_endpoints")
    if isinstance(raw_list, list):
        raw_items = cast(list[Any], raw_list)
        endpoints: list[ProxyApiEndpoint] = []
        for item_any in raw_items:
            if not isinstance(item_any, dict):
                continue
            item = cast(dict[str, Any], item_any)
            url_value = item.get("api_url") or item.get("url") or ""
            if not isinstance(url_value, str):
                url_value = ""
            api_url = url_value.strip()
            if not api_url:
                continue
            key_value = item.get("api_key") or item.get("key") or ""
            if not isinstance(key_value, str):
                key_value = ""
            api_key = key_value.strip()
            endpoints.append(ProxyApiEndpoint(api_url=api_url, api_key=api_key))
        if endpoints:
            return tuple(endpoints)

    api_url_value = raw_config.get("api_url", PLACEHOLDER_API_URL)
    if not isinstance(api_url_value, str):
        api_url_value = PLACEHOLDER_API_URL
    api_key_value = raw_config.get("api_key") or ""
    if not isinstance(api_key_value, str):
        api_key_value = ""
    return (
        ProxyApiEndpoint(
            api_url=api_url_value,
            api_key=api_key_value,
        ),
    )


def normalize_middle_route(value: str | None) -> str:
    raw_value = (value or "").strip()
    if not raw_value:
        raw_value = DEFAULT_MIDDLE_ROUTE
    if not raw_value.startswith("/"):
        raw_value = f"/{raw_value}"
    if len(raw_value) > 1:
        raw_value = raw_value.rstrip("/")
        if not raw_value:
            raw_value = "/"
    return raw_value


def build_proxy_config(
    raw_config: dict[str, Any] | None,
    *,
    resource_manager: ResourceManager,
    log_func: LogFunc = print,
) -> ProxyConfig | None:
    raw_config = raw_config or {}
    global_config = load_global_config(resource_manager=resource_manager, log_func=log_func)

    api_endpoints = _parse_api_endpoints(raw_config=raw_config)
    target_api_base_url = api_endpoints[0].api_url
    if target_api_base_url == PLACEHOLDER_API_URL:
        log_func("错误: 请在配置中设置正确的 API URL")
        return None

    custom_model_id = _resolve_custom_model_id(
        global_config=global_config,
        raw_config=raw_config,
    )
    target_model_id = _resolve_target_model_id(
        raw_config=raw_config,
        custom_model_id=custom_model_id,
    )
    middle_route = normalize_middle_route(raw_config.get("middle_route"))

    return ProxyConfig(
        target_api_base_url=target_api_base_url,
        api_endpoints=api_endpoints,
        middle_route=middle_route,
        custom_model_id=custom_model_id,
        target_model_id=target_model_id,
        stream_mode=raw_config.get("stream_mode"),
        debug_mode=bool(raw_config.get("debug_mode", False)),
        disable_ssl_strict_mode=bool(raw_config.get("disable_ssl_strict_mode", False)),
        api_key=api_endpoints[0].api_key,
        mtga_auth_key=(global_config.get("mtga_auth_key") or ""),
    )


__all__ = [
    "DEFAULT_MIDDLE_ROUTE",
    "ProxyApiEndpoint",
    "ProxyConfig",
    "PLACEHOLDER_API_URL",
    "build_proxy_config",
    "load_global_config",
    "normalize_middle_route",
]
