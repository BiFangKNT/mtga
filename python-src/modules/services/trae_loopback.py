from __future__ import annotations

import contextlib
import socket
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from werkzeug.serving import WSGIRequestHandler

from modules.proxy.proxy_app import ProxyApp
from modules.proxy.proxy_runtime import StoppableWSGIServer
from modules.runtime.error_codes import ErrorCode
from modules.runtime.operation_result import OperationResult
from modules.runtime.resource_manager import ResourceManager
from modules.runtime.thread_manager import ThreadManager

type LogFunc = Callable[[str], None]

DEFAULT_TRAE_LOOPBACK_HOST = "127.0.0.1"
DEFAULT_TRAE_LOOPBACK_PORT = 18083
DEFAULT_LOOPBACK_WAIT_SECONDS = 5.0


@dataclass(frozen=True)
class TraeLoopbackConfig:
    runtime_config: dict[str, Any]
    loopback_host: str = DEFAULT_TRAE_LOOPBACK_HOST
    loopback_port: int = DEFAULT_TRAE_LOOPBACK_PORT
    ready_wait_seconds: float = DEFAULT_LOOPBACK_WAIT_SECONDS


@dataclass
class _TraeLoopbackState:
    proxy_app: ProxyApp | None = None
    server: StoppableWSGIServer | None = None
    server_task_id: str | None = None
    running: bool = False


def build_trae_loopback_base_url(host: str, port: int) -> str:
    return f"http://{host}:{port}"


def build_trae_loopback_chat_url(host: str, port: int) -> str:
    return f"{build_trae_loopback_base_url(host, port)}/v1/chat/completions"


def _is_port_open(host: str, port: int) -> bool:
    with contextlib.suppress(OSError), socket.create_connection((host, port), timeout=0.5):
        return True
    return False


