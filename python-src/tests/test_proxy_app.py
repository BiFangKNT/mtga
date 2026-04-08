from __future__ import annotations

import tempfile
import unittest
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from unittest.mock import patch

from modules.proxy.proxy_app import ProxyApp
from modules.proxy.proxy_config import (
    GEMINI_PROVIDER,
    OPENAI_RESPONSE_PROVIDER,
    ProxyConfig,
)
from modules.proxy.upstream_adapter import (
    CHAT_COMPLETIONS_REQUEST_API,
    RESPONSES_REQUEST_API,
    UpstreamRoute,
)


@dataclass(frozen=True)
class DummyResourceManager:
    user_data_dir: str
    program_resource_dir: str


def _build_proxy_config(
    *,
    debug_mode: bool,
    provider: str = GEMINI_PROVIDER,
    target_api_base_url: str = "https://gemini.example.com",
    target_model_id: str = "gemini-2.5-pro",
    api_key: str = "upstream-key",
) -> ProxyConfig:
    return ProxyConfig(
        provider=provider,
        target_api_base_url=target_api_base_url,
        middle_route="/v1",
        custom_model_id="mapped-model",
        target_model_id=target_model_id,
        stream_mode=None,
        debug_mode=debug_mode,
        disable_ssl_strict_mode=False,
        api_key=api_key,
        mtga_auth_key="mtga-auth",
    )


class DummyAsyncClosableStream:
    def __init__(self, chunks: list[dict[str, Any]]) -> None:
        self._iterator = iter(chunks)
        self.closed = False

    def __iter__(self) -> DummyAsyncClosableStream:
        return self

    def __next__(self) -> dict[str, Any]:
        return next(self._iterator)

    async def aclose(self) -> None:
        self.closed = True


