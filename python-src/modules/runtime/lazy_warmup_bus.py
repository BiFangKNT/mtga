from __future__ import annotations

import threading
import time
from collections import deque

_MAX_ITEMS = 200


class LazyWarmupBus:
    def __init__(self) -> None:
        self._lock = threading.Condition()
        self._items: deque[tuple[int, float, str]] = deque()
        self._next_id = 1

    def push(self, message: str) -> int:
        payload = str(message)
        with self._lock:
            item_id = self._next_id
            self._next_id += 1
            self._items.append((item_id, time.time(), payload))
            while len(self._items) > _MAX_ITEMS:
                self._items.popleft()
            self._lock.notify_all()
            return item_id

    def pull(
        self,
        *,
        after_id: int | None,
        timeout: float = 0.0,
        max_items: int = 200,
    ) -> dict[str, object]:
        if max_items <= 0:
            max_items = 200

        def _collect() -> tuple[list[str], int]:
            items = list(self._items)
            if not items:
                return [], after_id or 0
            if after_id is None:
                selected = items[-max_items:]
            else:
                selected = [item for item in items if item[0] > after_id]
                if len(selected) > max_items:
                    selected = selected[:max_items]
            next_id = selected[-1][0] if selected else (after_id or items[-1][0])
            return [item[2] for item in selected], next_id

        with self._lock:
            if after_id is not None:
                has_new = bool(self._items) and self._items[-1][0] > after_id
            else:
                has_new = bool(self._items)
            if not has_new and timeout > 0:
                self._lock.wait(timeout=timeout)
            messages, next_id = _collect()

        return {"items": messages, "next_id": next_id}


_BUS = LazyWarmupBus()


def push_event(message: str) -> int:
    return _BUS.push(message)


def pull_events(
    *,
    after_id: int | None = None,
    timeout_ms: int = 0,
    max_items: int = 200,
) -> dict[str, object]:
    timeout = max(timeout_ms, 0) / 1000.0
    return _BUS.pull(after_id=after_id, timeout=timeout, max_items=max_items)


__all__ = ["push_event", "pull_events"]
