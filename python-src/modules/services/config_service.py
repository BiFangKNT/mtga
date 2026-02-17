from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import yaml


@dataclass(frozen=True)
class ConfigStore:
    config_file: str

    def load_config_groups(self) -> tuple[list[dict[str, Any]], int]:
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, encoding="utf-8") as f:
                    config = yaml.safe_load(f)
                    if config and "config_groups" in config:
                        config_groups = config["config_groups"]
                        current_index = config.get("current_config_index", 0)
                        return config_groups, current_index
        except Exception as e:
            print(f"Error loading config groups: {e}")
        return [], 0

    def load_global_config(self) -> tuple[str, str, str, bool, dict[str, Any] | None]:
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, encoding="utf-8") as f:
                    config = yaml.safe_load(f)
                    if config:
                        mapped_model_id = config.get("mapped_model_id", "")
                        mtga_auth_key = config.get("mtga_auth_key", "")
                        github_token = config.get("github_token", "")
                        disable_update_popup = config.get("disable_update_popup", False)
                        theme_config = config.get("theme_config", None)
                        return mapped_model_id, mtga_auth_key, github_token, disable_update_popup, theme_config
        except Exception as e:
            print(f"Error loading global config: {e}")
        return "", "", "", False, None

    def save_config_groups(
        self,
        config_groups: list[dict[str, Any]],
        current_index: int = 0,
        mapped_model_id: str | None = None,
        mtga_auth_key: str | None = None,
        github_token: str | None = None,
        disable_update_popup: bool | None = None,
        theme_config: dict[str, Any] | None = None,
    ) -> bool:
        try:
            config_data: dict[str, Any] = {}
            if os.path.exists(self.config_file):
                with open(self.config_file, encoding="utf-8") as f:
                    config_data = yaml.safe_load(f) or {}

            config_data["config_groups"] = config_groups
            config_data["current_config_index"] = current_index

            if mapped_model_id is not None:
                config_data["mapped_model_id"] = mapped_model_id
            if mtga_auth_key is not None:
                config_data["mtga_auth_key"] = mtga_auth_key
            if github_token is not None:
                config_data["github_token"] = github_token
            if disable_update_popup is not None:
                config_data["disable_update_popup"] = disable_update_popup
            if theme_config is not None:
                config_data["theme_config"] = theme_config

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
        except Exception as e:
            print(f"Error saving config groups: {e}")
            return False

    def get_current_config(self) -> dict[str, Any]:
        config_groups, current_index = self.load_config_groups()
        if config_groups and 0 <= current_index < len(config_groups):
            return config_groups[current_index]
        return {}