class ProxyAppGeminiTests(unittest.TestCase):
    def test_mtga_auth_header_is_not_reused_as_upstream_api_key(self) -> None:
        temp_dir = tempfile.mkdtemp(prefix="mtga-proxy-app-auth-boundary-")
        resource_manager = DummyResourceManager(
            user_data_dir=temp_dir,
            program_resource_dir=temp_dir,
        )
        logs: list[str] = []
        with patch(
            "modules.proxy.proxy_app.build_proxy_config",
            return_value=_build_proxy_config(debug_mode=False, api_key=""),
        ):
            app_layer = ProxyApp(
                log_func=logs.append,
                resource_manager=resource_manager,  # type: ignore[arg-type]
            )
        self.addCleanup(app_layer.close)

        captured_fallback_api_key: dict[str, str] = {}
        route = UpstreamRoute(
            provider=GEMINI_PROVIDER,
            request_api=CHAT_COMPLETIONS_REQUEST_API,
            litellm_model="gemini/gemini-2.5-pro",
            base_url="https://gemini.example.com/v1",
            api_key="",
            prompt_cache_enabled=True,
            middle_route_applied=True,
            middle_route_ignored=False,
        )

        def fake_build_route(
            proxy_config: ProxyConfig,
            *,
            fallback_api_key: str = "",
        ) -> UpstreamRoute:
            _ = proxy_config
            captured_fallback_api_key["value"] = fallback_api_key
            return route

        transport = app_layer.transport
        with patch.object(
            transport.adapter,
            "build_route",
            side_effect=fake_build_route,
        ), patch.object(
            transport.adapter,
            "create_chat_completion",
            return_value={
                "id": "chatcmpl_123",
                "object": "chat.completion",
                "created": 123,
                "model": "gemini-2.5-pro",
                "choices": [
                    {
                        "index": 0,
                        "message": {"role": "assistant", "content": "ok"},
                        "finish_reason": "stop",
                    }
                ],
            },
        ):
            client = app_layer.app.test_client()
            response = client.post(
                "/v1/chat/completions",
                headers={"Authorization": "Bearer mtga-auth"},
                json={
                    "model": "mapped-model",
                    "messages": [{"role": "user", "content": "hello"}],
                    "stream": False,
                },
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(captured_fallback_api_key["value"], "")
        self.assertTrue(any("下游 Authorization 仅用于 MTGA 鉴权" in item for item in logs))

    def test_developer_message_enters_system_prompt_override_chain(self) -> None:
        temp_dir = tempfile.mkdtemp(prefix="mtga-proxy-app-developer-")
        resource_manager = DummyResourceManager(
            user_data_dir=temp_dir,
            program_resource_dir=temp_dir,
        )
        with patch(
            "modules.proxy.proxy_app.build_proxy_config",
            return_value=_build_proxy_config(debug_mode=False),
        ):
            app_layer = ProxyApp(
                log_func=lambda _message: None,
                resource_manager=resource_manager,  # type: ignore[arg-type]
            )
        self.addCleanup(app_layer.close)

        original_prompt = "原始 developer 提示词"
        expected_hash = app_layer.system_prompt_store.compute_hash(original_prompt)
        request_data = {
            "messages": [
                {"role": "developer", "content": original_prompt},
                {"role": "user", "content": "hello"},
            ]
        }

        with patch.object(
            app_layer.system_prompt_store,
            "capture_and_collect_overrides",
            return_value=([], {expected_hash: "替换后的 developer 提示词"}),
        ) as capture_mock:
            app_layer._apply_system_prompt_overrides(
                request_data=request_data,
                log=lambda _message: None,
            )

        self.assertEqual(
            capture_mock.call_args.args[0],
            [(expected_hash, original_prompt)],
        )
        self.assertEqual(
            request_data["messages"][0]["content"],
            "替换后的 developer 提示词",
        )

    def test_gemini_non_stream_fallback_preserves_stream_intent(self) -> None:
        temp_dir = tempfile.mkdtemp(prefix="mtga-proxy-app-")
        resource_manager = DummyResourceManager(
            user_data_dir=temp_dir,
            program_resource_dir=temp_dir,
        )
        logs: list[str] = []
        with patch(
            "modules.proxy.proxy_app.build_proxy_config",
            return_value=_build_proxy_config(debug_mode=True),
        ):
            app_layer = ProxyApp(
                log_func=logs.append,
                resource_manager=resource_manager,  # type: ignore[arg-type]
            )
        self.addCleanup(app_layer.close)

        self.assertIsNotNone(app_layer.app)
        self.assertIsNotNone(app_layer.transport)

        route = UpstreamRoute(
            provider=GEMINI_PROVIDER,
            request_api=CHAT_COMPLETIONS_REQUEST_API,
            litellm_model="gemini/gemini-2.5-pro",
            base_url="https://gemini.example.com/v1",
            api_key="upstream-key",
            prompt_cache_enabled=True,
            middle_route_applied=True,
            middle_route_ignored=False,
        )
        response_payload = {
            "id": "chatcmpl_123",
            "object": "chat.completion",
            "created": 123,
            "model": "gemini/gemini-2.5-pro",
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": "你好"},
                    "finish_reason": "stop",
                }
            ],
        }
        captured_request_data: dict[str, Any] = {}

        def fake_create_chat_completion(
            *, route: UpstreamRoute, request_data: dict[str, Any]
        ) -> dict[str, Any]:
            _ = route
            captured_request_data.update(request_data)
            return response_payload

        transport = app_layer.transport
        with patch.object(transport.adapter, "build_route", return_value=route), patch.object(
            transport.adapter,
            "create_chat_completion",
            side_effect=fake_create_chat_completion,
        ):
            client = app_layer.app.test_client()
            response = client.post(
                "/v1/chat/completions",
                headers={"Authorization": "Bearer mtga-auth"},
                json={
                    "model": "mapped-model",
                    "messages": [{"role": "user", "content": "hello"}],
                    "stream": True,
                },
            )

        self.assertEqual(response.status_code, 200)
        self.assertIn("text/event-stream", response.content_type)
        self.assertTrue(captured_request_data["stream"])

        response_text = response.get_data(as_text=True)
        self.assertIn("data: [DONE]", response_text)
        self.assertIn('"content": "你好"', response_text)
        self.assertIn('"model": "gemini-2.5-pro"', response_text)
        self.assertNotIn('"model": "gemini/gemini-2.5-pro"', response_text)

        log_files = list(Path(temp_dir, "logs", "SSE").glob("sse_*.log"))
        self.assertEqual(len(log_files), 1)
        self.assertGreater(log_files[0].stat().st_size, 0)
        self.assertTrue(
            any("上游未返回流式结果，代理侧模拟 Chat Completions SSE" in item for item in logs)
        )
        self.assertTrue(any("SSE 记录完成" in item for item in logs))

    def test_gemini_stream_is_forwarded_to_upstream(self) -> None:
        temp_dir = tempfile.mkdtemp(prefix="mtga-proxy-app-stream-")
        resource_manager = DummyResourceManager(
            user_data_dir=temp_dir,
            program_resource_dir=temp_dir,
        )
        logs: list[str] = []
        with patch(
            "modules.proxy.proxy_app.build_proxy_config",
            return_value=_build_proxy_config(debug_mode=True),
        ):
            app_layer = ProxyApp(
                log_func=logs.append,
                resource_manager=resource_manager,  # type: ignore[arg-type]
            )
        self.addCleanup(app_layer.close)

        self.assertIsNotNone(app_layer.app)
        self.assertIsNotNone(app_layer.transport)

        route = UpstreamRoute(
            provider=GEMINI_PROVIDER,
            request_api=CHAT_COMPLETIONS_REQUEST_API,
            litellm_model="gemini/gemini-2.5-pro",
            base_url="https://gemini.example.com/v1",
            api_key="upstream-key",
            prompt_cache_enabled=True,
            middle_route_applied=True,
            middle_route_ignored=False,
        )
        captured_request_data: dict[str, Any] = {}

        def fake_create_chat_completion(
            *, route: UpstreamRoute, request_data: dict[str, Any]
        ) -> Any:
            _ = route
            captured_request_data.update(request_data)
            return iter(
                [
                    {
                        "id": "chatcmpl_123",
                        "created": 123,
                        "model": "gemini/gemini-2.5-pro",
                        "choices": [
                            {
                                "index": 0,
                                "delta": {"role": "assistant", "content": "你"},
                                "finish_reason": None,
                            }
                        ],
                    },
                    {
                        "id": "chatcmpl_123",
                        "created": 123,
                        "model": "gemini/gemini-2.5-pro",
                        "choices": [
                            {
                                "index": 0,
                                "delta": {"content": "好"},
                                "finish_reason": "stop",
                            }
                        ],
                    },
                ]
            )

        transport = app_layer.transport
        with patch.object(transport.adapter, "build_route", return_value=route), patch.object(
            transport.adapter,
            "create_chat_completion",
            side_effect=fake_create_chat_completion,
        ):
            client = app_layer.app.test_client()
            response = client.post(
                "/v1/chat/completions",
                headers={"Authorization": "Bearer mtga-auth"},
                json={
                    "model": "mapped-model",
                    "messages": [{"role": "user", "content": "hello"}],
                    "stream": True,
                },
            )

        self.assertEqual(response.status_code, 200)
        self.assertIn("text/event-stream", response.content_type)
        self.assertTrue(captured_request_data["stream"])

        response_text = response.get_data(as_text=True)
        self.assertIn("data: [DONE]", response_text)
        self.assertIn('"content": "你"', response_text)
        self.assertIn('"content": "好"', response_text)
        self.assertIn('"model": "gemini-2.5-pro"', response_text)
        self.assertNotIn('"model": "gemini/gemini-2.5-pro"', response_text)

        log_files = list(Path(temp_dir, "logs", "SSE").glob("sse_*.log"))
        self.assertEqual(len(log_files), 1)
        self.assertGreater(log_files[0].stat().st_size, 0)
        self.assertTrue(any("返回流式响应" in item for item in logs))
        self.assertFalse(any("Gemini 上游流式返回兼容性较差" in item for item in logs))


