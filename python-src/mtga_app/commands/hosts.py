from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel
from pytauri import Commands

from modules.services.hosts_service import (
    backup_hosts_file_result,
    modify_hosts_file_result,
    open_hosts_file_result,
    remove_hosts_entry_result,
    restore_hosts_file_result,
)

from .common import build_result_payload, collect_logs, register_command


class HostsModifyPayload(BaseModel):
    mode: Literal["add", "backup", "restore", "remove"]
    domain: str | None = None
    ip: list[str] | str | None = None


def register_hosts_commands(commands: Commands) -> None:
    @register_command(commands)
    async def hosts_modify(body: HostsModifyPayload) -> dict[str, Any]:
        logs, log_func = collect_logs()
        domain_value = body.domain or "api.openai.com"
        mode = body.mode
        ip = body.ip

        if mode == "add":
            result = modify_hosts_file_result(
                domain=domain_value,
                action="add",
                ip=ip,
                log_func=log_func,
            )
            return build_result_payload(result, logs, "hosts 修改完成")
        if mode == "remove":
            result = remove_hosts_entry_result(
                domain=domain_value,
                ip=ip,
                log_func=log_func,
            )
            return build_result_payload(result, logs, "hosts 删除完成")
        if mode == "backup":
            result = backup_hosts_file_result(log_func=log_func)
            return build_result_payload(result, logs, "hosts 备份完成")
        if mode == "restore":
            result = restore_hosts_file_result(log_func=log_func)
            return build_result_payload(result, logs, "hosts 还原完成")

        return {
            "ok": False,
            "message": f"不支持的 hosts 操作: {mode}",
            "code": None,
            "details": {},
            "logs": logs,
        }

    @register_command(commands)
    async def hosts_open() -> dict[str, Any]:
        logs, log_func = collect_logs()
        result = open_hosts_file_result(log_func=log_func)
        return build_result_payload(result, logs, "hosts 打开完成")

    _ = (hosts_modify, hosts_open)
