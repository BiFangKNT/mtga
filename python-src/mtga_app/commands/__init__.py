from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from importlib import import_module
from threading import Lock
from typing import Any, Literal, cast

from pytauri import Commands

type CommandBodyKind = Literal["none", "body"]
type CommandRegistrar = Callable[[Commands], None]
type WrappedCommandHandler = Callable[..., Awaitable[str]]


@dataclass(frozen=True)
class CommandSpec:
    name: str
    body_kind: CommandBodyKind = "none"


@dataclass(frozen=True)
class CommandGroupSpec:
    key: str
    module_name: str
    register_name: str
    commands: tuple[CommandSpec, ...]


@dataclass
class LazyGroupState:
    spec: CommandGroupSpec
    lock: Lock = field(default_factory=Lock)
    loaded: bool = False


@dataclass(frozen=True)
class WarmupPhaseSpec:
    key: str
    label: str
    detail: str
    group_keys: tuple[str, ...]


_REGISTER_EXPORTS: dict[str, tuple[str, str]] = {
    "register_cert_commands": ("mtga_app.commands.cert", "register_cert_commands"),
    "register_hosts_commands": ("mtga_app.commands.hosts", "register_hosts_commands"),
    "register_log_commands": ("mtga_app.commands.logs", "register_log_commands"),
    "register_model_test_commands": (
        "mtga_app.commands.model_tests",
        "register_model_test_commands",
    ),
    "register_proxy_commands": ("mtga_app.commands.proxy", "register_proxy_commands"),
    "register_startup_commands": ("mtga_app.commands.startup", "register_startup_commands"),
    "register_system_prompt_commands": (
        "mtga_app.commands.system_prompts",
        "register_system_prompt_commands",
    ),
    "register_update_commands": ("mtga_app.commands.update", "register_update_commands"),
    "register_user_data_commands": ("mtga_app.commands.user_data", "register_user_data_commands"),
}

_EAGER_COMMAND_GROUPS: tuple[CommandGroupSpec, ...] = (
    CommandGroupSpec(
        key="logs",
        module_name="mtga_app.commands.logs",
        register_name="register_log_commands",
        commands=(
            CommandSpec("pull_logs_command", "body"),
            CommandSpec("frontend_report", "body"),
        ),
    ),
    CommandGroupSpec(
        key="startup",
        module_name="mtga_app.commands.startup",
        register_name="register_startup_commands",
        commands=(CommandSpec("startup_status"),),
    ),
    CommandGroupSpec(
        key="update",
        module_name="mtga_app.commands.update",
        register_name="register_update_commands",
        commands=(CommandSpec("check_updates"),),
    ),
)

_LAZY_COMMAND_GROUPS: tuple[CommandGroupSpec, ...] = (
    CommandGroupSpec(
        key="cert",
        module_name="mtga_app.commands.cert",
        register_name="register_cert_commands",
        commands=(
            CommandSpec("generate_certificates"),
            CommandSpec("install_ca_cert"),
            CommandSpec("clear_ca_cert", "body"),
        ),
    ),
    CommandGroupSpec(
        key="hosts",
        module_name="mtga_app.commands.hosts",
        register_name="register_hosts_commands",
        commands=(
            CommandSpec("hosts_modify", "body"),
            CommandSpec("hosts_open"),
        ),
    ),
    CommandGroupSpec(
        key="model_tests",
        module_name="mtga_app.commands.model_tests",
        register_name="register_model_test_commands",
        commands=(
            CommandSpec("config_group_test", "body"),
            CommandSpec("config_group_models", "body"),
        ),
    ),
    CommandGroupSpec(
        key="proxy",
        module_name="mtga_app.commands.proxy",
        register_name="register_proxy_commands",
        commands=(
            CommandSpec("proxy_start", "body"),
            CommandSpec("proxy_apply_current_config", "body"),
            CommandSpec("proxy_stop"),
            CommandSpec("proxy_check_network"),
            CommandSpec("proxy_start_all", "body"),
        ),
    ),
    CommandGroupSpec(
        key="system_prompts",
        module_name="mtga_app.commands.system_prompts",
        register_name="register_system_prompt_commands",
        commands=(
            CommandSpec("system_prompts_list"),
            CommandSpec("system_prompts_update", "body"),
            CommandSpec("system_prompts_delete", "body"),
        ),
    ),
    CommandGroupSpec(
        key="user_data",
        module_name="mtga_app.commands.user_data",
        register_name="register_user_data_commands",
        commands=(
            CommandSpec("user_data_open_dir"),
            CommandSpec("user_data_backup"),
            CommandSpec("user_data_restore_latest"),
            CommandSpec("user_data_clear"),
        ),
    ),
)

_LAZY_GROUP_STATES_ATTR = "_mtga_lazy_group_states"

_LAZY_WARMUP_PHASES: tuple[WarmupPhaseSpec, ...] = (
    WarmupPhaseSpec(
        key="crypto-core",
        label="正在预热证书能力",
        detail="证书生成、校验与安装链路准备中",
        group_keys=("cert",),
    ),
    WarmupPhaseSpec(
        key="hosts-core",
        label="正在预热系统网络能力",
        detail="hosts 检查与修改链路准备中",
        group_keys=("hosts",),
    ),
    WarmupPhaseSpec(
        key="misc",
        label="正在预热常用工具",
        detail="提示词与用户数据能力准备中",
        group_keys=("system_prompts", "user_data"),
    ),
    WarmupPhaseSpec(
        key="network-core",
        label="正在预热网络核心",
        detail="上游适配与模型测活链路准备中",
        group_keys=("model_tests",),
    ),
    WarmupPhaseSpec(
        key="proxy-runtime",
        label="正在预热代理运行时",
        detail="代理服务、路由与运行时准备中",
        group_keys=("proxy",),
    ),
)

