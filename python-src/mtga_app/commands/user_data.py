from __future__ import annotations

import os
import subprocess
import sys
from collections.abc import Callable
from functools import lru_cache
from typing import Any

from pytauri import Commands

from modules.runtime.operation_result import OperationResult
from modules.runtime.resource_manager import ResourceManager, copy_template_files
from modules.services.app_metadata import DEFAULT_METADATA
from modules.services.user_data_service import (
    backup_user_data_result,
    clear_user_data_result,
    restore_latest_backup_result,
)

from .common import build_result_payload, collect_logs, register_command

type LogFunc = Callable[[str], None]


@lru_cache(maxsize=1)
def _get_resource_manager() -> ResourceManager:
    return ResourceManager()


def _open_directory(path: str, *, log_func: LogFunc) -> OperationResult:
    try:
        if os.name == "nt":
            os.startfile(path)  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.run(["open", path], check=True)
        else:
            subprocess.run(["xdg-open", path], check=True)
        log_func(f"已打开目录: {path}")
        return OperationResult.success()
    except Exception as exc:
        log_func(f"打开目录失败: {exc}")
        return OperationResult.failure(f"打开目录失败: {exc}")


def register_user_data_commands(commands: Commands) -> None:
    @register_command(commands)
    async def user_data_open_dir() -> dict[str, Any]:
        logs, log_func = collect_logs()
        user_dir = _get_resource_manager().user_data_dir
        result = _open_directory(user_dir, log_func=log_func)
        return build_result_payload(result, logs, "打开用户数据目录完成")

    @register_command(commands)
    async def user_data_backup() -> dict[str, Any]:
        logs, _ = collect_logs()
        user_dir = _get_resource_manager().user_data_dir
        result = backup_user_data_result(
            user_dir,
            error_log_filename=DEFAULT_METADATA.error_log_filename,
        )
        return build_result_payload(result, logs, "用户数据备份完成")

    @register_command(commands)
    async def user_data_restore_latest() -> dict[str, Any]:
        logs, _ = collect_logs()
        user_dir = _get_resource_manager().user_data_dir
        result = restore_latest_backup_result(user_dir)
        return build_result_payload(result, logs, "用户数据还原完成")

    @register_command(commands)
    async def user_data_clear() -> dict[str, Any]:
        logs, _ = collect_logs()
        user_dir = _get_resource_manager().user_data_dir
        result = clear_user_data_result(
            user_dir,
            error_log_filename=DEFAULT_METADATA.error_log_filename,
            copy_template_files_fn=copy_template_files,
        )
        return build_result_payload(result, logs, "用户数据清除完成")

    _ = (user_data_open_dir, user_data_backup, user_data_restore_latest, user_data_clear)
