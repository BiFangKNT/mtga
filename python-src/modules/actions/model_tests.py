from __future__ import annotations

from collections.abc import Callable
from typing import Any

import requests

from modules.network.outbound_proxy import create_outbound_session
from modules.proxy.proxy_config import normalize_middle_route

HTTP_OK = 200
CONTENT_PREVIEW_LEN = 50


def _extract_model_items(payload: Any) -> list[dict[str, Any]]:
    if not isinstance(payload, dict):
        return []

    data = payload.get("data")
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]

    result = payload.get("result")
    if isinstance(result, dict):
        result_data = result.get("data")
        if isinstance(result_data, list):
            return [item for item in result_data if isinstance(item, dict)]

    alt = payload.get("models")
    if isinstance(alt, list):
        return [item for item in alt if isinstance(item, dict)]

    return []


def _collect_model_ids(model_items: list[dict[str, Any]]) -> set[str]:
    model_ids: set[str] = set()
    for item in model_items:
        model_id = item.get("id")
        if isinstance(model_id, str):
            model_ids.add(model_id)
    return model_ids


def _build_middle_route_path(middle_route: str, suffix: str) -> str:
    normalized = normalize_middle_route(middle_route)
    if normalized == "/":
        return f"/{suffix.lstrip('/')}"
    return f"{normalized.rstrip('/')}/{suffix.lstrip('/')}"


def _log_model_list(
    payload: Any,
    model_id: str,
    log_func: Callable[[str], None],
) -> None:
    model_ids = _parse_model_ids(payload, log_func)
    if not model_ids:
        return
    if model_id in model_ids:
        log_func(f"✅ 发现模型: {model_id}")
    else:
        log_func(f"❌ 未找到模型: {model_id}")


def _log_response_error(
    response: requests.Response,
    log_func: Callable[[str], None],
) -> None:
    log_func(f"❌ 模型列表获取失败: HTTP {response.status_code}")
    try:
        error_info = response.text[:200]
        log_func(f"   错误信息: {error_info}")
    except Exception:
        log_func("   (无法获取错误详情)")


def _parse_response_json(
    response: requests.Response,
    log_func: Callable[[str], None],
) -> Any | None:
    try:
        return response.json()
    except Exception:
        log_func("   (响应成功，但无法解析详细信息)")
        return None


def _parse_model_ids(
    payload: Any,
    log_func: Callable[[str], None],
) -> list[str]:
    if isinstance(payload, dict) and payload.get("object"):
        log_func(f"   对象类型: {payload['object']}")

    model_items = _extract_model_items(payload)
    if not model_items:
        log_func("❌ 响应中未发现模型列表")
        return []

    model_ids = sorted(_collect_model_ids(model_items))
    log_func(f"   模型数量: {len(model_ids)}")
    return model_ids


def _prepare_chat_test_request(
    config_group: dict[str, Any],
    log_func: Callable[[str], None],
) -> tuple[str, dict[str, str], dict[str, Any], str] | None:
    api_url = config_group.get("api_url", "").rstrip("/")
    model_id = config_group.get("model_id", "")
    api_key = config_group.get("api_key", "")

    if not api_url or not model_id:
        log_func("测活失败: API URL或模型ID为空")
        return None

    route_path = _build_middle_route_path(
        config_group.get("middle_route", ""),
        "chat/completions",
    )
    test_url = f"{api_url}{route_path}"

    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    test_data = {
        "model": model_id,
        "messages": [{"role": "user", "content": "1"}],
        "max_tokens": 1,
        "temperature": 0,
    }

    return test_url, headers, test_data, model_id


