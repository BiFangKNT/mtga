from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProxyAuth:
    mtga_auth_key: str = ""

    def verify(self, auth_header: str | None) -> bool:
        # 如果未设置 Global Key，则放行所有请求（不强制一致性）
        if not self.mtga_auth_key:
            return True

        # 如果设置了 Global Key，则必须提供请求头且通过校验
        if not auth_header:
            return False

        provided_key = (auth_header[7:] if auth_header.startswith("Bearer ") else auth_header).strip()
        
        is_valid = provided_key == self.mtga_auth_key
        if not is_valid:
            # 简单的调试日志，帮助排查 Key 不匹配问题
            expected_masked = (self.mtga_auth_key[:2] + "***") if self.mtga_auth_key else "EMPTY"
            provided_masked = (provided_key[:2] + "***") if provided_key else "EMPTY"
            print(f"[ProxyAuth] 鉴权失败. 收到: {provided_masked}, 期望: {expected_masked}, 长度: {len(provided_key)} vs {len(self.mtga_auth_key)}")
            
        return is_valid

    def build_forward_headers(
        self,
        auth_header: str | None,
        api_key: str,
        *,
        log_func=print,
    ) -> dict:
        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
            log_func("使用配置组中的API key")
        elif auth_header:
            headers["Authorization"] = auth_header
            log_func("透传原始Authorization header")
        return headers


__all__ = ["ProxyAuth"]
