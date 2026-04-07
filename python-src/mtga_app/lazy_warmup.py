from __future__ import annotations

import json
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from threading import Lock, Thread
from typing import Any, Literal

from pytauri import Commands

from modules.runtime.lazy_warmup_bus import push_event

from .commands import WarmupPhaseSpec, get_lazy_warmup_phases, warmup_lazy_phase

type WarmupEventPhase = Literal["start", "progress", "done", "error"]
type LogFunc = Callable[[str], None]


@dataclass
class LazyWarmupState:
    running: bool = False
    completed: bool = False
    failed: bool = False
    active_phase: str | None = None
    last_event: dict[str, Any] | None = None
    lock: Lock = field(default_factory=Lock)


_STATE = LazyWarmupState()


def _build_event(
    phase: WarmupEventPhase,
    completed: int,
    total: int,
    *,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload = {
        "phase": phase,
        "stage": None,
        "label": None,
        "detail": None,
        "completed": completed,
        "total": total,
        "error_message": None,
    }
    if extra:
        payload.update(extra)
    return payload


def _emit_event(payload: dict[str, Any]) -> None:
    with _STATE.lock:
        _STATE.last_event = dict(payload)
    push_event(json.dumps(payload, ensure_ascii=False))


def _replay_last_event() -> None:
    with _STATE.lock:
        payload = dict(_STATE.last_event) if _STATE.last_event else None
    if payload is not None:
        push_event(json.dumps(payload, ensure_ascii=False))


def _run_warmup(commands: Commands, *, log_func: LogFunc) -> None:
    phases = get_lazy_warmup_phases()
    total = len(phases)
    try:
        _emit_event(
            _build_event(
                "start",
                0,
                total,
                extra={
                    "label": "正在准备后台能力",
                    "detail": "常用功能将在后台完成预热",
                },
            )
        )

        for index, phase in enumerate(phases, start=1):
            with _STATE.lock:
                _STATE.active_phase = phase.key

            _emit_event(
                _build_event(
                    "progress",
                    index - 1,
                    total,
                    extra={
                        "stage": phase.key,
                        "label": phase.label,
                        "detail": phase.detail,
                    },
                )
            )

            started_at = time.perf_counter()
            warmup_lazy_phase(commands, phase.key)
            elapsed_ms = (time.perf_counter() - started_at) * 1000
            log_func(f"lazy warmup phase done: {phase.key} ({elapsed_ms:.1f} ms)")

        done_payload = _build_event(
            "done",
            total,
            total,
            extra={
                "label": "后台能力已就绪",
                "detail": "常用功能预热完成",
            },
        )
        with _STATE.lock:
            _STATE.running = False
            _STATE.completed = True
            _STATE.failed = False
            _STATE.active_phase = None
        _emit_event(done_payload)
    except Exception as exc:
        error_payload = _build_event(
            "error",
            0,
            total,
            extra={
                "stage": _STATE.active_phase,
                "label": "后台预热失败",
                "detail": "部分能力仍会在首次使用时按需加载",
                "error_message": str(exc),
            },
        )
        with _STATE.lock:
            _STATE.running = False
            _STATE.completed = False
            _STATE.failed = True
            _STATE.active_phase = None
        _emit_event(error_payload)
        log_func(f"lazy warmup failed: {exc}")


def start_lazy_warmup(
    commands: Commands,
    *,
    log_func: LogFunc,
) -> Literal["started", "running", "completed"]:
    with _STATE.lock:
        if _STATE.running:
            replay_needed = True
            result: Literal["started", "running", "completed"] = "running"
        elif _STATE.completed:
            replay_needed = True
            result = "completed"
        else:
            _STATE.running = True
            _STATE.completed = False
            _STATE.failed = False
            _STATE.active_phase = None
            _STATE.last_event = None
            replay_needed = False
            result = "started"

    if replay_needed:
        _replay_last_event()
        return result

    Thread(
        target=_run_warmup,
        args=(commands,),
        kwargs={"log_func": log_func},
        name="mtga-lazy-warmup",
        daemon=True,
    ).start()
    return result


def get_lazy_warmup_status() -> dict[str, Any] | None:
    with _STATE.lock:
        if _STATE.last_event is not None:
            return dict(_STATE.last_event)
        running = _STATE.running
        completed = _STATE.completed
        failed = _STATE.failed

    total = len(get_lazy_warmup_phases())
    if running:
        return _build_event(
            "start",
            0,
            total,
            extra={
                "label": "正在准备后台能力",
                "detail": "常用功能将在后台完成预热",
            },
        )
    if completed:
        return _build_event(
            "done",
            total,
            total,
            extra={
                "label": "后台能力已就绪",
                "detail": "常用功能预热完成",
            },
        )
    if failed:
        return _build_event(
            "error",
            0,
            total,
            extra={
                "label": "后台预热失败",
                "detail": "部分能力仍会在首次使用时按需加载",
            },
        )
    return None


def get_lazy_warmup_phases_snapshot() -> tuple[WarmupPhaseSpec, ...]:
    return get_lazy_warmup_phases()


__all__ = ["get_lazy_warmup_phases_snapshot", "get_lazy_warmup_status", "start_lazy_warmup"]
