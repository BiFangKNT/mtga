from __future__ import annotations

from .cert import register_cert_commands
from .hosts import register_hosts_commands
from .logs import register_log_commands
from .model_tests import register_model_test_commands
from .proxy import register_proxy_commands
from .startup import register_startup_commands
from .system_prompts import register_system_prompt_commands
from .update import register_update_commands
from .user_data import register_user_data_commands

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
]