class ProxyAppOpenAIResponseTests(unittest.TestCase):
    def test_openai_response_stream_is_forwarded_and_closed_on_disconnect(self) -> None:
        temp_dir = tempfile.mkdtemp(prefix="mtga-proxy-app-openai-response-")
        resource_manager = DummyResourceManager(
            user_data_dir=temp_dir,
            program_resource_dir=temp_dir,
        )
        logs: list[str] = []
        with patch(
            "modules.proxy.proxy_app.build_proxy_config",
            return_value=_build_proxy_config(
                debug_mode=True,
                provider=OPENAI_RESPONSE_PROVIDER,
                target_api_base_url="https://responses.example.com",
                target_model_id="gpt-5.2-codex",
            ),
        ):
            app_layer = ProxyApp(
                log_func=logs.append,
                resource_manager=resource_manager,  # type: ignore[arg-type]
            )
        self.addCleanup(app_layer.close)

        self.assertIsNotNone(app_layer.app)
        self.assertIsNotNone(app_layer.transport)

        route = UpstreamRoute(
            provider=OPENAI_RESPONSE_PROVIDER,
            request_api=RESPONSES_REQUEST_API,
            litellm_model="gpt-5.2-codex",
            base_url="https://responses.example.com/v1",
            api_key="upstream-key",
            prompt_cache_enabled=True,
            middle_route_applied=True,
            middle_route_ignored=False,
        )
        upstream_stream = DummyAsyncClosableStream(
            [
                {
                    "id": "chatcmpl_123",
                    "created": 123,
                    "model": "gpt-5.2-codex",
                    "choices": [
                        {
                            "index": 0,
                            "delta": {"role": "assistant", "content": "你"},
                            "finish_reason": None,
                        }
                    ],
                },
                {
                    "id": "chatcmpl_123",
                    "created": 123,
                    "model": "gpt-5.2-codex",
                    "choices": [
                        {
                            "index": 0,
                            "delta": {"content": "好"},
                            "finish_reason": "stop",
                        }
                    ],
                },
            ]
        )

        transport = app_layer.transport
        with patch.object(transport.adapter, "build_route", return_value=route), patch.object(
            transport.adapter,
            "create_chat_completion",
            return_value=upstream_stream,
        ):
            client = app_layer.app.test_client()
            response = client.post(
                "/v1/chat/completions",
                headers={"Authorization": "Bearer mtga-auth"},
                json={
                    "model": "mapped-model",
                    "messages": [{"role": "user", "content": "hello"}],
                    "stream": True,
                },
                buffered=False,
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn("text/event-stream", response.content_type)
            first_chunk = next(iter(response.response))
            self.assertIn(b"data: ", first_chunk)
            response.close()

        self.assertTrue(upstream_stream.closed)
        self.assertTrue(any("返回流式响应" in item for item in logs))
