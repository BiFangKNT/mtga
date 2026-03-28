from __future__ import annotations

import socket
import unittest
from unittest.mock import Mock, patch

from modules.proxy import proxy_runtime as proxy_runtime_module
from modules.proxy.proxy_runtime import ProxyRuntime, StoppableWSGIServer


class DummyThreadManager:
    def get_status(self, *, task_id: str | None = None) -> None:
        _ = task_id

    def get_active_tasks(self) -> list[dict[str, str]]:
        return []


class ProxyRuntimeListenerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.logs: list[str] = []
        self.runtime = ProxyRuntime(
            app=object(),
            log_func=self.logs.append,
            resource_manager=object(),  # type: ignore[arg-type]
            thread_manager=DummyThreadManager(),  # type: ignore[arg-type]
        )

    def test_prefers_dual_stack_for_default_ipv4_host(self) -> None:
        fake_server = Mock(spec=StoppableWSGIServer)
        with patch.object(
            self.runtime,
            "_create_server_instance",
            return_value=fake_server,
        ) as create_server, patch.object(socket, "has_ipv6", True):
            result = self.runtime._create_server_with_fallback(
                host="0.0.0.0",
                port=443,
                ssl_context=Mock(),
            )

        self.assertEqual(result.mode, "dual_stack")
        self.assertEqual(result.host, "::")
        self.assertIsNone(result.fallback_reason)
        create_server.assert_called_once_with(
            host="::",
            port=443,
            ssl_context=unittest.mock.ANY,
            dual_stack=True,
        )

    def test_falls_back_to_ipv4_when_dual_stack_creation_fails(self) -> None:
        dual_stack_error = RuntimeError("dual-stack unsupported")
        fallback_server = Mock(spec=StoppableWSGIServer)
        with patch.object(
            self.runtime,
            "_create_server_instance",
            side_effect=[dual_stack_error, fallback_server],
        ) as create_server, patch.object(socket, "has_ipv6", True):
            result = self.runtime._create_server_with_fallback(
                host="0.0.0.0",
                port=443,
                ssl_context=Mock(),
            )

        self.assertEqual(result.mode, "ipv4_only")
        self.assertEqual(result.host, "0.0.0.0")
        self.assertEqual(result.fallback_reason, str(dual_stack_error))
        self.assertTrue(
            any("dual-stack 监听不可用，将回退到 IPv4" in message for message in self.logs)
        )
        self.assertEqual(create_server.call_count, 2)
        first_call = create_server.call_args_list[0]
        second_call = create_server.call_args_list[1]
        self.assertEqual(first_call.kwargs["host"], "::")
        self.assertTrue(first_call.kwargs["dual_stack"])
        self.assertEqual(second_call.kwargs["host"], "0.0.0.0")
        self.assertFalse(second_call.kwargs.get("dual_stack", False))

    def test_explicit_ipv4_host_skips_dual_stack_attempt(self) -> None:
        fake_server = Mock(spec=StoppableWSGIServer)
        with patch.object(
            self.runtime,
            "_create_server_instance",
            return_value=fake_server,
        ) as create_server, patch.object(socket, "has_ipv6", True):
            result = self.runtime._create_server_with_fallback(
                host="127.0.0.1",
                port=443,
                ssl_context=Mock(),
            )

        self.assertEqual(result.mode, "ipv4_only")
        self.assertEqual(result.host, "127.0.0.1")
        self.assertIsNone(result.fallback_reason)
        create_server.assert_called_once_with(
            host="127.0.0.1",
            port=443,
            ssl_context=unittest.mock.ANY,
        )

    def test_create_server_instance_translates_system_exit_to_runtime_error(self) -> None:
        with patch(
            "modules.proxy.proxy_runtime.StoppableWSGIServer",
            side_effect=SystemExit(1),
        ), self.assertRaisesRegex(RuntimeError, r"监听 \[::\]:443 失败"):
            self.runtime._create_server_instance(
                host="::",
                port=443,
                ssl_context=Mock(),
                dual_stack=True,
            )


@unittest.skipUnless(
    hasattr(socket, "IPPROTO_IPV6") and hasattr(socket, "IPV6_V6ONLY"),
    "当前环境缺少 IPv6 socket 常量",
)
class StoppableWSGIServerBindTests(unittest.TestCase):
    def test_server_bind_enables_dual_stack_before_binding(self) -> None:
        server = StoppableWSGIServer.__new__(StoppableWSGIServer)
        server._dual_stack_requested = True
        server._dual_stack_enabled = False
        server.address_family = socket.AF_INET6
        server.socket = Mock()

        with patch.object(
            proxy_runtime_module.ThreadedWSGIServer,
            "server_bind",
            autospec=True,
        ) as base_bind:
            StoppableWSGIServer.server_bind(server)

        server.socket.setsockopt.assert_called_once_with(
            socket.IPPROTO_IPV6,
            socket.IPV6_V6ONLY,
            0,
        )
        self.assertTrue(server._dual_stack_enabled)
        base_bind.assert_called_once_with(server)


if __name__ == "__main__":
    unittest.main()
