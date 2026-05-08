from __future__ import annotations

from collections.abc import Callable
from functools import lru_cache
from typing import Any, Literal, cast

from pydantic import BaseModel
from pytauri import Commands

from modules.actions import model_tests
from modules.proxy.proxy_config import (
    OPENAI_CHAT_COMPLETION_PROVIDER,
    normalize_middle_route,
    normalize_provider,
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


class ConfigGroupTestPayload(BaseModel):
    index: int
    target_id: str = ""
    mode: Literal["chat", "models"] = "chat"


class ConfigGroupModelListPayload(BaseModel):
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


def _persist_model_discovery_strategy_at_index(
    *,
    config_store: ConfigStore,
    index: int,
    strategy_id: str,
    log_func: Callable[[str], None],
) -> None:
    config_groups, current_index = config_store.load_config_groups()
    if index < 0 or index >= len(config_groups):
        return
    current_group = config_groups[index]
    updated = _apply_model_discovery_strategy_to_scope(
        config_groups=config_groups,
        scope_group=current_group,
        strategy_id=strategy_id,
    )
    if not updated:
        return
    if config_store.save_config_groups(config_groups, current_index):
        log_func(f"已缓存模型发现策略: {strategy_id}")
    else:
        log_func("缓存模型发现策略失败")


def _build_model_discovery_cache_scope(group: dict[str, Any]) -> tuple[str, str, str, str]:
    provider_obj = group.get("provider")
    provider = normalize_provider(provider_obj if isinstance(provider_obj, str) else None)
    api_url_obj = group.get("api_url")
    api_url = api_url_obj.strip().rstrip("/") if isinstance(api_url_obj, str) else ""
    api_key_obj = group.get("api_key")
    api_key = api_key_obj.strip() if isinstance(api_key_obj, str) else ""
    middle_route = normalize_middle_route(
        group.get("middle_route"),
        provider=provider,
    )
    return provider, api_url, api_key, middle_route


def _apply_model_discovery_strategy_to_scope(
    *,
    config_groups: list[dict[str, Any]],
    scope_group: dict[str, Any],
    strategy_id: str,
) -> bool:
    target_scope = _build_model_discovery_cache_scope(scope_group)
    updated = False
    for saved_group in config_groups:
        if _build_model_discovery_cache_scope(saved_group) != target_scope:
            continue
        if saved_group.get("model_discovery_strategy") == strategy_id:
            continue
        saved_group["model_discovery_strategy"] = strategy_id
        updated = True
    return updated


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


def _resolve_test_group(
    *,
    config_store: ConfigStore,
    target_id: str,
    index: int,
) -> tuple[dict[str, Any] | None, str | None]:
    normalized_target_id = target_id.strip()
    if normalized_target_id:
        routing_config = config_store.load_model_routing_config()
        targets_obj = routing_config.get("targets")
        targets = cast(list[Any], targets_obj) if isinstance(targets_obj, list) else []
        normalized_targets = [
            cast(dict[str, Any], target_obj)
            for target_obj in targets
            if isinstance(target_obj, dict)
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

    config_groups, _ = config_store.load_config_groups()
    if not config_groups:
        return None, "没有可用的配置组"
    if index < 0 or index >= len(config_groups):
        return None, "配置组索引无效"
    group_obj: object = config_groups[index]
    if not isinstance(group_obj, dict):  # pyright: ignore[reportUnnecessaryIsInstance]
        return None, "配置组格式无效"
    return {str(key): value for key, value in group_obj.items()}, None


def _persist_model_discovery_strategy_for_matching_group(
    *,
    config_store: ConfigStore,
    request_group: dict[str, Any],
    strategy_id: str,
    log_func: Callable[[str], None],
) -> None:
    config_groups, current_index = config_store.load_config_groups()
    if not config_groups:
        return
    updated = _apply_model_discovery_strategy_to_scope(
        config_groups=config_groups,
        scope_group=request_group,
        strategy_id=strategy_id,
    )
    if not updated:
        return
    if config_store.save_config_groups(config_groups, current_index):
        log_func(f"已缓存模型发现策略: {strategy_id}")
    else:
        log_func("缓存模型发现策略失败")


def register_model_test_commands(commands: Commands) -> None:
    @register_command(commands)
    async def config_group_test(body: ConfigGroupTestPayload) -> dict[str, Any]:
        logs, log_func = collect_logs()
        config_store = _get_config_store()
        config_group, error_message = _resolve_test_group(
            config_store=config_store,
            target_id=body.target_id,
            index=body.index,
        )
        if config_group is None:
            result = OperationResult.failure(error_message or "测活目标无效")
            return build_result_payload(result, logs, "配置组测活失败")

        thread_manager = InlineThreadManager()
        if body.mode == "models":
            result = model_tests.fetch_model_list_result(
                config_group,
                log_func=log_func,
            )
            if result.ok and result.strategy_id and not body.target_id.strip():
                _persist_model_discovery_strategy_at_index(
                    config_store=config_store,
                    index=body.index,
                    strategy_id=result.strategy_id,
                    log_func=log_func,
                )
            if result.ok:
                target_model_id = (config_group.get("model_id") or "").strip()
                if target_model_id:
                    if target_model_id in result.model_ids:
                        log_func(f"✅ 发现模型: {target_model_id}")
                    else:
                        log_func(f"❌ 未找到模型: {target_model_id}")
        else:
            model_tests.test_chat_completion(
                config_group,
                log_func=log_func,
                thread_manager=thread_manager,
            )
        result = OperationResult.success()
        return build_result_payload(result, logs, "配置组测活完成")

    @register_command(commands)
    async def config_group_models(body: ConfigGroupModelListPayload) -> dict[str, Any]:
        logs, log_func = collect_logs()
        config_store = _get_config_store()
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
        if discovery_result.strategy_id:
            _persist_model_discovery_strategy_for_matching_group(
                config_store=config_store,
                request_group=group,
                strategy_id=discovery_result.strategy_id,
                log_func=log_func,
            )
        result = OperationResult.success(
            models=discovery_result.model_ids,
            strategy_id=discovery_result.strategy_id,
        )
        return build_result_payload(result, logs, "模型列表获取完成")

    _ = (config_group_test, config_group_models)
