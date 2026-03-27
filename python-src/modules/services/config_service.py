from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, cast

import yaml

from modules.proxy.proxy_config import (
    OPENAI_CHAT_COMPLETION_PROVIDER,
    normalize_model_discovery_strategy,
    normalize_provider,
)

DEFAULT_PROVIDER = OPENAI_CHAT_COMPLETION_PROVIDER
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
    }
)


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

    def save_config_groups(
        self,
        config_groups: list[dict[str, Any]],
        current_index: int = 0,
        mapped_model_id: str | None = None,
        mtga_auth_key: str | None = None,
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
