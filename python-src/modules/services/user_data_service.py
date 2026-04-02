from __future__ import annotations

import glob
import os
import shutil
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime

from modules.runtime.error_codes import ErrorCode
from modules.runtime.operation_result import OperationResult
from modules.runtime.resource_manager import LOGS_DIR_NAME


@dataclass(frozen=True)
class BackupResult:
    backup_dir: str | None
    item_count: int


@dataclass(frozen=True)
class ClearResult:
    removed_count: int
    copied_files_count: int


@dataclass(frozen=True)
class RestoreResult:
    backup_name: str
    restored_count: int


@dataclass(frozen=True)
class LatestBackupInfo:
    backup_name: str
    backup_path: str


class BackupNotFoundError(FileNotFoundError):
    pass


class NoBackupsError(FileNotFoundError):
    pass


def _collect_user_items(
    user_data_dir: str,
    *,
    exclude_names: set[str],
) -> list[tuple[str, str]]:
    items: list[tuple[str, str]] = []
    for item in os.listdir(user_data_dir):
        if item in exclude_names:
            continue
        item_path = os.path.join(user_data_dir, item)
        items.append((item, item_path))
    return items


def backup_user_data(
    user_data_dir: str,
    *,
    error_log_filename: str,
) -> BackupResult:
    backup_base_dir = os.path.join(user_data_dir, "backups")
    os.makedirs(backup_base_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.join(backup_base_dir, f"backup_{timestamp}")

    items_to_backup = _collect_user_items(
        user_data_dir,
        exclude_names={"backups", LOGS_DIR_NAME, error_log_filename},
    )

    if not items_to_backup:
        return BackupResult(None, 0)

    os.makedirs(backup_dir, exist_ok=True)
    for item_name, item_path in items_to_backup:
        dest_path = os.path.join(backup_dir, item_name)
        if os.path.isfile(item_path):
            shutil.copy2(item_path, dest_path)
        elif os.path.isdir(item_path):
            shutil.copytree(item_path, dest_path)

    return BackupResult(backup_dir, len(items_to_backup))


def clear_user_data(
    user_data_dir: str,
    *,
    error_log_filename: str,
    copy_template_files_fn: Callable[[], list[str]] | None = None,
) -> ClearResult:
    items_to_remove = _collect_user_items(
        user_data_dir,
        exclude_names={"backups", LOGS_DIR_NAME, error_log_filename},
    )
    if not items_to_remove:
        return ClearResult(0, 0)

    for _item_name, item_path in items_to_remove:
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)

    copied_files_count = 0
    if copy_template_files_fn is not None:
        copied_files = copy_template_files_fn()
        copied_files_count = len(copied_files) if copied_files else 0

    return ClearResult(len(items_to_remove), copied_files_count)


def find_latest_backup(
    user_data_dir: str,
) -> LatestBackupInfo:
    backup_base_dir = os.path.join(user_data_dir, "backups")
    if not os.path.exists(backup_base_dir):
        raise BackupNotFoundError("未找到备份目录")

    backup_pattern = os.path.join(backup_base_dir, "backup_*")
    backup_folders = glob.glob(backup_pattern)
    if not backup_folders:
        raise NoBackupsError("未找到任何备份")

    latest_backup = max(backup_folders, key=lambda x: os.path.basename(x))
    backup_name = os.path.basename(latest_backup)
    return LatestBackupInfo(backup_name=backup_name, backup_path=latest_backup)


def restore_backup(
    user_data_dir: str,
    *,
    backup_path: str,
) -> RestoreResult:
    backup_name = os.path.basename(backup_path)
    restored_count = 0
    for item in os.listdir(backup_path):
        src_path = os.path.join(backup_path, item)
        dest_path = os.path.join(user_data_dir, item)

        if os.path.exists(dest_path):
            if os.path.isfile(dest_path):
                os.remove(dest_path)
            elif os.path.isdir(dest_path):
                shutil.rmtree(dest_path)

        if os.path.isfile(src_path):
            shutil.copy2(src_path, dest_path)
        elif os.path.isdir(src_path):
            shutil.copytree(src_path, dest_path)

        restored_count += 1

    return RestoreResult(backup_name, restored_count)


def restore_latest_backup(
    user_data_dir: str,
) -> RestoreResult:
    latest = find_latest_backup(user_data_dir)
    return restore_backup(user_data_dir, backup_path=latest.backup_path)


def backup_user_data_result(
    user_data_dir: str,
    *,
    error_log_filename: str,
) -> OperationResult:
    try:
        result = backup_user_data(user_data_dir, error_log_filename=error_log_filename)
        return OperationResult.success(backup_result=result)
    except Exception as exc:
        return OperationResult.failure(f"备份用户数据失败: {exc}")


def clear_user_data_result(
    user_data_dir: str,
    *,
    error_log_filename: str,
    copy_template_files_fn: Callable[[], list[str]] | None = None,
) -> OperationResult:
    try:
        result = clear_user_data(
            user_data_dir,
            error_log_filename=error_log_filename,
            copy_template_files_fn=copy_template_files_fn,
        )
        return OperationResult.success(clear_result=result)
    except Exception as exc:
        return OperationResult.failure(f"清除用户数据失败: {exc}")


def find_latest_backup_result(
    user_data_dir: str,
) -> OperationResult:
    try:
        result = find_latest_backup(user_data_dir)
        return OperationResult.success(latest_backup=result)
    except BackupNotFoundError as exc:
        return OperationResult.failure(str(exc), code=ErrorCode.BACKUP_DIR_MISSING)
    except NoBackupsError as exc:
        return OperationResult.failure(str(exc), code=ErrorCode.NO_BACKUPS)
    except Exception as exc:
        return OperationResult.failure(
            f"读取备份失败: {exc}",
            code=ErrorCode.UNKNOWN,
        )


def restore_backup_result(
    user_data_dir: str,
    *,
    backup_path: str,
) -> OperationResult:
    try:
        result = restore_backup(user_data_dir, backup_path=backup_path)
        return OperationResult.success(restore_result=result)
    except Exception as exc:
        return OperationResult.failure(f"还原数据失败: {exc}")


def restore_latest_backup_result(
    user_data_dir: str,
) -> OperationResult:
    latest_result = find_latest_backup_result(user_data_dir)
    if not latest_result.ok:
        return latest_result
    latest_info = latest_result.details.get("latest_backup")
    if not isinstance(latest_info, LatestBackupInfo):
        return OperationResult.failure("未找到可用备份")
    return restore_backup_result(user_data_dir, backup_path=latest_info.backup_path)
