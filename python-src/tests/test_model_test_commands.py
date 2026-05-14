from __future__ import annotations

import asyncio
import unittest
from dataclasses import dataclass
from typing import Any
from unittest.mock import patch

from modules.actions.model_tests import ModelDiscoveryResult
from modules.proxy.proxy_config import GEMINI_PROVIDER
from mtga_app.commands.model_tests import (
    ModelRoutingTargetModelListPayload,
    ModelRoutingTargetTestPayload,
    register_model_test_commands,
)


@dataclass
class DummyConfigStore:
    config_groups: list[dict[str, Any]]
    current_index: int = 0
    save_calls: int = 0
    routing_config: dict[str, Any] | None = None

    def load_model_routing_config(self) -> dict[str, Any]:
        if self.routing_config is not None:
            return self.routing_config
        return {
            "schema_version": 2,
            "mtga_auth_key": "",
            "targets": [],
            "failover_pools": [],
            "published_models": [],
            "prompt_cache_bucket_id": "",
        }


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
    def test_model_routing_target_models_returns_discovered_strategy_for_unsaved_target(
        self,
    ) -> None:
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
            payload = ModelRoutingTargetModelListPayload(
                provider=GEMINI_PROVIDER,
                api_url="https://provider.example.com",
                model_id="gemini-2.5-pro",
                api_key="test-key",
                middle_route="/v1beta",
            )
            result = asyncio.run(commands.handlers["model_routing_target_models"](payload))

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

    def test_model_routing_target_test_uses_target_id(self) -> None:
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
            payload = ModelRoutingTargetTestPayload(target_id="target-main")
            result = asyncio.run(commands.handlers["model_routing_target_test"](payload))

        self.assertTrue(result["ok"])
        test_chat_completion.assert_called_once()
        called_group = test_chat_completion.call_args.args[0]
        self.assertEqual(called_group["api_url"], "https://provider.example.com")
        self.assertEqual(called_group["model_id"], "gemini-2.5-pro")


if __name__ == "__main__":
    unittest.main()
