from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from modules.runtime.operation_result import OperationResult
from modules.services import proxy_orchestration
from modules.services.config_service import ConfigStore


@dataclass(frozen=True)
class ProxyUiDeps:
    log: Callable[[str], None]
    config_store: ConfigStore
    runtime_options: Any
    thread_manager: Any
    check_network_environment: Callable[..., Any]
    modify_hosts_file: Callable[..., OperationResult]
    get_proxy_instance: Callable[[], Any | None]
    set_proxy_instance: Callable[[Any | None], None]
    hosts_runner: Any


class ProxyUiCoordinator:
    def __init__(self, deps: ProxyUiDeps) -> None:
        self._deps = deps
        self._network_env_precheck_enabled = False

    def set_network_env_precheck_enabled(self, enabled: bool) -> None:
        self._network_env_precheck_enabled = enabled

    def ensure_global_config_ready(self) -> bool:
        result = proxy_orchestration.ensure_global_config_ready(
            load_global_config=self._deps.config_store.load_global_config,
        )
        if not result.ok:
            missing_display = "、".join(result.missing_fields)
            self._deps.log(
                f"⚠️ 全局配置缺失: {missing_display} 不能为空，请在左侧“全局配置”中填写后再试。"
            )
            return False
        return True

    def get_current_config(self) -> dict[str, Any]:
        return self._deps.config_store.get_current_config()

    def build_proxy_config(self) -> list[dict[str, Any]] | None:
        config = proxy_orchestration.build_proxy_config(
            get_all_configs=self._deps.config_store.load_config_groups,
            debug_mode=self._deps.runtime_options.debug_mode_var.get(),
            disable_ssl_strict_mode=self._deps.runtime_options.disable_ssl_strict_var.get(),
            stream_mode=(
                self._deps.runtime_options.stream_mode_combo.get()
                if self._deps.runtime_options.stream_mode_var.get()
                else None
            ),
        )
        if not config:
            self._deps.log("❌ 错误: 没有可用的配置组")
            return None
        return config

    def restart_proxy(
        self,
        config: list[dict[str, Any]],
        *,
        success_message: str = "✅ 代理服务器启动成功",
        hosts_modified: bool = False,
    ) -> OperationResult:
        return proxy_orchestration.restart_proxy_result(
            config=config,
            deps=proxy_orchestration.RestartProxyDeps(
                log=self._deps.log,
                stop_proxy_instance=self.stop_proxy_instance,
                start_proxy_instance=self.start_proxy_instance,
            ),
            success_message=success_message,
            hosts_modified=hosts_modified,
        )

    def stop_proxy_instance(
        self, reason: str = "stop", show_idle_message: bool = False
    ) -> OperationResult:
        return proxy_orchestration.stop_proxy_instance_result(
            get_proxy_instance=self._deps.get_proxy_instance,
            set_proxy_instance=self._deps.set_proxy_instance,
            log=self._deps.log,
            reason=reason,
            show_idle_message=show_idle_message,
        )

    def start_proxy_instance(
        self,
        config: list[dict[str, Any]],
        success_message: str = "✅ 代理服务器启动成功",
        *,
        hosts_modified: bool = False,
    ) -> OperationResult:
        return proxy_orchestration.start_proxy_instance_result(
            config=config,
            deps=proxy_orchestration.StartProxyDeps(
                log=self._deps.log,
                thread_manager=self._deps.thread_manager,
                check_network_environment=self._deps.check_network_environment,
                set_proxy_instance=self._deps.set_proxy_instance,
                modify_hosts_file=self._deps.modify_hosts_file,
                network_env_precheck_enabled=self._network_env_precheck_enabled,
            ),
            success_message=success_message,
            hosts_modified=hosts_modified,
        )

    def stop_proxy_and_restore(
        self,
        show_idle_message: bool = False,
        *,
        block_hosts_cleanup: bool = False,
    ) -> OperationResult:
        stopped = self.stop_proxy_instance(show_idle_message=show_idle_message)
        self._deps.hosts_runner.modify_hosts("remove", block=block_hosts_cleanup)
        return stopped
