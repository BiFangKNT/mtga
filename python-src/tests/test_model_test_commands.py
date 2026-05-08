from __future__ import annotations

import asyncio
import copy
import unittest
from dataclasses import dataclass
from typing import Any
from unittest.mock import patch

from modules.actions.model_tests import ModelDiscoveryResult
from modules.proxy.proxy_config import GEMINI_PROVIDER
from mtga_app.commands.model_tests import (
    ConfigGroupModelListPayload,
    ConfigGroupTestPayload,
    _persist_model_discovery_strategy_at_index,
    _persist_model_discovery_strategy_for_matching_group,
    register_model_test_commands,
)


@dataclass
class DummyConfigStore:
    config_groups: list[dict[str, Any]]
    current_index: int = 0
    save_calls: int = 0
    routing_config: dict[str, Any] | None = None

    def load_config_groups(self) -> tuple[list[dict[str, Any]], int]:
        return copy.deepcopy(self.config_groups), self.current_index

    def load_model_routing_config(self) -> dict[str, Any]:
        if self.routing_config is not None:
            return copy.deepcopy(self.routing_config)
        return {
            "schema_version": 2,
            "mtga_auth_key": "",
            "targets": [],
            "failover_pools": [],
            "published_models": [],
            "prompt_cache_bucket_id": "",
        }

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


@dataclass
class DummyCommands:
    handlers: dict[str, Any]

    def __init__(self) -> None:
        self.handlers = {}

    def command(self) -> Any:
        def _decorator(func: Any) -> Any:
            self.handlers[func.__name__] = func
            return func

        return _decorator

    def set_command(self, name: str, func: Any) -> None:
        self.handlers[name] = func


class ModelTestCommandPersistenceTests(unittest.TestCase):
    def test_config_group_models_returns_discovered_strategy_for_unsaved_group(self) -> None:
        store = DummyConfigStore(config_groups=[])
        commands = DummyCommands()

        with patch(
            "mtga_app.commands.model_tests._get_config_store",
            return_value=store,
        ), patch(
            "mtga_app.commands.model_tests.model_tests.fetch_model_list_result",
            return_value=ModelDiscoveryResult(
                model_ids=["gemini-2.5-flash", "gemini-2.5-pro"],
                ok=True,
                strategy_id="gemini_native_x_goog_api_key",
            ),
        ):
            register_model_test_commands(commands)  # type: ignore[arg-type]
            payload = ConfigGroupModelListPayload(
                provider=GEMINI_PROVIDER,
                api_url="https://provider.example.com",
                model_id="gemini-2.5-pro",
                api_key="test-key",
                middle_route="/v1beta",
            )
            result = asyncio.run(commands.handlers["config_group_models"](payload))

        self.assertTrue(result["ok"])
        self.assertEqual(
            result["details"]["models"],
            ["gemini-2.5-flash", "gemini-2.5-pro"],
        )
        self.assertEqual(
            result["details"]["strategy_id"],
            "gemini_native_x_goog_api_key",
        )
        self.assertEqual(store.save_calls, 0)

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

    def test_config_group_test_can_use_model_routing_target_id(self) -> None:
        store = DummyConfigStore(
            config_groups=[],
            routing_config={
                "schema_version": 2,
                "targets": [
                    {
                        "id": "target-main",
                        "provider": GEMINI_PROVIDER,
                        "api_base": "https://provider.example.com",
                        "upstream_model": "gemini-2.5-pro",
                        "api_key": "test-key",
                        "middle_route": "/v1beta",
                    }
                ],
                "failover_pools": [],
                "published_models": [],
            },
        )
        commands = DummyCommands()

        with patch(
            "mtga_app.commands.model_tests._get_config_store",
            return_value=store,
        ), patch(
            "mtga_app.commands.model_tests.model_tests.test_chat_completion",
        ) as test_chat_completion:
            register_model_test_commands(commands)  # type: ignore[arg-type]
            payload = ConfigGroupTestPayload(index=-1, target_id="target-main")
            result = asyncio.run(commands.handlers["config_group_test"](payload))

        self.assertTrue(result["ok"])
        test_chat_completion.assert_called_once()
        called_group = test_chat_completion.call_args.args[0]
        self.assertEqual(called_group["api_url"], "https://provider.example.com")
        self.assertEqual(called_group["model_id"], "gemini-2.5-pro")

    def test_matching_group_treats_api_url_with_and_without_trailing_slash_as_same(self) -> None:
        logs: list[str] = []
        store = DummyConfigStore(
            config_groups=[
                {
                    "provider": GEMINI_PROVIDER,
                    "api_url": "https://provider.example.com/",
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

    def test_matching_group_does_not_cross_pollute_different_api_keys(self) -> None:
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

        self.assertEqual(store.save_calls, 0)
        self.assertEqual(
            store.config_groups[0]["model_discovery_strategy"],
            "gemini_native_bearer",
        )
        self.assertNotIn("model_discovery_strategy", store.config_groups[1])
        self.assertFalse(any("已缓存模型发现策略" in item for item in logs))

    def test_index_persistence_reuses_cache_only_for_same_provider_api_key_and_middle_route(
        self,
    ) -> None:
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
        self.assertNotIn("model_discovery_strategy", store.config_groups[1])
        self.assertTrue(any("已缓存模型发现策略" in item for item in logs))


if __name__ == "__main__":
    unittest.main()
