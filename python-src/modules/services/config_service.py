from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, cast

import yaml

from modules.proxy.model_routing import (
    build_model_routing_config,
    normalize_model_routing_config,
    serialize_model_routing_config,
)
from modules.proxy.proxy_config import (
    OPENAI_CHAT_COMPLETION_PROVIDER,
    normalize_model_discovery_strategy,
    normalize_provider,
)

DEFAULT_PROVIDER = OPENAI_CHAT_COMPLETION_PROVIDER
OFFICIAL_BASE_URL_PROXY_MODE = "trae_official_base_url"
DEFAULT_PROXY_MODE = OFFICIAL_BASE_URL_PROXY_MODE
NATIVE_PROXY_MODE = "trae_native"
DEFAULT_MINIMIZE_TO_TRAY_ON_CLOSE = False
SUPPORTED_PROXY_MODES = frozenset(
    {
        DEFAULT_PROXY_MODE,
        NATIVE_PROXY_MODE,
        OFFICIAL_BASE_URL_PROXY_MODE,
    }
)
# Breaking change:
# `config_groups[*].mapped_model_id` 已经不符合当前“一份全局映射模型ID + 多个配置组”的语义。
# 新版本不会自动迁移该字段；读取时会直接忽略，保存时会按当前 schema 清理掉。
# 代理启动也不会再使用它兜底，用户必须改为在全局配置维护 `mapped_model_id`。
LEGACY_GROUP_MAPPED_MODEL_ID_KEY = "mapped_model_id"
LEGACY_GROUP_MAPPED_MODEL_ID_WARNING = (
    "⚠️ 检测到不再受支持的字段 config_groups[*].mapped_model_id；"
    "当前版本不会自动迁移或继续使用该字段，请在“全局配置”中填写映射模型ID。"
)
CONFIG_GROUP_ALLOWED_KEYS = frozenset(
    {
        "name",
        "provider",
        "api_url",
        "model_id",
        "api_key",
        "middle_route",
        "model_discovery_strategy",
        "prompt_cache_enabled",
    }
)


def _normalize_proxy_mode(value: Any) -> str:
    if isinstance(value, str):
        normalized = value.strip()
        if normalized in SUPPORTED_PROXY_MODES:
            return normalized
    return DEFAULT_PROXY_MODE


def _normalize_bool(value: Any, *, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"true", "1", "on", "yes"}:
            return True
        if normalized in {"false", "0", "off", "no"}:
            return False
    if value is None:
        return default
    return bool(value)


def _normalize_config_group(raw_group: Any) -> dict[str, Any] | None:
    if not isinstance(raw_group, dict):
        return None

    raw_group_map = cast(dict[object, Any], raw_group)
    normalized: dict[str, Any] = {}
    for raw_key, value in raw_group_map.items():
        key = str(raw_key)
        # 有意不兼容 legacy `mapped_model_id`：
        # 当前版本不会自动迁移它，也不会在运行时继续读取；一旦保存就按新 schema 清理。
        if key in CONFIG_GROUP_ALLOWED_KEYS:
            normalized[key] = value
    provider = normalized.get("provider")
    normalized["provider"] = normalize_provider(provider if isinstance(provider, str) else None)
    strategy = normalized.get("model_discovery_strategy")
    normalized["model_discovery_strategy"] = normalize_model_discovery_strategy(
        strategy if isinstance(strategy, str) else None
    )
    prompt_cache_enabled = normalized.get("prompt_cache_enabled")
    if isinstance(prompt_cache_enabled, str):
        normalized["prompt_cache_enabled"] = prompt_cache_enabled.strip().lower() not in {
            "false",
            "0",
            "off",
            "no",
        }
    elif isinstance(prompt_cache_enabled, bool):
        normalized["prompt_cache_enabled"] = prompt_cache_enabled
    else:
        normalized["prompt_cache_enabled"] = False
    return normalized


def _collect_config_warnings(raw_config: Any) -> list[str]:
    if not isinstance(raw_config, dict):
        return []

    raw_config_map = cast(dict[object, Any], raw_config)
    raw_groups = raw_config_map.get("config_groups")
    if not isinstance(raw_groups, list):
        return []

    for raw_group in cast(list[Any], raw_groups):
        if not isinstance(raw_group, dict):
            continue
        raw_group_map = cast(dict[object, Any], raw_group)
        if LEGACY_GROUP_MAPPED_MODEL_ID_KEY in raw_group_map:
            return [LEGACY_GROUP_MAPPED_MODEL_ID_WARNING]
    return []


