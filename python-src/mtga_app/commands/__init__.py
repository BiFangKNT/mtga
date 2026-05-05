from __future__ import annotations

from collections.abc import Callable
from importlib import import_module
from typing import cast

from pytauri import Commands

type CommandRegistrar = Callable[[Commands], None]

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

_COMMAND_GROUPS: tuple[str, ...] = (
    "register_log_commands",
    "register_startup_commands",
    "register_update_commands",
    "register_cert_commands",
    "register_hosts_commands",
    "register_model_test_commands",
    "register_proxy_commands",
    "register_system_prompt_commands",
    "register_user_data_commands",
)


def _load_register(export_name: str) -> CommandRegistrar:
    module_name, attr_name = _REGISTER_EXPORTS[export_name]
    module = import_module(module_name)
    return cast(CommandRegistrar, getattr(module, attr_name))


def register_command_groups(commands: Commands) -> None:
    for export_name in _COMMAND_GROUPS:
        _load_register(export_name)(commands)


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
    "register_command_groups",
]