class TraeLoopbackManager:
    def __init__(
        self,
        *,
        thread_manager: ThreadManager,
        resource_manager: ResourceManager,
    ) -> None:
        self._thread_manager = thread_manager
        self._resource_manager = resource_manager
        self._state = _TraeLoopbackState()
        self._lock = threading.Lock()

    def is_running(self) -> bool:
        with self._lock:
            self._refresh_running_state_locked()
            return self._state.running

    def apply_runtime_config(self, raw_config: dict[str, Any] | None) -> OperationResult:
        with self._lock:
            self._refresh_running_state_locked()
            proxy_app = self._state.proxy_app
            if not self._state.running or proxy_app is None:
                return OperationResult.failure("Trae loopback 未运行")
            return proxy_app.apply_runtime_config(raw_config)

    def start(
        self,
        config: TraeLoopbackConfig,
        *,
        log_func: LogFunc,
        task_name: str,
        log_label: str = "Trae custom model loopback",
    ) -> OperationResult:
        with self._lock:
            self._stop_locked()

            if _is_port_open(config.loopback_host, config.loopback_port):
                message = (
                    "Trae loopback 端口已被占用: "
                    f"{config.loopback_host}:{config.loopback_port}"
                )
                log_func(f"❌ {message}")
                return OperationResult.failure(message, code=ErrorCode.PORT_IN_USE)

            app_result = self._create_proxy_app(
                runtime_config=config.runtime_config,
                log_func=log_func,
            )
            if not app_result.ok:
                return app_result

            proxy_app = self._state.proxy_app
            assert proxy_app is not None and proxy_app.app is not None

            server_result = self._create_server(
                host=config.loopback_host,
                port=config.loopback_port,
                proxy_app=proxy_app,
                log_func=log_func,
            )
            if not server_result.ok:
                return server_result

            server = self._state.server
            assert server is not None

            def run_server() -> None:
                server.serve_forever()

            self._state.proxy_app = proxy_app
            self._state.server = server

            try:
                self._state.server_task_id = self._thread_manager.run(
                    task_name,
                    run_server,
                    allow_parallel=False,
                )
            except Exception as exc:  # noqa: BLE001
                self._stop_locked()
                message = f"Trae loopback 启动失败: {exc}"
                log_func(f"❌ {message}")
                return OperationResult.failure(message, code=ErrorCode.UNKNOWN)

            listen_result = self._wait_until_listening(
                task_id=self._state.server_task_id,
                host=config.loopback_host,
                port=config.loopback_port,
                timeout_seconds=config.ready_wait_seconds,
                log_func=log_func,
            )
            if not listen_result.ok:
                self._stop_locked()
                return listen_result

            self._state.running = True

            base_url = build_trae_loopback_base_url(config.loopback_host, config.loopback_port)
            chat_url = build_trae_loopback_chat_url(config.loopback_host, config.loopback_port)
            log_func(f"{log_label} 已启动: {base_url}/v1")
            log_func(f"{log_label} chat 入口: {chat_url}")
            return OperationResult.success(
                base_url=base_url,
                loopback_url=chat_url,
            )

    def _create_proxy_app(
        self,
        *,
        runtime_config: dict[str, Any],
        log_func: LogFunc,
    ) -> OperationResult:
        proxy_app = ProxyApp(
            runtime_config,
            log_func,
            resource_manager=self._resource_manager,
        )
        if not proxy_app.valid or proxy_app.app is None:
            proxy_app.close()
            return OperationResult.failure("Trae loopback 初始化失败", code=ErrorCode.UNKNOWN)

        self._state.proxy_app = proxy_app
        return OperationResult.success()

    def _create_server(
        self,
        *,
        host: str,
        port: int,
        proxy_app: ProxyApp,
        log_func: LogFunc,
    ) -> OperationResult:
        try:
            server = StoppableWSGIServer(
                host,
                port,
                proxy_app.app,
            )
            server.RequestHandlerClass = WSGIRequestHandler
        except OSError as exc:
            proxy_app.close()
            self._state.proxy_app = None
            message = f"Trae loopback 监听失败: {exc}"
            log_func(f"❌ {message}")
            return OperationResult.failure(message, code=ErrorCode.PORT_IN_USE)
        except Exception as exc:  # noqa: BLE001
            proxy_app.close()
            self._state.proxy_app = None
            message = f"Trae loopback 创建失败: {exc}"
            log_func(f"❌ {message}")
            return OperationResult.failure(message, code=ErrorCode.UNKNOWN)

        self._state.server = server
        return OperationResult.success()

    def _wait_until_listening(
        self,
        *,
        task_id: str | None,
        host: str,
        port: int,
        timeout_seconds: float,
        log_func: LogFunc,
    ) -> OperationResult:
        deadline = time.monotonic() + timeout_seconds
        while time.monotonic() < deadline:
            if _is_port_open(host, port):
                return OperationResult.success()
            status = self._thread_manager.get_status(task_id=task_id)
            if status is not None and status.get("status") in {"failed", "finished"}:
                error = str(status.get("error") or "<empty>")
                message = f"Trae loopback 提前退出: status={status.get('status')} error={error}"
                log_func(f"❌ {message}")
                return OperationResult.failure(message, code=ErrorCode.UNKNOWN)
            time.sleep(0.15)

        message = f"Trae loopback 启动超时: {host}:{port}"
        log_func(f"❌ {message}")
        return OperationResult.failure(message, code=ErrorCode.UNKNOWN)

    def _refresh_running_state_locked(self) -> None:
        if not self._state.running:
            return

        task_id = self._state.server_task_id
        if not task_id:
            self._stop_locked()
            return

        status = self._thread_manager.get_status(task_id=task_id)
        if status is None:
            return

        if status.get("status") in {"failed", "finished"}:
            self._stop_locked()

    def stop(self) -> bool:
        with self._lock:
            return self._stop_locked()

    def _stop_locked(self) -> bool:
        clean = True
        server = self._state.server
        if server is not None:
            with contextlib.suppress(Exception):
                server.server_close()
        if self._state.server_task_id:
            clean = self._thread_manager.wait(self._state.server_task_id, timeout=5)
        self._state.server = None
        self._state.server_task_id = None

        if self._state.proxy_app is not None:
            with contextlib.suppress(Exception):
                self._state.proxy_app.close()
            self._state.proxy_app = None

        self._state.running = False
        return clean
