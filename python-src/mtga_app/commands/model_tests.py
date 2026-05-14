from __future__ import annotations

from collections.abc import Callable
from functools import lru_cache
from typing import Any, Literal, cast

from pydantic import BaseModel
from pytauri import Commands

from modules.actions import model_tests
from modules.proxy.proxy_config import (
    OPENAI_CHAT_COMPLETION_PROVIDER,
)
from modules.runtime.operation_result import OperationResult
from modules.runtime.resource_manager import ResourceManager
from modules.services.config_service import ConfigStore

from .common import build_result_payload, collect_logs, register_command


class InlineThreadManager:
    def run(  # noqa: PLR0913
        self,
        name: str,
        target: Callable[..., None],
        *,
        args: tuple[Any, ...] | None = None,
        kwargs: dict[str, Any] | None = None,
        wait_for: list[str] | None = None,
        allow_parallel: bool = False,
        daemon: bool = True,
    ) -> str:
        _ = (wait_for, allow_parallel, daemon)
        target(*(args or ()), **(kwargs or {}))
        return f"{name}-inline"

    def wait(self, _task_id: str | None, _timeout: float | None = None) -> bool:
        return True


class ModelRoutingTargetTestPayload(BaseModel):
    target_id: str
    mode: Literal["chat", "models"] = "chat"


class ModelRoutingTargetModelListPayload(BaseModel):
    provider: str = OPENAI_CHAT_COMPLETION_PROVIDER
    api_url: str = ""
    model_id: str = ""
    api_key: str = ""
    middle_route: str = ""


@lru_cache(maxsize=1)
def _get_resource_manager() -> ResourceManager:
    return ResourceManager()


@lru_cache(maxsize=1)
def _get_config_store() -> ConfigStore:
    resource_manager = _get_resource_manager()
    return ConfigStore(resource_manager.get_user_config_file())


def _target_to_test_group(target: dict[str, Any]) -> dict[str, Any]:
    return {
        "provider": target.get("provider"),
        "api_url": target.get("api_base"),
        "model_id": target.get("upstream_model"),
        "api_key": target.get("api_key"),
        "middle_route": target.get("middle_route"),
        "model_discovery_strategy": target.get("model_discovery_strategy"),
        "prompt_cache_enabled": target.get("prompt_cache_enabled"),
    }


def _resolve_target_test_group(
    *,
    config_store: ConfigStore,
    target_id: str,
) -> tuple[dict[str, Any] | None, str | None]:
    normalized_target_id = target_id.strip()
    if not normalized_target_id:
        return None, "目标 ID 为空"
    routing_config = config_store.load_model_routing_config()
    targets_obj = routing_config.get("targets")
    targets = cast(list[Any], targets_obj) if isinstance(targets_obj, list) else []
    normalized_targets = [
        cast(dict[str, Any], target_obj) for target_obj in targets if isinstance(target_obj, dict)
    ]
    target = next(
        (
            target_obj
            for target_obj in normalized_targets
            if str(target_obj.get("id") or "") == normalized_target_id
        ),
        None,
    )
    if target is None:
        return None, "目标不存在"
    return _target_to_test_group(target), None


def register_model_test_commands(commands: Commands) -> None:
    @register_command(commands)
    async def model_routing_target_test(body: ModelRoutingTargetTestPayload) -> dict[str, Any]:
        logs, log_func = collect_logs()
        config_store = _get_config_store()
        target_group, error_message = _resolve_target_test_group(
            config_store=config_store,
            target_id=body.target_id,
        )
        if target_group is None:
            result = OperationResult.failure(error_message or "测活目标无效")
            return build_result_payload(result, logs, "目标测活失败")

        thread_manager = InlineThreadManager()
        if body.mode == "models":
            result = model_tests.fetch_model_list_result(
                target_group,
                log_func=log_func,
            )
            if result.ok:
                target_model_id = (target_group.get("model_id") or "").strip()
                if target_model_id:
                    if target_model_id in result.model_ids:
                        log_func(f"✅ 发现模型: {target_model_id}")
                    else:
                        log_func(f"❌ 未找到模型: {target_model_id}")
        else:
            model_tests.test_chat_completion(
                target_group,
                log_func=log_func,
                thread_manager=thread_manager,
            )
        result = OperationResult.success()
        return build_result_payload(result, logs, "目标测活完成")

    @register_command(commands)
    async def model_routing_target_models(
        body: ModelRoutingTargetModelListPayload,
    ) -> dict[str, Any]:
        logs, log_func = collect_logs()
        group = {
            "provider": body.provider,
            "api_url": body.api_url,
            "model_id": body.model_id,
            "api_key": body.api_key,
            "middle_route": body.middle_route,
        }
        discovery_result = model_tests.fetch_model_list_result(group, log_func=log_func)
        if not discovery_result.ok:
            result = OperationResult.failure("模型列表获取失败", models=discovery_result.model_ids)
            return build_result_payload(result, logs, "模型列表获取失败")
        result = OperationResult.success(
            models=discovery_result.model_ids,
            strategy_id=discovery_result.strategy_id,
        )
        return build_result_payload(result, logs, "模型列表获取完成")

    _ = (model_routing_target_test, model_routing_target_models)
