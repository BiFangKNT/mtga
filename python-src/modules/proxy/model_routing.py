from __future__ import annotations

import copy
import time
from dataclasses import dataclass
from typing import Any, cast

import httpx

from modules.proxy.proxy_config import (
    normalize_middle_route,
    normalize_model_discovery_strategy,
    normalize_prompt_cache_enabled,
    normalize_provider,
)

MODEL_ROUTING_SCHEMA_VERSION = 2
DEFAULT_FAILOVER_TRIGGER_STATUSES = (429,)
DEFAULT_FAILOVER_COOLDOWN_SECONDS = 10


@dataclass(frozen=True)
class ModelRoutingTarget:
    id: str
    display_name: str
    provider: str
    api_base: str
    upstream_model: str
    api_key: str
    middle_route: str
    model_discovery_strategy: str | None
    prompt_cache_enabled: bool


@dataclass(frozen=True)
class FailoverPoolMember:
    target_id: str


@dataclass(frozen=True)
class FailoverPool:
    id: str
    trigger_statuses: tuple[int, ...]
    cooldown_seconds: int
    members: tuple[FailoverPoolMember, ...]


@dataclass(frozen=True)
class PublishedModel:
    name: str
    enabled: bool
    primary_target_id: str
    failover_pool_id: str | None


@dataclass(frozen=True)
class ModelRoutingConfig:
    schema_version: int
    mtga_auth_key: str
    targets: tuple[ModelRoutingTarget, ...]
    failover_pools: tuple[FailoverPool, ...]
    published_models: tuple[PublishedModel, ...]
    prompt_cache_bucket_id: str = ""

    def enabled_published_models(self) -> tuple[PublishedModel, ...]:
        return tuple(model for model in self.published_models if model.enabled)

    def target_by_id(self) -> dict[str, ModelRoutingTarget]:
        return {target.id: target for target in self.targets}

    def pool_by_id(self) -> dict[str, FailoverPool]:
        return {pool.id: pool for pool in self.failover_pools}


@dataclass(frozen=True)
class ResolvedRoute:
    published_model: PublishedModel
    primary_target: ModelRoutingTarget
    failover_pool: FailoverPool | None


@dataclass(frozen=True)
class RouteResolutionError:
    status_code: int
    code: str
    message: str


@dataclass(frozen=True)
class TargetAttempt:
    target: ModelRoutingTarget
    index: int
    source: str


class TargetCooldowns:
    def __init__(self) -> None:
        self._cooldowns: dict[str, float] = {}

    def is_cooling(self, target_id: str) -> bool:
        expires_at = self._cooldowns.get(target_id)
        if expires_at is None:
            return False
        if expires_at <= time.monotonic():
            self._cooldowns.pop(target_id, None)
            return False
        return True

    def mark_cooling(self, target_id: str, cooldown_seconds: int) -> float:
        expires_at = time.monotonic() + max(1, cooldown_seconds)
        self._cooldowns[target_id] = expires_at
        return expires_at

    def remaining_seconds(self, target_id: str) -> int:
        expires_at = self._cooldowns.get(target_id)
        if expires_at is None:
            return 0
        remaining = int(max(0, expires_at - time.monotonic()))
        if remaining <= 0:
            self._cooldowns.pop(target_id, None)
        return remaining


def _coerce_text(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    if value is None:
        return ""
    return str(value).strip()


def _coerce_bool(value: Any, *, default: bool = True) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"true", "1", "on", "yes"}:
            return True
        if normalized in {"false", "0", "off", "no"}:
            return False
    if value is None:
        return default
    return bool(value)


