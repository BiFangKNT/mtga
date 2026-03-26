from __future__ import annotations

import copy
import unittest
from dataclasses import dataclass
from typing import Any

from modules.proxy.proxy_config import GEMINI_PROVIDER
from mtga_app.commands.model_tests import (
    _persist_model_discovery_strategy_at_index,
    _persist_model_discovery_strategy_for_matching_group,
)


@dataclass
class DummyConfigStore:
    config_groups: list[dict[str, Any]]
    current_index: int = 0
    save_calls: int = 0

    def load_config_groups(self) -> tuple[list[dict[str, Any]], int]:
        return copy.deepcopy(self.config_groups), self.current_index

    def save_config_groups(
        self,
        config_groups: list[dict[str, Any]],
        current_index: int = 0,
        mapped_model_id: str | None = None,
        mtga_auth_key: str | None = None,
    ) -> bool:
        _ = (mapped_model_id, mtga_auth_key)
        self.config_groups = copy.deepcopy(config_groups)
        self.current_index = current_index
        self.save_calls += 1
        return True


class ModelTestCommandPersistenceTests(unittest.TestCase):
    def test_matching_group_treats_implicit_and_explicit_default_middle_route_as_same(self) -> None:
        logs: list[str] = []
        store = DummyConfigStore(
            config_groups=[
                {
                    "provider": GEMINI_PROVIDER,
                    "api_url": "https://provider.example.com",
                    "api_key": "test-key",
                    "model_id": "gemini-2.5-pro",
                }
            ]
        )

        _persist_model_discovery_strategy_for_matching_group(
            config_store=store,  # type: ignore[arg-type]
            request_group={
                "provider": GEMINI_PROVIDER,
                "api_url": "https://provider.example.com",
                "api_key": "test-key",
                "model_id": "gemini-2.5-pro",
                "middle_route": "/v1beta",
            },
            strategy_id="gemini_native_bearer",
            log_func=logs.append,
        )

        self.assertEqual(store.save_calls, 1)
        self.assertEqual(
            store.config_groups[0]["model_discovery_strategy"],
            "gemini_native_bearer",
        )
        self.assertTrue(any("已缓存模型发现策略" in item for item in logs))

    def test_matching_group_updates_all_groups_in_same_cache_scope(self) -> None:
        logs: list[str] = []
        store = DummyConfigStore(
            config_groups=[
                {
                    "provider": GEMINI_PROVIDER,
                    "api_url": "https://provider.example.com",
                    "api_key": "test-key-a",
                    "middle_route": "/v1beta",
                    "model_discovery_strategy": "gemini_native_bearer",
                },
                {
                    "provider": GEMINI_PROVIDER,
                    "api_url": "https://provider.example.com",
                    "api_key": "test-key-b",
                    "model_id": "gemini-2.5-pro",
                },
            ]
        )

        _persist_model_discovery_strategy_for_matching_group(
            config_store=store,  # type: ignore[arg-type]
            request_group={
                "provider": GEMINI_PROVIDER,
                "api_url": "https://provider.example.com",
                "api_key": "test-key-c",
                "model_id": "gemini-2.5-pro",
                "middle_route": "",
            },
            strategy_id="gemini_native_bearer",
            log_func=logs.append,
        )

        self.assertEqual(store.save_calls, 1)
        self.assertEqual(
            store.config_groups[0]["model_discovery_strategy"],
            "gemini_native_bearer",
        )
        self.assertEqual(
            store.config_groups[1]["model_discovery_strategy"],
            "gemini_native_bearer",
        )
        self.assertTrue(any("已缓存模型发现策略" in item for item in logs))

    def test_index_persistence_reuses_cache_for_same_provider_api_and_middle_route(self) -> None:
        logs: list[str] = []
        store = DummyConfigStore(
            config_groups=[
                {
                    "provider": GEMINI_PROVIDER,
                    "api_url": "https://provider.example.com",
                    "api_key": "test-key-a",
                    "middle_route": "/v1beta",
                    "model_id": "gemini-2.5-pro",
                },
                {
                    "provider": GEMINI_PROVIDER,
                    "api_url": "https://provider.example.com",
                    "api_key": "test-key-b",
                    "middle_route": "",
                    "model_id": "gemini-2.5-flash",
                },
            ]
        )

        _persist_model_discovery_strategy_at_index(
            config_store=store,  # type: ignore[arg-type]
            index=0,
            strategy_id="gemini_native_bearer",
            log_func=logs.append,
        )

        self.assertEqual(store.save_calls, 1)
        self.assertEqual(
            store.config_groups[0]["model_discovery_strategy"],
            "gemini_native_bearer",
        )
        self.assertEqual(
            store.config_groups[1]["model_discovery_strategy"],
            "gemini_native_bearer",
        )
        self.assertTrue(any("已缓存模型发现策略" in item for item in logs))


if __name__ == "__main__":
    unittest.main()
