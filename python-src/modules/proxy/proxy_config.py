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
    target_model_id: str
    middle_route: str = DEFAULT_MIDDLE_ROUTE


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
    enable_429_failover: bool
    failover_429_cooldown_seconds: int


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


def _parse_endpoint_from_group(
    group: dict[str, Any], *, custom_model_id: str
) -> ProxyApiEndpoint | None:
    url = (group.get("api_url") or "").strip()
    if not url or url == PLACEHOLDER_API_URL:
        return None
    key = (group.get("api_key") or "").strip()
    model = (group.get("model_id") or "").strip() or custom_model_id
    route = normalize_middle_route(group.get("middle_route"))
    return ProxyApiEndpoint(
        api_url=url,
        api_key=key,
        target_model_id=model,
        middle_route=route,
    )


def _extract_config_groups(global_config: dict[str, Any]) -> list[dict[str, Any]]:
    config_groups: list[dict[str, Any]] = []
    raw_groups_obj = global_config.get("config_groups")
    if not isinstance(raw_groups_obj, list):
        return config_groups
    for group_any in cast(list[object], raw_groups_obj):
        if isinstance(group_any, dict):
            config_groups.append(cast(dict[str, Any], group_any))
    return config_groups


def _extract_routing_group_ids(global_config: dict[str, Any]) -> list[str]:
    routing_group_ids: list[str] = []
    routing_group_ids_raw = global_config.get("routing_group_ids")
    if not isinstance(routing_group_ids_raw, list):
        return routing_group_ids
    for item in cast(list[object], routing_group_ids_raw):
        if isinstance(item, str):
            value = item.strip()
            if value:
                routing_group_ids.append(value)
    return routing_group_ids


def _parse_api_endpoints(
    *,
    raw_config: dict[str, Any],
    global_config: dict[str, Any],
    custom_model_id: str,
) -> tuple[ProxyApiEndpoint, ...]:
    enable_failover = bool(global_config.get("enable_429_failover", False))
    config_groups = _extract_config_groups(global_config)
    routing_group_ids = _extract_routing_group_ids(global_config)
    endpoints: list[ProxyApiEndpoint] = []
    endpoint_signatures: set[tuple[str, str, str, str]] = set()

    def append_unique(group: dict[str, Any]) -> None:
        endpoint = _parse_endpoint_from_group(group, custom_model_id=custom_model_id)
        if endpoint is None:
            return
        signature = (
            endpoint.api_url,
            endpoint.api_key,
            endpoint.target_model_id,
            endpoint.middle_route,
        )
        if signature in endpoint_signatures:
            return
        endpoint_signatures.add(signature)
        endpoints.append(endpoint)

    selected_mode = bool(enable_failover and routing_group_ids)
    if selected_mode:
        selected_ids = set(routing_group_ids)
        for group in config_groups:
            group_id = str(group.get("id") or "").strip()
            if group_id and group_id in selected_ids:
                append_unique(group)

    # 如果启用了选择模式但结果为空（例如：选中组均无效），回退到仅使用当前激活配置
    # 这意味着如果用户开启轮询但没选任何组，就相当于没开启轮询
    if selected_mode and not endpoints:
        selected_mode = False
        # 清空以便重新添加单点
        endpoints.clear()
        endpoint_signatures.clear()

    # 如果未启用选择模式（或回退），只添加当前激活的配置
    if not selected_mode:
        append_unique(raw_config)

    return tuple(endpoints)


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


def _parse_cooldown_seconds(global_config: dict[str, Any]) -> int:
    try:
        val = global_config.get("failover_429_cooldown_seconds")
        if isinstance(val, (int, float)):
            return max(1, int(val))
        if isinstance(val, str) and val.strip().isdigit():
            return max(1, int(val))
        return 60
    except (ValueError, TypeError):
        return 60


def build_proxy_config(
    raw_config: dict[str, Any] | None,
    *,
    resource_manager: ResourceManager,
    log_func: LogFunc = print,
) -> ProxyConfig | None:
    raw_config = raw_config or {}
    global_config = load_global_config(resource_manager=resource_manager, log_func=log_func)

    custom_model_id = _resolve_custom_model_id(
        global_config=global_config,
        raw_config=raw_config,
    )

    api_endpoints = _parse_api_endpoints(
        raw_config=raw_config,
        global_config=global_config,
        custom_model_id=custom_model_id,
    )
    if not api_endpoints:
        log_func("错误: 没有可用的 API 端点")
        return None
    target_api_base_url = api_endpoints[0].api_url
    if target_api_base_url == PLACEHOLDER_API_URL:
        log_func("错误: 请在配置中设置正确的 API URL")
        return None

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
        enable_429_failover=bool(global_config.get("enable_429_failover", False)),
        failover_429_cooldown_seconds=_parse_cooldown_seconds(global_config),
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