def _coerce_positive_int(value: Any, *, default: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return parsed if parsed > 0 else default


def _coerce_trigger_statuses(value: Any) -> tuple[int, ...]:
    if not isinstance(value, list):
        return DEFAULT_FAILOVER_TRIGGER_STATUSES
    statuses: list[int] = []
    for item in cast(list[Any], value):
        try:
            status = int(item)
        except (TypeError, ValueError):
            continue
        if status > 0 and status not in statuses:
            statuses.append(status)
    return tuple(statuses) or DEFAULT_FAILOVER_TRIGGER_STATUSES


def _unique_identifier(
    requested: str,
    used: set[str],
    *,
    fallback_prefix: str,
    index: int,
) -> str:
    base = requested.strip() or f"{fallback_prefix}-{index}"
    candidate = base
    suffix = 2
    while candidate in used:
        candidate = f"{base}-{suffix}"
        suffix += 1
    used.add(candidate)
    return candidate


def _normalize_target(raw_target: Any, *, index: int, used_ids: set[str]) -> dict[str, Any] | None:
    if not isinstance(raw_target, dict):
        return None
    target = cast(dict[str, Any], raw_target)
    target_id = _unique_identifier(
        _coerce_text(target.get("id")),
        used_ids,
        fallback_prefix="target",
        index=index,
    )
    provider = normalize_provider(_coerce_text(target.get("provider")) or None)
    api_base = _coerce_text(target.get("api_base") or target.get("api_url"))
    upstream_model = _coerce_text(target.get("upstream_model") or target.get("model_id"))
    api_key = _coerce_text(target.get("api_key"))
    middle_route = normalize_middle_route(
        _coerce_text(target.get("middle_route")),
        provider=provider,
    )
    model_discovery_strategy = normalize_model_discovery_strategy(
        _coerce_text(target.get("model_discovery_strategy")) or None
    )
    if not api_base or not upstream_model:
        return None
    return {
        "id": target_id,
        "display_name": _coerce_text(target.get("display_name") or target.get("name")),
        "provider": provider,
        "api_base": api_base.rstrip("/"),
        "upstream_model": upstream_model,
        "api_key": api_key,
        "middle_route": middle_route,
        "model_discovery_strategy": model_discovery_strategy,
        "prompt_cache_enabled": normalize_prompt_cache_enabled(
            target.get("prompt_cache_enabled")
        ),
    }


def _normalize_failover_pool(
    raw_pool: Any,
    *,
    index: int,
    used_ids: set[str],
) -> dict[str, Any] | None:
    if not isinstance(raw_pool, dict):
        return None
    pool = cast(dict[str, Any], raw_pool)
    pool_id = _unique_identifier(
        _coerce_text(pool.get("id")),
        used_ids,
        fallback_prefix="failover-pool",
        index=index,
    )
    members_obj = pool.get("members")
    members: list[dict[str, str]] = []
    seen_member_ids: set[str] = set()
    if isinstance(members_obj, list):
        for member_obj in cast(list[Any], members_obj):
            if isinstance(member_obj, dict):
                member_id = _coerce_text(cast(dict[str, Any], member_obj).get("target_id"))
            else:
                member_id = _coerce_text(member_obj)
            if not member_id or member_id in seen_member_ids:
                continue
            seen_member_ids.add(member_id)
            members.append({"target_id": member_id})
    return {
        "id": pool_id,
        "trigger_statuses": list(_coerce_trigger_statuses(pool.get("trigger_statuses"))),
        "cooldown_seconds": _coerce_positive_int(
            pool.get("cooldown_seconds"),
            default=DEFAULT_FAILOVER_COOLDOWN_SECONDS,
        ),
        "members": members,
    }


def _normalize_published_model(
    raw_model: Any,
    *,
    used_names: set[str],
) -> dict[str, Any] | None:
    if not isinstance(raw_model, dict):
        return None
    model = cast(dict[str, Any], raw_model)
    name = _coerce_text(model.get("name"))
    if not name or name in used_names:
        return None
    used_names.add(name)
    failover_pool_id = _coerce_text(model.get("failover_pool_id")) or None
    return {
        "name": name,
        "enabled": _coerce_bool(model.get("enabled"), default=True),
        "primary_target_id": _coerce_text(model.get("primary_target_id")),
        "failover_pool_id": failover_pool_id,
    }


def normalize_model_routing_config(raw_config: Any) -> dict[str, Any]:
    if not isinstance(raw_config, dict):
        raw_config = {}
    config = cast(dict[str, Any], raw_config)
    if int(config.get("schema_version") or 0) == MODEL_ROUTING_SCHEMA_VERSION:
        normalized = _normalize_v2_config(config)
        if not normalized["targets"] and isinstance(config.get("config_groups"), list):
            return migrate_legacy_config_to_model_routing(config)
        return normalized
    return migrate_legacy_config_to_model_routing(config)


def _normalize_v2_config(config: dict[str, Any]) -> dict[str, Any]:
    used_target_ids: set[str] = set()
    targets: list[dict[str, Any]] = []
    raw_targets = config.get("targets")
    if isinstance(raw_targets, list):
        for index, raw_target in enumerate(cast(list[Any], raw_targets), start=1):
            normalized = _normalize_target(raw_target, index=index, used_ids=used_target_ids)
            if normalized is not None:
                targets.append(normalized)

    target_ids = {target["id"] for target in targets}

    used_pool_ids: set[str] = set()
    failover_pools: list[dict[str, Any]] = []
    raw_pools = config.get("failover_pools")
    if isinstance(raw_pools, list):
        for index, raw_pool in enumerate(cast(list[Any], raw_pools), start=1):
            normalized_pool = _normalize_failover_pool(
                raw_pool,
                index=index,
                used_ids=used_pool_ids,
            )
            if normalized_pool is None:
                continue
            normalized_pool["members"] = [
                member
                for member in normalized_pool["members"]
                if member["target_id"] in target_ids
            ]
            failover_pools.append(normalized_pool)

    pool_ids = {pool["id"] for pool in failover_pools}

    used_model_names: set[str] = set()
    published_models: list[dict[str, Any]] = []
    raw_models = config.get("published_models")
    if isinstance(raw_models, list):
        for raw_model in cast(list[Any], raw_models):
            normalized_model = _normalize_published_model(
                raw_model,
                used_names=used_model_names,
            )
            if normalized_model is None:
                continue
            if normalized_model["primary_target_id"] not in target_ids:
                continue
            failover_pool_id = normalized_model.get("failover_pool_id")
            if failover_pool_id and failover_pool_id not in pool_ids:
                normalized_model["failover_pool_id"] = None
            published_models.append(normalized_model)

    return {
        "schema_version": MODEL_ROUTING_SCHEMA_VERSION,
        "mtga_auth_key": _coerce_text(config.get("mtga_auth_key")),
        "targets": targets,
        "failover_pools": failover_pools,
        "published_models": published_models,
        "prompt_cache_bucket_id": _coerce_text(config.get("prompt_cache_bucket_id")),
    }


def migrate_legacy_config_to_model_routing(config: dict[str, Any]) -> dict[str, Any]:
    raw_groups = config.get("config_groups")
    groups = cast(list[Any], raw_groups) if isinstance(raw_groups, list) else []
    used_target_ids: set[str] = set()
    targets: list[dict[str, Any]] = []
    selected_target_id = ""
    current_index = _coerce_positive_int(config.get("current_config_index"), default=0)
    current_index = max(0, current_index)
    for index, raw_group in enumerate(groups, start=1):
        target = _normalize_target(
            raw_group,
            index=index,
            used_ids=used_target_ids,
        )
        if target is None:
            continue
        if not target["id"].startswith("target-"):
            target["id"] = _unique_identifier(
                f"target-{index}",
                {item["id"] for item in targets},
                fallback_prefix="target",
                index=index,
            )
        targets.append(target)
        if index - 1 == current_index:
            selected_target_id = target["id"]

    if not selected_target_id and targets and current_index < len(targets):
        selected_target_id = targets[current_index]["id"]
    if not selected_target_id and targets:
        selected_target_id = targets[0]["id"]

    mapped_model_id = _coerce_text(config.get("mapped_model_id"))
    published_models: list[dict[str, Any]] = []
    if mapped_model_id and selected_target_id:
        published_models.append(
            {
                "name": mapped_model_id,
                "enabled": True,
                "primary_target_id": selected_target_id,
                "failover_pool_id": None,
            }
        )

    return {
        "schema_version": MODEL_ROUTING_SCHEMA_VERSION,
        "mtga_auth_key": _coerce_text(config.get("mtga_auth_key")),
        "targets": targets,
        "failover_pools": [],
        "published_models": published_models,
        "prompt_cache_bucket_id": _coerce_text(config.get("prompt_cache_bucket_id")),
    }


def build_model_routing_config(raw_config: Any) -> ModelRoutingConfig:
    normalized = normalize_model_routing_config(raw_config)
    targets = tuple(
        ModelRoutingTarget(
            id=str(target["id"]),
            display_name=str(target.get("display_name") or ""),
            provider=str(target["provider"]),
            api_base=str(target["api_base"]),
            upstream_model=str(target["upstream_model"]),
            api_key=str(target.get("api_key") or ""),
            middle_route=str(target["middle_route"]),
            model_discovery_strategy=(
                str(target["model_discovery_strategy"])
                if target.get("model_discovery_strategy")
                else None
            ),
            prompt_cache_enabled=bool(target.get("prompt_cache_enabled")),
        )
        for target in normalized["targets"]
    )
    failover_pools = tuple(
        FailoverPool(
            id=str(pool["id"]),
            trigger_statuses=tuple(int(status) for status in pool["trigger_statuses"]),
            cooldown_seconds=int(pool["cooldown_seconds"]),
            members=tuple(
                FailoverPoolMember(target_id=str(member["target_id"]))
                for member in pool["members"]
            ),
        )
        for pool in normalized["failover_pools"]
    )
    published_models = tuple(
        PublishedModel(
            name=str(model["name"]),
            enabled=bool(model["enabled"]),
            primary_target_id=str(model["primary_target_id"]),
            failover_pool_id=(
                str(model["failover_pool_id"]) if model.get("failover_pool_id") else None
            ),
        )
        for model in normalized["published_models"]
    )
    return ModelRoutingConfig(
        schema_version=MODEL_ROUTING_SCHEMA_VERSION,
        mtga_auth_key=str(normalized.get("mtga_auth_key") or ""),
        targets=targets,
        failover_pools=failover_pools,
        published_models=published_models,
        prompt_cache_bucket_id=str(normalized.get("prompt_cache_bucket_id") or ""),
    )


def serialize_model_routing_config(config: ModelRoutingConfig | dict[str, Any]) -> dict[str, Any]:
    if isinstance(config, dict):
        return copy.deepcopy(normalize_model_routing_config(config))
    return {
        "schema_version": MODEL_ROUTING_SCHEMA_VERSION,
        "mtga_auth_key": config.mtga_auth_key,
        "targets": [
            {
                "id": target.id,
                "display_name": target.display_name,
                "provider": target.provider,
                "api_base": target.api_base,
                "api_key": target.api_key,
                "middle_route": target.middle_route,
                "upstream_model": target.upstream_model,
                "model_discovery_strategy": target.model_discovery_strategy,
                "prompt_cache_enabled": target.prompt_cache_enabled,
            }
            for target in config.targets
        ],
        "failover_pools": [
            {
                "id": pool.id,
                "trigger_statuses": list(pool.trigger_statuses),
                "cooldown_seconds": pool.cooldown_seconds,
                "members": [{"target_id": member.target_id} for member in pool.members],
            }
            for pool in config.failover_pools
        ],
        "published_models": [
            {
                "name": model.name,
                "enabled": model.enabled,
                "primary_target_id": model.primary_target_id,
                "failover_pool_id": model.failover_pool_id,
            }
            for model in config.published_models
        ],
        "prompt_cache_bucket_id": config.prompt_cache_bucket_id,
    }


def resolve_published_model(
    config: ModelRoutingConfig,
    request_model: Any,
) -> ResolvedRoute | RouteResolutionError:
    if not isinstance(request_model, str) or not request_model.strip():
        return RouteResolutionError(
            status_code=400,
            code="model_required",
            message="The request body must include a non-empty model string.",
        )
    model_name = request_model.strip()
    published_model = next(
        (model for model in config.published_models if model.name == model_name),
        None,
    )
    if published_model is None or not published_model.enabled:
        return RouteResolutionError(
            status_code=404,
            code="model_not_found",
            message=f"Model not found: {model_name}",
        )

    targets = config.target_by_id()
    primary_target = targets.get(published_model.primary_target_id)
    if primary_target is None:
        return RouteResolutionError(
            status_code=500,
            code="route_config_invalid",
            message=f"Published model has invalid primary target: {model_name}",
        )

    failover_pool: FailoverPool | None = None
    if published_model.failover_pool_id:
        failover_pool = config.pool_by_id().get(published_model.failover_pool_id)
        if failover_pool is None:
            return RouteResolutionError(
                status_code=500,
                code="route_config_invalid",
                message=f"Published model has invalid failover pool: {model_name}",
            )
    return ResolvedRoute(
        published_model=published_model,
        primary_target=primary_target,
        failover_pool=failover_pool,
    )


def build_target_attempts(
    resolved_route: ResolvedRoute,
    *,
    routing_config: ModelRoutingConfig,
    cooldowns: TargetCooldowns,
) -> tuple[TargetAttempt, ...]:
    attempts: list[TargetAttempt] = []
    if not cooldowns.is_cooling(resolved_route.primary_target.id):
        attempts.append(
            TargetAttempt(
                target=resolved_route.primary_target,
                index=1,
                source="primary",
            )
        )
    if resolved_route.failover_pool is None:
        return tuple(attempts)

    targets = routing_config.target_by_id()
    seen_target_ids = {attempt.target.id for attempt in attempts}
    next_index = len(attempts) + 1
    for member in resolved_route.failover_pool.members:
        target = targets.get(member.target_id)
        if target is None or target.id in seen_target_ids:
            continue
        if cooldowns.is_cooling(target.id):
            continue
        attempts.append(
            TargetAttempt(
                target=target,
                index=next_index,
                source="failover",
            )
        )
        seen_target_ids.add(target.id)
        next_index += 1
    return tuple(attempts)


def is_retryable_transport_error(exc: Exception) -> bool:
    retryable_types = (
        httpx.ConnectError,
        httpx.ConnectTimeout,
        httpx.ProxyError,
    )
    pending: list[BaseException] = [exc]
    seen: set[int] = set()
    while pending:
        current = pending.pop()
        current_id = id(current)
        if current_id in seen:
            continue
        seen.add(current_id)
        if isinstance(current, retryable_types):
            return True
        cause = getattr(current, "__cause__", None)
        context = getattr(current, "__context__", None)
        if isinstance(cause, BaseException):
            pending.append(cause)
        if isinstance(context, BaseException):
            pending.append(context)
    return False


def build_openai_error_body(*, message: str, code: str, error_type: str) -> dict[str, Any]:
    return {
        "error": {
            "message": message,
            "type": error_type,
            "code": code,
        }
    }


__all__ = [
    "DEFAULT_FAILOVER_COOLDOWN_SECONDS",
    "DEFAULT_FAILOVER_TRIGGER_STATUSES",
    "FailoverPool",
    "FailoverPoolMember",
    "MODEL_ROUTING_SCHEMA_VERSION",
    "ModelRoutingConfig",
    "ModelRoutingTarget",
    "PublishedModel",
    "ResolvedRoute",
    "RouteResolutionError",
    "TargetAttempt",
    "TargetCooldowns",
    "build_model_routing_config",
    "build_openai_error_body",
    "build_target_attempts",
    "is_retryable_transport_error",
    "migrate_legacy_config_to_model_routing",
    "normalize_model_routing_config",
    "resolve_published_model",
    "serialize_model_routing_config",
]
