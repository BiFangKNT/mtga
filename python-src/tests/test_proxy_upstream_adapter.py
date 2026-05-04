from __future__ import annotations

import json
import ssl
import tempfile
import unittest
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from unittest.mock import patch

import httpx
import yaml

from modules import mlitellm
from modules.mlitellm import APIConnectionError, RateLimitError
from modules.mlitellm.exceptions import BadRequestError
from modules.proxy.proxy_config import (
    GEMINI_NATIVE_X_GOOG_API_KEY_MODEL_DISCOVERY,
    OPENAI_CHAT_COMPLETION_PROVIDER,
    OPENAI_COMPATIBLE_MODEL_DISCOVERY,
    OPENAI_RESPONSE_PROVIDER,
    ProxyConfig,
    normalize_provider,
)
from modules.proxy.proxy_config import (
    build_proxy_config as build_runtime_proxy_config,
)
from modules.proxy.proxy_transport import ProxyTransport
from modules.proxy.upstream_adapter import (
    ANTHROPIC_PROVIDER,
    CHAT_COMPLETIONS_REQUEST_API,
    GEMINI_PROVIDER,
    RESPONSES_REQUEST_API,
    LiteLLMUpstreamAdapter,
    build_upstream_route,
    normalize_upstream_error,
)


@dataclass(frozen=True)
class DummyResourceManager:
    user_data_dir: str
    program_resource_dir: str

    def get_user_config_file(self) -> str:
        return str(Path(self.user_data_dir) / "mtga_config.yaml")


class DummyModelResponse:
    def __init__(self, payload: dict[str, Any]) -> None:
        self._payload = payload

    def model_dump(self, *, exclude_none: bool = False) -> dict[str, Any]:
        if exclude_none:
            return {key: value for key, value in self._payload.items() if value is not None}
        return dict(self._payload)


def _build_proxy_config(  # noqa: PLR0913
    *,
    provider: str = OPENAI_CHAT_COMPLETION_PROVIDER,
    target_api_base_url: str,
    target_model_id: str,
    middle_route: str | None = None,
    api_key: str = "test-key",
    model_discovery_strategy: str | None = None,
    prompt_cache_bucket_id: str = "",
    prompt_cache_enabled: bool = True,
) -> ProxyConfig:
    return ProxyConfig(
        provider=provider,
        target_api_base_url=target_api_base_url,
        middle_route=middle_route or "",
        custom_model_id="gpt-5",
        target_model_id=target_model_id,
        stream_mode=None,
        debug_mode=False,
        disable_ssl_strict_mode=False,
        api_key=api_key,
        mtga_auth_key="mtga-auth",
        model_discovery_strategy=model_discovery_strategy,
        prompt_cache_bucket_id=prompt_cache_bucket_id,
        prompt_cache_enabled=prompt_cache_enabled,
    )


def _build_bad_request_error(
    *,
    message: str,
    body: dict[str, Any] | None = None,
    model: str = "gpt-5",
) -> BadRequestError:
    request = httpx.Request("POST", "https://example.com/v1/chat/completions")
    response_body = body or {
        "error": {
            "code": None,
            "message": message,
            "param": None,
            "type": "invalid_request_error",
        }
    }
    response = httpx.Response(400, request=request, json=response_body)
    return BadRequestError(
        f"OpenAIException - {message}",
        model=model,
        llm_provider="openai",
        response=response,
        body=response_body,
    )


class UpstreamRouteTests(unittest.TestCase):
    def test_build_proxy_config_ignores_legacy_group_mapped_model_id(self) -> None:
        temp_dir = tempfile.mkdtemp(prefix="mtga-proxy-config-")
        resource_manager = DummyResourceManager(
            user_data_dir=temp_dir,
            program_resource_dir=temp_dir,
        )

        proxy_config = build_runtime_proxy_config(
            {
                "api_url": "https://api.openai.com",
                "model_id": "gpt-4o-mini",
                "api_key": "test-key",
                "mapped_model_id": "legacy-group-model",
            },
            resource_manager=resource_manager,  # type: ignore[arg-type]
            log_func=lambda _message: None,
        )

        self.assertIsNotNone(proxy_config)
        assert proxy_config is not None
        self.assertEqual(proxy_config.custom_model_id, "")
        self.assertEqual(proxy_config.target_model_id, "gpt-4o-mini")

    def test_openai_chat_completion_route_keeps_middle_route(self) -> None:
        route = build_upstream_route(
            _build_proxy_config(
                provider=OPENAI_CHAT_COMPLETION_PROVIDER,
                target_api_base_url="https://api.openai.com",
                target_model_id="gpt-4o-mini",
                middle_route="/v1",
            )
        )

        self.assertEqual(route.provider, OPENAI_CHAT_COMPLETION_PROVIDER)
        self.assertEqual(route.request_api, CHAT_COMPLETIONS_REQUEST_API)
        self.assertEqual(route.litellm_model, "gpt-4o-mini")
        self.assertEqual(route.base_url, "https://api.openai.com/v1")
        self.assertEqual(route.litellm_base_url, "https://api.openai.com/v1")
        self.assertTrue(route.middle_route_applied)
        self.assertFalse(route.middle_route_ignored)

    def test_openai_response_route_keeps_middle_route(self) -> None:
        route = build_upstream_route(
            _build_proxy_config(
                provider=OPENAI_RESPONSE_PROVIDER,
                target_api_base_url="https://api.openai.com",
                target_model_id="gpt-5",
                middle_route="/v1",
            )
        )

        self.assertEqual(route.provider, OPENAI_RESPONSE_PROVIDER)
        self.assertEqual(route.request_api, RESPONSES_REQUEST_API)
        self.assertEqual(route.litellm_model, "gpt-5")
        self.assertEqual(route.base_url, "https://api.openai.com/v1")
        self.assertEqual(route.litellm_base_url, "https://api.openai.com/v1")
        self.assertTrue(route.middle_route_applied)
        self.assertFalse(route.middle_route_ignored)

    def test_anthropic_route_uses_explicit_provider(self) -> None:
        route = build_upstream_route(
            _build_proxy_config(
                provider=ANTHROPIC_PROVIDER,
                target_api_base_url="https://api.anthropic.com",
                target_model_id="claude-3-7-sonnet-latest",
                middle_route="/custom",
            )
        )

        self.assertEqual(route.provider, ANTHROPIC_PROVIDER)
        self.assertEqual(route.request_api, CHAT_COMPLETIONS_REQUEST_API)
        self.assertEqual(route.litellm_model, "anthropic/claude-3-7-sonnet-latest")
        self.assertEqual(route.base_url, "https://api.anthropic.com/custom")
        self.assertEqual(route.litellm_base_url, "https://api.anthropic.com/custom")
        self.assertTrue(route.middle_route_applied)
        self.assertFalse(route.middle_route_ignored)

    def test_anthropic_openai_compatible_strategy_uses_openai_route(self) -> None:
        route = build_upstream_route(
            _build_proxy_config(
                provider=ANTHROPIC_PROVIDER,
                target_api_base_url="https://provider.example.com",
                target_model_id="claude-3-7-sonnet-latest",
                middle_route="/proxy/v1",
                model_discovery_strategy=OPENAI_COMPATIBLE_MODEL_DISCOVERY,
            )
        )

        self.assertEqual(route.provider, OPENAI_CHAT_COMPLETION_PROVIDER)
        self.assertEqual(route.request_api, CHAT_COMPLETIONS_REQUEST_API)
        self.assertEqual(route.litellm_model, "claude-3-7-sonnet-latest")
        self.assertEqual(route.base_url, "https://provider.example.com/proxy/v1")
        self.assertEqual(route.litellm_base_url, "https://provider.example.com/proxy/v1")
        self.assertTrue(route.middle_route_applied)
        self.assertFalse(route.middle_route_ignored)

    def test_gemini_route_uses_explicit_provider(self) -> None:
        route = build_upstream_route(
            _build_proxy_config(
                provider=GEMINI_PROVIDER,
                target_api_base_url="https://generativelanguage.googleapis.com",
                target_model_id="gemini-2.5-pro",
            )
        )

        self.assertEqual(route.provider, GEMINI_PROVIDER)
        self.assertEqual(route.request_api, CHAT_COMPLETIONS_REQUEST_API)
        self.assertEqual(route.litellm_model, "gemini/gemini-2.5-pro")
        self.assertEqual(route.base_url, "https://generativelanguage.googleapis.com/v1beta")
        self.assertEqual(
            route.litellm_base_url,
            "https://generativelanguage.googleapis.com/v1beta",
        )
        self.assertTrue(route.middle_route_applied)
        self.assertFalse(route.middle_route_ignored)

    def test_gemini_openai_compatible_strategy_rewrites_v1beta_to_v1(self) -> None:
        route = build_upstream_route(
            _build_proxy_config(
                provider=GEMINI_PROVIDER,
                target_api_base_url="https://provider.example.com",
                target_model_id="gemini-2.5-pro",
                middle_route="/proxy/google/v1beta",
                model_discovery_strategy=OPENAI_COMPATIBLE_MODEL_DISCOVERY,
            )
        )

        self.assertEqual(route.provider, OPENAI_CHAT_COMPLETION_PROVIDER)
        self.assertEqual(route.request_api, CHAT_COMPLETIONS_REQUEST_API)
        self.assertEqual(route.litellm_model, "gemini-2.5-pro")
        self.assertEqual(route.base_url, "https://provider.example.com/proxy/google/v1")
        self.assertEqual(route.litellm_base_url, "https://provider.example.com/proxy/google/v1")
        self.assertTrue(route.middle_route_applied)
        self.assertFalse(route.middle_route_ignored)

    def test_build_proxy_config_preserves_model_discovery_strategy(self) -> None:
        temp_dir = tempfile.mkdtemp(prefix="mtga-proxy-config-gemini-strategy-")
        resource_manager = DummyResourceManager(
            user_data_dir=temp_dir,
            program_resource_dir=temp_dir,
        )

        proxy_config = build_runtime_proxy_config(
            {
                "provider": GEMINI_PROVIDER,
                "api_url": "https://provider.example.com",
                "model_id": "gemini-2.5-pro",
                "api_key": "test-key",
                "model_discovery_strategy": GEMINI_NATIVE_X_GOOG_API_KEY_MODEL_DISCOVERY,
            },
            resource_manager=resource_manager,  # type: ignore[arg-type]
            log_func=lambda _message: None,
        )

        self.assertIsNotNone(proxy_config)
        assert proxy_config is not None
        self.assertEqual(
            proxy_config.model_discovery_strategy,
            GEMINI_NATIVE_X_GOOG_API_KEY_MODEL_DISCOVERY,
        )

    def test_build_proxy_config_generates_and_persists_prompt_cache_bucket_id(self) -> None:
        temp_dir = tempfile.mkdtemp(prefix="mtga-proxy-config-cache-bucket-")
        resource_manager = DummyResourceManager(
            user_data_dir=temp_dir,
            program_resource_dir=temp_dir,
        )

        first_proxy_config = build_runtime_proxy_config(
            {
                "api_url": "https://api.openai.com",
                "model_id": "gpt-4o-mini",
                "api_key": "test-key",
            },
            resource_manager=resource_manager,  # type: ignore[arg-type]
            log_func=lambda _message: None,
        )
        second_proxy_config = build_runtime_proxy_config(
            {
                "api_url": "https://api.openai.com",
                "model_id": "gpt-4o-mini",
                "api_key": "test-key",
            },
            resource_manager=resource_manager,  # type: ignore[arg-type]
            log_func=lambda _message: None,
        )

        self.assertIsNotNone(first_proxy_config)
        self.assertIsNotNone(second_proxy_config)
        assert first_proxy_config is not None
        assert second_proxy_config is not None
        self.assertTrue(first_proxy_config.prompt_cache_bucket_id)
        self.assertEqual(
            second_proxy_config.prompt_cache_bucket_id,
            first_proxy_config.prompt_cache_bucket_id,
        )

        with open(resource_manager.get_user_config_file(), encoding="utf-8") as f:
            persisted = yaml.safe_load(f) or {}

        self.assertEqual(
            persisted["prompt_cache_bucket_id"],
            first_proxy_config.prompt_cache_bucket_id,
        )

    def test_build_proxy_config_defaults_prompt_cache_enabled_to_false(self) -> None:
        temp_dir = tempfile.mkdtemp(prefix="mtga-proxy-config-prompt-cache-enabled-")
        resource_manager = DummyResourceManager(
            user_data_dir=temp_dir,
            program_resource_dir=temp_dir,
        )

        proxy_config = build_runtime_proxy_config(
            {
                "api_url": "https://api.openai.com",
                "model_id": "gpt-4o-mini",
                "api_key": "test-key",
            },
            resource_manager=resource_manager,  # type: ignore[arg-type]
            log_func=lambda _message: None,
        )

        self.assertIsNotNone(proxy_config)
        assert proxy_config is not None
        self.assertFalse(proxy_config.prompt_cache_enabled)

    def test_build_proxy_config_preserves_prompt_cache_enabled_false(self) -> None:
        temp_dir = tempfile.mkdtemp(prefix="mtga-proxy-config-prompt-cache-disabled-")
        resource_manager = DummyResourceManager(
            user_data_dir=temp_dir,
            program_resource_dir=temp_dir,
        )

        proxy_config = build_runtime_proxy_config(
            {
                "api_url": "https://api.openai.com",
                "model_id": "gpt-4o-mini",
                "api_key": "test-key",
                "prompt_cache_enabled": False,
            },
            resource_manager=resource_manager,  # type: ignore[arg-type]
            log_func=lambda _message: None,
        )

        self.assertIsNotNone(proxy_config)
        assert proxy_config is not None
        self.assertFalse(proxy_config.prompt_cache_enabled)

    def test_build_proxy_config_does_not_overwrite_invalid_global_config(self) -> None:
        temp_dir = tempfile.mkdtemp(prefix="mtga-proxy-config-invalid-global-")
        resource_manager = DummyResourceManager(
            user_data_dir=temp_dir,
            program_resource_dir=temp_dir,
        )
        invalid_config_text = "config_groups:\n  - name: broken\n    api_url: [\n"
        config_file = resource_manager.get_user_config_file()
        Path(config_file).write_text(invalid_config_text, encoding="utf-8")
        logs: list[str] = []

        proxy_config = build_runtime_proxy_config(
            {
                "api_url": "https://api.openai.com",
                "model_id": "gpt-4o-mini",
                "api_key": "test-key",
            },
            resource_manager=resource_manager,  # type: ignore[arg-type]
            log_func=logs.append,
        )

        self.assertIsNotNone(proxy_config)
        assert proxy_config is not None
        self.assertEqual(proxy_config.prompt_cache_bucket_id, "")
        self.assertEqual(
            Path(config_file).read_text(encoding="utf-8"),
            invalid_config_text,
        )
        self.assertTrue(any("加载全局配置失败" in item for item in logs))
        self.assertTrue(
            any("跳过 prompt cache bucket id 自动持久化" in item for item in logs)
        )

    def test_missing_provider_defaults_to_openai_chat_completion(self) -> None:
        route = build_upstream_route(
            _build_proxy_config(
                provider="",
                target_api_base_url="https://api.openai.com",
                target_model_id="gpt-4o-mini",
            )
        )

        self.assertEqual(route.provider, OPENAI_CHAT_COMPLETION_PROVIDER)
        self.assertEqual(route.litellm_model, "gpt-4o-mini")
        self.assertEqual(route.base_url, "https://api.openai.com/v1")
        self.assertEqual(route.litellm_base_url, "https://api.openai.com/v1")

    def test_legacy_openai_alias_maps_to_chat_completion_provider(self) -> None:
        self.assertEqual(normalize_provider("openai"), OPENAI_CHAT_COMPLETION_PROVIDER)


