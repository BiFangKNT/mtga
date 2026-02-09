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
        except Exception:
            pass
        return [], 0

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

    def load_outbound_proxy_config(self) -> dict[str, Any]:
        default = {
            "outbound_proxy_enabled": False,
            "outbound_proxy_type": "http",
            "outbound_proxy_host": "",
            "outbound_proxy_port": 0,
            "outbound_proxy_username": "",
            "outbound_proxy_password": "",
        }
        try:
            if not os.path.exists(self.config_file):
                return default
            with open(self.config_file, encoding="utf-8") as f:
                config = yaml.safe_load(f) or {}
            enabled = config.get("outbound_proxy_enabled", False)
            if isinstance(enabled, bool):
                default["outbound_proxy_enabled"] = enabled
            elif isinstance(enabled, (int, float)):
                default["outbound_proxy_enabled"] = bool(enabled)
            elif isinstance(enabled, str):
                default["outbound_proxy_enabled"] = enabled.strip().lower() in {
                    "1",
                    "true",
                    "yes",
                    "on",
                }
            proxy_type = config.get("outbound_proxy_type", "http")
            if isinstance(proxy_type, str) and proxy_type.lower() in {
                "http",
                "https",
                "socks4",
                "socks5",
            }:
                default["outbound_proxy_type"] = proxy_type.lower()
            host = config.get("outbound_proxy_host", "")
            if isinstance(host, str):
                default["outbound_proxy_host"] = host
            port = config.get("outbound_proxy_port", 0)
            if isinstance(port, (int, float)):
                default["outbound_proxy_port"] = int(port)
            elif isinstance(port, str) and port.strip().isdigit():
                default["outbound_proxy_port"] = int(port.strip())
            username = config.get("outbound_proxy_username", "")
            if isinstance(username, str):
                default["outbound_proxy_username"] = username
            password = config.get("outbound_proxy_password", "")
            if isinstance(password, str):
                default["outbound_proxy_password"] = password
        except Exception:
            return default
        return default

    def save_config_groups(
        self,
        config_groups: list[dict[str, Any]],
        current_index: int = 0,
        mapped_model_id: str | None = None,
        mtga_auth_key: str | None = None,
        outbound_proxy: dict[str, Any] | None = None,
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
            if outbound_proxy is not None:
                for key in (
                    "outbound_proxy_enabled",
                    "outbound_proxy_type",
                    "outbound_proxy_host",
                    "outbound_proxy_port",
                    "outbound_proxy_username",
                    "outbound_proxy_password",
                ):
                    if key in outbound_proxy:
                        config_data[key] = outbound_proxy[key]

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
