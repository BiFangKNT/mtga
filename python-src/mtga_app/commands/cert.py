from __future__ import annotations

from typing import Any

from pydantic import BaseModel
from pytauri import Commands

from modules.services.app_metadata import DEFAULT_METADATA
from modules.services.cert_service import (
    clear_ca_cert_result,
    generate_certificates_result,
    install_ca_cert_result,
)

from .common import build_result_payload, collect_logs, register_command


class ClearCaCertPayload(BaseModel):
    ca_common_name: str | None = None


def register_cert_commands(commands: Commands) -> None:
    @register_command(commands)
    async def generate_certificates() -> dict[str, Any]:
        logs, log_func = collect_logs()
        result = generate_certificates_result(
            log_func=log_func,
            ca_common_name=DEFAULT_METADATA.ca_common_name,
        )
        return build_result_payload(result, logs, "证书生成完成")

    @register_command(commands)
    async def install_ca_cert() -> dict[str, Any]:
        logs, log_func = collect_logs()
        result = install_ca_cert_result(log_func=log_func)
        return build_result_payload(result, logs, "CA 证书安装完成")

    @register_command(commands)
    async def clear_ca_cert(body: ClearCaCertPayload) -> dict[str, Any]:
        logs, log_func = collect_logs()
        result = clear_ca_cert_result(
            body.ca_common_name or DEFAULT_METADATA.ca_common_name,
            log_func=log_func,
        )
        return build_result_payload(result, logs, "CA 证书清除完成")

    _ = (generate_certificates, install_ca_cert, clear_ca_cert)
