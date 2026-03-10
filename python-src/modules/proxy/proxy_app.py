from __future__ import annotations

import contextlib
import json
import logging
import threading
import time
import uuid
from collections.abc import Callable, Generator
from typing import Any, cast

import requests
from flask import Flask, Response, jsonify, request

from modules.proxy.proxy_auth import ProxyAuth
from modules.proxy.proxy_config import DEFAULT_MIDDLE_ROUTE, ProxyConfig, build_proxy_config
from modules.proxy.proxy_transport import ProxyTransport
from modules.runtime.error_codes import ErrorCode
from modules.runtime.operation_result import OperationResult
from modules.runtime.resource_manager import ResourceManager


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
        self.http_client: requests.Session | None = None
        self.target_api_base_url = ""
        self.middle_route = ""
        self.inbound_route = DEFAULT_MIDDLE_ROUTE
        self.custom_model_id = ""
        self.target_model_id = ""
        self.stream_mode: str | None = None
        self.debug_mode = False
        self.disable_ssl_strict_mode = False

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
        self.http_client = self.transport.session

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
            self.http_client = None
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
                "http_client": self.http_client,
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
                "http_client": self.http_client,
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
            self.http_client = new_transport.session

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

    def _log_request(self, request_id: str, message: str) -> None:
        self.log_func(f"{self._timestamp_ms()} [{request_id}] {message}")

    def _get_mapped_model_id(self) -> str:
        return self.custom_model_id

    def _build_route(self, base_route: str, suffix: str) -> str:
        middle_route = base_route or ""
        if not middle_route.startswith("/"):
            middle_route = f"/{middle_route}"
        if middle_route == "/":
            return f"/{suffix.lstrip('/')}"
        return f"{middle_route.rstrip('/')}/{suffix.lstrip('/')}"

    def _create_app(self) -> None:
        self.app = Flask(__name__)
        self._app_logger_default_level = self.app.logger.level
        self._apply_debug_logging(self.debug_mode)

        models_route = self._build_route(self.inbound_route, "models")
        chat_route = self._build_route(self.inbound_route, "chat/completions")

        self.app.add_url_rule(models_route, "get_models", self._get_models, methods=["GET"])
        self.app.add_url_rule(
            chat_route,
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

    def _chat_completions(self) -> tuple[Response, int] | Response:  # noqa: PLR0911, PLR0912, PLR0915
        request_id = self._new_request_id()

        def log(message: str) -> None:
            self._log_request(request_id, message)

        snapshot = self._snapshot_chat_runtime_state()
        inbound_route = str(snapshot["inbound_route"])
        target_model_id = str(snapshot["target_model_id"])
        target_api_base_url = str(snapshot["target_api_base_url"])
        middle_route = str(snapshot["middle_route"])
        stream_mode = snapshot["stream_mode"]
        debug_mode = bool(snapshot["debug_mode"])
        auth = snapshot["auth"]
        transport = snapshot["transport"]
        http_client = snapshot["http_client"]
        proxy_config = snapshot["proxy_config"]
        transport_released = False

        def release_transport() -> None:
            nonlocal transport_released
            if transport_released:
                return
            transport_released = True
            self._release_transport_ref(transport)

        log(f"收到聊天补全请求 {self._build_route(inbound_route, 'chat/completions')}")

        if not (auth and transport and http_client):
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

        messages = request_data.get("messages", [])
        if isinstance(messages, list):
            cleaned = False
            for msg in cast(list[Any], messages):
                if not isinstance(msg, dict):
                    continue
                msg_dict: dict[str, Any] = msg  # pyright: ignore[reportUnknownVariableType]
                content = msg_dict.get("content")
                if isinstance(content, str):
                    if not content.strip():
                        msg_dict["content"] = "-"
                        cleaned = True
                elif isinstance(content, list):
                    for block in cast(list[Any], content):
                        if not isinstance(block, dict):
                            continue
                        block_dict: dict[str, Any] = block  # pyright: ignore[reportUnknownVariableType]
                        block_type = block_dict.get("type")
                        block_text = block_dict.get("text", "")
                        if block_type == "text" and not block_text.strip():
                            block_dict["text"] = "-"
                            cleaned = True
            if cleaned:
                log(
                    "检测到空文本块/内容或纯空白符，已自动将其修改为单个横杠"
                    "以防止目标 API 报错 (例如 Anthropic API)"
                )

        auth_header = request.headers.get("Authorization")
        if not auth.verify(auth_header):
            log("聊天补全请求MTGA鉴权失败")
            release_transport()
            return jsonify(
                {"error": {"message": "Invalid authentication", "type": "authentication_error"}}
            ), 401

        target_api_key = ""
        if isinstance(proxy_config, ProxyConfig):
            target_api_key = proxy_config.api_key
        forward_headers = auth.build_forward_headers(
            auth_header,
            target_api_key,
            log_func=log,
        )

        try:
            target_url = (
                f"{target_api_base_url.rstrip('/')}"
                f"{self._build_route(middle_route, 'chat/completions')}"
            )
            log(f"转发请求到: {target_url}")

            is_stream = request_data.get("stream", False)
            log(f"流模式: {is_stream}")

            response_from_target = http_client.post(
                target_url,
                json=request_data,
                headers=forward_headers,
                stream=is_stream,
                timeout=300,
            )
            response_from_target.raise_for_status()
            if debug_mode:
                log(f"上游响应状态码: {response_from_target.status_code}")
                log(f"上游 Content-Type: {response_from_target.headers.get('content-type')}")

            if is_stream:
                log("返回流式响应")

                log_file = None
                log_file_stack = None
                log_path = None
                if debug_mode:
                    try:
                        log_path = transport.prepare_sse_log_path()
                        log_file_stack = contextlib.ExitStack()
                        log_file = log_file_stack.enter_context(open(log_path, "wb"))  # noqa: SIM115
                        log(f"SSE 原始数据将记录到: {log_path}")
                    except Exception as log_exc:  # noqa: BLE001
                        log(f"SSE 日志文件创建失败: {log_exc}")

                def generate_stream() -> Generator[bytes]:  # noqa: PLR0915, PLR0912
                    nonlocal log_file, log_file_stack
                    event_index = 0
                    done_sent = False
                    finish_reason_seen = None
                    try:
                        for upstream_chunk_index, raw_event in transport.extract_sse_events(
                            response_from_target, log_file=log_file, log=log
                        ):
                            event_index += 1
                            event_text = raw_event.decode("utf-8", errors="replace")
                            data_lines = [
                                line[len("data:") :].lstrip()
                                for line in event_text.splitlines()
                                if line.startswith("data:")
                            ]
                            if not data_lines:
                                log(f"evt#{event_index} 跳过无 data 行的事件: {event_text!r}")
                                continue
                            data_str = "\n".join(data_lines)

                            if debug_mode:
                                log(
                                    f"UP<< evt#{event_index} src_chunk#{upstream_chunk_index} "
                                    f"bytes={len(raw_event)} | {data_str.strip()}"
                                )

                            if data_str.strip() == "[DONE]":
                                done_sent = True
                                done_bytes = b"data: [DONE]\n\n"
                                try:
                                    yield done_bytes
                                except GeneratorExit:
                                    log(
                                        f"DOWN 连接提前中断，已读取上游 evt#{event_index} (DONE)"
                                    )
                                    raise
                                except Exception as downstream_exc:  # noqa: BLE001
                                    log(f"DOWN 写入异常 (DONE)，停止向下游发送: {downstream_exc}")
                                    break
                                log("已转发 [DONE]")
                                break

                            normalized_bytes, finish_reason = transport.normalize_openai_event(
                                data_str,
                                event_index,
                                model_name=target_model_id,
                                log=log,
                            )
                            if finish_reason:
                                finish_reason_seen = finish_reason
                            try:
                                yield normalized_bytes
                            except GeneratorExit:
                                log(
                                    f"DOWN 连接提前中断，已读取上游 evt#{event_index} "
                                    f"finish={finish_reason_seen}"
                                )
                                raise
                            except Exception as downstream_exc:  # noqa: BLE001
                                log(f"DOWN 写入异常，停止向下游发送: {downstream_exc}")
                                break
                        if not done_sent:
                            tail_bytes = b"data: [DONE]\n\n"
                            with contextlib.suppress(Exception):
                                yield tail_bytes
                            if debug_mode:
                                extra = (
                                    f"，finish_reason={finish_reason_seen}"
                                    if finish_reason_seen
                                    else ""
                                )
                                log(f"未收到上游 [DONE]，已补发终止事件{extra}")
                    finally:
                        release_transport()
                        if log_file_stack:
                            with contextlib.suppress(Exception):
                                log_file_stack.close()
                        if log_path:
                            log(f"SSE 记录完成: {log_path}")
                        with contextlib.suppress(Exception):
                            response_from_target.close()
                        if debug_mode:
                            log(f"UP 流结束，累计 {event_index} 个事件")

                downstream_content_type = response_from_target.headers.get(
                    "content-type", "text/event-stream"
                )
                if debug_mode:
                    log(f"下游响应 Content-Type: {downstream_content_type}")

                return Response(
                    generate_stream(),
                    content_type=downstream_content_type,
                )

            response_json_obj = response_from_target.json()
            if not isinstance(response_json_obj, dict):
                log("上游响应不是 JSON 对象")
                release_transport()
                return jsonify({"error": "Invalid response from target API"}), 502
            response_json = cast(dict[str, Any], response_json_obj)

            if client_requested_stream and stream_mode == "false":
                log("将非流式响应转换为流式格式返回给客户端")

                def simulate_stream() -> Generator[str]:
                    choices = response_json.get("choices", [])
                    if not choices:
                        log("响应中没有找到 choices 字段")
                        yield f"data: {json.dumps({'error': 'No choices in response'})}\\n\\n"
                        return

                    first_choice = choices[0]
                    message = first_choice.get("message", {})
                    content = message.get("content", "")

                    if not content:
                        log("响应中没有找到内容")
                        yield f"data: {json.dumps({'error': 'No content in response'})}\\n\\n"
                        return

                    model = response_json.get("model", "")
                    id_value = response_json.get("id", "")
                    created = response_json.get("created", 0)

                    chunk_size = 10
                    total_chars = len(content)

                    for i in range(0, total_chars, chunk_size):
                        chunk = content[i : i + chunk_size]

                        chunk_data = {
                            "id": id_value,
                            "object": "chat.completion.chunk",
                            "created": created,
                            "model": model,
                            "choices": [
                                {
                                    "index": 0,
                                    "delta": {"content": chunk},
                                    "finish_reason": None
                                    if i + chunk_size < total_chars
                                    else first_choice.get("finish_reason", "stop"),
                                }
                            ],
                        }

                        yield f"data: {json.dumps(chunk_data)}\\n\\n"
                        time.sleep(0.01)

                    yield "data: [DONE]\\n\\n"

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
            return jsonify(response_json), response_from_target.status_code

        except requests.exceptions.HTTPError as e:
            error_msg = f"目标 API HTTP 错误: {e.response.status_code} - {e.response.text}"
            log(error_msg)
            release_transport()
            return jsonify(
                {"error": f"Target API error: {e.response.status_code}", "details": e.response.text}
            ), e.response.status_code
        except requests.exceptions.RequestException as e:
            error_msg = f"连接目标 API 时出错: {e}"
            log(error_msg)
            release_transport()
            return jsonify({"error": f"Error contacting target API: {str(e)}"}), 503
        except Exception as e:
            error_msg = f"发生意外错误: {e}"
            log(error_msg)
            release_transport()
            return jsonify({"error": "An internal server error occurred"}), 500


__all__ = ["ProxyApp"]
