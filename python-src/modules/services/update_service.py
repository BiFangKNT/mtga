from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import requests

from modules.network.outbound_proxy import create_outbound_session
from modules.runtime.error_codes import ErrorCode
from modules.runtime.operation_result import OperationResult
from modules.update import update_checker

UpdateStatus = Literal[
    "network_error",
    "remote_error",
    "no_version",
    "up_to_date",
    "new_version",
]


@dataclass(frozen=True)
class UpdateCheckResult:
    status: UpdateStatus
    latest_version: str | None = None
    release_notes: str | None = None
    release_url: str | None = None
    error_message: str | None = None


@dataclass(frozen=True)
class UpdateFontOptions:
    family: str | None = None
    size: int | None = None
    weight: str | None = None


def check_for_updates(
    *,
    repo: str,
    app_version: str,
    timeout: int = 10,
    user_agent: str | None = None,
    font: UpdateFontOptions | None = None,
) -> UpdateCheckResult:
    font_options = None
    if font and (font.family or font.size or font.weight):
        font_options = update_checker.HtmlFontOptions(
            family=font.family,
            size=font.size,
            weight=font.weight,
        )

    try:
        session = create_outbound_session()
        try:
            release_info = update_checker.fetch_latest_release(
                repo,
                timeout=timeout,
                user_agent=user_agent,
                font=font_options,
                session=session,
            )
        finally:
            session.close()
    except requests.RequestException as exc:
        return UpdateCheckResult(
            status="network_error",
            error_message=f"检查更新失败：网络异常 {exc}",
        )
    except (ValueError, RuntimeError) as exc:
        return UpdateCheckResult(
            status="remote_error",
            error_message=f"检查更新失败：{exc}",
        )

    latest_version = release_info.version_label
    if not latest_version:
        return UpdateCheckResult(status="no_version")

    if not update_checker.is_remote_version_newer(latest_version, app_version):
        return UpdateCheckResult(status="up_to_date", latest_version=latest_version)

    release_notes = release_info.release_notes or "该版本暂无更新说明。"
    return UpdateCheckResult(
        status="new_version",
        latest_version=latest_version,
        release_notes=release_notes,
        release_url=release_info.release_url,
    )


def check_for_updates_result(
    *,
    repo: str,
    app_version: str,
    timeout: int = 10,
    user_agent: str | None = None,
    font: UpdateFontOptions | None = None,
) -> OperationResult:
    result = check_for_updates(
        repo=repo,
        app_version=app_version,
        timeout=timeout,
        user_agent=user_agent,
        font=font,
    )

    if result.status == "network_error":
        message = result.error_message or "检查更新失败：网络异常"
        return OperationResult.failure(
            message,
            code=ErrorCode.NETWORK_ERROR,
            status=result.status,
            update_result=result,
        )
    if result.status == "remote_error":
        message = result.error_message or "检查更新失败"
        return OperationResult.failure(
            message,
            code=ErrorCode.REMOTE_ERROR,
            status=result.status,
            update_result=result,
        )
    if result.status == "no_version":
        return OperationResult.failure(
            "未解析到版本号，请稍后再试。",
            code=ErrorCode.NO_VERSION,
            status=result.status,
            update_result=result,
        )

    return OperationResult.success(status=result.status, update_result=result)
