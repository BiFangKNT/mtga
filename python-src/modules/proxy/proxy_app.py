from __future__ import annotations

import asyncio
import contextlib
import inspect
import json
import logging
import threading
import time
import uuid
from collections.abc import Callable, Generator
from typing import Any, cast

from flask import Flask, Response, jsonify, request

from modules.proxy.proxy_auth import ProxyAuth
from modules.proxy.proxy_config import DEFAULT_MIDDLE_ROUTE, ProxyConfig, build_proxy_config
from modules.proxy.proxy_transport import ProxyTransport
from modules.proxy.upstream_adapter import (
    RESPONSES_REQUEST_API,
    normalize_upstream_error,
)
from modules.runtime.error_codes import ErrorCode
from modules.runtime.operation_result import OperationResult
from modules.runtime.resource_manager import ResourceManager
from modules.services.system_prompt_service import SystemPromptStore


class ProxyApp:
    """代理服务的领域逻辑：配置解析 + Flask 路由 + 上游转发。"""

    def __init__(
        self,
        config: dict[str, Any] | None = None,
        log_func: Callable[[str], None] = print,
        *,
        resource_manager: ResourceManager,
    ) -> None:
        self.config: dict[str, Any] = config or {}
        self.log_func = log_func
        self.resource_manager = resource_manager
        self._config_lock = threading.RLock()
        self._retired_transports: dict[int, ProxyTransport] = {}
        self._transport_ref_counts: dict[int, int] = {}
        self._root_logger_default_level = logging.getLogger().level
        self._app_logger_default_level = logging.WARNING
        self.app: Flask | None = None
        self.valid = True
        self.proxy_config: ProxyConfig | None = None
        self.auth: ProxyAuth | None = None
        self.transport: ProxyTransport | None = None
        self.target_api_base_url = ""
        self.middle_route = ""
        self.inbound_route = DEFAULT_MIDDLE_ROUTE
        self.custom_model_id = ""
        self.target_model_id = ""
        self.stream_mode: str | None = None
        self.debug_mode = False
        self.disable_ssl_strict_mode = False
        self.system_prompt_store = SystemPromptStore(resource_manager)

        proxy_config = build_proxy_config(
            self.config,
            resource_manager=self.resource_manager,
            log_func=self.log_func,
        )
        if not proxy_config:
            self.valid = False
            return

        self.proxy_config = proxy_config
        self.target_api_base_url = proxy_config.target_api_base_url
        self.middle_route = proxy_config.middle_route
        self.custom_model_id = proxy_config.custom_model_id
        self.target_model_id = proxy_config.target_model_id
        self.stream_mode = proxy_config.stream_mode  # None, 'true', 'false'
        self.debug_mode = proxy_config.debug_mode
        self.disable_ssl_strict_mode = proxy_config.disable_ssl_strict_mode
        self.auth = ProxyAuth(proxy_config.mtga_auth_key)
        self.transport = ProxyTransport(
            resource_manager=self.resource_manager,
            disable_ssl_strict_mode=self.disable_ssl_strict_mode,
            log_func=self.log_func,
        )

        self._create_app()

    def close(self) -> None:
        transports_to_close: list[ProxyTransport] = []
        with self._config_lock:
            if self.transport:
                transports_to_close.append(self.transport)
            transports_to_close.extend(self._retired_transports.values())
            self._retired_transports = {}
            self._transport_ref_counts = {}
            self.transport = None
            self.auth = None
        for transport in transports_to_close:
            with contextlib.suppress(Exception):
                transport.close()

    def _snapshot_runtime_state(self) -> dict[str, Any]:
        with self._config_lock:
            return {
                "inbound_route": self.inbound_route,
                "target_api_base_url": self.target_api_base_url,
                "middle_route": self.middle_route,
                "custom_model_id": self.custom_model_id,
                "target_model_id": self.target_model_id,
                "stream_mode": self.stream_mode,
                "debug_mode": self.debug_mode,
                "auth": self.auth,
                "transport": self.transport,
                "proxy_config": self.proxy_config,
            }

    def _snapshot_chat_runtime_state(self) -> dict[str, Any]:
        with self._config_lock:
            transport = self.transport
            if transport is not None:
                key = id(transport)
                self._transport_ref_counts[key] = (
                    self._transport_ref_counts.get(key, 0) + 1
                )
            return {
                "inbound_route": self.inbound_route,
                "target_api_base_url": self.target_api_base_url,
                "middle_route": self.middle_route,
                "custom_model_id": self.custom_model_id,
                "target_model_id": self.target_model_id,
                "stream_mode": self.stream_mode,
                "debug_mode": self.debug_mode,
                "auth": self.auth,
                "transport": transport,
                "proxy_config": self.proxy_config,
            }

    def _release_transport_ref(self, transport: ProxyTransport | None) -> None:
        if transport is None:
            return
        close_target: ProxyTransport | None = None
        with self._config_lock:
            key = id(transport)
            current = self._transport_ref_counts.get(key, 0)
            if current <= 1:
                self._transport_ref_counts.pop(key, None)
                retired = self._retired_transports.pop(key, None)
                if retired is not None:
                    close_target = retired
            else:
                self._transport_ref_counts[key] = current - 1
        if close_target is not None:
            with contextlib.suppress(Exception):
                close_target.close()

    def _retire_transport(self, transport: ProxyTransport | None) -> None:
        if transport is None:
            return
        close_target: ProxyTransport | None = None
        with self._config_lock:
            key = id(transport)
            if self._transport_ref_counts.get(key, 0) > 0:
                self._retired_transports[key] = transport
                return
            close_target = transport
        with contextlib.suppress(Exception):
            close_target.close()

    def _apply_debug_logging(self, debug_mode: bool) -> None:
        app = self.app
        if not app:
            return
        root_logger = logging.getLogger()
        if debug_mode:
            root_logger.setLevel(logging.INFO)
            app.logger.setLevel(logging.INFO)
            return
        root_logger.setLevel(self._root_logger_default_level)
        app.logger.setLevel(self._app_logger_default_level)

    def apply_runtime_config(self, raw_config: dict[str, Any] | None) -> OperationResult:
        new_proxy_config = build_proxy_config(
            raw_config,
            resource_manager=self.resource_manager,
            log_func=lambda _message: None,
        )
        if not new_proxy_config:
            return OperationResult.failure(
                "config_invalid",
                code=ErrorCode.CONFIG_INVALID,
            )

        new_auth = ProxyAuth(new_proxy_config.mtga_auth_key)
        new_transport = ProxyTransport(
            resource_manager=self.resource_manager,
            disable_ssl_strict_mode=new_proxy_config.disable_ssl_strict_mode,
            log_func=self.log_func,
        )
        old_transport: ProxyTransport | None = None
        with self._config_lock:
            old_transport = self.transport
            self.proxy_config = new_proxy_config
            self.target_api_base_url = new_proxy_config.target_api_base_url
            self.middle_route = new_proxy_config.middle_route
            self.custom_model_id = new_proxy_config.custom_model_id
            self.target_model_id = new_proxy_config.target_model_id
            self.stream_mode = new_proxy_config.stream_mode
            self.debug_mode = new_proxy_config.debug_mode
            self.disable_ssl_strict_mode = new_proxy_config.disable_ssl_strict_mode
            self.auth = new_auth
            self.transport = new_transport

        self._apply_debug_logging(self.debug_mode)

        self._retire_transport(old_transport)
        return OperationResult.success("config_applied", apply_status="applied")

    @staticmethod
    def _new_request_id() -> str:
        return uuid.uuid4().hex[:6]

    @staticmethod
    def _timestamp_ms() -> str:
        now = time.time()
        base = time.strftime("%H:%M:%S", time.localtime(now))
        ms = int((now % 1) * 1000)
        return f"{base}.{ms:03d}"

    @staticmethod
    def _is_proxy_stream_response(
        payload: Any,
        payload_dict: dict[str, Any] | None,
        *,
        stream_enabled: bool,
    ) -> bool:
        if not stream_enabled or payload_dict is not None:
            return False
        if isinstance(payload, (str, bytes, bytearray)):
            return False
        return hasattr(payload, "__iter__")

    @staticmethod
    def _close_upstream_stream(payload: Any, *, log: Callable[[str], None]) -> None:
        if payload is None:
            return

        close_method = getattr(payload, "close", None)
        if callable(close_method):
            try:
                close_result = close_method()
                if inspect.isawaitable(close_result):
                    asyncio.run(ProxyApp._consume_awaitable(close_result))
                return
            except Exception as exc:  # noqa: BLE001
                log(f"关闭上游流 close() 失败，尝试 aclose(): {exc}")

        aclose_method = getattr(payload, "aclose", None)
        if callable(aclose_method):
            try:
                asyncio.run(ProxyApp._consume_awaitable(aclose_method()))
            except Exception as exc:  # noqa: BLE001
                log(f"关闭上游流 aclose() 失败: {exc}")

    @staticmethod
    async def _consume_awaitable(awaitable: Any) -> None:
        await awaitable

    def _log_request(self, request_id: str, message: str) -> None:
        self.log_func(f"{self._timestamp_ms()} [{request_id}] {message}")

    def _get_mapped_model_id(self) -> str:
        return self.custom_model_id

    def _extract_system_prompt_text(self, content: Any) -> str:
        if isinstance(content, str):
            return content.strip()
        if not isinstance(content, list):
            return ""
        content_list = cast(list[Any], content)

        parts: list[str] = []
        for item in content_list:
            if isinstance(item, str):
                text = item.strip()
                if text:
                    parts.append(text)
                continue
            if not isinstance(item, dict):
                continue
            item_map = cast(dict[str, Any], item)
            text_value = item_map.get("text")
            if isinstance(text_value, str):
                text = text_value.strip()
                if text:
                    parts.append(text)
        return "\n".join(parts).strip()

    def _collect_message_system_prompt_entries(
        self,
        messages: list[Any],
    ) -> tuple[dict[int, str], list[tuple[str, str]]]:
        indexed_hashes: dict[int, str] = {}
        capture_entries: list[tuple[str, str]] = []

        for index, message in enumerate(messages):
            if not isinstance(message, dict):
                continue
            message_map = cast(dict[str, Any], message)
            if message_map.get("role") not in {"system", "developer"}:
                continue
            extracted = self._extract_system_prompt_text(message_map.get("content"))
            if not extracted:
                continue
            hash_value = self.system_prompt_store.compute_hash(extracted)
            indexed_hashes[index] = hash_value
            capture_entries.append((hash_value, extracted))

        return indexed_hashes, capture_entries

    def _apply_overrides_to_messages(
        self,
        *,
        messages: list[Any],
        indexed_hashes: dict[int, str],
        overrides: dict[str, str],
        log: Callable[[str], None],
    ) -> tuple[list[Any], bool]:
        changed = False
        next_messages: list[Any] = []

        for index, message in enumerate(messages):
            hash_value = indexed_hashes.get(index)
            if not hash_value:
                next_messages.append(message)
                continue
            edited_text = overrides.get(hash_value)
            if edited_text is None:
                next_messages.append(message)
                continue

            changed = True
            if edited_text == "":
                log(f"🧹 清空系统提示词并移除消息 hash={hash_value[:12]}")
                continue

            if isinstance(message, dict):
                message_map = cast(dict[str, Any], message)
                replaced = dict(message_map)
                replaced["content"] = edited_text
                next_messages.append(replaced)
            else:
                next_messages.append(message)
            log(f"✏️ 应用系统提示词增量 hash={hash_value[:12]}")

        return next_messages, changed

    def _collect_response_prompt_entries(
        self,
        request_data: dict[str, Any],
    ) -> tuple[str | None, dict[int, str], list[tuple[str, str]]]:
        instructions_hash: str | None = None
        indexed_hashes: dict[int, str] = {}
        capture_entries: list[tuple[str, str]] = []

        instructions_text = self._extract_system_prompt_text(request_data.get("instructions"))
        if instructions_text:
            instructions_hash = self.system_prompt_store.compute_hash(instructions_text)
            capture_entries.append((instructions_hash, instructions_text))

        input_items_obj = request_data.get("input")
        if not isinstance(input_items_obj, list):
            return instructions_hash, indexed_hashes, capture_entries

        input_items = cast(list[Any], input_items_obj)
        for index, item in enumerate(input_items):
            if not isinstance(item, dict):
                continue
            item_map = cast(dict[str, Any], item)
            if item_map.get("role") not in {"system", "developer"}:
                continue
            extracted = self._extract_system_prompt_text(item_map.get("content"))
            if not extracted:
                continue
            hash_value = self.system_prompt_store.compute_hash(extracted)
            indexed_hashes[index] = hash_value
            capture_entries.append((hash_value, extracted))

        return instructions_hash, indexed_hashes, capture_entries

    def _apply_overrides_to_input_items(
        self,
        *,
        input_items: list[Any],
        indexed_hashes: dict[int, str],
        overrides: dict[str, str],
        log: Callable[[str], None],
    ) -> tuple[list[Any], bool]:
        changed = False
        next_items: list[Any] = []

        for index, item in enumerate(input_items):
            hash_value = indexed_hashes.get(index)
            if not hash_value:
                next_items.append(item)
                continue
            edited_text = overrides.get(hash_value)
            if edited_text is None:
                next_items.append(item)
                continue

            changed = True
            if edited_text == "":
                log(f"🧹 清空系统提示词并移除输入消息 hash={hash_value[:12]}")
                continue

            if isinstance(item, dict):
                item_map = cast(dict[str, Any], item)
                replaced = dict(item_map)
                replaced["content"] = edited_text
                next_items.append(replaced)
            else:
                next_items.append(item)
            log(f"✏️ 应用系统提示词增量 hash={hash_value[:12]}")

        return next_items, changed

    def _apply_system_prompt_overrides(  # noqa: PLR0912
        self,
        *,
        request_data: dict[str, Any],
        log: Callable[[str], None],
    ) -> None:
        messages_obj = request_data.get("messages")
        if isinstance(messages_obj, list):
            messages = cast(list[Any], messages_obj)
            indexed_hashes, capture_entries = self._collect_message_system_prompt_entries(
                messages
            )

            if not capture_entries:
                return

            added_hashes, overrides = self.system_prompt_store.capture_and_collect_overrides(
                capture_entries
            )
            for added_hash in added_hashes:
                log(f"📝 收录系统提示词 hash={added_hash[:12]}")

            if not overrides:
                return

            next_messages, changed = self._apply_overrides_to_messages(
                messages=messages,
                indexed_hashes=indexed_hashes,
                overrides=overrides,
                log=log,
            )
            if changed:
                request_data["messages"] = next_messages
            return

        instructions_hash, indexed_hashes, capture_entries = (
            self._collect_response_prompt_entries(request_data)
        )

        if not capture_entries:
            return

        added_hashes, overrides = self.system_prompt_store.capture_and_collect_overrides(
            capture_entries
        )
        for added_hash in added_hashes:
            log(f"📝 收录系统提示词 hash={added_hash[:12]}")

        if not overrides:
            return

        if instructions_hash:
            edited_instructions = overrides.get(instructions_hash)
            if edited_instructions is not None:
                if edited_instructions == "":
                    request_data.pop("instructions", None)
                    log(f"🧹 清空系统提示词并移除 instructions hash={instructions_hash[:12]}")
                else:
                    request_data["instructions"] = edited_instructions
                    log(f"✏️ 应用系统提示词增量 hash={instructions_hash[:12]}")

        input_items_obj = request_data.get("input")
        if not isinstance(input_items_obj, list):
            return

        next_input_items, changed = self._apply_overrides_to_input_items(
            input_items=cast(list[Any], input_items_obj),
            indexed_hashes=indexed_hashes,
            overrides=overrides,
            log=log,
        )
        if changed:
            request_data["input"] = next_input_items

    def _try_apply_system_prompt_overrides(
        self,
        *,
        request_data: dict[str, Any],
        log: Callable[[str], None],
    ) -> None:
        try:
            self._apply_system_prompt_overrides(request_data=request_data, log=log)
        except Exception as prompt_exc:  # noqa: BLE001
            log(f"⚠️ 系统提示词处理失败: {prompt_exc}")

    def _build_route(self, base_route: str, suffix: str) -> str:
        middle_route = base_route or ""
        if not middle_route.startswith("/"):
            middle_route = f"/{middle_route}"
        if middle_route == "/":
            return f"/{suffix.lstrip('/')}"
        return f"{middle_route.rstrip('/')}/{suffix.lstrip('/')}"

    def _open_sse_debug_log(
        self,
        *,
        debug_mode: bool,
        transport: ProxyTransport,
        log: Callable[[str], None],
    ) -> tuple[contextlib.ExitStack | None, Any | None, str | None]:
        if not debug_mode:
            return None, None, None
        try:
            log_path = transport.prepare_sse_log_path()
            log_file_stack = contextlib.ExitStack()
            log_file = log_file_stack.enter_context(open(log_path, "wb"))  # noqa: SIM115
            log(f"SSE 归一化数据将记录到: {log_path}")
            return log_file_stack, log_file, log_path
        except Exception as log_exc:  # noqa: BLE001
            log(f"SSE 日志文件创建失败: {log_exc}")
            return None, None, None

    @staticmethod
    def _write_sse_debug_chunk(
        log_file: Any | None,
        chunk_bytes: bytes,
        *,
        log: Callable[[str], None],
    ) -> Any | None:
        if not log_file:
            return log_file
        try:
            log_file.write(chunk_bytes)
            log_file.flush()
            return log_file
        except Exception as write_exc:  # noqa: BLE001
            log(f"SSE 日志写入失败，停止记录: {write_exc}")
            with contextlib.suppress(Exception):
                log_file.close()
            return None

    def _create_app(self) -> None:
        self.app = Flask(__name__)
        self._app_logger_default_level = self.app.logger.level
        self._apply_debug_logging(self.debug_mode)

        models_route = self._build_route(self.inbound_route, "models")
        chat_completions_route = self._build_route(
            self.inbound_route, "chat/completions"
        )

        self.app.add_url_rule(models_route, "get_models", self._get_models, methods=["GET"])
        self.app.add_url_rule(
            chat_completions_route,
            "chat_completions",
            self._chat_completions,
            methods=["POST"],
        )

    def _get_models(self) -> tuple[Response, int] | Response:
        snapshot = self._snapshot_runtime_state()
        inbound_route = str(snapshot["inbound_route"])
        auth = snapshot["auth"]
        mapped_model_id = str(snapshot["custom_model_id"])
        self.log_func(f"收到模型列表请求 {self._build_route(inbound_route, 'models')}")
        if not auth:
            self.log_func("代理鉴权未就绪")
            return jsonify(
                {"error": {"message": "Proxy not ready", "type": "server_error"}}
            ), 500

        auth_header = request.headers.get("Authorization")
        if not auth.verify(auth_header):
            self.log_func("模型列表请求鉴权失败")
            return jsonify(
                {"error": {"message": "Invalid authentication", "type": "authentication_error"}}
            ), 401

        model_data = {
            "object": "list",
            "data": [
                {
                    "id": mapped_model_id,
                    "object": "model",
                    "owned_by": "openai",
                    "created": int(time.time()),
                    "permission": [
                        {
                            "id": f"modelperm-{mapped_model_id}",
                            "object": "model_permission",
                            "created": int(time.time()),
                            "allow_create_engine": False,
                            "allow_sampling": True,
                            "allow_logprobs": True,
                            "allow_search_indices": False,
                            "allow_view": True,
                            "allow_fine_tuning": False,
                            "organization": "*",
                            "group": None,
                            "is_blocking": False,
                        }
                    ],
                }
            ],
        }

        self.log_func(f"返回映射模型: {mapped_model_id}")
        return jsonify(model_data)

    def _chat_completions(  # noqa: PLR0911, PLR0912, PLR0915
        self,
    ) -> tuple[Response, int] | Response:
        request_id = self._new_request_id()

        def log(message: str) -> None:
            self._log_request(request_id, message)

        snapshot = self._snapshot_chat_runtime_state()
        inbound_route = str(snapshot["inbound_route"])
        target_model_id = str(snapshot["target_model_id"])
        stream_mode = snapshot["stream_mode"]
        debug_mode = bool(snapshot["debug_mode"])
        auth = snapshot["auth"]
        transport = snapshot["transport"]
        proxy_config_obj = snapshot["proxy_config"]
        proxy_config = (
            proxy_config_obj if isinstance(proxy_config_obj, ProxyConfig) else None
        )
        transport_released = False

        def release_transport() -> None:
            nonlocal transport_released
            if transport_released:
                return
            transport_released = True
            self._release_transport_ref(transport)

        log(
            "收到 Chat Completions 请求 "
            f"{self._build_route(inbound_route, 'chat/completions')}"
        )

        if not (auth and transport and proxy_config):
            log("代理服务未就绪")
            release_transport()
            return jsonify({"error": "Proxy not ready"}), 500

        if debug_mode:
            headers_str = "\\n".join(f"{k}: {v}" for k, v in request.headers.items())
            log_message = (
                f"--- 请求头 (调试模式) ---\\n{headers_str}\\n"
                "--------------------------------------"
            )
            try:
                body_str = request.get_data(as_text=True)
                log_message += (
                    f"--- 请求体 (调试模式) ---\\n{body_str}\\n"
                    "--------------------------------------"
                )
            except Exception as body_exc:
                error_msg = f"读取请求体数据时出错: {body_exc}\\n"
                log(error_msg)
                log_message += error_msg
            log(log_message)

        request_data_obj = request.get_json(silent=True)

        if not isinstance(request_data_obj, dict):
            log("解析 JSON 失败或请求不是 JSON 格式")
            log(f"Content-Type: {request.headers.get('Content-Type')}")
            release_transport()
            return jsonify(
                {
                    "error": "Invalid JSON or Content-Type",
                    "message": (
                        "The request body must be valid JSON and the Content-Type header "
                        "must be 'application/json'."
                    ),
                }
            ), 400
        request_data = cast(dict[str, Any], request_data_obj)
        self._try_apply_system_prompt_overrides(request_data=request_data, log=log)

        client_requested_stream = request_data.get("stream", False)
        log(f"客户端请求的流模式: {client_requested_stream}")

        if "model" in request_data:
            original_model = request_data["model"]
            log(f"替换模型名: {original_model} -> {target_model_id}")
            request_data["model"] = target_model_id
        else:
            log(f"请求中没有 model 字段，添加 model: {target_model_id}")
            request_data["model"] = target_model_id

        if stream_mode is not None:
            stream_value = stream_mode == "true"
            if "stream" in request_data:
                original_stream_value = request_data["stream"]
                log(f"强制修改流模式: {original_stream_value} -> {stream_value}")
                request_data["stream"] = stream_value
            else:
                log(f"请求中没有 stream 参数，设置为 {stream_value}")
                request_data["stream"] = stream_value

        auth_header = request.headers.get("Authorization")
        if not auth.verify(auth_header):
            log("Chat Completions 请求 MTGA 鉴权失败")
            release_transport()
            return jsonify(
                {"error": {"message": "Invalid authentication", "type": "authentication_error"}}
            ), 401

        try:
            fallback_api_key = (proxy_config.api_key or "").strip()
            if fallback_api_key:
                log("使用配置组中的 API key")
            else:
                log("配置组未设置 API key；下游 Authorization 仅用于 MTGA 鉴权，不会透传到上游")

            route = transport.adapter.build_route(
                proxy_config,
                fallback_api_key=fallback_api_key,
            )
            log(
                f"LiteLLM 路由: provider={route.provider} "
                f"request_api={route.request_api} model={route.litellm_model} "
                f"base_url={route.base_url}"
            )
            if route.litellm_base_url and route.litellm_base_url != route.base_url:
                log(f"LiteLLM 内部基路径: {route.litellm_base_url}")

            is_stream = bool(request_data.get("stream", False))
            log(f"流模式: {is_stream}")

            response_from_target = transport.adapter.create_chat_completion(
                route=route,
                request_data=request_data,
            )

            response_json = transport.coerce_payload_dict(response_from_target)
            if response_json is not None:
                normalized_response_json = transport.normalize_chat_completion_payload(
                    response_json,
                    provider=route.provider,
                    fallback_model=route.litellm_model,
                )
                if normalized_response_json is not None:
                    response_json = normalized_response_json
            should_proxy_stream = self._is_proxy_stream_response(
                response_from_target,
                response_json,
                stream_enabled=is_stream,
            )

            if should_proxy_stream:
                log("返回流式响应")

                log_file_stack, log_file, log_path = self._open_sse_debug_log(
                    debug_mode=debug_mode,
                    transport=transport,
                    log=log,
                )

                def generate_stream() -> Generator[bytes]:  # noqa: PLR0915, PLR0912
                    nonlocal log_file, log_file_stack
                    event_index = 0
                    done_sent = False
                    client_model_name = transport.normalize_provider_model_name(
                        route.litellm_model,
                        provider=route.provider,
                    )

                    try:
                        for chunk in response_from_target:
                            normalized_chunk = transport.normalize_chat_completion_payload(
                                chunk,
                                provider=route.provider,
                                fallback_model=route.litellm_model,
                            )
                            event_payload = (
                                normalized_chunk if normalized_chunk is not None else chunk
                            )
                            event_index += 1

                            normalized_bytes, _finish_reason = transport.normalize_openai_event(
                                event_payload,
                                event_index,
                                model_name=client_model_name,
                                log=log,
                            )
                            log_file = self._write_sse_debug_chunk(
                                log_file,
                                normalized_bytes,
                                log=log,
                            )
                            if normalized_bytes == b"data: [DONE]\n\n":
                                done_sent = True
                            try:
                                yield normalized_bytes
                            except GeneratorExit:
                                log(f"DOWN 连接提前中断，已读取上游 evt#{event_index}")
                                raise
                            except Exception as downstream_exc:  # noqa: BLE001
                                log(f"DOWN 写入异常，停止向下游发送: {downstream_exc}")
                                break
                        if not done_sent:
                            done_bytes = b"data: [DONE]\n\n"
                            log_file = self._write_sse_debug_chunk(
                                log_file,
                                done_bytes,
                                log=log,
                            )
                            yield done_bytes
                    finally:
                        self._close_upstream_stream(response_from_target, log=log)
                        release_transport()
                        if log_file_stack:
                            with contextlib.suppress(Exception):
                                log_file_stack.close()
                        if log_path:
                            log(f"SSE 记录完成: {log_path}")
                        if debug_mode:
                            log(f"UP 流结束，累计 {event_index} 个事件")

                return Response(
                    generate_stream(),
                    content_type="text/event-stream",
                )

            if response_json is None:
                log("上游响应不是 JSON 对象")
                release_transport()
                return jsonify({"error": "Invalid response from target API"}), 502

            if client_requested_stream:
                if route.request_api == RESPONSES_REQUEST_API:
                    log("上游为 Responses API，代理侧模拟 Chat Completions SSE")
                elif stream_mode == "false":
                    log("将非流式响应转换为 Chat Completions SSE 返回给客户端")
                else:
                    log("上游未返回流式结果，代理侧模拟 Chat Completions SSE")

                log_file_stack, log_file, log_path = self._open_sse_debug_log(
                    debug_mode=debug_mode,
                    transport=transport,
                    log=log,
                )

                def simulate_stream() -> Generator[bytes]:
                    nonlocal log_file, log_file_stack
                    model_name_obj = response_json.get("model")
                    model_name = (
                        model_name_obj
                        if isinstance(model_name_obj, str)
                        else route.litellm_model
                    )
                    try:
                        simulated_chunks = transport.build_chat_completion_stream_chunks(
                            response_json
                        )
                        for event_index, chunk_payload in enumerate(
                            simulated_chunks,
                            start=1,
                        ):
                            event_bytes, _finish_reason = transport.normalize_openai_event(
                                chunk_payload,
                                event_index,
                                model_name=model_name,
                                log=log,
                            )
                            log_file = self._write_sse_debug_chunk(
                                log_file,
                                event_bytes,
                                log=log,
                            )
                            yield event_bytes
                            time.sleep(0.01)
                        done_bytes = b"data: [DONE]\n\n"
                        log_file = self._write_sse_debug_chunk(
                            log_file,
                            done_bytes,
                            log=log,
                        )
                        yield done_bytes
                    finally:
                        if log_file_stack:
                            with contextlib.suppress(Exception):
                                log_file_stack.close()
                        if log_path:
                            log(f"SSE 记录完成: {log_path}")

                release_transport()
                return Response(simulate_stream(), content_type="text/event-stream")

            if debug_mode:
                response_str = json.dumps(response_json, indent=2, ensure_ascii=False)
                log(
                    f"--- 完整响应体 (调试模式) ---\\n{response_str}\\n"
                    "--------------------------------------"
                )
            else:
                log("返回非流式 JSON 响应")
            release_transport()
            return jsonify(response_json)

        except Exception as e:
            error_info = normalize_upstream_error(e)
            log(error_info.log_message)
            release_transport()
            return jsonify(error_info.response_body), error_info.status_code


__all__ = ["ProxyApp"]
