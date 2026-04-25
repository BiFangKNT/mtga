from __future__ import annotations

import threading
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from modules.runtime.error_codes import ErrorCode
from modules.runtime.operation_result import OperationResult
from modules.runtime.resource_manager import ResourceManager
from modules.runtime.thread_manager import ThreadManager
from modules.services.trae_loopback import (
    DEFAULT_TRAE_LOOPBACK_HOST,
    DEFAULT_TRAE_LOOPBACK_PORT,
    TraeLoopbackConfig,
    TraeLoopbackManager,
    build_trae_loopback_base_url,
)

type LogFunc = Callable[[str], None]


@dataclass(frozen=True)
class TraeOfficialBaseUrlRouteConfig:
    runtime_config: dict[str, Any]
    loopback_host: str = DEFAULT_TRAE_LOOPBACK_HOST
    loopback_port: int = DEFAULT_TRAE_LOOPBACK_PORT


class TraeOfficialBaseUrlRouteManager:
    def __init__(
        self,
        *,
        thread_manager: ThreadManager,
        resource_manager: ResourceManager,
    ) -> None:
        self._loopback = TraeLoopbackManager(
            thread_manager=thread_manager,
            resource_manager=resource_manager,
        )
        self._running = False
        self._lock = threading.Lock()

    def is_running(self) -> bool:
        with self._lock:
            if self._running and not self._loopback.is_running():
                self._running = False
            return self._running

    def apply_runtime_config(self, raw_config: dict[str, Any] | None) -> OperationResult:
        with self._lock:
            if self._running and not self._loopback.is_running():
                self._running = False
            if not self._running:
                return OperationResult.failure("Trae 官方 base_url 路线未运行")
        return self._loopback.apply_runtime_config(raw_config)

    def start(
        self,
        config: TraeOfficialBaseUrlRouteConfig,
        *,
        log_func: LogFunc,
    ) -> OperationResult:
        with self._lock:
            stop_result = self._stop_locked(log_func=log_func, show_idle_message=False)
            if not stop_result.ok:
                return stop_result

            log_func(
                "Trae 官方 base_url 路线："
                "仅启动本地 custom model loopback，不拉起 Trae、不打 patch"
            )
            loopback_result = self._loopback.start(
                TraeLoopbackConfig(
                    runtime_config=config.runtime_config,
                    loopback_host=config.loopback_host,
                    loopback_port=config.loopback_port,
                ),
                log_func=log_func,
                task_name="trae_official_base_url_loopback",
            )
            if not loopback_result.ok:
                return loopback_result

            self._running = True
            api_base_url = self._api_base_url(config)
            log_func(f"Trae 自定义模型 base_url 请填写: {api_base_url}")
            log_func("✅ Trae 官方 base_url 路线已就绪")
            return OperationResult.success(
                "Trae 官方 base_url 路线已就绪",
                base_url=api_base_url,
                loopback_url=f"{api_base_url}/chat/completions",
            )

    def stop(
        self,
        *,
        log_func: LogFunc,
        show_idle_message: bool = False,
    ) -> OperationResult:
        with self._lock:
            return self._stop_locked(
                log_func=log_func,
                show_idle_message=show_idle_message,
            )

    def _stop_locked(
        self,
        *,
        log_func: LogFunc,
        show_idle_message: bool,
    ) -> OperationResult:
        had_runtime = self._running or self._loopback.is_running()
        if not had_runtime:
            if show_idle_message:
                log_func("Trae 官方 base_url 路线未运行")
            return OperationResult.success()

        log_func("正在停止 Trae 官方 base_url 路线...")
        clean = self._loopback.stop()
        self._running = False
        log_func("Trae 官方 base_url 路线已停止")
        if clean:
            return OperationResult.success()
        return OperationResult.failure(
            "Trae 官方 base_url 路线未完全停止",
            code=ErrorCode.UNKNOWN,
        )

    @staticmethod
    def _api_base_url(config: TraeOfficialBaseUrlRouteConfig) -> str:
        return f"{build_trae_loopback_base_url(config.loopback_host, config.loopback_port)}/v1"
