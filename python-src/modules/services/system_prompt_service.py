from __future__ import annotations

import os
from contextlib import suppress
from datetime import UTC, datetime
from pathlib import Path
from threading import RLock
from typing import Any, NotRequired, TypedDict, cast

import xxhash
import yaml

from modules.runtime.operation_result import OperationResult
from modules.runtime.resource_manager import ResourceManager

SYSTEM_PROMPTS_FILE_NAME = "system_prompts.yaml"


def _now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


class SystemPromptDelta(TypedDict):
    edited_at: str
    editor: str
    edited_text: NotRequired[str]


class SystemPromptItem(TypedDict):
    hash: str
    original_text: str
    created_at: str
    latest_delta: NotRequired[SystemPromptDelta]


class SystemPromptData(TypedDict):
    version: int
    items: list[SystemPromptItem]


def _empty_data() -> SystemPromptData:
    return {"version": 1, "items": []}


class SystemPromptStore:
    """系统提示词持久化与增量覆盖管理。"""

    def __init__(self, resource_manager: ResourceManager) -> None:
        self._path = Path(resource_manager.user_data_dir) / SYSTEM_PROMPTS_FILE_NAME
        self._lock = RLock()

    @staticmethod
    def compute_hash(text: str) -> str:
        return xxhash.xxh3_128_hexdigest(text)

    @staticmethod
    def resolve_effective_text(item: dict[str, Any]) -> str:
        delta_obj = item.get("latest_delta")
        if isinstance(delta_obj, dict):
            delta_map = cast(dict[str, Any], delta_obj)
            edited_text = delta_map.get("edited_text")
            if isinstance(edited_text, str):
                return edited_text
        original_text = item.get("original_text")
        if isinstance(original_text, str):
            return original_text
        return ""

    def list_items(self) -> list[dict[str, Any]]:
        with self._lock:
            data = self._load_unlocked()
            return [dict(item) for item in data["items"]]

    def capture_and_collect_overrides(
        self,
        entries: list[tuple[str, str]],
    ) -> tuple[list[str], dict[str, str]]:
        """写入新增 hash，并返回存在增量修改的 hash -> edited_text 映射。"""
        if not entries:
            return [], {}

        with self._lock:
            data = self._load_unlocked()
            items = list(data["items"])
            item_map: dict[str, SystemPromptItem] = {}
            for normalized in items:
                hash_value = normalized["hash"]
                if hash_value in item_map:
                    continue
                item_map[hash_value] = normalized

            added_hashes: list[str] = []
            for hash_value, original_text in entries:
                if hash_value in item_map:
                    continue
                now = _now_iso()
                new_item: SystemPromptItem = {
                    "hash": hash_value,
                    "original_text": original_text,
                    "created_at": now,
                }
                items.append(new_item)
                item_map[hash_value] = new_item
                added_hashes.append(hash_value)

            if added_hashes:
                data["version"] = 1
                data["items"] = items
                self._save_unlocked(data)

            overrides: dict[str, str] = {}
            for hash_value, item in item_map.items():
                delta_obj = item.get("latest_delta")
                if not delta_obj:
                    continue
                edited_text = delta_obj.get("edited_text")
                if isinstance(edited_text, str):
                    overrides[hash_value] = edited_text
            return added_hashes, overrides

    def update_prompt_delta(
        self,
        *,
        hash_value: str,
        edited_text: str,
        editor: str = "ui",
    ) -> OperationResult:
        normalized_hash = hash_value.strip()
        if not normalized_hash:
            return OperationResult.failure("hash 不能为空")

        with self._lock:
            data = self._load_unlocked()
            target_index = -1
            items = list(data["items"])
            for index, normalized in enumerate(items):
                if normalized["hash"] == normalized_hash and target_index < 0:
                    target_index = index

            if target_index < 0:
                return OperationResult.failure("未找到对应的系统提示词")

            now = _now_iso()
            current_item = items[target_index]
            item: SystemPromptItem = {
                "hash": current_item["hash"],
                "original_text": current_item["original_text"],
                "created_at": current_item["created_at"],
            }
            next_delta: SystemPromptDelta = {
                "edited_at": now,
                "editor": editor,
            }
            if edited_text != current_item["original_text"]:
                next_delta["edited_text"] = edited_text
            item["latest_delta"] = next_delta
            items[target_index] = item

            data["version"] = 1
            data["items"] = items
            self._save_unlocked(data)

            return OperationResult.success(
                "系统提示词增量已更新",
                item=self._normalize_item(item),
            )

    def delete_items(self, hashes: list[str]) -> OperationResult:
        if not hashes:
            return OperationResult.failure("至少提供一条待删除记录")

        normalized_hashes: list[str] = []
        seen_hashes: set[str] = set()
        for raw_hash in hashes:
            hash_value = raw_hash.strip()
            if not hash_value or hash_value in seen_hashes:
                continue
            seen_hashes.add(hash_value)
            normalized_hashes.append(hash_value)

        if not normalized_hashes:
            return OperationResult.failure("至少提供一条有效 hash")

        with self._lock:
            data = self._load_unlocked()
            items = list(data["items"])
            targets = set(normalized_hashes)
            remaining_items: list[SystemPromptItem] = []
            deleted_hashes: list[str] = []
            for item in items:
                item_hash = item["hash"]
                if item_hash in targets:
                    deleted_hashes.append(item_hash)
                    continue
                remaining_items.append(item)

            deleted_count = len(deleted_hashes)
            if deleted_count == 0:
                return OperationResult.success(
                    "未找到可删除的系统提示词",
                    requested_count=len(normalized_hashes),
                    deleted_count=0,
                    deleted_hashes=[],
                )

            data["version"] = 1
            data["items"] = remaining_items
            self._save_unlocked(data)

            return OperationResult.success(
                "系统提示词记录已删除",
                requested_count=len(normalized_hashes),
                deleted_count=deleted_count,
                deleted_hashes=deleted_hashes,
                remaining_count=len(remaining_items),
            )

    def _load_unlocked(self) -> SystemPromptData:
        if not self._path.exists():
            return _empty_data()
        try:
            with self._path.open(encoding="utf-8") as f:
                loaded = yaml.safe_load(f)
        except Exception:
            return _empty_data()
        if not isinstance(loaded, dict):
            return _empty_data()

        loaded_map = cast(dict[str, Any], loaded)
        raw_items_obj = loaded_map.get("items")
        raw_items = cast(list[Any], raw_items_obj) if isinstance(raw_items_obj, list) else []
        version_obj = loaded_map.get("version")
        version = version_obj if isinstance(version_obj, int) else 1
        return {
            "version": version,
            "items": [self._normalize_item(raw_item) for raw_item in raw_items],
        }

    def _save_unlocked(self, data: SystemPromptData) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = self._path.with_suffix(".tmp")
        with tmp_path.open("w", encoding="utf-8") as f:
            yaml.dump(
                data,
                f,
                default_flow_style=False,
                allow_unicode=True,
                indent=2,
                sort_keys=False,
            )
        os.replace(tmp_path, self._path)
        with suppress(Exception):
            if tmp_path.exists():
                tmp_path.unlink()

    def _normalize_item(self, raw_item: Any) -> SystemPromptItem:
        if not isinstance(raw_item, dict):
            return {
                "hash": "",
                "original_text": "",
                "created_at": _now_iso(),
            }
        raw_item_map = cast(dict[str, Any], raw_item)

        hash_value = raw_item_map.get("hash")
        original_text = raw_item_map.get("original_text")
        created_at = raw_item_map.get("created_at")

        normalized_hash = hash_value if isinstance(hash_value, str) else ""
        normalized_text = original_text if isinstance(original_text, str) else ""
        normalized_created_at = (
            created_at if isinstance(created_at, str) and created_at else _now_iso()
        )

        item: SystemPromptItem = {
            "hash": normalized_hash,
            "original_text": normalized_text,
            "created_at": normalized_created_at,
        }

        delta_obj = raw_item_map.get("latest_delta")
        if isinstance(delta_obj, dict):
            delta_map = cast(dict[str, Any], delta_obj)
            edited_text = delta_map.get("edited_text")
            edited_at = delta_map.get("edited_at")
            editor = delta_map.get("editor")
            delta: SystemPromptDelta = {
                "edited_at": edited_at if isinstance(edited_at, str) and edited_at else _now_iso(),
                "editor": editor if isinstance(editor, str) and editor else "ui",
            }
            if isinstance(edited_text, str):
                delta["edited_text"] = edited_text
            item["latest_delta"] = delta
        return item