def _log_chat_completion_response(
    response: requests.Response,
    model_id: str,
    log_func: Callable[[str], None],
) -> None:
    if response.status_code == HTTP_OK:
        log_func(f"✅ 模型测活成功: {model_id}")
        try:
            completion_info = response.json()
            if "choices" in completion_info and completion_info["choices"]:
                content = (
                    completion_info["choices"][0]
                    .get("message", {})
                    .get("content", "")
                    .strip()
                )
                preview = content[:CONTENT_PREVIEW_LEN]
                suffix = "..." if len(content) > CONTENT_PREVIEW_LEN else ""
                log_func(f"   响应内容: {preview}{suffix}")
            if "usage" in completion_info:
                usage = completion_info["usage"]
                log_func(f"   消耗tokens: {usage.get('total_tokens', '未知')}")
        except Exception:
            log_func("   (响应成功，但无法解析详细信息)")
        return

    log_func(f"❌ 模型测活失败: HTTP {response.status_code}")
    try:
        error_info = response.text[:200]
        log_func(f"   错误信息: {error_info}")
    except Exception:
        log_func("   (无法获取错误详情)")


def _fetch_model_payload(
    config_group: dict[str, Any],
    log_func: Callable[[str], None],
    *,
    model_id: str | None = None,
) -> Any | None:
    api_url = config_group.get("api_url", "").rstrip("/")
    if not api_url:
        log_func("检查失败: API URL为空")
        return None

    route_path = _build_middle_route_path(
        config_group.get("middle_route", ""),
        "models",
    )
    test_url = f"{api_url}{route_path}"
    headers: dict[str, str] = {}
    api_key = config_group.get("api_key", "")
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    log_func(f"正在获取模型列表: {test_url}")

    suffix = f": {model_id}" if model_id else ""
    session = create_outbound_session()
    try:
        response = session.get(test_url, headers=headers, timeout=10)
    except requests.exceptions.Timeout:
        log_func(f"❌ 模型列表获取超时{suffix}")
        return None
    except requests.exceptions.RequestException as exc:
        log_func(f"❌ 模型列表获取网络错误{suffix}: {str(exc)}")
        return None
    except Exception as exc:
        log_func(f"❌ 模型列表获取意外错误{suffix}: {str(exc)}")
        return None
    finally:
        session.close()

    if response.status_code != HTTP_OK:
        _log_response_error(response, log_func)
        return None

    log_func("✅ 模型列表获取成功")
    return _parse_response_json(response, log_func)


def _run_model_connection_test(
    config_group: dict[str, Any],
    log_func: Callable[[str], None],
) -> None:
    model_id = "未知模型"
    model_id = config_group.get("model_id", "")
    if not config_group.get("api_url") or not model_id:
        log_func("检查失败: API URL或模型ID为空")
        return

    payload = _fetch_model_payload(config_group, log_func, model_id=model_id)
    if payload is None:
        return
    _log_model_list(payload, model_id, log_func)


def fetch_model_list(
    config_group: dict[str, Any],
    *,
    log_func: Callable[[str], None] = print,
) -> tuple[list[str], bool]:
    payload = _fetch_model_payload(config_group, log_func)
    if payload is None:
        return [], False
    model_ids = _parse_model_ids(payload, log_func)
    if not model_ids:
        return [], False
    return model_ids, True


def test_model_in_list(
    config_group: dict[str, Any],
    *,
    log_func: Callable[[str], None] = print,
    thread_manager,
) -> None:
    """测试模型是否在列表中（GET /v1/models）。"""
    thread_manager.run(
        "test_model_in_list",
        lambda: _run_model_connection_test(config_group, log_func),
    )


def test_chat_completion(
    config_group: dict[str, Any],
    *,
    log_func: Callable[[str], None] = print,
    thread_manager,
) -> None:
    """测试聊天补全连接（POST /v1/chat/completions）。"""

    def run_test():
        try:
            request_info = _prepare_chat_test_request(config_group, log_func)
            if not request_info:
                return
            test_url, headers, test_data, model_id = request_info
            log_func(f"正在测活模型: {model_id} (会消耗少量tokens)")

            session = create_outbound_session()
            try:
                response = session.post(
                    test_url,
                    json=test_data,
                    headers=headers,
                    timeout=30,
                )
            finally:
                session.close()

            _log_chat_completion_response(response, model_id, log_func)

        except requests.exceptions.Timeout:
            log_func("❌ 模型测活超时")
        except requests.exceptions.RequestException as exc:
            log_func(f"❌ 模型测活网络错误: {str(exc)}")
        except Exception as exc:
            log_func(f"❌ 模型测活意外错误: {str(exc)}")

    thread_manager.run("test_chat_completion", run_test)
