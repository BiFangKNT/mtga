from __future__ import annotations

import os
from dataclasses import dataclass

import yaml

from modules.runtime.resource_manager import ResourceManager

PLACEHOLDER_API_URL = "YOUR_REVERSE_ENGINEERED_API_ENDPOINT_BASE_URL"
DEFAULT_MIDDLE_ROUTE = "/v1"


@dataclass(frozen=True)
class SingleProxyConfig:
    target_api_base_url: str
    middle_route: str
    custom_model_id: str
    target_model_id: str
    stream_mode: str | None
    debug_mode: bool
    disable_ssl_strict_mode: bool
    api_key: str

@dataclass(frozen=True)
class MultiProxyConfig:
    route_map: dict[str, SingleProxyConfig]
    mtga_auth_key: str
    default_config: SingleProxyConfig | None


def load_global_config(*, resource_manager: ResourceManager, log_func=print) -> dict:
    try:
        config_file = resource_manager.get_user_config_file()
        if os.path.exists(config_file):
            with open(config_file, encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
    except Exception as exc:
        log_func(f"加载全局配置失败: {exc}")
    return {}


def _resolve_custom_model_id(*, raw_config: dict) -> str:
    # 优先使用配置组的映射模型ID
    group_mapped_model_id = (raw_config.get("mapped_model_id") or "").strip()
    if group_mapped_model_id:
        return group_mapped_model_id
    
    # 如果配置组没有设置，则使用实际模型ID作为默认值
    actual_model_id = (raw_config.get("model_id") or "").strip()
    if actual_model_id:
        return actual_model_id
    
    # 最后的默认值
    return "CUSTOM_MODEL_ID"


def _resolve_target_model_id(*, raw_config: dict, custom_model_id: str) -> str:
    target_model_id = (raw_config.get("model_id") or "").strip()
    return target_model_id if target_model_id else custom_model_id


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


def build_single_config(raw_config: dict, log_func=print) -> SingleProxyConfig | None:
    target_api_base_url = raw_config.get("api_url", PLACEHOLDER_API_URL)
    if target_api_base_url == PLACEHOLDER_API_URL:
        # log_func("警告: 发现配置组未设置 API URL，跳过") # Optional: log warning if needed
        return None

    custom_model_id = _resolve_custom_model_id(raw_config=raw_config)
    target_model_id = _resolve_target_model_id(
        raw_config=raw_config,
        custom_model_id=custom_model_id,
    )
    middle_route = normalize_middle_route(raw_config.get("middle_route"))

    return SingleProxyConfig(
        target_api_base_url=target_api_base_url,
        middle_route=middle_route,
        custom_model_id=custom_model_id,
        target_model_id=target_model_id,
        stream_mode=raw_config.get("stream_mode"),
        debug_mode=bool(raw_config.get("debug_mode", False)),
        disable_ssl_strict_mode=bool(raw_config.get("disable_ssl_strict_mode", False)),
        api_key=(raw_config.get("api_key") or ""),
    )


def build_proxy_config(
    raw_config_groups: list[dict] | None,  # Changed to list of dicts
    *,
    resource_manager: ResourceManager,
    log_func=print,
) -> MultiProxyConfig | None:
    raw_config_groups = raw_config_groups or []
    global_config = load_global_config(resource_manager=resource_manager, log_func=log_func)
    
    route_map: dict[str, SingleProxyConfig] = {}
    default_config: SingleProxyConfig | None = None
    
    for idx, raw_config in enumerate(raw_config_groups):
        single_cfg = build_single_config(raw_config, log_func)
        if single_cfg:
            # First valid config becomes default
            if default_config is None:
                default_config = single_cfg
            
            # Add to routing strategy
            # Use custom_model_id (Mapped ID) as the key for routing
            if single_cfg.custom_model_id:
                route_map[single_cfg.custom_model_id] = single_cfg
    
    if not default_config:
        log_func("错误: 没有有效的配置组")
        return None

    return MultiProxyConfig(
        route_map=route_map,
        mtga_auth_key=str(global_config.get("mtga_auth_key") or "").strip(),
        default_config=default_config,
    )


__all__ = [
    "DEFAULT_MIDDLE_ROUTE",
    "SingleProxyConfig",
    "MultiProxyConfig",
    "PLACEHOLDER_API_URL",
    "build_proxy_config",
    "load_global_config",
    "normalize_middle_route",
]
