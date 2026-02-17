from __future__ import annotations

import asyncio
from functools import lru_cache
from pathlib import Path
from typing import Any

from pytauri import Commands

from modules.runtime.resource_manager import ResourceManager
from modules.services.app_metadata import DEFAULT_METADATA
from modules.services.app_version import resolve_app_version
from modules.services.config_service import ConfigStore
from modules.services.update_service import check_for_updates_result

from .common import build_result_payload, collect_logs


@lru_cache(maxsize=1)
def _get_resource_manager() -> ResourceManager:
    return ResourceManager()


@lru_cache(maxsize=1)
def _get_config_store() -> ConfigStore:
    resource_manager = _get_resource_manager()
    return ConfigStore(resource_manager.get_user_config_file())


@lru_cache(maxsize=1)
def _get_project_root() -> Path:
    p = Path(__file__).resolve()
    for parent in p.parents:
        if (parent / "modules").exists() and (parent / "mtga-tauri").exists():
            return parent
    return p.parents[3]


def register_update_commands(commands: Commands) -> None:
    @commands.command()
    async def check_updates() -> dict[str, Any]:
        logs, log_func = collect_logs()
        version = resolve_app_version(project_root=_get_project_root())
        
        config_store = _get_config_store()
        # load_global_config now returns 5 values: mapped_model_id, mtga_auth_key, github_token, disable_update_popup, theme_config
        # We only need github_token here.
        config_tuple = config_store.load_global_config()
        # Safe unpacking: get 3rd element if exists
        github_token = config_tuple[2] if len(config_tuple) > 2 else ""

        # Run sync network I/O off the main event loop to avoid blocking other commands.
        result = await asyncio.to_thread(
            check_for_updates_result,
            repo=DEFAULT_METADATA.github_repo,
            app_version=version,
            github_token=github_token,
        )
        return build_result_payload(result, logs, "更新检查完成")
