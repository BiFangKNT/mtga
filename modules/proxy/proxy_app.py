from __future__ import annotations

import contextlib
import json
import logging
import time
import uuid

import requests
from flask import Flask, Response, jsonify, request

from modules.proxy.proxy_auth import ProxyAuth
from modules.proxy.proxy_config import DEFAULT_MIDDLE_ROUTE, ProxyConfig, build_proxy_config
from modules.proxy.proxy_transport import ProxyTransport
from modules.runtime.resource_manager import ResourceManager


class ProxyApp:
    """代理服务的领域逻辑：配置解析 + Flask 路由 + 上游转发。"""

    def __init__(self, config=None, log_func=print, *, resource_manager: ResourceManager):
        self.config = config or {}
        self.log_func = log_func
        self.resource_manager = resource_manager
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
        self.stream_mode = None
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
        if self.transport:
            self.transport.close()

    @staticmethod
    def _new_request_id() -> str:
        return uuid.uuid4().hex[:6]

    @staticmethod
    def _timestamp_ms() -> str:
        now = time.time()
        base = time.strftime("%H:%M:%S", time.localtime(now))
        ms = int((now % 1) * 1000)
        return f"{base}.{ms:03d}"

    def _log_request(self, request_id: str, message: str):
        self.log_func(f"{self._timestamp_ms()} [{request_id}] {message}")

    def _get_mapped_model_id(self):
        return self.custom_model_id

    def _build_route(self, base_route: str, suffix: str) -> str:
        middle_route = base_route or ""
        if not middle_route.startswith("/"):
            middle_route = f"/{middle_route}"
        if middle_route == "/":
            return f"/{suffix.lstrip('/')}"
        return f"{middle_route.rstrip('/')}/{suffix.lstrip('/')}"

    def _create_app(self):
        self.app = Flask(__name__)

        if self.debug_mode:
            logging.getLogger().setLevel(logging.INFO)
            self.app.logger.setLevel(logging.INFO)

        models_route = self._build_route(self.inbound_route, "models")
        chat_route = self._build_route(self.inbound_route, "chat/completions")

        self.app.add_url_rule(models_route, "get_models", self._get_models, methods=["GET"])
        self.app.add_url_rule(
            chat_route,
            "chat_completions",
            self._chat_completions,
            methods=["POST"],
        )

    def _get_models(self):
        self.log_func(f"收到模型列表请求 {self._build_route(self.inbound_route, 'models')}")

        auth = self.auth
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

        mapped_model_id = self._get_mapped_model_id()

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

    def _chat_completions(self):  # noqa: PLR0911, PLR0912, PLR0915
        request_id = self._new_request_id()

        def log(message: str):
            self._log_request(request_id, message)

        log("="*60)
        log(f"📥 [1/4] 接收客户端请求: {self._build_route(self.inbound_route, 'chat/completions')}")
        log("="*60)

        auth = self.auth
        transport = self.transport
        http_client = self.http_client
        if not (auth and transport and http_client):
            log("代理服务未就绪")
            return jsonify({"error": "Proxy not ready"}), 500

        if self.debug_mode:
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

        request_data = request.get_json(silent=True)

        if request_data is None:
            log("解析 JSON 失败或请求不是 JSON 格式")
            log(f"Content-Type: {request.headers.get('Content-Type')}")
            return jsonify(
                {
                    "error": "Invalid JSON or Content-Type",
                    "message": (
                        "The request body must be valid JSON and the Content-Type header "
                        "must be 'application/json'."
                    ),
                }
            ), 400

        # 显示原始请求信息
        log("-"*60)
        log("📋 原始请求信息:")
        client_requested_stream = request_data.get("stream", False)
        if "model" in request_data:
            log(f"  • 客户端请求模型: {request_data['model']}")
        log(f"  • 客户端请求流模式: {client_requested_stream}")
        if "messages" in request_data:
            msg_count = len(request_data.get("messages", []))
            log(f"  • 消息数量: {msg_count}")
        log("-"*60)

        # 模型替换
        log("="*60)
        log("🔄 [2/4] 劫持并替换请求参数")
        log("="*60)
        if "model" in request_data:
            original_model = request_data["model"]
            log(f"  ✓ 模型名替换: {original_model} → {self.target_model_id}")
            request_data["model"] = self.target_model_id
        else:
            log(f"  ✓ 添加模型名: {self.target_model_id}")
            request_data["model"] = self.target_model_id

        if self.stream_mode is not None:
            stream_value = self.stream_mode == "true"
            if "stream" in request_data:
                original_stream_value = request_data["stream"]
                log(f"  ✓ 流模式替换: {original_stream_value} → {stream_value}")
                request_data["stream"] = stream_value
            else:
                log(f"  ✓ 设置流模式: {stream_value}")
                request_data["stream"] = stream_value

        auth_header = request.headers.get("Authorization")
        if not auth.verify(auth_header):
            log("聊天补全请求MTGA鉴权失败")
            return jsonify(
                {"error": {"message": "Invalid authentication", "type": "authentication_error"}}
            ), 401

        target_api_key = ""
        if self.proxy_config:
            target_api_key = self.proxy_config.api_key
        forward_headers = auth.build_forward_headers(
            auth_header,
            target_api_key,
            log_func=log,
        )

        try:
            target_url = (
                f"{self.target_api_base_url.rstrip('/')}"
                f"{self._build_route(self.middle_route, 'chat/completions')}"
            )
            log("-"*60)
            log("="*60)
            log("📤 [3/4] 转发请求到上游API")
            log("="*60)
            log(f"  • 目标URL: {target_url}")
            log(f"  • 实际模型: {request_data.get('model')}")
            is_stream = request_data.get("stream", False)
            log(f"  • 流模式: {is_stream}")
            log("-"*60)

            response_from_target = http_client.post(
                target_url,
                json=request_data,
                headers=forward_headers,
                stream=is_stream,
                timeout=300,
            )
            response_from_target.raise_for_status()
            
            log("="*60)
            log("📨 [4/4] 接收上游响应并返回客户端")
            log("="*60)
            log(f"  • 响应状态码: {response_from_target.status_code}")
            log(f"  • 响应类型: {response_from_target.headers.get('content-type', 'N/A')}")
            
            if self.debug_mode:
                log(f"  • [调试] Content-Type: {response_from_target.headers.get('content-type')}")

            if is_stream:
                log("  ✓ 返回流式响应")
                log("-"*60)

                log_file = None
                log_file_stack = None
                log_path = None
                if self.debug_mode:
                    try:
                        log_path = transport.prepare_sse_log_path()
                        log_file_stack = contextlib.ExitStack()
                        log_file = log_file_stack.enter_context(open(log_path, "wb"))  # noqa: SIM115
                        log(f"SSE 原始数据将记录到: {log_path}")
                    except Exception as log_exc:  # noqa: BLE001
                        log(f"SSE 日志文件创建失败: {log_exc}")

                def generate_stream():  # noqa: PLR0915, PLR0912
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

                            if self.debug_mode:
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
                                model_name=self.custom_model_id,
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
                            if self.debug_mode:
                                extra = (
                                    f"，finish_reason={finish_reason_seen}"
                                    if finish_reason_seen
                                    else ""
                                )
                                log(f"未收到上游 [DONE]，已补发终止事件{extra}")
                    finally:
                        if log_file_stack:
                            with contextlib.suppress(Exception):
                                log_file_stack.close()
                        if log_path:
                            log(f"SSE 记录完成: {log_path}")
                        with contextlib.suppress(Exception):
                            response_from_target.close()
                        if self.debug_mode:
                            log(f"UP 流结束，累计 {event_index} 个事件")

                downstream_content_type = response_from_target.headers.get(
                    "content-type", "text/event-stream"
                )
                if self.debug_mode:
                    log(f"下游响应 Content-Type: {downstream_content_type}")

                return Response(
                    generate_stream(),
                    content_type=downstream_content_type,
                )

            response_json = response_from_target.json()
            
            # 替换响应中的模型名为映射ID
            original_model = response_json.get("model", "N/A")
            if "model" in response_json:
                response_json["model"] = self.custom_model_id
                log(f"  ✓ 响应模型名替换: {original_model} → {self.custom_model_id}")
            log("-"*60)

            if client_requested_stream and self.stream_mode == "false":
                log("  ✓ 将非流式响应转换为流式格式")

                def simulate_stream():
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

                    model = response_json.get("model", self.custom_model_id)
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

                return Response(simulate_stream(), content_type="text/event-stream")

            if self.debug_mode:
                response_str = json.dumps(response_json, indent=2, ensure_ascii=False)
                log(
                    f"--- 完整响应体 (调试模式) ---\\n{response_str}\\n"
                    "--------------------------------------"
                )
            else:
                log("  ✓ 返回非流式 JSON 响应")
            log("="*60)
            log("✅ 请求处理完成")
            log("="*60)
            return jsonify(response_json), response_from_target.status_code

        except requests.exceptions.HTTPError as e:
            error_msg = f"目标 API HTTP 错误: {e.response.status_code} - {e.response.text}"
            log(error_msg)
            return jsonify(
                {"error": f"Target API error: {e.response.status_code}", "details": e.response.text}
            ), e.response.status_code
        except requests.exceptions.RequestException as e:
            error_msg = f"连接目标 API 时出错: {e}"
            log(error_msg)
            return jsonify({"error": f"Error contacting target API: {str(e)}"}), 503
        except Exception as e:
            error_msg = f"发生意外错误: {e}"
            log(error_msg)
            return jsonify({"error": "An internal server error occurred"}), 500


__all__ = ["ProxyApp"]
