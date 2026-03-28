from __future__ import annotations

import contextlib
import io
import os
import socket
import ssl
import threading
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from werkzeug.serving import ThreadedWSGIServer, WSGIRequestHandler

from modules.runtime.error_codes import ErrorCode
from modules.runtime.operation_result import OperationResult
from modules.runtime.resource_manager import ResourceManager
from modules.runtime.thread_manager import ThreadManager

type LogFunc = Callable[[str], None]


class StoppableWSGIServer(ThreadedWSGIServer):
    """可停止的 WSGI 服务器"""

    def __init__(
        self,
        *args: Any,
        dual_stack: bool = False,
        **kwargs: Any,
    ) -> None:
        self._stop_event = threading.Event()
        self._dual_stack_requested = dual_stack
        self._dual_stack_enabled = False
        super().__init__(*args, **kwargs)

    def server_bind(self) -> None:
        if self._dual_stack_requested and self.address_family == socket.AF_INET6:
            if not (
                hasattr(socket, "IPPROTO_IPV6")
                and hasattr(socket, "IPV6_V6ONLY")
            ):
                raise RuntimeError("当前环境不支持 dual-stack IPv6 socket 配置")
            try:
                self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
            except OSError as exc:
                raise RuntimeError(f"设置 dual-stack socket 失败: {exc}") from exc
            self._dual_stack_enabled = True
        super().server_bind()

    def server_close(self) -> None:
        stop_event = getattr(self, "_stop_event", None)
        if stop_event:
            stop_event.set()
        super().server_close()

    def serve_forever(self, poll_interval: float = 0.5) -> None:
        self.timeout = poll_interval
        while not self._stop_event.is_set():
            try:
                self.handle_request()
            except OSError:
                break


@dataclass
class RuntimeState:
    server: StoppableWSGIServer | None = None
    server_thread: threading.Thread | None = None
    server_task_id: str | None = None
    running: bool = False
    listen_mode: str | None = None


@dataclass(frozen=True)
class ListenerSetupResult:
    server: StoppableWSGIServer
    host: str
    mode: str
    fallback_reason: str | None = None