@dataclass(frozen=True)
class ConfigStore:
    config_file: str

    def load_config_groups(self) -> tuple[list[dict[str, Any]], int]:
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, encoding="utf-8") as f:
                    config = yaml.safe_load(f)
                    if config and "config_groups" in config:
                        raw_groups = config["config_groups"]
                        config_groups: list[dict[str, Any]] = []
                        if isinstance(raw_groups, list):
                            raw_group_list = cast(list[Any], raw_groups)
                            for raw_group in raw_group_list:
                                normalized = _normalize_config_group(raw_group)
                                if normalized is not None:
                                    config_groups.append(normalized)
                        current_index = config.get("current_config_index", 0)
                        return config_groups, current_index
        except Exception:
            pass
        return [], 0

    def load_config_warnings(self) -> list[str]:
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, encoding="utf-8") as f:
                    config = yaml.safe_load(f)
                    return _collect_config_warnings(config)
        except Exception:
            pass
        return []

    def load_global_config(self) -> tuple[str, str]:
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, encoding="utf-8") as f:
                    config = yaml.safe_load(f)
                    if config:
                        mapped_model_id = config.get("mapped_model_id", "")
                        mtga_auth_key = config.get("mtga_auth_key", "")
                        return mapped_model_id, mtga_auth_key
        except Exception:
            pass
        return "", ""

    def load_proxy_settings(self) -> tuple[str, str]:
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, encoding="utf-8") as f:
                    config = yaml.safe_load(f)
                    if config:
                        proxy_mode = _normalize_proxy_mode(config.get("proxy_mode"))
                        trae_path = config.get("trae_path", "")
                        return proxy_mode, str(trae_path or "")
        except Exception:
            pass
        return DEFAULT_PROXY_MODE, ""

    def load_minimize_to_tray_on_close(self) -> bool:
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, encoding="utf-8") as f:
                    config = yaml.safe_load(f)
                    if config:
                        return _normalize_bool(
                            config.get("minimize_to_tray_on_close"),
                            default=DEFAULT_MINIMIZE_TO_TRAY_ON_CLOSE,
                        )
        except Exception:
            pass
        return DEFAULT_MINIMIZE_TO_TRAY_ON_CLOSE

    def load_model_routing_config(self) -> dict[str, Any]:
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, encoding="utf-8") as f:
                    config_obj: Any = yaml.safe_load(f) or {}
                    config = (
                        cast(dict[str, Any], config_obj)
                        if isinstance(config_obj, dict)
                        else {}
                    )
                    return serialize_model_routing_config(
                        build_model_routing_config(config)
                    )
        except Exception:
            pass
        return serialize_model_routing_config(build_model_routing_config({}))

    def save_model_routing_config(
        self,
        routing_config: dict[str, Any],
        *,
        proxy_mode: str | None = None,
        trae_path: str | None = None,
        minimize_to_tray_on_close: bool | None = None,
    ) -> bool:
        try:
            config_data: dict[str, Any] = {}
            if os.path.exists(self.config_file):
                with open(self.config_file, encoding="utf-8") as f:
                    config_data = yaml.safe_load(f) or {}

            normalized = normalize_model_routing_config(routing_config)
            for legacy_key in (
                "config_groups",
                "current_config_index",
                "mapped_model_id",
            ):
                config_data.pop(legacy_key, None)
            config_data.update(normalized)
            if proxy_mode is not None:
                config_data["proxy_mode"] = _normalize_proxy_mode(proxy_mode)
            if trae_path is not None:
                config_data["trae_path"] = str(trae_path or "").strip()
            if minimize_to_tray_on_close is not None:
                config_data["minimize_to_tray_on_close"] = _normalize_bool(
                    minimize_to_tray_on_close,
                    default=DEFAULT_MINIMIZE_TO_TRAY_ON_CLOSE,
                )

            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)

            with open(self.config_file, "w", encoding="utf-8") as f:
                yaml.dump(
                    config_data,
                    f,
                    default_flow_style=False,
                    allow_unicode=True,
                    indent=2,
                    sort_keys=False,
                )
            return True
        except Exception:
            return False

    def save_config_groups(  # noqa: PLR0913
        self,
        config_groups: list[dict[str, Any]],
        current_index: int = 0,
        mapped_model_id: str | None = None,
        mtga_auth_key: str | None = None,
        proxy_mode: str | None = None,
        trae_path: str | None = None,
        minimize_to_tray_on_close: bool | None = None,
    ) -> bool:
        try:
            config_data: dict[str, Any] = {}
            if os.path.exists(self.config_file):
                with open(self.config_file, encoding="utf-8") as f:
                    config_data = yaml.safe_load(f) or {}

            normalized_groups: list[dict[str, Any]] = []
            for config_group in config_groups:
                normalized = _normalize_config_group(config_group)
                if normalized is not None:
                    normalized_groups.append(normalized)

            config_data["config_groups"] = normalized_groups
            config_data["current_config_index"] = current_index

            if mapped_model_id is not None:
                config_data["mapped_model_id"] = mapped_model_id
            if mtga_auth_key is not None:
                config_data["mtga_auth_key"] = mtga_auth_key
            if proxy_mode is not None:
                config_data["proxy_mode"] = _normalize_proxy_mode(proxy_mode)
            if trae_path is not None:
                config_data["trae_path"] = str(trae_path or "").strip()
            if minimize_to_tray_on_close is not None:
                config_data["minimize_to_tray_on_close"] = _normalize_bool(
                    minimize_to_tray_on_close,
                    default=DEFAULT_MINIMIZE_TO_TRAY_ON_CLOSE,
                )

            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)

            with open(self.config_file, "w", encoding="utf-8") as f:
                yaml.dump(
                    config_data,
                    f,
                    default_flow_style=False,
                    allow_unicode=True,
                    indent=2,
                    sort_keys=False,
                )
            return True
        except Exception:
            return False

    def save_app_settings(self, *, minimize_to_tray_on_close: bool | None = None) -> bool:
        try:
            config_data: dict[str, Any] = {}
            if os.path.exists(self.config_file):
                with open(self.config_file, encoding="utf-8") as f:
                    config_data = yaml.safe_load(f) or {}

            if minimize_to_tray_on_close is not None:
                config_data["minimize_to_tray_on_close"] = _normalize_bool(
                    minimize_to_tray_on_close,
                    default=DEFAULT_MINIMIZE_TO_TRAY_ON_CLOSE,
                )

            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)

            with open(self.config_file, "w", encoding="utf-8") as f:
                yaml.dump(
                    config_data,
                    f,
                    default_flow_style=False,
                    allow_unicode=True,
                    indent=2,
                    sort_keys=False,
                )
            return True
        except Exception:
            return False

    def get_current_config(self) -> dict[str, Any]:
        config_groups, current_index = self.load_config_groups()
        if config_groups and 0 <= current_index < len(config_groups):
            return config_groups[current_index]
        return {}