class ProxyTransportTests(unittest.TestCase):
    def setUp(self) -> None:
        temp_dir = tempfile.mkdtemp(prefix="mtga-proxy-transport-")
        resource_manager = DummyResourceManager(
            user_data_dir=temp_dir,
            program_resource_dir=temp_dir,
        )
        self.transport = ProxyTransport(
            resource_manager=resource_manager,  # type: ignore[arg-type]
            disable_ssl_strict_mode=False,
            log_func=lambda _message: None,
        )

    def tearDown(self) -> None:
        self.transport.close()

    def test_coerce_payload_dict_supports_model_dump_payloads(self) -> None:
        payload = {
            "id": "resp_123",
            "object": "response",
            "output": [
                {
                    "id": "msg_123",
                    "type": "message",
                    "role": "assistant",
                    "content": [{"type": "output_text", "text": "hello", "annotations": []}],
                }
            ],
        }

        response_dict = self.transport.coerce_payload_dict(DummyModelResponse(payload))

        self.assertEqual(response_dict, payload)

    def test_openai_event_is_serialized_to_sse(self) -> None:
        event = {
            "id": "chatcmpl_123",
            "created": 123,
            "model": "gpt-5",
            "choices": [
                {
                    "index": 0,
                    "delta": {"role": "assistant", "content": "你好"},
                    "finish_reason": None,
                }
            ],
        }

        chunk_bytes, finish_reason = self.transport.normalize_openai_event(
            event,
            1,
            model_name="gpt-5",
            log=lambda _message: None,
        )

        self.assertIsNone(finish_reason)
        decoded = chunk_bytes.decode("utf-8")
        self.assertTrue(decoded.startswith("data: "))
        payload_json = decoded.split("data: ", maxsplit=1)[1].strip()
        chunk_payload = json.loads(payload_json)
        self.assertEqual(chunk_payload["object"], "chat.completion.chunk")
        self.assertEqual(chunk_payload["choices"][0]["delta"]["content"], "你好")

    def test_openai_event_preserves_all_choices_usage_and_logprobs(self) -> None:
        event = {
            "id": "chatcmpl_456",
            "created": 456,
            "model": "gpt-5",
            "usage": {"prompt_tokens": 10, "completion_tokens": 2, "total_tokens": 12},
            "choices": [
                {
                    "index": 0,
                    "delta": {"role": "assistant", "content": "甲"},
                    "logprobs": {"content": [{"token": "甲", "logprob": -0.1}]},
                    "finish_reason": None,
                },
                {
                    "index": 1,
                    "delta": {"role": "assistant", "content": "乙"},
                    "logprobs": {"content": [{"token": "乙", "logprob": -0.2}]},
                    "finish_reason": "stop",
                },
            ],
        }

        chunk_bytes, finish_reason = self.transport.normalize_openai_event(
            event,
            1,
            model_name="gpt-5",
            log=lambda _message: None,
        )

        self.assertEqual(finish_reason, "stop")
        payload_json = chunk_bytes.decode("utf-8").split("data: ", maxsplit=1)[1].strip()
        chunk_payload = json.loads(payload_json)
        self.assertEqual(len(chunk_payload["choices"]), 2)
        self.assertEqual(chunk_payload["usage"]["total_tokens"], 12)
        self.assertEqual(
            chunk_payload["choices"][0]["logprobs"]["content"][0]["token"],
            "甲",
        )
        self.assertEqual(
            chunk_payload["choices"][1]["logprobs"]["content"][0]["token"],
            "乙",
        )

    def test_openai_event_preserves_empty_terminal_delta(self) -> None:
        event = {
            "id": "chatcmpl_789",
            "created": 789,
            "model": "gpt-5",
            "choices": [
                {
                    "index": 0,
                    "delta": {},
                    "finish_reason": "stop",
                }
            ],
        }

        chunk_bytes, finish_reason = self.transport.normalize_openai_event(
            event,
            2,
            model_name="gpt-5",
            log=lambda _message: None,
        )

        self.assertEqual(finish_reason, "stop")
        payload_json = chunk_bytes.decode("utf-8").split("data: ", maxsplit=1)[1].strip()
        chunk_payload = json.loads(payload_json)
        self.assertEqual(chunk_payload["choices"][0]["delta"], {})
        self.assertEqual(chunk_payload["choices"][0]["finish_reason"], "stop")

    def test_non_stream_chat_completion_can_be_simulated_as_chunks(self) -> None:
        response_payload = {
            "id": "chatcmpl_123",
            "object": "chat.completion",
            "created": 123,
            "model": "gpt-5",
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "reasoning_content": "先思考",
                        "content": "你好世界",
                        "tool_calls": [
                            {
                                "id": "call_1",
                                "type": "function",
                                "function": {
                                    "name": "lookup_weather",
                                    "arguments": "{\"city\":\"北京\"}",
                                },
                            }
                        ],
                    },
                    "finish_reason": "tool_calls",
                }
            ],
        }

        chunks = self.transport.build_chat_completion_stream_chunks(response_payload)

        self.assertGreaterEqual(len(chunks), 4)
        self.assertEqual(chunks[0]["choices"][0]["delta"]["role"], "assistant")
        self.assertTrue(
            any(
                chunk["choices"][0]["delta"].get("reasoning_content")
                for chunk in chunks[1:-1]
            )
        )
        self.assertTrue(
            any(chunk["choices"][0]["delta"].get("content") for chunk in chunks[1:-1])
        )
        self.assertTrue(
            any(chunk["choices"][0]["delta"].get("tool_calls") for chunk in chunks[1:-1])
        )
        tool_call_chunks = [
            chunk["choices"][0]["delta"]["tool_calls"]
            for chunk in chunks[1:-1]
            if chunk["choices"][0]["delta"].get("tool_calls")
        ]
        self.assertEqual(tool_call_chunks[0][0]["index"], 0)
        self.assertEqual(chunks[-1]["choices"][0]["finish_reason"], "tool_calls")
        self.assertEqual(chunks[-1]["choices"][0]["delta"], {})

    def test_non_stream_chat_completion_simulation_preserves_all_choices(self) -> None:
        response_payload = {
            "id": "chatcmpl_multi",
            "object": "chat.completion",
            "created": 456,
            "model": "gpt-5",
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": "甲",
                    },
                    "finish_reason": "stop",
                },
                {
                    "index": 1,
                    "message": {
                        "role": "assistant",
                        "reasoning_content": "先想",
                        "content": "乙",
                    },
                    "finish_reason": "length",
                },
            ],
        }

        chunks = self.transport.build_chat_completion_stream_chunks(response_payload)

        self.assertEqual(len(chunks[0]["choices"]), 2)
        self.assertEqual(
            [choice["index"] for choice in chunks[0]["choices"]],
            [0, 1],
        )
        self.assertTrue(
            any(
                chunk["choices"][0]["index"] == 1
                and chunk["choices"][0]["delta"].get("reasoning_content")
                for chunk in chunks[1:-1]
            )
        )
        self.assertTrue(
            any(
                chunk["choices"][0]["index"] == 1
                and chunk["choices"][0]["delta"].get("content")
                for chunk in chunks[1:-1]
            )
        )
        self.assertEqual(len(chunks[-1]["choices"]), 2)
        self.assertEqual(chunks[-1]["choices"][0]["delta"], {})
        self.assertEqual(chunks[-1]["choices"][0]["finish_reason"], "stop")
        self.assertEqual(chunks[-1]["choices"][1]["delta"], {})
        self.assertEqual(chunks[-1]["choices"][1]["finish_reason"], "length")

    def test_normalize_chat_completion_payload_strips_provider_prefix_from_model(self) -> None:
        payload = {
            "id": "chatcmpl_123",
            "object": "chat.completion",
            "model": "gemini/gemini-2.5-pro",
            "choices": [],
        }

        normalized = self.transport.normalize_chat_completion_payload(
            payload,
            provider=GEMINI_PROVIDER,
            fallback_model="gemini/gemini-2.5-pro",
        )

        self.assertIsNotNone(normalized)
        self.assertEqual(normalized["model"], "gemini-2.5-pro")


