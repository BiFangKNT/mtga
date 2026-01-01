from __future__ import annotations

import contextlib
import json
import os
import ssl
import time
import uuid
from collections.abc import Generator

import requests
from requests.adapters import HTTPAdapter

from modules.runtime.resource_manager import ResourceManager, is_packaged


class SSLContextAdapter(HTTPAdapter):
    """支持自定义 SSLContext 的适配器，用于调整验证策略。"""

    def __init__(self, ssl_context, *args, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(*args, **kwargs)

    def init_poolmanager(self, connections, maxsize, block=False, **pool_kwargs):
        pool_kwargs.setdefault("ssl_context", self.ssl_context)
        return super().init_poolmanager(connections, maxsize, block=block, **pool_kwargs)

    def proxy_manager_for(self, proxy, **proxy_kwargs):
        proxy_kwargs.setdefault("ssl_context", self.ssl_context)
        return super().proxy_manager_for(proxy, **proxy_kwargs)


class ProxyTransport:
    """代理传输层：HTTP 会话、SSE 解析、上游事件归一化。"""

    def __init__(
        self,
        *,
        resource_manager: ResourceManager,
        disable_ssl_strict_mode: bool,
        log_func=print,
    ) -> None:
        self._resource_manager = resource_manager
        self._log = log_func
        self._session = self._create_http_client(disable_ssl_strict_mode)

    @property
    def session(self) -> requests.Session:
        return self._session

    def close(self) -> None:
        if self._session:
            with contextlib.suppress(Exception):
                self._session.close()

    def _create_http_client(self, disable_ssl_strict_mode: bool) -> requests.Session:
        session = requests.Session()
        if disable_ssl_strict_mode:
            try:
                ctx = ssl.create_default_context()
                ctx.verify_flags &= ~ssl.VERIFY_X509_STRICT
                adapter = SSLContextAdapter(ctx)
                session.mount("https://", adapter)
                self._log("关闭 SSL 严格模式: 使用自定义 HTTPS 上下文")
            except Exception as exc:  # noqa: BLE001
                self._log(f"配置非严格 SSL 上下文失败，继续使用默认设置: {exc}")
        return session

    def prepare_sse_log_path(self) -> str:
        base_dir = (
            self._resource_manager.user_data_dir
            if is_packaged()
            else self._resource_manager.program_resource_dir
        )
        log_dir = os.path.join(base_dir, "logs")
        os.makedirs(log_dir, exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"sse_{timestamp}_{int(time.time() * 1000)}.log"
        return os.path.join(log_dir, filename)

    def extract_sse_events(
        self, response, *, log_file=None, log
    ) -> Generator[tuple[int, bytes]]:
        buffer = b""
        chunk_index = 0
        for chunk in response.iter_content(chunk_size=None):
            chunk_index += 1
            if log_file:
                try:
                    log_file.write(chunk)
                    log_file.flush()
                except Exception as write_exc:  # noqa: BLE001
                    log(f"SSE 日志写入失败，停止记录: {write_exc}")
                    with contextlib.suppress(Exception):
                        log_file.close()
                    log_file = None
            buffer += chunk
            while True:
                sep = buffer.find(b"\n\n")
                if sep == -1:
                    break
                event = buffer[:sep]
                buffer = buffer[sep + 2 :]
                yield chunk_index, event
        if buffer.strip():
            log("警告: 上游 SSE 结束时存在未完整分隔的残留数据")
            yield chunk_index, buffer

    @staticmethod
    def _new_request_id() -> str:
        return uuid.uuid4().hex[:6]

    def normalize_openai_event(
        self, data_str: str, event_index: int, *, model_name: str, log
    ) -> tuple[bytes, str | None]:
        try:
            payload = json.loads(data_str)
        except Exception as exc:  # noqa: BLE001
            log(f"chunk#{event_index} JSON 解析失败，原样透传: {exc}")
            return f"data: {data_str}\n\n".encode(), None

        choices = payload.get("choices") or []
        choice0 = choices[0] if choices else {}
        raw_delta = choice0.get("delta") or {}
        message = choice0.get("message") or {}

        delta: dict[str, object] = {}
        role = raw_delta.get("role") or message.get("role")
        if role or event_index == 1:
            delta["role"] = role or "assistant"

        content = raw_delta.get("content") or message.get("content")
        if content:
            delta["content"] = content

        for key in ("tool_calls", "function_calls", "reasoning_content"):
            value = raw_delta.get(key)
            if value not in (None, []):
                delta[key] = value

        finish_reason = choice0.get("finish_reason")
        normalized_finish = finish_reason if finish_reason not in (None, "") else None

        chunk_obj = {
            "id": payload.get("id") or self._new_request_id(),
            "object": "chat.completion.chunk",
            "created": int(payload.get("created") or time.time()),
            "model": payload.get("model") or model_name,
            "choices": [
                {
                    "index": choice0.get("index", 0),
                    "delta": delta,
                    "logprobs": None,
                    "finish_reason": normalized_finish,
                }
            ],
        }
        chunk_json = json.dumps(chunk_obj, ensure_ascii=False)
        return f"data: {chunk_json}\n\n".encode(), normalized_finish


__all__ = ["ProxyTransport", "SSLContextAdapter"]
