from __future__ import annotations

import json
import ssl
import tempfile
import unittest
from dataclasses import dataclass
from typing import Any
from unittest.mock import patch

import httpx
import litellm
from litellm import APIConnectionError, RateLimitError

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
    _sanitize_empty_gemini_block_reason,
    build_upstream_route,
    normalize_upstream_error,
)


@dataclass(frozen=True)
class DummyResourceManager:
    user_data_dir: str
    program_resource_dir: str


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
    def test_adapter_init_does_not_apply_litellm_compat_patches(self) -> None:
        with patch(
            "modules.proxy.upstream_adapter.apply_litellm_compat_patches"
        ) as compat_patch_mock:
            LiteLLMUpstreamAdapter(
                disable_ssl_strict_mode=False,
                log_func=lambda _message: None,
            )

        compat_patch_mock.assert_not_called()

    def test_openai_request_does_not_apply_gemini_compat_patches(self) -> None:
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

        with patch(
            "modules.proxy.upstream_adapter.apply_litellm_compat_patches"
        ) as compat_patch_mock, patch(
            "modules.proxy.upstream_adapter.litellm.completion",
            return_value={"id": "chatcmpl_123", "choices": []},
        ):
            adapter.create_chat_completion(
                route=route,
                request_data={"messages": [{"role": "user", "content": "你好"}]},
            )

        compat_patch_mock.assert_not_called()

    def test_gemini_request_applies_litellm_compat_patches(self) -> None:
        def log_func(_message: str) -> None:
            return

        adapter = LiteLLMUpstreamAdapter(
            disable_ssl_strict_mode=False,
            log_func=log_func,
        )
        route = build_upstream_route(
            _build_proxy_config(
                provider=GEMINI_PROVIDER,
                target_api_base_url="https://gemini-proxy.example.com",
                target_model_id="gemini-2.5-pro",
            )
        )

        with patch.dict(
            "modules.proxy.upstream_adapter._litellm_compat_patch_state",
            {"applied": False},
        ), patch(
            "modules.proxy.upstream_adapter.apply_litellm_compat_patches"
        ) as compat_patch_mock, patch(
            "modules.proxy.upstream_adapter.litellm.completion",
            return_value={"id": "chatcmpl_123", "choices": []},
        ):
            adapter.create_chat_completion(
                route=route,
                request_data={"messages": [{"role": "user", "content": "你好"}]},
            )

        compat_patch_mock.assert_called_once_with(log_func=log_func)

    def test_gemini_empty_block_reason_is_sanitized(self) -> None:
        payload = {
            "promptFeedback": {
                "blockReason": "",
                "blockReasonMessage": "",
            },
            "candidates": [
                {
                    "content": {
                        "role": "model",
                        "parts": [{"text": "OK"}],
                    },
                    "finishReason": "STOP",
                }
            ],
        }

        sanitized = _sanitize_empty_gemini_block_reason(payload)

        self.assertNotIn("promptFeedback", sanitized)
        self.assertEqual(
            sanitized["candidates"][0]["content"]["parts"][0]["text"],
            "OK",
        )

    def test_gemini_real_block_reason_is_preserved(self) -> None:
        payload = {
            "promptFeedback": {
                "blockReason": "SAFETY",
                "blockReasonMessage": "blocked",
            }
        }

        sanitized = _sanitize_empty_gemini_block_reason(payload)

        self.assertEqual(
            sanitized["promptFeedback"],
            {
                "blockReason": "SAFETY",
                "blockReasonMessage": "blocked",
            },
        )

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
            "modules.proxy.upstream_adapter.litellm.get_supported_openai_params",
            return_value=["verbosity", "web_search_options"],
        ), patch(
            "modules.proxy.upstream_adapter.litellm.completion",
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
            "modules.proxy.upstream_adapter.litellm.get_supported_openai_params",
            return_value=["verbosity"],
        ), patch(
            "modules.proxy.upstream_adapter.litellm.completion",
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
            "modules.proxy.upstream_adapter.litellm.completion",
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
            "modules.proxy.upstream_adapter.litellm.completion",
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
            "modules.proxy.upstream_adapter.litellm.completion",
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
            "modules.proxy.upstream_adapter.litellm.get_supported_openai_params",
            return_value=["stream", "thinking", "tools", "tool_choice"],
        ), patch(
            "modules.proxy.upstream_adapter.litellm.completion",
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
            "modules.proxy.upstream_adapter.litellm.completion",
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
            "modules.proxy.upstream_adapter.litellm.completion",
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
            "modules.proxy.upstream_adapter.litellm.completion",
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
            "modules.proxy.upstream_adapter.litellm.completion",
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
            "modules.proxy.upstream_adapter.litellm.get_supported_openai_params",
            return_value=["stream", "thinking", "tools", "response_format"],
        ), patch(
            "modules.proxy.upstream_adapter.litellm.completion",
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
            "modules.proxy.upstream_adapter.litellm.get_supported_openai_params",
            return_value=["verbosity", "web_search_options"],
        ), patch(
            "modules.proxy.upstream_adapter.litellm.completion",
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

        original_ssl_verify = litellm.ssl_verify
        litellm.ssl_verify = "global-sentinel"
        try:
            with patch(
                "modules.proxy.upstream_adapter.litellm.completion",
                return_value={"id": "chatcmpl_123", "choices": []},
            ) as completion_mock:
                adapter.create_chat_completion(
                    route=route,
                    request_data={"messages": [{"role": "user", "content": "你好"}]},
                )
            self.assertEqual(litellm.ssl_verify, "global-sentinel")
        finally:
            litellm.ssl_verify = original_ssl_verify

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
        self.assertIn("too many requests", info.response_body["details"])


if __name__ == "__main__":
    unittest.main()
