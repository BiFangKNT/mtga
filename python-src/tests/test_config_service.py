from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import httpx
import yaml

from modules.proxy.model_routing import (
    build_model_routing_config,
    is_retryable_transport_error,
    normalize_model_routing_config,
    resolve_published_model,
)
from modules.services.config_service import (
    LEGACY_GROUP_MAPPED_MODEL_ID_WARNING,
    ConfigStore,
    _collect_config_warnings,
    _normalize_config_group,
)
from modules.services.proxy_orchestration import build_model_routing_runtime_config


class ConfigGroupNormalizationTests(unittest.TestCase):
    def test_normalize_config_group_strips_legacy_fields(self) -> None:
        normalized = _normalize_config_group(
            {
                "name": "legacy",
                "provider": "openai_chat_completion",
                "api_url": "https://api.openai.com",
                "model_id": "gpt-4o-mini",
                "api_key": "test-key",
                "mapped_model_id": "legacy-mapped",
                "target_model_id": "legacy-target",
            }
        )

        self.assertIsNotNone(normalized)
        assert normalized is not None
        self.assertNotIn("mapped_model_id", normalized)
        self.assertNotIn("target_model_id", normalized)
        self.assertEqual(normalized["model_id"], "gpt-4o-mini")
        self.assertEqual(normalized["provider"], "openai_chat_completion")

    def test_normalize_config_group_keeps_supported_fields(self) -> None:
        normalized = _normalize_config_group(
            {
                "name": "group-1",
                "provider": "gemini",
                "api_url": "https://provider.example.com",
                "model_id": "gemini-2.5-pro",
                "api_key": "test-key",
                "middle_route": "/v1beta",
                "model_discovery_strategy": "gemini_native_bearer",
                "prompt_cache_enabled": False,
            }
        )

        self.assertEqual(
            normalized,
            {
                "name": "group-1",
                "provider": "gemini",
                "api_url": "https://provider.example.com",
                "model_id": "gemini-2.5-pro",
                "api_key": "test-key",
                "middle_route": "/v1beta",
                "model_discovery_strategy": "gemini_native_bearer",
                "prompt_cache_enabled": False,
            },
        )

    def test_normalize_config_group_defaults_prompt_cache_enabled_to_false(self) -> None:
        normalized = _normalize_config_group(
            {
                "provider": "openai_chat_completion",
                "api_url": "https://api.openai.com",
                "model_id": "gpt-4o-mini",
                "api_key": "test-key",
            }
        )

        self.assertIsNotNone(normalized)
        assert normalized is not None
        self.assertFalse(normalized["prompt_cache_enabled"])

    def test_collect_config_warnings_reports_legacy_group_mapped_model_id(self) -> None:
        warnings = _collect_config_warnings(
            {
                "config_groups": [
                    {
                        "provider": "openai_chat_completion",
                        "api_url": "https://api.openai.com",
                        "model_id": "gpt-4o-mini",
                        "mapped_model_id": "legacy-group-model",
                        "api_key": "test-key",
                    }
                ],
                "current_config_index": 0,
            }
        )

        self.assertEqual(warnings, [LEGACY_GROUP_MAPPED_MODEL_ID_WARNING])

    def test_collect_config_warnings_is_empty_for_current_schema(self) -> None:
        warnings = _collect_config_warnings(
            {
                "config_groups": [
                    {
                        "provider": "openai_chat_completion",
                        "api_url": "https://api.openai.com",
                        "model_id": "gpt-4o-mini",
                        "api_key": "test-key",
                    }
                ],
                "mapped_model_id": "gpt-5",
                "current_config_index": 0,
            }
        )

        self.assertEqual(warnings, [])


class AppSettingsConfigTests(unittest.TestCase):
    def test_minimize_to_tray_on_close_round_trips_without_rewriting_routing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            config_file = Path(temp_dir) / "mtga_config.yaml"
            config_file.write_text(
                yaml.safe_dump(
                    {
                        "schema_version": 2,
                        "targets": [
                            {
                                "id": "main",
                                "provider": "openai_chat_completion",
                                "api_base": "https://api.example.com",
                                "upstream_model": "gpt-5",
                                "api_key": "key",
                            }
                        ],
                    },
                    allow_unicode=True,
                    sort_keys=False,
                ),
                encoding="utf-8",
            )
            store = ConfigStore(str(config_file))

            self.assertFalse(store.load_minimize_to_tray_on_close())
            self.assertTrue(store.save_app_settings(minimize_to_tray_on_close=True))
            self.assertTrue(store.load_minimize_to_tray_on_close())

            saved = yaml.safe_load(config_file.read_text(encoding="utf-8"))
            self.assertEqual(saved["targets"][0]["id"], "main")
            self.assertTrue(saved["minimize_to_tray_on_close"])


