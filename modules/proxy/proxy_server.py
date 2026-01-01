"""
代理服务器模块
将代理逻辑拆分为领域逻辑（ProxyApp）与运行时（ProxyRuntime）。
"""

from __future__ import annotations

from modules.proxy.proxy_app import ProxyApp
from modules.proxy.proxy_runtime import ProxyRuntime
from modules.runtime.resource_manager import ResourceManager
from modules.runtime.thread_manager import ThreadManager


class ProxyServer:
    """代理服务器类，负责装配领域逻辑与运行时。"""

    def __init__(self, config=None, log_func=print, *, thread_manager: ThreadManager):
        self.config = config or []
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

    def start(self, host="0.0.0.0", port=443) -> bool:
        if not self.app_layer.valid:
            return False

        multi_config = self.app_layer.multi_proxy_config
        if not multi_config:
            self.log_func("错误: 代理配置未初始化")
            return False
        default_config = multi_config.default_config
        target_api_base_url = default_config.target_api_base_url if default_config else "Multi-Config"
        custom_model_id = default_config.custom_model_id if default_config else "Dynamic"
        target_model_id = default_config.target_model_id if default_config else "Dynamic"
        stream_mode = default_config.stream_mode if default_config else None

        result = self.runtime.start(
            host=host,
            port=port,
            target_api_base_url=target_api_base_url,
            custom_model_id=custom_model_id,
            target_model_id=target_model_id,
            stream_mode=stream_mode,
        )
        return result.ok

    def stop(self) -> None:
        self.runtime.stop()
        self.app_layer.close()

    def is_running(self) -> bool:
        return self.runtime.is_running()


def start_proxy_server(config, log_func=print, *, thread_manager: ThreadManager):
    proxy = ProxyServer(config, log_func, thread_manager=thread_manager)
    if proxy.start():
        return proxy
    return None


__all__ = ["ProxyServer", "start_proxy_server"]