class LiteLLMUpstreamAdapterTests(unittest.TestCase):
    def test_openai_chat_completion_moves_compat_params_to_extra_body(self) -> None:
        adapter = LiteLLMUpstreamAdapter(
            disable_ssl_strict_mode=False,
            log_func=lambda _message: None,
        )
        route = build_upstream_route(
            _build_proxy_config(
                provider=OPENAI_CHAT_COMPLETION_PROVIDER,
                target_api_base_url="https://example.com",
                target_model_id="Qwen/Qwen3.5-27B",
            )
        )

        with patch(
            "modules.proxy.upstream_adapter.mlitellm.get_supported_openai_params",
            return_value=["verbosity", "web_search_options"],
        ), patch(
            "modules.proxy.upstream_adapter.mlitellm.completion",
            return_value={"id": "chatcmpl_123", "choices": []},
        ) as completion_mock:
            adapter.create_chat_completion(
                route=route,
                request_data={
                    "messages": [{"role": "user", "content": "你好"}],
                    "extra_body": {"return_reasoning": True},
                    "thinking": {"type": "enabled"},
                    "verbosity": "high",
                    "web_search_options": {"search_context_size": "low"},
                },
            )

        call_kwargs = completion_mock.call_args.kwargs
        self.assertEqual(call_kwargs["model"], "Qwen/Qwen3.5-27B")
        self.assertNotIn("thinking", call_kwargs)
        self.assertEqual(call_kwargs["verbosity"], "high")
        self.assertEqual(
            call_kwargs["web_search_options"],
            {"search_context_size": "low"},
        )
        self.assertEqual(
            call_kwargs["extra_body"],
            {
                "return_reasoning": True,
                "thinking": {"type": "enabled"},
            },
        )
        self.assertEqual(call_kwargs["base_url"], "https://example.com/v1")
        self.assertNotIn("api_base", call_kwargs)
        self.assertEqual(call_kwargs["custom_llm_provider"], "openai")

    def test_openai_chat_completion_keeps_allowed_openai_params_top_level(self) -> None:
        adapter = LiteLLMUpstreamAdapter(
            disable_ssl_strict_mode=False,
            log_func=lambda _message: None,
        )
        route = build_upstream_route(
            _build_proxy_config(
                provider=OPENAI_CHAT_COMPLETION_PROVIDER,
                target_api_base_url="https://example.com",
                target_model_id="Qwen/Qwen3.5-27B",
            )
        )

        with patch(
            "modules.proxy.upstream_adapter.mlitellm.get_supported_openai_params",
            return_value=["verbosity"],
        ), patch(
            "modules.proxy.upstream_adapter.mlitellm.completion",
            return_value={"id": "chatcmpl_123", "choices": []},
        ) as completion_mock:
            adapter.create_chat_completion(
                route=route,
                request_data={
                    "messages": [{"role": "user", "content": "你好"}],
                    "allowed_openai_params": ["thinking"],
                    "thinking": {"type": "enabled"},
                    "verbosity": "high",
                    "vendor_context": {"mode": "strict"},
                },
            )

        call_kwargs = completion_mock.call_args.kwargs
        self.assertEqual(
            call_kwargs["allowed_openai_params"],
            ["thinking"],
        )
        self.assertEqual(
            call_kwargs["thinking"],
            {"type": "enabled"},
        )
        self.assertEqual(call_kwargs["verbosity"], "high")
        self.assertEqual(
            call_kwargs["extra_body"],
            {"vendor_context": {"mode": "strict"}},
        )

    def test_openai_chat_completion_keeps_allowed_unsupported_standard_param(self) -> None:
        adapter = LiteLLMUpstreamAdapter(
            disable_ssl_strict_mode=False,
            log_func=lambda _message: None,
        )
        route = build_upstream_route(
            _build_proxy_config(
                provider=OPENAI_CHAT_COMPLETION_PROVIDER,
                target_api_base_url="https://example.com",
                target_model_id="gpt-5",
            )
        )

        with patch(
            "modules.proxy.upstream_adapter.mlitellm.get_supported_openai_params",
            return_value=["stream"],
        ), patch(
            "modules.proxy.upstream_adapter.mlitellm.completion",
            return_value={"id": "chatcmpl_123", "choices": []},
        ) as completion_mock:
            adapter.create_chat_completion(
                route=route,
                request_data={
                    "messages": [{"role": "user", "content": "你好"}],
                    "allowed_openai_params": ["temperature"],
                    "temperature": 0,
                },
            )

        call_kwargs = completion_mock.call_args.kwargs
        self.assertEqual(call_kwargs["allowed_openai_params"], ["temperature"])
        self.assertEqual(call_kwargs["temperature"], 0)

    def test_openai_response_uses_completion_bridge_with_base_url(self) -> None:
        adapter = LiteLLMUpstreamAdapter(
            disable_ssl_strict_mode=False,
            log_func=lambda _message: None,
        )
        route = build_upstream_route(
            _build_proxy_config(
                provider=OPENAI_RESPONSE_PROVIDER,
                target_api_base_url="https://example.com",
                target_model_id="gpt-5",
            )
        )

        with patch(
            "modules.proxy.upstream_adapter.mlitellm.completion",
            return_value={"id": "chatcmpl_123", "choices": []},
        ) as completion_mock:
            adapter.create_chat_completion(
                route=route,
                request_data={"messages": [{"role": "user", "content": "你好"}]},
            )

        call_kwargs = completion_mock.call_args.kwargs
        self.assertEqual(call_kwargs["base_url"], "https://example.com/v1")
        self.assertNotIn("api_base", call_kwargs)
        self.assertEqual(call_kwargs["custom_llm_provider"], "openai")
        self.assertEqual(call_kwargs["model"], "responses/gpt-5")
        self.assertEqual(call_kwargs["max_retries"], 0)
        self.assertEqual(call_kwargs["num_retries"], 0)

    def test_openai_chat_completion_retries_connection_error_before_success(self) -> None:
        logs: list[str] = []
        adapter = LiteLLMUpstreamAdapter(
            disable_ssl_strict_mode=False,
            log_func=logs.append,
        )
        route = build_upstream_route(
            _build_proxy_config(
                provider=OPENAI_CHAT_COMPLETION_PROVIDER,
                target_api_base_url="https://example.com",
                target_model_id="gpt-4o-mini",
            )
        )

        request = httpx.Request("POST", "https://example.com/v1/chat/completions")
        transient_error = APIConnectionError(
            "connect failed",
            llm_provider="openai",
            model="gpt-4o-mini",
            request=request,
        )
        transient_error.__cause__ = httpx.ConnectError(
            "connect failed",
            request=request,
        )
        with patch(
            "modules.proxy.upstream_adapter.mlitellm.completion",
            side_effect=[
                transient_error,
                {"id": "chatcmpl_123", "choices": []},
            ],
        ) as completion_mock:
            response = adapter.create_chat_completion(
                route=route,
                request_data={
                    "messages": [{"role": "user", "content": "你好"}],
                },
            )

        self.assertEqual(response["id"], "chatcmpl_123")
        self.assertEqual(completion_mock.call_count, 2)
        call_kwargs = completion_mock.call_args.kwargs
        self.assertEqual(call_kwargs["max_retries"], 0)
        self.assertEqual(call_kwargs["num_retries"], 0)
        self.assertIn(
            (
                "provider=openai_chat_completion request_api=chat_completions "
                "model=gpt-4o-mini 遇到建连阶段故障，准备重试: attempt=2/3 "
                "error=mlitellm.APIConnectionError: connect failed"
            ),
            logs,
        )

    def test_openai_chat_completion_does_not_retry_read_timeout_error(self) -> None:
        logs: list[str] = []
        adapter = LiteLLMUpstreamAdapter(
            disable_ssl_strict_mode=False,
            log_func=logs.append,
        )
        route = build_upstream_route(
            _build_proxy_config(
                provider=OPENAI_CHAT_COMPLETION_PROVIDER,
                target_api_base_url="https://example.com",
                target_model_id="gpt-4o-mini",
            )
        )

        request = httpx.Request("POST", "https://example.com/v1/chat/completions")
        timeout_error = APIConnectionError(
            "read timeout",
            llm_provider="openai",
            model="gpt-4o-mini",
            request=request,
        )
        timeout_error.__cause__ = httpx.ReadTimeout(
            "read timeout",
            request=request,
        )
        with patch(
            "modules.proxy.upstream_adapter.mlitellm.completion",
            side_effect=timeout_error,
        ) as completion_mock, self.assertRaises(APIConnectionError):
            adapter.create_chat_completion(
                route=route,
                request_data={
                    "messages": [{"role": "user", "content": "你好"}],
                },
            )

        self.assertEqual(completion_mock.call_count, 1)
        self.assertEqual(logs, [])

    def test_openai_chat_completion_does_not_retry_bad_request_error(self) -> None:
        adapter = LiteLLMUpstreamAdapter(
            disable_ssl_strict_mode=False,
            log_func=lambda _message: None,
        )
        route = build_upstream_route(
            _build_proxy_config(
                provider=OPENAI_CHAT_COMPLETION_PROVIDER,
                target_api_base_url="https://example.com",
                target_model_id="gpt-4o-mini",
            )
        )

        request = httpx.Request("POST", "https://example.com/v1/chat/completions")
        response = httpx.Response(400, request=request, text="invalid request")
        bad_request_error = BadRequestError(
            "invalid request",
            model="gpt-4o-mini",
            llm_provider="openai",
            response=response,
        )
        with patch(
            "modules.proxy.upstream_adapter.mlitellm.completion",
            side_effect=bad_request_error,
        ) as completion_mock, self.assertRaises(BadRequestError):
            adapter.create_chat_completion(
                route=route,
                request_data={
                    "messages": [{"role": "user", "content": "你好"}],
                },
            )

        self.assertEqual(completion_mock.call_count, 1)

    def test_openai_chat_completion_retries_by_dropping_only_nested_extra_body_field(self) -> None:
        logs: list[str] = []
        adapter = LiteLLMUpstreamAdapter(
            disable_ssl_strict_mode=False,
            log_func=logs.append,
        )
        route = build_upstream_route(
            _build_proxy_config(
                provider=OPENAI_CHAT_COMPLETION_PROVIDER,
                target_api_base_url="https://example.com",
                target_model_id="Qwen/Qwen3.5-27B",
            )
        )
        bad_request_error = _build_bad_request_error(
            message="Unsupported parameter: 'thinking.budget_tokens'",
            body={
                "error": {
                    "code": None,
                    "message": "Unsupported parameter: 'thinking.budget_tokens'",
                    "param": "thinking",
                    "type": "invalid_request_error",
                }
            },
            model="Qwen/Qwen3.5-27B",
        )

        with patch(
            "modules.proxy.upstream_adapter.mlitellm.get_supported_openai_params",
            return_value=["verbosity"],
        ), patch(
            "modules.proxy.upstream_adapter.mlitellm.completion",
            side_effect=[
                bad_request_error,
                {"id": "chatcmpl_retry_1", "choices": []},
                {"id": "chatcmpl_retry_2", "choices": []},
            ],
        ) as completion_mock:
            first_response = adapter.create_chat_completion(
                route=route,
                request_data={
                    "messages": [{"role": "user", "content": "你好"}],
                    "extra_body": {"return_reasoning": True},
                    "thinking": {"type": "enabled", "budget_tokens": 1024},
                    "verbosity": "high",
                },
            )
            second_response = adapter.create_chat_completion(
                route=route,
                request_data={
                    "messages": [{"role": "user", "content": "你好"}],
                    "extra_body": {"return_reasoning": True},
                    "thinking": {"type": "enabled", "budget_tokens": 1024},
                    "verbosity": "high",
                },
            )

        self.assertEqual(first_response["id"], "chatcmpl_retry_1")
        self.assertEqual(second_response["id"], "chatcmpl_retry_2")
        self.assertEqual(completion_mock.call_count, 3)

        first_attempt_kwargs = completion_mock.call_args_list[0].kwargs
        retry_attempt_kwargs = completion_mock.call_args_list[1].kwargs
        cached_attempt_kwargs = completion_mock.call_args_list[2].kwargs

        self.assertEqual(
            first_attempt_kwargs["extra_body"],
            {
                "return_reasoning": True,
                "thinking": {"type": "enabled", "budget_tokens": 1024},
            },
        )
        self.assertEqual(
            retry_attempt_kwargs["extra_body"],
            {
                "return_reasoning": True,
                "thinking": {"type": "enabled"},
            },
        )
        self.assertEqual(
            cached_attempt_kwargs["extra_body"],
            {
                "return_reasoning": True,
                "thinking": {"type": "enabled"},
            },
        )
        self.assertIn(
            (
                "⚠️ [临时兼容] provider=openai_chat_completion request_api=chat_completions "
                "model=Qwen/Qwen3.5-27B\n"
                "error=Unsupported parameter: 'thinking.budget_tokens'\n"
                "上游拒绝参数，自动剔除后重试: extra_body.thinking.budget_tokens"
            ),
            logs,
        )
        self.assertIn(
            (
                "⚠️ [临时兼容] provider=openai_chat_completion request_api=chat_completions "
                "model=Qwen/Qwen3.5-27B 命中上游不兼容参数缓存，已跳过: "
                "extra_body.thinking.budget_tokens"
            ),
            logs,
        )

    def test_openai_chat_completion_retries_inferred_nested_field_without_caching(self) -> None:
        logs: list[str] = []
        adapter = LiteLLMUpstreamAdapter(
            disable_ssl_strict_mode=False,
            log_func=logs.append,
        )
        route = build_upstream_route(
            _build_proxy_config(
                provider=OPENAI_CHAT_COMPLETION_PROVIDER,
                target_api_base_url="https://example.com",
                target_model_id="Qwen/Qwen3.5-27B",
            )
        )
        bad_request_error = _build_bad_request_error(
            message="'type' must be in [\"enabled\", \"disabled\", \"auto\"]",
            model="Qwen/Qwen3.5-27B",
        )

        with patch(
            "modules.proxy.upstream_adapter.mlitellm.get_supported_openai_params",
            return_value=["verbosity"],
        ), patch(
            "modules.proxy.upstream_adapter.mlitellm.completion",
            side_effect=[
                bad_request_error,
                {"id": "chatcmpl_retry_1", "choices": []},
                bad_request_error,
                {"id": "chatcmpl_retry_2", "choices": []},
            ],
        ) as completion_mock:
            first_response = adapter.create_chat_completion(
                route=route,
                request_data={
                    "messages": [{"role": "user", "content": "你好"}],
                    "extra_body": {"return_reasoning": True},
                    "thinking": {"type": "enabled"},
                    "verbosity": "high",
                },
            )
            second_response = adapter.create_chat_completion(
                route=route,
                request_data={
                    "messages": [{"role": "user", "content": "你好"}],
                    "extra_body": {"return_reasoning": True},
                    "thinking": {"type": "enabled"},
                    "verbosity": "high",
                },
            )

        self.assertEqual(first_response["id"], "chatcmpl_retry_1")
        self.assertEqual(second_response["id"], "chatcmpl_retry_2")
        self.assertEqual(completion_mock.call_count, 4)
        first_attempt_kwargs = completion_mock.call_args_list[0].kwargs
        retry_attempt_kwargs = completion_mock.call_args_list[1].kwargs
        second_attempt_kwargs = completion_mock.call_args_list[2].kwargs
        second_retry_attempt_kwargs = completion_mock.call_args_list[3].kwargs
        self.assertEqual(
            first_attempt_kwargs["extra_body"],
            {
                "return_reasoning": True,
                "thinking": {"type": "enabled"},
            },
        )
        self.assertEqual(
            retry_attempt_kwargs["extra_body"],
            {"return_reasoning": True},
        )
        self.assertEqual(
            second_attempt_kwargs["extra_body"],
            {
                "return_reasoning": True,
                "thinking": {"type": "enabled"},
            },
        )
        self.assertEqual(
            second_retry_attempt_kwargs["extra_body"],
            {"return_reasoning": True},
        )
        self.assertIn(
            (
                "⚠️ [临时兼容] provider=openai_chat_completion request_api=chat_completions "
                "model=Qwen/Qwen3.5-27B\n"
                "error='type' must be in [\"enabled\", \"disabled\", \"auto\"]\n"
                "根据上游报错临时剔除参数后重试（本次不缓存）: extra_body.thinking.type"
            ),
            logs,
        )
        self.assertFalse(
            any("命中上游不兼容参数缓存" in log for log in logs)
        )

    def test_openai_chat_completion_retries_by_dropping_explicit_unsupported_param(self) -> None:
        adapter = LiteLLMUpstreamAdapter(
            disable_ssl_strict_mode=False,
            log_func=lambda _message: None,
        )
        route = build_upstream_route(
            _build_proxy_config(
                provider=OPENAI_CHAT_COMPLETION_PROVIDER,
                target_api_base_url="https://example.com",
                target_model_id="gpt-5",
            )
        )
        bad_request_error = _build_bad_request_error(
            message="Unsupported parameter: 'verbosity'",
        )

        with patch(
            "modules.proxy.upstream_adapter.mlitellm.get_supported_openai_params",
            return_value=["verbosity"],
        ), patch(
            "modules.proxy.upstream_adapter.mlitellm.completion",
            side_effect=[
                bad_request_error,
                {"id": "chatcmpl_verbosity_retry", "choices": []},
            ],
        ) as completion_mock:
            response = adapter.create_chat_completion(
                route=route,
                request_data={
                    "messages": [{"role": "user", "content": "你好"}],
                    "verbosity": "high",
                },
            )

        self.assertEqual(response["id"], "chatcmpl_verbosity_retry")
        self.assertEqual(completion_mock.call_count, 2)
        first_attempt_kwargs = completion_mock.call_args_list[0].kwargs
        retry_attempt_kwargs = completion_mock.call_args_list[1].kwargs
        self.assertEqual(first_attempt_kwargs["verbosity"], "high")
        self.assertNotIn("verbosity", retry_attempt_kwargs)

    def test_openai_chat_completion_retries_scalar_invalid_value_without_caching(
        self,
    ) -> None:
        logs: list[str] = []
        adapter = LiteLLMUpstreamAdapter(
            disable_ssl_strict_mode=False,
            log_func=logs.append,
        )
        route = build_upstream_route(
            _build_proxy_config(
                provider=OPENAI_CHAT_COMPLETION_PROVIDER,
                target_api_base_url="https://example.com",
                target_model_id="gpt-5",
            )
        )
        bad_request_error = _build_bad_request_error(
            message="Invalid value for 'temperature': expected a number between 0 and 2",
        )

        with patch(
            "modules.proxy.upstream_adapter.mlitellm.completion",
            side_effect=[
                bad_request_error,
                {"id": "chatcmpl_temperature_retry", "choices": []},
                bad_request_error,
                {"id": "chatcmpl_temperature_retry_2", "choices": []},
            ],
        ) as completion_mock:
            first_response = adapter.create_chat_completion(
                route=route,
                request_data={
                    "messages": [{"role": "user", "content": "你好"}],
                    "temperature": 9,
                },
            )
            second_response = adapter.create_chat_completion(
                route=route,
                request_data={
                    "messages": [{"role": "user", "content": "你好"}],
                    "temperature": 9,
                },
            )

        self.assertEqual(first_response["id"], "chatcmpl_temperature_retry")
        self.assertEqual(second_response["id"], "chatcmpl_temperature_retry_2")
        self.assertEqual(completion_mock.call_count, 4)
        self.assertEqual(completion_mock.call_args_list[0].kwargs["temperature"], 9)
        self.assertNotIn("temperature", completion_mock.call_args_list[1].kwargs)
        self.assertEqual(completion_mock.call_args_list[2].kwargs["temperature"], 9)
        self.assertNotIn("temperature", completion_mock.call_args_list[3].kwargs)
        self.assertIn(
            (
                "⚠️ [临时兼容] provider=openai_chat_completion request_api=chat_completions "
                "model=gpt-5\n"
                "error=Invalid value for 'temperature': expected a number between 0 and 2\n"
                "根据上游报错临时剔除参数后重试（本次不缓存）: temperature"
            ),
            logs,
        )
        self.assertFalse(any("命中上游不兼容参数缓存" in log for log in logs))

    def test_openai_chat_completion_retries_explicit_nested_invalid_value_without_caching(
        self,
    ) -> None:
        logs: list[str] = []
        adapter = LiteLLMUpstreamAdapter(
            disable_ssl_strict_mode=False,
            log_func=logs.append,
        )
        route = build_upstream_route(
            _build_proxy_config(
                provider=OPENAI_CHAT_COMPLETION_PROVIDER,
                target_api_base_url="https://example.com",
                target_model_id="gpt-5",
            )
        )
        bad_request_error = _build_bad_request_error(
            message="Invalid value for 'response_format.strict': expected a boolean",
        )

        with patch(
            "modules.proxy.upstream_adapter.mlitellm.get_supported_openai_params",
            return_value=["response_format"],
        ), patch(
            "modules.proxy.upstream_adapter.mlitellm.completion",
            side_effect=[
                bad_request_error,
                {"id": "chatcmpl_response_format_retry", "choices": []},
                bad_request_error,
                {"id": "chatcmpl_response_format_retry_2", "choices": []},
            ],
        ) as completion_mock:
            first_response = adapter.create_chat_completion(
                route=route,
                request_data={
                    "messages": [{"role": "user", "content": "你好"}],
                    "response_format": {
                        "type": "json_schema",
                        "strict": "wrong",
                    },
                },
            )
            second_response = adapter.create_chat_completion(
                route=route,
                request_data={
                    "messages": [{"role": "user", "content": "你好"}],
                    "response_format": {
                        "type": "json_schema",
                        "strict": "wrong",
                    },
                },
            )

        self.assertEqual(first_response["id"], "chatcmpl_response_format_retry")
        self.assertEqual(second_response["id"], "chatcmpl_response_format_retry_2")
        self.assertEqual(completion_mock.call_count, 4)
        self.assertEqual(
            completion_mock.call_args_list[0].kwargs["response_format"],
            {
                "type": "json_schema",
                "strict": "wrong",
            },
        )
        self.assertEqual(
            completion_mock.call_args_list[1].kwargs["response_format"],
            {"type": "json_schema"},
        )
        self.assertEqual(
            completion_mock.call_args_list[2].kwargs["response_format"],
            {
                "type": "json_schema",
                "strict": "wrong",
            },
        )
        self.assertEqual(
            completion_mock.call_args_list[3].kwargs["response_format"],
            {"type": "json_schema"},
        )
        self.assertIn(
            (
                "⚠️ [临时兼容] provider=openai_chat_completion request_api=chat_completions "
                "model=gpt-5\n"
                "error=Invalid value for 'response_format.strict': expected a boolean\n"
                "根据上游报错临时剔除参数后重试（本次不缓存）: response_format.strict"
            ),
            logs,
        )
        self.assertFalse(any("命中上游不兼容参数缓存" in log for log in logs))

    def test_openai_chat_completion_cache_is_scoped_by_model(self) -> None:
        logs: list[str] = []
        adapter = LiteLLMUpstreamAdapter(
            disable_ssl_strict_mode=False,
            log_func=logs.append,
        )
        route_gpt5 = build_upstream_route(
            _build_proxy_config(
                provider=OPENAI_CHAT_COMPLETION_PROVIDER,
                target_api_base_url="https://example.com",
                target_model_id="gpt-5",
            )
        )
        route_gpt4o = build_upstream_route(
            _build_proxy_config(
                provider=OPENAI_CHAT_COMPLETION_PROVIDER,
                target_api_base_url="https://example.com",
                target_model_id="gpt-4o-mini",
            )
        )
        bad_request_error_gpt5 = _build_bad_request_error(
            message="Unsupported parameter: 'verbosity'",
            model="gpt-5",
        )
        bad_request_error_gpt4o = _build_bad_request_error(
            message="Unsupported parameter: 'verbosity'",
            model="gpt-4o-mini",
        )

        with patch(
            "modules.proxy.upstream_adapter.mlitellm.get_supported_openai_params",
            return_value=["verbosity"],
        ), patch(
            "modules.proxy.upstream_adapter.mlitellm.completion",
            side_effect=[
                bad_request_error_gpt5,
                {"id": "chatcmpl_gpt5", "choices": []},
                bad_request_error_gpt4o,
                {"id": "chatcmpl_gpt4o", "choices": []},
            ],
        ) as completion_mock:
            response_gpt5 = adapter.create_chat_completion(
                route=route_gpt5,
                request_data={
                    "messages": [{"role": "user", "content": "你好"}],
                    "verbosity": "high",
                },
            )
            response_gpt4o = adapter.create_chat_completion(
                route=route_gpt4o,
                request_data={
                    "messages": [{"role": "user", "content": "你好"}],
                    "verbosity": "high",
                },
            )

        self.assertEqual(response_gpt5["id"], "chatcmpl_gpt5")
        self.assertEqual(response_gpt4o["id"], "chatcmpl_gpt4o")
        self.assertEqual(completion_mock.call_count, 4)
        self.assertEqual(completion_mock.call_args_list[0].kwargs["verbosity"], "high")
        self.assertNotIn("verbosity", completion_mock.call_args_list[1].kwargs)
        self.assertEqual(completion_mock.call_args_list[2].kwargs["verbosity"], "high")
        self.assertNotIn("verbosity", completion_mock.call_args_list[3].kwargs)
        self.assertFalse(
            any("命中上游不兼容参数缓存" in log for log in logs)
        )

    def test_openai_chat_completion_cache_is_scoped_by_api_key(self) -> None:
        logs: list[str] = []
        adapter = LiteLLMUpstreamAdapter(
            disable_ssl_strict_mode=False,
            log_func=logs.append,
        )
        route_key_a = build_upstream_route(
            _build_proxy_config(
                provider=OPENAI_CHAT_COMPLETION_PROVIDER,
                target_api_base_url="https://example.com",
                target_model_id="gpt-5",
                api_key="key-a",
            )
        )
        route_key_b = build_upstream_route(
            _build_proxy_config(
                provider=OPENAI_CHAT_COMPLETION_PROVIDER,
                target_api_base_url="https://example.com",
                target_model_id="gpt-5",
                api_key="key-b",
            )
        )
        bad_request_error = _build_bad_request_error(
            message="Unsupported parameter: 'verbosity'",
            model="gpt-5",
        )

        with patch(
            "modules.proxy.upstream_adapter.mlitellm.get_supported_openai_params",
            return_value=["verbosity"],
        ), patch(
            "modules.proxy.upstream_adapter.mlitellm.completion",
            side_effect=[
                bad_request_error,
                {"id": "chatcmpl_key_a_retry", "choices": []},
                {"id": "chatcmpl_key_b_first_try", "choices": []},
            ],
        ) as completion_mock:
            response_key_a = adapter.create_chat_completion(
                route=route_key_a,
                request_data={
                    "messages": [{"role": "user", "content": "你好"}],
                    "verbosity": "high",
                },
            )
            response_key_b = adapter.create_chat_completion(
                route=route_key_b,
                request_data={
                    "messages": [{"role": "user", "content": "你好"}],
                    "verbosity": "high",
                },
            )

        self.assertEqual(response_key_a["id"], "chatcmpl_key_a_retry")
        self.assertEqual(response_key_b["id"], "chatcmpl_key_b_first_try")
        self.assertEqual(completion_mock.call_count, 3)
        self.assertEqual(completion_mock.call_args_list[0].kwargs["verbosity"], "high")
        self.assertNotIn("verbosity", completion_mock.call_args_list[1].kwargs)
        self.assertEqual(completion_mock.call_args_list[2].kwargs["verbosity"], "high")
        self.assertFalse(
            any("命中上游不兼容参数缓存" in log for log in logs)
        )

    def test_openai_chat_completion_persists_learned_rules_after_fallback_success(
        self,
    ) -> None:
        logs: list[str] = []
        adapter = LiteLLMUpstreamAdapter(
            disable_ssl_strict_mode=False,
            log_func=logs.append,
        )
        route = build_upstream_route(
            _build_proxy_config(
                provider=OPENAI_CHAT_COMPLETION_PROVIDER,
                target_api_base_url="https://example.com",
                target_model_id="gpt-5",
            )
        )
        bad_request_error_foo = _build_bad_request_error(
            message="Unsupported parameter: 'foo'",
            model="gpt-5",
        )
        bad_request_error_bar = _build_bad_request_error(
            message="Unsupported parameter: 'bar'",
            model="gpt-5",
        )
        bad_request_error_baz = _build_bad_request_error(
            message="Unsupported parameter: 'baz'",
            model="gpt-5",
        )

        with patch(
            "modules.proxy.upstream_adapter.mlitellm.get_supported_openai_params",
            return_value=[],
        ), patch(
            "modules.proxy.upstream_adapter.mlitellm.completion",
            side_effect=[
                bad_request_error_foo,
                bad_request_error_bar,
                bad_request_error_baz,
                {"id": "chatcmpl_fallback_success", "choices": []},
                {"id": "chatcmpl_cached_success", "choices": []},
            ],
        ) as completion_mock:
            first_response = adapter.create_chat_completion(
                route=route,
                request_data={
                    "messages": [{"role": "user", "content": "你好"}],
                    "foo": 1,
                    "bar": 2,
                    "baz": 3,
                },
            )
            second_response = adapter.create_chat_completion(
                route=route,
                request_data={
                    "messages": [{"role": "user", "content": "你好"}],
                    "foo": 1,
                    "bar": 2,
                    "baz": 3,
                },
            )

        self.assertEqual(first_response["id"], "chatcmpl_fallback_success")
        self.assertEqual(second_response["id"], "chatcmpl_cached_success")
        self.assertEqual(completion_mock.call_count, 5)
        self.assertEqual(
            completion_mock.call_args_list[0].kwargs["extra_body"],
            {"foo": 1, "bar": 2, "baz": 3},
        )
        self.assertEqual(
            completion_mock.call_args_list[1].kwargs["extra_body"],
            {"bar": 2, "baz": 3},
        )
        self.assertEqual(
            completion_mock.call_args_list[2].kwargs["extra_body"],
            {"baz": 3},
        )
        self.assertNotIn("extra_body", completion_mock.call_args_list[3].kwargs)
        self.assertNotIn("extra_body", completion_mock.call_args_list[4].kwargs)
        self.assertIn(
            (
                "⚠️ [临时兼容] provider=openai_chat_completion request_api=chat_completions "
                "model=gpt-5 命中上游不兼容参数缓存，已跳过: "
                "extra_body.bar, extra_body.baz, extra_body.foo"
            ),
            logs,
        )

    def test_openai_response_drops_unsupported_standard_params_before_litellm(self) -> None:
        logs: list[str] = []
        adapter = LiteLLMUpstreamAdapter(
            disable_ssl_strict_mode=False,
            log_func=logs.append,
        )
        route = build_upstream_route(
            _build_proxy_config(
                provider=OPENAI_RESPONSE_PROVIDER,
                target_api_base_url="https://example.com",
                target_model_id="gpt-5",
            )
        )

        with patch(
            "modules.proxy.upstream_adapter.mlitellm.get_supported_openai_params",
            return_value=["reasoning_effort", "stream"],
        ), patch(
            "modules.proxy.upstream_adapter.mlitellm.completion",
            return_value={"id": "chatcmpl_123", "choices": []},
        ) as completion_mock:
            adapter.create_chat_completion(
                route=route,
                request_data={
                    "messages": [{"role": "user", "content": "你好"}],
                    "temperature": 0,
                    "service_tier": "priority",
                    "store": True,
                    "reasoning_effort": "medium",
                },
            )

        call_kwargs = completion_mock.call_args.kwargs
        self.assertEqual(call_kwargs["model"], "responses/gpt-5")
        self.assertEqual(call_kwargs["reasoning_effort"], "medium")
        self.assertNotIn("temperature", call_kwargs)
        self.assertNotIn("service_tier", call_kwargs)
        self.assertNotIn("store", call_kwargs)
        self.assertIn(
            (
                "provider=openai_response request_api=responses model=gpt-5 "
                "已忽略不兼容参数: service_tier, store, temperature"
            ),
            logs,
        )

    def test_anthropic_uses_custom_base_url_without_openai_provider_override(self) -> None:
        adapter = LiteLLMUpstreamAdapter(
            disable_ssl_strict_mode=False,
            log_func=lambda _message: None,
        )
        route = build_upstream_route(
            _build_proxy_config(
                provider=ANTHROPIC_PROVIDER,
                target_api_base_url="https://anthropic-proxy.example.com",
                target_model_id="claude-3-7-sonnet-latest",
            )
        )

        with patch(
            "modules.proxy.upstream_adapter.mlitellm.completion",
            return_value={"id": "chatcmpl_123", "choices": []},
        ) as completion_mock:
            adapter.create_chat_completion(
                route=route,
                request_data={"messages": [{"role": "user", "content": "你好"}]},
            )

        call_kwargs = completion_mock.call_args.kwargs
        self.assertEqual(call_kwargs["base_url"], "https://anthropic-proxy.example.com")
        self.assertNotIn("api_base", call_kwargs)
        self.assertNotIn("custom_llm_provider", call_kwargs)

    def test_anthropic_custom_middle_route_preserves_prefix_before_messages(self) -> None:
        route = build_upstream_route(
            _build_proxy_config(
                provider=ANTHROPIC_PROVIDER,
                target_api_base_url="https://anthropic-proxy.example.com",
                target_model_id="claude-3-7-sonnet-latest",
                middle_route="/proxy/anthropic/v1",
            )
        )

        self.assertEqual(route.base_url, "https://anthropic-proxy.example.com/proxy/anthropic/v1")
        self.assertEqual(
            route.litellm_base_url,
            "https://anthropic-proxy.example.com/proxy/anthropic",
        )
        self.assertTrue(route.middle_route_applied)
        self.assertFalse(route.middle_route_ignored)

    def test_anthropic_preserves_thinking_param(self) -> None:
        adapter = LiteLLMUpstreamAdapter(
            disable_ssl_strict_mode=False,
            log_func=lambda _message: None,
        )
        route = build_upstream_route(
            _build_proxy_config(
                provider=ANTHROPIC_PROVIDER,
                target_api_base_url="https://anthropic-proxy.example.com",
                target_model_id="claude-3-5-haiku-20241022",
            )
        )

        with patch(
            "modules.proxy.upstream_adapter.mlitellm.completion",
            return_value={"id": "chatcmpl_123", "choices": []},
        ) as completion_mock:
            adapter.create_chat_completion(
                route=route,
                request_data={
                    "messages": [{"role": "user", "content": "你好"}],
                    "thinking": {"type": "enabled", "budget_tokens": 1024},
                },
            )

        call_kwargs = completion_mock.call_args.kwargs
        self.assertEqual(
            call_kwargs["thinking"],
            {"type": "enabled", "budget_tokens": 1024},
        )

    def test_anthropic_retries_litellm_local_unsupported_param_and_caches(self) -> None:
        logs: list[str] = []
        adapter = LiteLLMUpstreamAdapter(
            disable_ssl_strict_mode=False,
            log_func=logs.append,
        )
        route = build_upstream_route(
            _build_proxy_config(
                provider=ANTHROPIC_PROVIDER,
                target_api_base_url="https://anthropic-proxy.example.com",
                target_model_id="glm-4.7-flash",
            )
        )
        litellm_validation_error = Exception(
            "anthropic does not support parameters: ['thinking'], for model=glm-4.7-flash. "
            "To drop these, set `litellm.drop_params=True` or for proxy:\n\n"
            "`litellm_settings:\n drop_params: true`\n.\n"
            "If you want to use these params dynamically send "
            "allowed_openai_params=['thinking'] in your request."
        )

        with patch(
            "modules.proxy.upstream_adapter.mlitellm.get_supported_openai_params",
            return_value=["stream", "tools", "tool_choice"],
        ), patch(
            "modules.proxy.upstream_adapter.mlitellm.completion",
            side_effect=[
                litellm_validation_error,
                {"id": "chatcmpl_anthropic_retry", "choices": []},
                {"id": "chatcmpl_anthropic_cached", "choices": []},
            ],
        ) as completion_mock:
            first_response = adapter.create_chat_completion(
                route=route,
                request_data={
                    "messages": [{"role": "user", "content": "你好"}],
                    "thinking": {"type": "enabled", "budget_tokens": 1024},
                },
            )
            second_response = adapter.create_chat_completion(
                route=route,
                request_data={
                    "messages": [{"role": "user", "content": "你好"}],
                    "thinking": {"type": "enabled", "budget_tokens": 1024},
                },
            )

        self.assertEqual(first_response["id"], "chatcmpl_anthropic_retry")
        self.assertEqual(second_response["id"], "chatcmpl_anthropic_cached")
        self.assertEqual(completion_mock.call_count, 3)
        self.assertEqual(
            completion_mock.call_args_list[0].kwargs["thinking"],
            {"type": "enabled", "budget_tokens": 1024},
        )
        self.assertNotIn("thinking", completion_mock.call_args_list[1].kwargs)
        self.assertNotIn("thinking", completion_mock.call_args_list[2].kwargs)
        self.assertTrue(
            any(
                "error=anthropic does not support parameters: ['thinking'], "
                "for model=glm-4.7-flash."
                in log
                and "\n上游拒绝参数，自动剔除后重试: thinking" in log
                for log in logs
            )
        )
        self.assertIn(
            (
                "⚠️ [临时兼容] provider=anthropic request_api=chat_completions "
                "model=anthropic/glm-4.7-flash 命中上游不兼容参数缓存，已跳过: "
                "thinking"
            ),
            logs,
        )

    def test_anthropic_retries_multiple_litellm_local_unsupported_params_and_caches(
        self,
    ) -> None:
        logs: list[str] = []
        adapter = LiteLLMUpstreamAdapter(
            disable_ssl_strict_mode=False,
            log_func=logs.append,
        )
        route = build_upstream_route(
            _build_proxy_config(
                provider=ANTHROPIC_PROVIDER,
                target_api_base_url="https://anthropic-proxy.example.com",
                target_model_id="glm-4.7-flash",
            )
        )
        litellm_validation_error = Exception(
            "anthropic does not support parameters: ['foo', 'bar'], for model=glm-4.7-flash. "
            "To drop these, set `litellm.drop_params=True` or for proxy:\n\n"
            "`litellm_settings:\n drop_params: true`\n.\n"
            "If you want to use these params dynamically send "
            "allowed_openai_params=['foo', 'bar'] in your request."
        )

        with patch(
            "modules.proxy.upstream_adapter.mlitellm.get_supported_openai_params",
            return_value=["stream", "tools", "tool_choice"],
        ), patch(
            "modules.proxy.upstream_adapter.mlitellm.completion",
            side_effect=[
                litellm_validation_error,
                litellm_validation_error,
                {"id": "chatcmpl_anthropic_multi_retry", "choices": []},
                {"id": "chatcmpl_anthropic_multi_cached", "choices": []},
            ],
        ) as completion_mock:
            first_response = adapter.create_chat_completion(
                route=route,
                request_data={
                    "messages": [{"role": "user", "content": "你好"}],
                    "foo": 1,
                    "bar": 2,
                },
            )
            second_response = adapter.create_chat_completion(
                route=route,
                request_data={
                    "messages": [{"role": "user", "content": "你好"}],
                    "foo": 1,
                    "bar": 2,
                },
            )

        self.assertEqual(first_response["id"], "chatcmpl_anthropic_multi_retry")
        self.assertEqual(second_response["id"], "chatcmpl_anthropic_multi_cached")
        self.assertEqual(completion_mock.call_count, 4)
        self.assertEqual(
            {key: completion_mock.call_args_list[0].kwargs[key] for key in ("foo", "bar")},
            {"foo": 1, "bar": 2},
        )
        self.assertNotIn("foo", completion_mock.call_args_list[1].kwargs)
        self.assertEqual(completion_mock.call_args_list[1].kwargs["bar"], 2)
        self.assertNotIn("foo", completion_mock.call_args_list[2].kwargs)
        self.assertNotIn("bar", completion_mock.call_args_list[2].kwargs)
        self.assertNotIn("foo", completion_mock.call_args_list[3].kwargs)
        self.assertNotIn("bar", completion_mock.call_args_list[3].kwargs)
        self.assertIn(
            (
                "⚠️ [临时兼容] provider=anthropic request_api=chat_completions "
                "model=anthropic/glm-4.7-flash 命中上游不兼容参数缓存，已跳过: "
                "bar, foo"
            ),
            logs,
        )

    def test_anthropic_drops_unsupported_openai_params(self) -> None:
        adapter = LiteLLMUpstreamAdapter(
            disable_ssl_strict_mode=False,
            log_func=lambda _message: None,
        )
        route = build_upstream_route(
            _build_proxy_config(
                provider=ANTHROPIC_PROVIDER,
                target_api_base_url="https://anthropic-proxy.example.com",
                target_model_id="claude-3-5-haiku-20241022",
            )
        )

        with patch(
            "modules.proxy.upstream_adapter.mlitellm.get_supported_openai_params",
            return_value=["stream", "thinking", "tools", "tool_choice"],
        ), patch(
            "modules.proxy.upstream_adapter.mlitellm.completion",
            return_value={"id": "chatcmpl_123", "choices": []},
        ) as completion_mock:
            adapter.create_chat_completion(
                route=route,
                request_data={
                    "messages": [{"role": "user", "content": "你好"}],
                    "thinking": {"type": "enabled", "budget_tokens": 1024},
                    "stream_options": {"include_usage": True},
                    "service_tier": "priority",
                    "store": True,
                },
            )

        call_kwargs = completion_mock.call_args.kwargs
        self.assertEqual(
            call_kwargs["thinking"],
            {"type": "enabled", "budget_tokens": 1024},
        )
        self.assertNotIn("stream_options", call_kwargs)
        self.assertNotIn("service_tier", call_kwargs)
        self.assertNotIn("store", call_kwargs)

    def test_gemini_uses_custom_base_url_without_openai_provider_override(self) -> None:
        adapter = LiteLLMUpstreamAdapter(
            disable_ssl_strict_mode=False,
            log_func=lambda _message: None,
        )
        route = build_upstream_route(
            _build_proxy_config(
                provider=GEMINI_PROVIDER,
                target_api_base_url="https://gemini-proxy.example.com",
                target_model_id="gemini-2.5-pro",
            )
        )

        with patch(
            "modules.proxy.upstream_adapter.mlitellm.completion",
            return_value={"id": "chatcmpl_123", "choices": []},
        ) as completion_mock:
            adapter.create_chat_completion(
                route=route,
                request_data={"messages": [{"role": "user", "content": "你好"}]},
            )

        call_kwargs = completion_mock.call_args.kwargs
        self.assertEqual(call_kwargs["base_url"], "https://gemini-proxy.example.com/v1beta")
        self.assertNotIn("api_base", call_kwargs)
        self.assertNotIn("custom_llm_provider", call_kwargs)
        self.assertEqual(
            call_kwargs["extra_headers"],
            {"Authorization": "Bearer test-key"},
        )

    def test_gemini_x_goog_strategy_uses_x_goog_api_key_header(self) -> None:
        adapter = LiteLLMUpstreamAdapter(
            disable_ssl_strict_mode=False,
            log_func=lambda _message: None,
        )
        route = build_upstream_route(
            ProxyConfig(
                provider=GEMINI_PROVIDER,
                target_api_base_url="https://gemini-proxy.example.com",
                middle_route="",
                custom_model_id="gpt-5",
                target_model_id="gemini-2.5-pro",
                stream_mode=None,
                debug_mode=False,
                disable_ssl_strict_mode=False,
                api_key="test-key",
                mtga_auth_key="mtga-auth",
                model_discovery_strategy=GEMINI_NATIVE_X_GOOG_API_KEY_MODEL_DISCOVERY,
            )
        )

        with patch(
            "modules.proxy.upstream_adapter.mlitellm.completion",
            return_value={"id": "chatcmpl_123", "choices": []},
        ) as completion_mock:
            adapter.create_chat_completion(
                route=route,
                request_data={"messages": [{"role": "user", "content": "你好"}]},
            )

        call_kwargs = completion_mock.call_args.kwargs
        self.assertEqual(
            call_kwargs["extra_headers"],
            {"x-goog-api-key": "test-key"},
        )

    def test_gemini_explicit_v1_middle_route_is_preserved(self) -> None:
        route = build_upstream_route(
            _build_proxy_config(
                provider=GEMINI_PROVIDER,
                target_api_base_url="https://generativelanguage.googleapis.com",
                target_model_id="gemini-2.5-pro",
                middle_route="/v1",
            )
        )

        self.assertEqual(route.base_url, "https://generativelanguage.googleapis.com/v1")
        self.assertEqual(
            route.litellm_base_url,
            "https://generativelanguage.googleapis.com/v1",
        )

    def test_gemini_preserves_existing_auth_headers_when_adding_bearer(self) -> None:
        adapter = LiteLLMUpstreamAdapter(
            disable_ssl_strict_mode=False,
            log_func=lambda _message: None,
        )
        route = build_upstream_route(
            _build_proxy_config(
                provider=GEMINI_PROVIDER,
                target_api_base_url="https://gemini-proxy.example.com",
                target_model_id="gemini-2.5-pro",
            )
        )

        with patch(
            "modules.proxy.upstream_adapter.mlitellm.completion",
            return_value={"id": "chatcmpl_123", "choices": []},
        ) as completion_mock:
            adapter.create_chat_completion(
                route=route,
                request_data={
                    "messages": [{"role": "user", "content": "你好"}],
                    "extra_headers": {
                        "Authorization": "Bearer explicit-token",
                        "X-Test": "1",
                    },
                },
            )

        call_kwargs = completion_mock.call_args.kwargs
        self.assertEqual(
            call_kwargs["extra_headers"],
            {
                "Authorization": "Bearer explicit-token",
                "X-Test": "1",
            },
        )

    def test_gemini_preserves_thinking_param(self) -> None:
        adapter = LiteLLMUpstreamAdapter(
            disable_ssl_strict_mode=False,
            log_func=lambda _message: None,
        )
        route = build_upstream_route(
            _build_proxy_config(
                provider=GEMINI_PROVIDER,
                target_api_base_url="https://gemini-proxy.example.com",
                target_model_id="gemini-2.5-pro",
            )
        )

        with patch(
            "modules.proxy.upstream_adapter.mlitellm.completion",
            return_value={"id": "chatcmpl_123", "choices": []},
        ) as completion_mock:
            adapter.create_chat_completion(
                route=route,
                request_data={
                    "messages": [{"role": "user", "content": "你好"}],
                    "thinking": {"type": "enabled"},
                },
            )

        call_kwargs = completion_mock.call_args.kwargs
        self.assertEqual(call_kwargs["thinking"], {"type": "enabled"})

    def test_gemini_drops_unsupported_openai_params(self) -> None:
        adapter = LiteLLMUpstreamAdapter(
            disable_ssl_strict_mode=False,
            log_func=lambda _message: None,
        )
        route = build_upstream_route(
            _build_proxy_config(
                provider=GEMINI_PROVIDER,
                target_api_base_url="https://gemini-proxy.example.com",
                target_model_id="gemini-2.5-pro",
            )
        )

        with patch(
            "modules.proxy.upstream_adapter.mlitellm.get_supported_openai_params",
            return_value=["stream", "thinking", "tools", "response_format"],
        ), patch(
            "modules.proxy.upstream_adapter.mlitellm.completion",
            return_value={"id": "chatcmpl_123", "choices": []},
        ) as completion_mock:
            adapter.create_chat_completion(
                route=route,
                request_data={
                    "messages": [{"role": "user", "content": "你好"}],
                    "thinking": {"type": "enabled"},
                    "stream_options": {"include_usage": True},
                    "service_tier": "priority",
                    "store": True,
                },
            )

        call_kwargs = completion_mock.call_args.kwargs
        self.assertEqual(call_kwargs["thinking"], {"type": "enabled"})
        self.assertNotIn("stream_options", call_kwargs)
        self.assertNotIn("service_tier", call_kwargs)
        self.assertNotIn("store", call_kwargs)

    def test_openai_response_treats_unknown_params_as_openai_compatible_extra_body(self) -> None:
        adapter = LiteLLMUpstreamAdapter(
            disable_ssl_strict_mode=False,
            log_func=lambda _message: None,
        )
        route = build_upstream_route(
            _build_proxy_config(
                provider=OPENAI_RESPONSE_PROVIDER,
                target_api_base_url="https://example.com",
                target_model_id="gpt-5",
            )
        )

        with patch(
            "modules.proxy.upstream_adapter.mlitellm.get_supported_openai_params",
            return_value=["verbosity", "web_search_options"],
        ), patch(
            "modules.proxy.upstream_adapter.mlitellm.completion",
            return_value={"id": "chatcmpl_123", "choices": []},
        ) as completion_mock:
            adapter.create_chat_completion(
                route=route,
                request_data={
                    "messages": [{"role": "user", "content": "你好"}],
                    "extra_body": {"return_reasoning": True},
                    "thinking": {"type": "enabled"},
                    "verbosity": "medium",
                    "web_search_options": {"search_context_size": "medium"},
                },
            )

        call_kwargs = completion_mock.call_args.kwargs
        self.assertEqual(call_kwargs["model"], "responses/gpt-5")
        self.assertEqual(call_kwargs["verbosity"], "medium")
        self.assertEqual(
            call_kwargs["web_search_options"],
            {"search_context_size": "medium"},
        )
        self.assertEqual(
            call_kwargs["extra_body"],
            {
                "return_reasoning": True,
                "thinking": {"type": "enabled"},
            },
        )

    def test_openai_response_injects_prompt_cache_key(self) -> None:
        adapter = LiteLLMUpstreamAdapter(
            disable_ssl_strict_mode=False,
            log_func=lambda _message: None,
        )
        route = build_upstream_route(
            _build_proxy_config(
                provider=OPENAI_RESPONSE_PROVIDER,
                target_api_base_url="https://example.com",
                target_model_id="gpt-5",
                prompt_cache_bucket_id="abc123def4567890",
            )
        )

        with patch(
            "modules.proxy.upstream_adapter.mlitellm.completion",
            return_value={"id": "chatcmpl_123", "choices": []},
        ) as completion_mock:
            adapter.create_chat_completion(
                route=route,
                request_data={"messages": [{"role": "user", "content": "你好"}]},
            )

        call_kwargs = completion_mock.call_args.kwargs
        self.assertEqual(
            call_kwargs["prompt_cache_key"],
            "mtga:pc:v1:b:abc123def4567890",
        )

    def test_openai_response_preserves_explicit_prompt_cache_key(self) -> None:
        adapter = LiteLLMUpstreamAdapter(
            disable_ssl_strict_mode=False,
            log_func=lambda _message: None,
        )
        route = build_upstream_route(
            _build_proxy_config(
                provider=OPENAI_RESPONSE_PROVIDER,
                target_api_base_url="https://example.com",
                target_model_id="gpt-5",
                prompt_cache_bucket_id="abc123def4567890",
            )
        )

        with patch(
            "modules.proxy.upstream_adapter.mlitellm.completion",
            return_value={"id": "chatcmpl_123", "choices": []},
        ) as completion_mock:
            adapter.create_chat_completion(
                route=route,
                request_data={
                    "messages": [{"role": "user", "content": "你好"}],
                    "prompt_cache_key": "explicit-cache-key",
                },
            )

        call_kwargs = completion_mock.call_args.kwargs
        self.assertEqual(call_kwargs["prompt_cache_key"], "explicit-cache-key")

    def test_openai_response_does_not_inject_prompt_cache_key_when_disabled(self) -> None:
        adapter = LiteLLMUpstreamAdapter(
            disable_ssl_strict_mode=False,
            log_func=lambda _message: None,
        )
        route = build_upstream_route(
            _build_proxy_config(
                provider=OPENAI_RESPONSE_PROVIDER,
                target_api_base_url="https://example.com",
                target_model_id="gpt-5",
                prompt_cache_bucket_id="abc123def4567890",
                prompt_cache_enabled=False,
            )
        )

        with patch(
            "modules.proxy.upstream_adapter.mlitellm.completion",
            return_value={"id": "chatcmpl_123", "choices": []},
        ) as completion_mock:
            adapter.create_chat_completion(
                route=route,
                request_data={"messages": [{"role": "user", "content": "你好"}]},
            )

        call_kwargs = completion_mock.call_args.kwargs
        self.assertNotIn("prompt_cache_key", call_kwargs)

    def test_ssl_verify_is_passed_per_request_without_mutating_global_state(self) -> None:
        adapter = LiteLLMUpstreamAdapter(
            disable_ssl_strict_mode=True,
            log_func=lambda _message: None,
        )
        route = build_upstream_route(
            _build_proxy_config(
                provider=OPENAI_CHAT_COMPLETION_PROVIDER,
                target_api_base_url="https://example.com",
                target_model_id="gpt-4o-mini",
            )
        )

        original_ssl_verify = mlitellm.ssl_verify
        mlitellm.ssl_verify = "global-sentinel"
        try:
            with patch(
                "modules.proxy.upstream_adapter.mlitellm.completion",
                return_value={"id": "chatcmpl_123", "choices": []},
            ) as completion_mock:
                adapter.create_chat_completion(
                    route=route,
                    request_data={"messages": [{"role": "user", "content": "你好"}]},
                )
            self.assertEqual(mlitellm.ssl_verify, "global-sentinel")
        finally:
            mlitellm.ssl_verify = original_ssl_verify

        call_kwargs = completion_mock.call_args.kwargs
        ssl_verify = call_kwargs["ssl_verify"]
        self.assertIsInstance(ssl_verify, ssl.SSLContext)
        self.assertEqual(ssl_verify.verify_mode, ssl.CERT_REQUIRED)
        self.assertTrue(ssl_verify.check_hostname)
        strict_flag = getattr(ssl, "VERIFY_X509_STRICT", 0)
        if strict_flag and hasattr(ssl_verify, "verify_flags"):
            self.assertEqual(ssl_verify.verify_flags & strict_flag, 0)