class ModelRoutingConfigTests(unittest.TestCase):
    def test_migrate_legacy_config_to_model_routing(self) -> None:
        normalized = normalize_model_routing_config(
            {
                "config_groups": [
                    {
                        "name": "Main",
                        "provider": "anthropic",
                        "api_url": "https://anthropic.example.com/",
                        "model_id": "claude-3-7-sonnet",
                        "api_key": "upstream-key",
                        "middle_route": "/v1",
                        "prompt_cache_enabled": True,
                    },
                    {
                        "name": "Backup",
                        "provider": "gemini",
                        "api_url": "https://gemini.example.com",
                        "model_id": "gemini-2.5-pro",
                        "api_key": "backup-key",
                    },
                ],
                "current_config_index": 0,
                "mapped_model_id": "sonnet-proxy",
                "mtga_auth_key": "",
            }
        )

        self.assertEqual(normalized["schema_version"], 2)
        self.assertEqual(normalized["mtga_auth_key"], "")
        self.assertEqual(len(normalized["targets"]), 2)
        self.assertEqual(normalized["targets"][0]["id"], "target-1")
        self.assertEqual(normalized["targets"][0]["display_name"], "Main")
        self.assertEqual(normalized["targets"][0]["api_base"], "https://anthropic.example.com")
        self.assertEqual(normalized["published_models"][0]["name"], "sonnet-proxy")
        self.assertEqual(normalized["published_models"][0]["primary_target_id"], "target-1")
        self.assertEqual(normalized["targets"][0]["request_body_patch"], [])

    def test_legacy_config_without_mapped_model_does_not_publish_model(self) -> None:
        normalized = normalize_model_routing_config(
            {
                "config_groups": [
                    {
                        "provider": "openai_chat_completion",
                        "api_url": "https://api.example.com",
                        "model_id": "gpt-5",
                        "api_key": "key",
                    }
                ]
            }
        )

        self.assertEqual(len(normalized["targets"]), 1)
        self.assertEqual(normalized["published_models"], [])

    def test_resolve_published_model_uses_exact_enabled_model(self) -> None:
        config = build_model_routing_config(
            {
                "schema_version": 2,
                "targets": [
                    {
                        "id": "main",
                        "provider": "openai_chat_completion",
                        "api_base": "https://api.example.com",
                        "upstream_model": "gpt-5",
                        "api_key": "key",
                    }
                ],
                "published_models": [
                    {
                        "name": "public-gpt",
                        "enabled": True,
                        "primary_target_id": "main",
                    },
                    {
                        "name": "disabled-gpt",
                        "enabled": False,
                        "primary_target_id": "main",
                    },
                ],
            }
        )

        resolved = resolve_published_model(config, "public-gpt")
        self.assertFalse(hasattr(resolved, "status_code"))
        self.assertEqual(resolved.primary_target.id, "main")  # type: ignore[union-attr]

        missing = resolve_published_model(config, "disabled-gpt")
        self.assertEqual(missing.status_code, 404)  # type: ignore[union-attr]

    def test_target_request_body_patch_is_preserved(self) -> None:
        config = build_model_routing_config(
            {
                "schema_version": 2,
                "targets": [
                    {
                        "id": "main",
                        "provider": "openai_chat_completion",
                        "api_base": "https://api.example.com",
                        "upstream_model": "gpt-5",
                        "api_key": "key",
                        "request_body_patch": [
                            {
                                "op": "add",
                                "path": "/thinking",
                                "value": {"type": "enabled"},
                            }
                        ],
                    }
                ],
                "published_models": [
                    {
                        "name": "public-gpt",
                        "enabled": True,
                        "primary_target_id": "main",
                    }
                ],
            }
        )

        self.assertEqual(
            config.targets[0].request_body_patch,
            ({"op": "add", "path": "/thinking", "value": {"type": "enabled"}},),
        )

    def test_runtime_config_requires_enabled_published_model(self) -> None:
        runtime_config = build_model_routing_runtime_config(
            load_model_routing_config=lambda: {
                "schema_version": 2,
                "targets": [
                    {
                        "id": "main",
                        "provider": "openai_chat_completion",
                        "api_base": "https://api.example.com",
                        "upstream_model": "gpt-5",
                        "api_key": "key",
                    }
                ],
                "published_models": [
                    {
                        "name": "disabled-gpt",
                        "enabled": False,
                        "primary_target_id": "main",
                    }
                ],
            },
            debug_mode=False,
            disable_ssl_strict_mode=False,
            stream_mode=None,
        )

        self.assertIsNone(runtime_config)

    def test_failover_transport_retry_only_covers_connect_stage(self) -> None:
        self.assertTrue(is_retryable_transport_error(httpx.ConnectError("connect failed")))
        self.assertTrue(is_retryable_transport_error(httpx.ConnectTimeout("connect timeout")))
        self.assertTrue(is_retryable_transport_error(httpx.ProxyError("proxy failed")))

        self.assertFalse(is_retryable_transport_error(httpx.ReadTimeout("read timeout")))
        self.assertFalse(is_retryable_transport_error(httpx.RemoteProtocolError("broken stream")))
        self.assertFalse(is_retryable_transport_error(httpx.TransportError("generic transport")))


if __name__ == "__main__":
    unittest.main()
