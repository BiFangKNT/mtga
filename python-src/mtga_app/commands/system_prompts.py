from __future__ import annotations

from functools import lru_cache
from typing import Any

from pydantic import BaseModel
from pytauri import Commands

from modules.runtime.operation_result import OperationResult
from modules.runtime.resource_manager import ResourceManager
from modules.services.system_prompt_service import SystemPromptStore

from .common import build_result_payload, collect_logs, register_command


class SystemPromptUpdatePayload(BaseModel):
    hash: str
    edited_text: str


class SystemPromptDeletePayload(BaseModel):
    hashes: list[str]


@lru_cache(maxsize=1)
def _get_resource_manager() -> ResourceManager:
    return ResourceManager()


@lru_cache(maxsize=1)
def _get_prompt_store() -> SystemPromptStore:
    return SystemPromptStore(_get_resource_manager())


def register_system_prompt_commands(commands: Commands) -> None:
    @register_command(commands)
    async def system_prompts_list() -> dict[str, Any]:
        logs, _log = collect_logs()
        items = _get_prompt_store().list_items()
        result = OperationResult.success(items=items)
        return build_result_payload(result, logs, "系统提示词列表加载完成")

    @register_command(commands)
    async def system_prompts_update(body: SystemPromptUpdatePayload) -> dict[str, Any]:
        logs, log_func = collect_logs()
        hash_value = body.hash.strip()
        result = _get_prompt_store().update_prompt_delta(
            hash_value=hash_value,
            edited_text=body.edited_text,
        )
        if result.ok:
            log_func(f"已更新系统提示词增量 hash={hash_value[:12]}")
        return build_result_payload(result, logs, "系统提示词更新完成")

    @register_command(commands)
    async def system_prompts_delete(body: SystemPromptDeletePayload) -> dict[str, Any]:
        logs, log_func = collect_logs()
        result = _get_prompt_store().delete_items(body.hashes)
        if result.ok:
            deleted_count = result.details.get("deleted_count", 0)
            if isinstance(deleted_count, int):
                log_func(f"已删除系统提示词记录 count={deleted_count}")
        return build_result_payload(result, logs, "系统提示词删除完成")

    _ = system_prompts_list
    _ = system_prompts_update
    _ = system_prompts_delete


__all__ = ["register_system_prompt_commands"]
