from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from modules.network.network_utils import is_port_in_use
from modules.proxy.proxy_server import ProxyServer
from modules.runtime.error_codes import ErrorCode
from modules.runtime.operation_result import OperationResult


@dataclass(frozen=True)
class RestartProxyDeps:
    log: Callable[[str], None]
    stop_proxy_instance: Callable[..., OperationResult]
    start_proxy_instance: Callable[..., OperationResult]


@dataclass(frozen=True)
class StartProxyDeps:
    log: Callable[[str], None]
    thread_manager: Any
    check_network_environment: Callable[..., Any]
    set_proxy_instance: Callable[[Any | None], None]
    modify_hosts_file: Callable[..., OperationResult]
    network_env_precheck_enabled: bool


@dataclass(frozen=True)
class GlobalConfigCheckResult:
    ok: bool
    missing_fields: list[str]


def ensure_global_config_ready(
    *,
    load_global_config: Callable[[], tuple[str, str]],
) -> GlobalConfigCheckResult:
    mapped_model_id, mtga_auth_key = load_global_config()
    mapped_model_id = (mapped_model_id or "").strip()
    mtga_auth_key = (mtga_auth_key or "").strip()

    missing_fields: list[str] = []
    if not mapped_model_id:
        missing_fields.append("映射模型ID")
    if not mtga_auth_key:
        missing_fields.append("MTGA鉴权Key")

    return GlobalConfigCheckResult(ok=not missing_fields, missing_fields=missing_fields)


def build_proxy_config(
    *,
    get_current_config: Callable[[], dict[str, Any]],
    debug_mode: bool,
    disable_ssl_strict_mode: bool,
    stream_mode: str | None,
) -> dict[str, Any] | None:
    current_config = get_current_config()
    if not current_config:
        return None
    config = current_config.copy()
    config["debug_mode"] = debug_mode
    config["disable_ssl_strict_mode"] = disable_ssl_strict_mode
    config["stream_mode"] = stream_mode
    return config


def restart_proxy_result(
    *,
    config: dict[str, Any],
    deps: RestartProxyDeps,
    success_message: str = "✅ 代理服务器启动成功",
    hosts_modified: bool = False,
) -> OperationResult:
    stream_mode_value = config.get("stream_mode")
    if stream_mode_value is not None:
        deps.log(f"启用强制流模式: {stream_mode_value}")
    deps.stop_proxy_instance(reason="restart")
    start_result = deps.start_proxy_instance(
        config,
        success_message=success_message,
        hosts_modified=hosts_modified,
    )
    if start_result.ok:
        return OperationResult.success()
    return OperationResult.failure(
        start_result.message or "代理服务器启动失败",
        code=start_result.code,
    )


def restart_proxy(
    *,
    config: dict[str, Any],
    deps: RestartProxyDeps,
    success_message: str = "✅ 代理服务器启动成功",
    hosts_modified: bool = False,
) -> bool:
    return restart_proxy_result(
        config=config,
        deps=deps,
        success_message=success_message,
        hosts_modified=hosts_modified,
    ).ok


def stop_proxy_instance_result(
    *,
    get_proxy_instance: Callable[[], Any | None],
    set_proxy_instance: Callable[[Any | None], None],
    log: Callable[[str], None],
    reason: str = "stop",
    show_idle_message: bool = False,
) -> OperationResult:
    instance = get_proxy_instance()
    if instance and instance.is_running():
        if reason == "restart":
            log("检测到代理服务器正在运行，正在停止旧实例...")
        else:
            log("正在停止代理服务器...")
        try:
            instance.stop()
            log("✅ 代理服务器已停止")
        except Exception as exc:  # noqa: BLE001
            log(f"停止代理服务器时出错: {exc}")
        finally:
            set_proxy_instance(None)
        return OperationResult.success()
    if show_idle_message:
        log("代理服务器未运行")
    return OperationResult.success()


def stop_proxy_instance(
    *,
    get_proxy_instance: Callable[[], Any | None],
    set_proxy_instance: Callable[[Any | None], None],
    log: Callable[[str], None],
    reason: str = "stop",
    show_idle_message: bool = False,
) -> bool:
    return stop_proxy_instance_result(
        get_proxy_instance=get_proxy_instance,
        set_proxy_instance=set_proxy_instance,
        log=log,
        reason=reason,
        show_idle_message=show_idle_message,
    ).ok


def start_proxy_instance_result(
    *,
    config: dict[str, Any],
    deps: StartProxyDeps,
    success_message: str = "✅ 代理服务器启动成功",
    hosts_modified: bool = False,
) -> OperationResult:
    if deps.network_env_precheck_enabled:
        deps.check_network_environment(log_func=deps.log, emit_logs=True)

    if is_port_in_use(443):
        deps.log("⚠️ 端口 443 已被其他进程占用，代理服务器未启动。请释放该端口后重试。")
        return OperationResult.failure("端口已被占用", code=ErrorCode.PORT_IN_USE)

    if not hosts_modified:
        deps.log("正在修改hosts文件...")
        modify_result = deps.modify_hosts_file(log_func=deps.log)
        if not modify_result.ok:
            deps.log("⚠️ 修改hosts文件失败，将继续尝试启动代理服务器")
    deps.log("开始启动代理服务器...")
    instance = ProxyServer(config, log_func=deps.log, thread_manager=deps.thread_manager)
    deps.set_proxy_instance(instance)
    if instance.start():
        deps.log(success_message)
        return OperationResult.success()
    deps.log("❌ 代理服务器启动失败")
    deps.set_proxy_instance(None)
    return OperationResult.failure("代理服务器启动失败", code=ErrorCode.UNKNOWN)


def start_proxy_instance(
    *,
    config: dict[str, Any],
    deps: StartProxyDeps,
    success_message: str = "✅ 代理服务器启动成功",
    hosts_modified: bool = False,
) -> bool:
    return start_proxy_instance_result(
        config=config,
        deps=deps,
        success_message=success_message,
        hosts_modified=hosts_modified,
    ).ok
