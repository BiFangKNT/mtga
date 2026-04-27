from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path
from typing import Any

MODEL_LIST_MAP_SUFFIX = "_AI.agent.model.model_list_map"
GLOBAL_MODEL_MAP_SUFFIX = "_ai-chat:sessionRelation:globalModelMap"
SELECTION_TOKEN_PARTS = 3
CONNECTED_CONFIG_SOURCE = 3

ModelRecord = dict[str, Any]
ModelIndex = dict[str, ModelRecord]
FunctionModelMap = dict[str, list[ModelRecord]]


def _trae_support_root() -> Path:
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "Trae"
    return Path.home() / "AppData" / "Roaming" / "Trae"


def _global_storage_db() -> Path:
    return _trae_support_root() / "User" / "globalStorage" / "state.vscdb"


def _query_rows(db_path: Path, query: str, params: tuple[Any, ...] = ()) -> list[tuple[Any, ...]]:
    with sqlite3.connect(db_path) as connection:
        cursor = connection.execute(query, params)
        return cursor.fetchall()


def _list_candidate_keys(db_path: Path) -> dict[str, list[tuple[str, int]]]:
    rows = _query_rows(
        db_path,
        (
            "select key, length(value) "
            "from ItemTable "
            "where key like ? or key like ? "
            "order by key"
        ),
        (f"%{MODEL_LIST_MAP_SUFFIX}", f"%{GLOBAL_MODEL_MAP_SUFFIX}"),
    )
    model_list_keys: list[tuple[str, int]] = []
    global_model_keys: list[tuple[str, int]] = []
    for key, value_length in rows:
        record = (str(key), int(value_length))
        if str(key).endswith(MODEL_LIST_MAP_SUFFIX):
            model_list_keys.append(record)
        elif str(key).endswith(GLOBAL_MODEL_MAP_SUFFIX):
            global_model_keys.append(record)
    return {
        "model_list_map": model_list_keys,
        "global_model_map": global_model_keys,
    }


def _read_json_value(db_path: Path, key: str) -> Any:
    rows = _query_rows(db_path, "select value from ItemTable where key = ?", (key,))
    if not rows:
        return None
    raw_value = rows[0][0]
    if not isinstance(raw_value, str):
        raise RuntimeError(f"key={key} 的 value 不是文本")
    return json.loads(raw_value)


def _pick_user_id(
    candidates: dict[str, list[tuple[str, int]]],
    explicit_user_id: str | None,
) -> str:
    if explicit_user_id:
        return explicit_user_id
    if candidates["global_model_map"]:
        key = candidates["global_model_map"][0][0]
        return key[: -len(GLOBAL_MODEL_MAP_SUFFIX)]
    if not candidates["model_list_map"]:
        raise RuntimeError("未找到 Trae model_list_map 缓存键")
    key = max(candidates["model_list_map"], key=lambda item: item[1])[0]
    return key[: -len(MODEL_LIST_MAP_SUFFIX)]


def _safe_model_record(model: dict[str, Any]) -> ModelRecord:
    return {
        "name": model.get("name"),
        "display_name": model.get("display_name"),
        "provider": model.get("provider"),
        "base_url": model.get("base_url"),
        "is_custom_base_url": model.get("is_custom_base_url"),
        "config_source": model.get("config_source"),
        "custom_model_id": model.get("custom_model_id"),
        "builder": model.get("builder"),
        "client_connect": model.get("client_connect"),
        "is_preset": model.get("is_preset"),
        "status": model.get("status"),
        "auth_type": model.get("auth_type"),
    }


def _index_models(model_list_map: dict[str, Any]) -> tuple[ModelIndex, FunctionModelMap]:
    model_index: ModelIndex = {}
    function_map: FunctionModelMap = {}
    for function_name, raw_models in model_list_map.items():
        if not isinstance(raw_models, list):
            continue
        safe_models: list[dict[str, Any]] = []
        for raw_model in raw_models:
            if not isinstance(raw_model, dict):
                continue
            safe_model = _safe_model_record(raw_model)
            safe_models.append(safe_model)
            name = safe_model.get("name")
            if isinstance(name, str) and name and name not in model_index:
                model_index[name] = safe_model
        function_map[str(function_name)] = safe_models
    return model_index, function_map