class ProxyRuntime:
    """代理运行时：负责证书/监听/线程生命周期。"""

    def __init__(
        self,
        app: Any,
        log_func: LogFunc,
        *,
        resource_manager: ResourceManager,
        thread_manager: ThreadManager,
    ) -> None:
        self._app = app
        self._log = log_func
        self._resource_manager = resource_manager
        self._thread_manager = thread_manager
        self._state = RuntimeState()

    def is_running(self) -> bool:
        return self._state.running

    def _log_task_diagnostics(self, prefix: str) -> None:
        task_id = self._state.server_task_id
        if task_id:
            status = self._thread_manager.get_status(task_id=task_id)
            if status:
                self._log(f"{prefix} task_status={status}")
            else:
                self._log(f"{prefix} task_status=<missing task_id={task_id}>")
        active_tasks = self._thread_manager.get_active_tasks()
        if active_tasks:
            self._log(f"{prefix} active_tasks={active_tasks}")

    @staticmethod
    def _format_listener_endpoint(host: str, port: int) -> str:
        if ":" in host:
            return f"[{host}]:{port}"
        return f"{host}:{port}"

    def _create_server_instance(
        self,
        *,
        host: str,
        port: int,
        ssl_context: ssl.SSLContext,
        dual_stack: bool = False,
    ) -> StoppableWSGIServer:
        stderr_buffer = io.StringIO()
        try:
            with contextlib.redirect_stderr(stderr_buffer):
                server = StoppableWSGIServer(
                    host,
                    port,
                    self._app,
                    ssl_context=ssl_context,
                    dual_stack=dual_stack,
                )
        except SystemExit as exc:
            detail = stderr_buffer.getvalue().strip()
            reason = detail or f"SystemExit({exc.code})"
            endpoint = self._format_listener_endpoint(host, port)
            raise RuntimeError(f"监听 {endpoint} 失败: {reason}") from exc

        server.RequestHandlerClass = WSGIRequestHandler
        return server

    def _create_server_with_fallback(
        self,
        *,
        host: str,
        port: int,
        ssl_context: ssl.SSLContext,
    ) -> ListenerSetupResult:
        if host == "0.0.0.0" and socket.has_ipv6:
            try:
                server = self._create_server_instance(
                    host="::",
                    port=port,
                    ssl_context=ssl_context,
                    dual_stack=True,
                )
            except Exception as exc:
                fallback_reason = str(exc)
                self._log(f"dual-stack 监听不可用，将回退到 IPv4: {fallback_reason}")
            else:
                return ListenerSetupResult(
                    server=server,
                    host="::",
                    mode="dual_stack",
                )
        else:
            fallback_reason = None

        listen_mode = "ipv6_only" if ":" in host else "ipv4_only"
        server = self._create_server_instance(
            host=host,
            port=port,
            ssl_context=ssl_context,
        )
        return ListenerSetupResult(
            server=server,
            host=host,
            mode=listen_mode,
            fallback_reason=fallback_reason,
        )

    def start(  # noqa: PLR0911, PLR0912, PLR0913, PLR0915
        self,
        *,
        host: str,
        port: int,
        target_api_base_url: str,
        custom_model_id: str,
        target_model_id: str,
        stream_mode: str | None,
    ) -> OperationResult:
        if self._state.running:
            self._log("代理服务器已在运行")
            return OperationResult.success()

        if not self._app:
            self._log("Flask 应用未初始化")
            return OperationResult.failure("Flask 应用未初始化")

        cert_file = self._resource_manager.get_cert_file()
        key_file = self._resource_manager.get_key_file()

        if not cert_file or not key_file:
            self._log("证书路径为空")
            return OperationResult.failure("证书路径为空", code=ErrorCode.CONFIG_INVALID)

        if not (os.path.exists(cert_file) and os.path.exists(key_file)):
            self._log(f"证书文件不存在: {cert_file} 或 {key_file}")
            return OperationResult.failure("证书文件不存在", code=ErrorCode.FILE_NOT_FOUND)

        try:
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            ssl_context.load_cert_chain(cert_file, key_file)

            endpoint = self._format_listener_endpoint(host, port)
            self._log(f"启动代理服务器，目标监听地址 https://{endpoint}")
            self._log(f"目标 API 地址: {target_api_base_url}")
            self._log(f"自定义模型 ID: {custom_model_id}")
            self._log(f"实际模型 ID: {target_model_id}")
            if stream_mode:
                self._log(f"强制流模式: {stream_mode}")

            if self._state.server_task_id:
                previous_finished = self._thread_manager.wait(
                    self._state.server_task_id,
                    timeout=5,
                )
                if not previous_finished:
                    self._log("旧服务器线程仍在退出，暂时无法启动新实例")
                    self._log_task_diagnostics("启动前等待旧线程超时诊断:")
                    return OperationResult.failure(
                        "旧服务器线程仍在退出",
                        code=ErrorCode.UNKNOWN,
                    )

            try:
                listener_setup = self._create_server_with_fallback(
                    host=host,
                    port=port,
                    ssl_context=ssl_context,
                )
                self._state.server = listener_setup.server
                self._state.listen_mode = listener_setup.mode
                if listener_setup.mode == "dual_stack":
                    self._log(f"监听模式: dual_stack (https://[::]:{port}，同时接受 IPv4/IPv6)")
                else:
                    fallback_endpoint = self._format_listener_endpoint(
                        listener_setup.host,
                        port,
                    )
                    self._log(f"监听模式: {listener_setup.mode} (https://{fallback_endpoint})")
                self._log("服务器实例创建成功")
            except Exception as exc:
                self._state.listen_mode = None
                self._log(f"创建服务器实例失败: {exc}")
                return OperationResult.failure("创建服务器实例失败", code=ErrorCode.UNKNOWN)

            server_ready_event = threading.Event()

            def run_server():
                self._state.server_thread = threading.current_thread()
                try:
                    if not self._state.server:
                        server_ready_event.set()
                        self._log("服务器实例为空，无法启动")
                        return
                    server_ready_event.set()
                    self._state.server.serve_forever()
                except Exception as exc:
                    self._log(f"服务器运行出错: {exc}")
                finally:
                    self._state.running = False
                    self._state.server_task_id = None
                    self._state.server_thread = None
                    self._log("服务器线程已退出")

            self._state.server_task_id = self._thread_manager.run(
                "proxy_server",
                run_server,
                allow_parallel=False,
            )
            self._state.running = True

            if not server_ready_event.wait(timeout=5):
                self._log("代理服务器启动超时")
                self._log_task_diagnostics("启动超时诊断:")
                return OperationResult.failure("代理服务器启动超时", code=ErrorCode.UNKNOWN)

            if self._state.running:
                self._log("代理服务器已成功启动")
                return OperationResult.success()

            self._log("代理服务器启动失败")
            return OperationResult.failure("代理服务器启动失败", code=ErrorCode.UNKNOWN)

        except PermissionError:
            self._log(f"权限不足，无法监听 {port} 端口。请以管理员身份运行。")
            return OperationResult.failure("权限不足", code=ErrorCode.PERMISSION_DENIED)
        except OSError as exc:
            if "address already in use" in str(exc).lower():
                self._log(f"端口 {port} 已被占用。请检查是否有其他服务占用了该端口。")
                return OperationResult.failure("端口已被占用", code=ErrorCode.PORT_IN_USE)
            self._log(f"启动服务器时发生 OS 错误: {exc}")
            return OperationResult.failure("启动服务器时发生 OS 错误", code=ErrorCode.UNKNOWN)
        except Exception as exc:
            self._log(f"启动代理服务器时发生意外错误: {exc}")
            return OperationResult.failure("启动代理服务器时发生意外错误", code=ErrorCode.UNKNOWN)

    def stop(self) -> OperationResult:
        has_pending_task = bool(self._state.server_task_id)
        if not self._state.running and not has_pending_task:
            self._log("代理服务器未运行")
            return OperationResult.success()

        self._log("正在停止代理服务器...")
        self._state.running = False

        stop_requested = False
        if self._state.server:
            try:
                self._state.server.server_close()
                stop_requested = True
                self._log("服务器停止指令已发送")
            except Exception as exc:
                self._log(f"停止服务器时出错: {exc}")
        else:
            self._log("未检测到可停止的服务器实例")

        clean_stop = True
        wait_finished = True
        if self._state.server_task_id:
            try:
                finished = self._thread_manager.wait(self._state.server_task_id, timeout=5)
                wait_finished = finished
                if finished:
                    self._log("服务器线程已安全停止")
                    self._state.server_task_id = None
                else:
                    clean_stop = False
                    self._log("服务器线程未能在 5 秒内停止")
                    self._log_task_diagnostics("停止超时诊断:")
            except Exception as exc:
                wait_finished = False
                clean_stop = False
                self._log(f"等待线程结束时出错: {exc}")
                self._log_task_diagnostics("停止异常诊断:")

        if wait_finished:
            self._state.server = None
            self._state.server_thread = None
            self._state.listen_mode = None

        if clean_stop:
            self._log("代理服务器已完全停止")
            return OperationResult.success()

        if not stop_requested:
            self._log("未发送停止指令，代理线程可能仍在运行")
        self._log("代理服务器仍在后台清理，请稍后关注日志")
        return OperationResult.failure("代理服务器未完全停止", code=ErrorCode.UNKNOWN)


__all__ = ["ProxyRuntime"]
