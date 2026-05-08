from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

type LogFunc = Callable[[str], None]


@dataclass(frozen=True)
class ProxyAuth:
    mtga_auth_key: str = ""

    def verify(self, auth_header: str | None) -> bool:
        if not self.mtga_auth_key:
            return True
        if not auth_header:
            return False
        provided_key = auth_header[7:] if auth_header.startswith("Bearer ") else auth_header
        return provided_key == self.mtga_auth_key

    def build_forward_headers(
        self,
        auth_header: str | None,
        api_key: str,
        *,
        log_func: LogFunc = print,
    ) -> dict[str, str]:
        headers: dict[str, str] = {"Content-Type": "application/json"}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
            log_func("使用配置组中的API key")
        elif auth_header:
            headers["Authorization"] = auth_header
            log_func("透传原始Authorization header")
        return headers


__all__ = ["ProxyAuth"]