def _selected_model_summary(
    global_model_map: dict[str, Any],
    model_index: ModelIndex,
) -> dict[str, dict[str, Any]]:
    resolved: dict[str, dict[str, Any]] = {}
    for slot, raw_value in global_model_map.items():
        if not isinstance(raw_value, str):
            continue
        parts = raw_value.split("_", 2)
        selected_name = (
            parts[2] if len(parts) == SELECTION_TOKEN_PARTS else raw_value
        )
        resolved[str(slot)] = {
            "selection_token": raw_value,
            "config_source": (
                int(parts[0])
                if len(parts) == SELECTION_TOKEN_PARTS and parts[0].isdigit()
                else None
            ),
            "provider": parts[1] if len(parts) == SELECTION_TOKEN_PARTS else None,
            "name": selected_name,
            "model": model_index.get(selected_name),
        }
    return resolved


def _local_custom_models(function_map: FunctionModelMap) -> FunctionModelMap:
    result: FunctionModelMap = {}
    for function_name, models in function_map.items():
        filtered = [
            model
            for model in models
            if model.get("is_custom_base_url") is True
            or (
                isinstance(model.get("base_url"), str)
                and "127.0.0.1" in str(model.get("base_url"))
            )
        ]
        if filtered:
            result[function_name] = filtered
    return result


def _connected_models(function_map: FunctionModelMap) -> FunctionModelMap:
    result: FunctionModelMap = {}
    for function_name, models in function_map.items():
        filtered = [
            model
            for model in models
            if model.get("config_source") == CONNECTED_CONFIG_SOURCE
            or model.get("client_connect") is True
        ]
        if filtered:
            result[function_name] = filtered
    return result


def _build_snapshot(db_path: Path, user_id: str) -> dict[str, Any]:
    model_list_key = f"{user_id}{MODEL_LIST_MAP_SUFFIX}"
    global_model_key = f"{user_id}{GLOBAL_MODEL_MAP_SUFFIX}"
    model_list_map = _read_json_value(db_path, model_list_key)
    if not isinstance(model_list_map, dict):
        raise RuntimeError(f"未找到或无法解析 model_list_map: {model_list_key}")
    global_model_map = _read_json_value(db_path, global_model_key)
    if global_model_map is None:
        global_model_map = {}
    if not isinstance(global_model_map, dict):
        raise RuntimeError(f"无法解析 globalModelMap: {global_model_key}")

    model_index, function_map = _index_models(model_list_map)
    return {
        "db_path": str(db_path),
        "user_id": user_id,
        "keys": {
            "model_list_map": model_list_key,
            "global_model_map": global_model_key,
        },
        "function_names": sorted(function_map),
        "function_counts": {
            function_name: len(models) for function_name, models in function_map.items()
        },
        "global_model_map": global_model_map,
        "selected_models": _selected_model_summary(global_model_map, model_index),
        "connected_models": _connected_models(function_map),
        "local_custom_models": _local_custom_models(function_map),
    }


def _render_text(snapshot: dict[str, Any]) -> str:
    lines = [
        f"db={snapshot['db_path']}",
        f"user_id={snapshot['user_id']}",
        f"function_names={','.join(snapshot['function_names'])}",
        "selected_models:",
    ]
    selected_models = snapshot["selected_models"]
    if not selected_models:
        lines.append("  <none>")
    else:
        for slot, item in selected_models.items():
            model = item.get("model") or {}
            lines.append(
                "  "
                f"{slot}: token={item.get('selection_token')} "
                f"name={item.get('name')} "
                f"base_url={model.get('base_url')} "
                f"is_custom_base_url={model.get('is_custom_base_url')} "
                f"config_source={model.get('config_source')}"
            )

    local_custom_models = snapshot["local_custom_models"]
    lines.append("local_custom_models:")
    if not local_custom_models:
        lines.append("  <none>")
    else:
        for function_name, models in local_custom_models.items():
            lines.append(f"  {function_name}: {len(models)}")
            for model in models:
                lines.append(
                    "    "
                    f"{model.get('name')} base_url={model.get('base_url')} "
                    f"is_custom_base_url={model.get('is_custom_base_url')}"
                )

    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="读取 Trae model_list_map/globalModelMap 快照")
    parser.add_argument("--db", type=Path, default=_global_storage_db())
    parser.add_argument("--user-id")
    parser.add_argument("--list-users", action="store_true", help="仅列出可用 user_id/key")
    parser.add_argument("--json", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    db_path = args.db.expanduser().resolve()
    if not db_path.is_file():
        raise SystemExit(f"未找到 state.vscdb: {db_path}")

    candidates = _list_candidate_keys(db_path)
    if args.list_users:
        payload = {
            "db_path": str(db_path),
            "candidates": candidates,
        }
        if args.json:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    user_id = _pick_user_id(candidates, args.user_id)
    snapshot = _build_snapshot(db_path, user_id)
    if args.json:
        print(json.dumps(snapshot, ensure_ascii=False, indent=2))
    else:
        print(_render_text(snapshot))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