_LAZY_WARMUP_PHASES_BY_KEY = {phase.key: phase for phase in _LAZY_WARMUP_PHASES}


def _load_register(export_name: str) -> CommandRegistrar:
    module_name, attr_name = _REGISTER_EXPORTS[export_name]
    module = import_module(module_name)
    return cast(CommandRegistrar, getattr(module, attr_name))


def _get_lazy_group_states(commands: Commands) -> dict[str, LazyGroupState]:
    states = getattr(commands, _LAZY_GROUP_STATES_ATTR, None)
    if not isinstance(states, dict):
        raise RuntimeError("lazy 命令组尚未注册")
    return cast(dict[str, LazyGroupState], states)


def _ensure_group_loaded(commands: Commands, state: LazyGroupState) -> None:
    if state.loaded:
        return

    with state.lock:
        if state.loaded:
            return

        previous_entries: dict[str, Any] = {}
        for command_spec in state.spec.commands:
            entry = commands.data.get(command_spec.name)
            if entry is not None:
                previous_entries[command_spec.name] = entry

        try:
            register = _load_register(state.spec.register_name)
            register(commands)
            missing_commands = [
                command_spec.name
                for command_spec in state.spec.commands
                if command_spec.name not in commands.data
            ]
            if missing_commands:
                missing_display = ", ".join(missing_commands)
                raise RuntimeError(
                    f"命令组 {state.spec.register_name} 注册后缺少命令: {missing_display}"
                )
        except Exception:
            for command_spec in state.spec.commands:
                previous_entry = previous_entries.get(command_spec.name)
                if previous_entry is None:
                    commands.data.pop(command_spec.name, None)
                else:
                    commands.data[command_spec.name] = previous_entry
            raise

        state.loaded = True


def _resolve_lazy_handler(
    commands: Commands,
    state: LazyGroupState,
    command_name: str,
) -> WrappedCommandHandler:
    _ensure_group_loaded(commands, state)
    handler_data = commands.data.get(command_name)
    if handler_data is None:
        raise RuntimeError(f"未找到惰性命令 {command_name} 的真实处理器")
    return cast(WrappedCommandHandler, handler_data.handler)


def _make_lazy_command(
    commands: Commands,
    state: LazyGroupState,
    command_spec: CommandSpec,
) -> Callable[..., Awaitable[str]]:
    if command_spec.body_kind == "body":

        async def lazy_command_with_body(*, body: bytes) -> str:
            handler = _resolve_lazy_handler(commands, state, command_spec.name)
            return await handler(body=body)

        lazy_command_with_body.__name__ = f"lazy_{command_spec.name}"
        return lazy_command_with_body

    async def lazy_command_without_body() -> str:
        handler = _resolve_lazy_handler(commands, state, command_spec.name)
        return await handler()

    lazy_command_without_body.__name__ = f"lazy_{command_spec.name}"
    return lazy_command_without_body


def register_eager_command_groups(commands: Commands) -> None:
    for command_group in _EAGER_COMMAND_GROUPS:
        register = _load_register(command_group.register_name)
        register(commands)


def register_lazy_command_groups(commands: Commands) -> None:
    lazy_group_states = {
        command_group.key: LazyGroupState(spec=command_group)
        for command_group in _LAZY_COMMAND_GROUPS
    }
    setattr(commands, _LAZY_GROUP_STATES_ATTR, lazy_group_states)

    for command_group in _LAZY_COMMAND_GROUPS:
        state = lazy_group_states[command_group.key]
        for command_spec in command_group.commands:
            commands.set_command(
                command_spec.name,
                _make_lazy_command(commands, state, command_spec),
            )


def get_lazy_warmup_phases() -> tuple[WarmupPhaseSpec, ...]:
    return _LAZY_WARMUP_PHASES


def warmup_lazy_phase(commands: Commands, phase_key: str) -> None:
    phase = _LAZY_WARMUP_PHASES_BY_KEY.get(phase_key)
    if phase is None:
        raise RuntimeError(f"未知的 warmup 阶段: {phase_key}")

    lazy_group_states = _get_lazy_group_states(commands)
    for group_key in phase.group_keys:
        state = lazy_group_states.get(group_key)
        if state is None:
            raise RuntimeError(f"未找到 lazy 命令组: {group_key}")
        _ensure_group_loaded(commands, state)


def register_cert_commands(commands: Commands) -> None:
    _load_register("register_cert_commands")(commands)


def register_hosts_commands(commands: Commands) -> None:
    _load_register("register_hosts_commands")(commands)


def register_log_commands(commands: Commands) -> None:
    _load_register("register_log_commands")(commands)


def register_model_test_commands(commands: Commands) -> None:
    _load_register("register_model_test_commands")(commands)


def register_proxy_commands(commands: Commands) -> None:
    _load_register("register_proxy_commands")(commands)


def register_startup_commands(commands: Commands) -> None:
    _load_register("register_startup_commands")(commands)


def register_system_prompt_commands(commands: Commands) -> None:
    _load_register("register_system_prompt_commands")(commands)


def register_update_commands(commands: Commands) -> None:
    _load_register("register_update_commands")(commands)


def register_user_data_commands(commands: Commands) -> None:
    _load_register("register_user_data_commands")(commands)


__all__ = [
    "register_cert_commands",
    "register_hosts_commands",
    "register_log_commands",
    "register_model_test_commands",
    "register_proxy_commands",
    "register_startup_commands",
    "register_system_prompt_commands",
    "register_update_commands",
    "register_user_data_commands",
    "register_eager_command_groups",
    "register_lazy_command_groups",
    "get_lazy_warmup_phases",
    "warmup_lazy_phase",
]
