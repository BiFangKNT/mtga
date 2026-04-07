from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, TypeVar, cast

from pytauri import Commands

from modules.runtime.log_bus import push_log
from modules.runtime.operation_result import OperationResult
from modules.runtime.result_messages import describe_result

_TCommandHandler = TypeVar("_TCommandHandler", bound=Callable[..., Awaitable[Any]])


def collect_logs() -> tuple[list[str], Any]:
    logs: list[str] = []

    def _log(message: Any) -> None:
        if message is None:
            return
        text = str(message)
        logs.append(text)
        push_log(text)

    return logs, _log


def _coerce_detail(value: Any) -> Any:
    if is_dataclass(value) and not isinstance(value, type):
        return asdict(value)
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        value_dict = cast(dict[str, Any], value)
        return {str(key): _coerce_detail(item) for key, item in value_dict.items()}
    if isinstance(value, list):
        value_list = cast(list[Any], value)
        return [_coerce_detail(item) for item in value_list]
    if isinstance(value, tuple):
        value_tuple = cast(tuple[Any, ...], value)
        return tuple(_coerce_detail(item) for item in value_tuple)
    return value


def build_result_payload(
    result: OperationResult,
    _logs: list[str],
    default_message: str,
) -> dict[str, Any]:
    return {
        "ok": result.ok,
        "message": describe_result(result, default_message),
        "code": str(result.code) if result.code else None,
        "details": _coerce_detail(result.details),
    }


def register_command(
    commands: Commands,
    command_name: str | None = None,
) -> Callable[[_TCommandHandler], _TCommandHandler]:
    def decorator(handler: _TCommandHandler) -> _TCommandHandler:
        commands.set_command(command_name or handler.__name__, handler)
        return handler

    return decorator
