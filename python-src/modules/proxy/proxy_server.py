"""
代理服务器模块
将代理逻辑拆分为领域逻辑（ProxyApp）与运行时（ProxyRuntime）。
"""

from __future__ import annotations

from modules.proxy.proxy_app import ProxyApp
from modules.proxy.proxy_runtime import ProxyRuntime
from modules.runtime.operation_result import OperationResult
from modules.runtime.resource_manager import ResourceManager
from modules.runtime.thread_manager import ThreadManager


class ProxyServer:
    """代理服务器类，负责装配领域逻辑与运行时。"""

    def __init__(self, config=None, log_func=print, *, thread_manager: ThreadManager):
        self.config = config or {}
        self.log_func = log_func
        self.resource_manager = ResourceManager()
        self.thread_manager = thread_manager

        self.app_layer = ProxyApp(
            self.config,
            self.log_func,
            resource_manager=self.resource_manager,
        )
        self.runtime = ProxyRuntime(
            self.app_layer.app,
            self.log_func,
            resource_manager=self.resource_manager,
            thread_manager=self.thread_manager,
        )

    def start(self, host="0.0.0.0", port=443) -> OperationResult:
        if not self.app_layer.valid:
            return OperationResult.failure("代理应用层初始化失败")

        return self.runtime.start(
            host=host,
            port=port,
            target_api_base_url=self.app_layer.target_api_base_url,
            custom_model_id=self.app_layer.custom_model_id,
            target_model_id=self.app_layer.target_model_id,
            stream_mode=self.app_layer.stream_mode,
        )

    def stop(self) -> OperationResult:
        stop_result = self.runtime.stop()
        self.app_layer.close()
        return stop_result

    def apply_runtime_config(self, config: dict) -> OperationResult:
        if not self.runtime.is_running():
            return OperationResult.failure("代理服务器未运行")
        return self.app_layer.apply_runtime_config(config)

    def is_running(self) -> bool:
        return self.runtime.is_running()


def start_proxy_server(config, log_func=print, *, thread_manager: ThreadManager):
    proxy = ProxyServer(config, log_func, thread_manager=thread_manager)
    if proxy.start().ok:
        return proxy
    return None


__all__ = ["ProxyServer", "start_proxy_server"]