class UpstreamErrorTests(unittest.TestCase):
    def test_connection_error_maps_to_503(self) -> None:
        request = httpx.Request("POST", "https://api.anthropic.com/v1/messages")
        error = APIConnectionError(
            "connect failed",
            llm_provider="anthropic",
            model="anthropic/claude-3-7-sonnet-latest",
            request=request,
        )

        info = normalize_upstream_error(error)

        self.assertEqual(info.status_code, 503)
        self.assertIn("Error contacting target API", info.response_body["error"])
        self.assertEqual(info.detail_text, "connect failed")
        self.assertIsNone(info.raw_response_text)
        self.assertIsNone(info.parsed_response_body)

    def test_http_status_error_keeps_upstream_status_code(self) -> None:
        request = httpx.Request("POST", "https://api.anthropic.com/v1/messages")
        response = httpx.Response(429, request=request, text="rate limited")
        error = RateLimitError(
            "too many requests",
            llm_provider="anthropic",
            model="anthropic/claude-3-7-sonnet-latest",
            response=response,
        )

        info = normalize_upstream_error(error)

        self.assertEqual(info.status_code, 429)
        self.assertEqual(info.response_body["error"], "Target API error: 429")
        self.assertEqual(info.response_body["details"], "too many requests")
        self.assertEqual(info.detail_text, "too many requests")
        self.assertIsNone(info.raw_response_text)
        self.assertIsNone(info.parsed_response_body)

    def test_http_status_error_parses_response_body_from_raw_response_text(self) -> None:
        request = httpx.Request("POST", "https://api.openai.com/v1/chat/completions")
        body = {
            "error": {
                "code": None,
                "message": "'type' must be in [\"enabled\", \"disabled\", \"auto\"]",
                "param": None,
                "type": "invalid_request_error",
            },
            "request_id": "b9393430-b194-9b50-bd81-f969ab0d3028",
        }
        response = httpx.Response(400, request=request, json=body)
        error = BadRequestError(
            "OpenAIException - 'type' must be in [\"enabled\", \"disabled\", \"auto\"]",
            model="gpt-5",
            llm_provider="openai",
            response=response,
            body=body,
        )

        info = normalize_upstream_error(error)

        self.assertEqual(info.status_code, 400)
        self.assertEqual(info.response_body, body)
        self.assertEqual(info.parsed_response_body, body)
        self.assertIsNotNone(info.raw_response_text)
        self.assertEqual(json.loads(info.raw_response_text or ""), body)
        self.assertEqual(info.detail_text, info.raw_response_text)
        self.assertIn(
            "\"request_id\":\"b9393430-b194-9b50-bd81-f969ab0d3028\"",
            info.log_message,
        )

    def test_http_status_error_restores_fallback_body_without_raw_response_text(self) -> None:
        request = httpx.Request("POST", "https://api.openai.com/v1/chat/completions")
        response = httpx.Response(
            400,
            request=request,
            headers={"x-request-id": "3f07cdeb-9258-4033-9845-db9df91f8d39"},
        )
        inner_error = {
            "code": None,
            "message": "'type' must be in [\"enabled\", \"disabled\", \"auto\"]",
            "param": None,
            "type": "invalid_request_error",
        }
        error = BadRequestError(
            "OpenAIException - 'type' must be in [\"enabled\", \"disabled\", \"auto\"]",
            model="gpt-5",
            llm_provider="openai",
            response=response,
            body=inner_error,
        )

        info = normalize_upstream_error(error)

        self.assertIsNone(info.raw_response_text)
        self.assertIsNone(info.parsed_response_body)
        self.assertEqual(
            info.response_body,
            {
                "error": inner_error,
                "request_id": "3f07cdeb-9258-4033-9845-db9df91f8d39",
            },
        )
        self.assertEqual(
            info.detail_text,
            json.dumps(
                {
                    "error": inner_error,
                    "request_id": "3f07cdeb-9258-4033-9845-db9df91f8d39",
                },
                ensure_ascii=False,
                separators=(",", ":"),
            ),
        )


if __name__ == "__main__":
    unittest.main()
