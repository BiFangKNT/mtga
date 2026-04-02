from __future__ import annotations

from functools import lru_cache
from typing import Any

from pytauri import Commands

from modules.hosts import hosts_state
from modules.runtime.operation_result import OperationResult
from modules.runtime.resource_manager import (
    ResourceManager,
    get_legacy_user_data_dir,
    get_packaging_runtime,
    has_legacy_user_data_dir,
)
from modules.services import environment_service, startup_context

from .common import build_result_payload, collect_logs


@lru_cache(maxsize=1)
def _get_resource_manager() -> ResourceManager:
    return ResourceManager()


@lru_cache(maxsize=1)
def _get_startup_context() -> startup_context.StartupContext:
    return startup_context.build_startup_context()


def _check_environment() -> tuple[bool, str]:
    resource_manager = _get_resource_manager()
    return environment_service.check_environment(
        check_resources=resource_manager.check_resources,
    )


def register_startup_commands(commands: Commands) -> None:
    @commands.command()
    async def startup_status() -> dict[str, Any]:
        logs, _log_func = collect_logs()
        context = _get_startup_context()
        env_ok, env_message = _check_environment()
        runtime = get_packaging_runtime()
        block_state = hosts_state.get_hosts_modify_block_state()
        hosts_preflight_report = context.hosts_preflight_report
        hosts_preflight_ok = None
        hosts_preflight_status = None
        if hosts_preflight_report is not None:
            hosts_preflight_ok = bool(getattr(hosts_preflight_report, "ok", False))
            status = getattr(hosts_preflight_report, "status", None)
            if status is not None:
                hosts_preflight_status = getattr(status, "value", str(status))

        block_status = None
        block_report = block_state.report
        if block_report is not None:
            status = getattr(block_report, "status", None)
            if status is not None:
                block_status = getattr(status, "value", str(status))

        explicit_proxy_detected = False
        network_env_report = context.network_env_report
        if network_env_report is not None:
            explicit_proxy_detected = bool(
                getattr(network_env_report, "explicit_proxy_detected", False)
            )

        result = OperationResult.success(
            env_ok=env_ok,
            env_message=env_message,
            runtime=runtime,
            legacy_user_data_dir_detected=has_legacy_user_data_dir(),
            legacy_user_data_dir=get_legacy_user_data_dir(),
            allow_unsafe_hosts_flag=hosts_state.ALLOW_UNSAFE_HOSTS_FLAG,
            hosts_modify_blocked=block_state.blocked,
            hosts_modify_block_status=block_status,
            hosts_preflight_ok=hosts_preflight_ok,
            hosts_preflight_status=hosts_preflight_status,
            explicit_proxy_detected=explicit_proxy_detected,
        )
        return build_result_payload(result, logs, "")

    _ = startup_status
