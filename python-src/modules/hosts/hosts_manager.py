"""
hosts 文件管理模块
处理 hosts 文件的备份、修改、还原等操作
"""

from __future__ import annotations

import ctypes
import os
import shutil
import subprocess
import sys
from collections.abc import Callable, Iterable

from modules.hosts.file_operability import (
    FileOperabilityReport,
    check_file_operability,
    ensure_windows_file_writable,
)
from modules.hosts.hosts_state import get_hosts_modify_block_state, guard_hosts_modify
from modules.hosts.hosts_text import (
    DEFAULT_HOSTS_IPS,
    append_hosts_block,
    build_hosts_block,
    normalize_ip_list,
    remove_hosts_block_from_content,
)
from modules.platform.macos_privileged_helper import get_mac_privileged_session
from modules.platform.privileges import is_windows_admin
from modules.runtime.resource_manager import ResourceManager

_HOSTS_PATH_FALLBACK_STATE = {"warned": False}
type LogFunc = Callable[[str], None]


def _append_hosts_block_fallback(
    hosts_file: str, hosts_block: str, encoding: str, *, log_func: LogFunc = print
) -> bool:
    """回退为追加写入（不做去重/删除/原子性写回）。"""
    if not hosts_block:
        return False
    try:
        try:
            with open(hosts_file, encoding=encoding, errors="replace") as f:
                content = f.read()
        except OSError:
            content = ""

        if (
            hosts_block in content
            or f"\n{hosts_block}" in content
            or f"\n\n{hosts_block}" in content
        ):
            log_func("hosts 文件已包含目标记录（检测为相同文本块），跳过追加")
            return True

        if not content or content.endswith("\n\n"):
            prefix = ""
        elif content.endswith("\n"):
            prefix = "\n"
        else:
            prefix = "\n\n"

        with open(hosts_file, "a", encoding=encoding) as f:
            f.write(prefix)
            f.write(hosts_block)
        log_func("⚠️ 已回退为追加写入：无法保证原子性增删/去重，请手动管理 hosts 记录。")
        return True
    except PermissionError as e:
        log_func(f"❌ 追加写入 hosts 文件失败: {e}")
        return False
    except OSError as e:
        log_func(f"❌ 追加写入 hosts 文件失败: {e}")
        return False


def _fallback_to_append(  # noqa: PLR0913
    *,
    hosts_file: str,
    hosts_block: str,
    encoding: str,
    log_func: LogFunc,
    reason: str,
    removed_entries: int = 0,
) -> bool:
    log_func(f"⚠️ {reason}")
    log_func("⚠️ 追加写入无法进行原子性删除/去重；如需清理请手动编辑 hosts。")
    if removed_entries:
        log_func("⚠️ 检测到历史重复记录：追加写入不会清理旧条目，请手动编辑 hosts。")
    return _append_hosts_block_fallback(
        hosts_file,
        hosts_block,
        encoding,
        log_func=log_func,
    )


def check_hosts_file_operability(
    hosts_file: str, *, log_func: LogFunc = print
) -> FileOperabilityReport:
    """对 hosts 文件做可写性预检（仅检查，不改变全局阻断开关）。"""
    return check_file_operability(hosts_file, log_func=log_func)


def get_hosts_file_path(log_func: LogFunc = print) -> str:
    """获取 hosts 文件路径"""
    if os.name == "nt":  # Windows
        warned = _HOSTS_PATH_FALLBACK_STATE
        system_root = os.environ.get("SYSTEMROOT") or os.environ.get("WINDIR")
        if not system_root:
            if not warned["warned"] and callable(log_func):
                log_func(
                    "⚠️ 环境变量 SYSTEMROOT/WINDIR 未设置，将尝试使用 WinAPI 获取 Windows 目录。"
                )
            try:
                buffer = ctypes.create_unicode_buffer(260)
                size = ctypes.windll.kernel32.GetWindowsDirectoryW(buffer, len(buffer))
                if size:
                    system_root = buffer.value
            except Exception:
                if not warned["warned"] and callable(log_func):
                    log_func("⚠️ 调用 GetWindowsDirectoryW 失败，稍后将使用默认路径兜底。")
                system_root = None

        if not system_root and not warned["warned"]:
            if callable(log_func):
                log_func("⚠️ 无法确定 Windows 目录，hosts 路径将回退为 C:\\Windows\\System32\\...。")
            warned["warned"] = True

        system_root = system_root or r"C:\Windows"
        log_func(f"[hosts] system_root={system_root}")
        return os.path.join(system_root, "System32", "drivers", "etc", "hosts")
    else:  # Unix/Linux/macOS
        return "/etc/hosts"


def get_backup_file_path() -> str:
    """获取备份文件路径（持久化到用户数据目录）"""
    resource_manager = ResourceManager()
    return resource_manager.get_hosts_backup_file()


def detect_file_encoding(file_path: str) -> str:
    """检测文件编码"""
    encodings = ["utf-8", "gbk", "gb2312", "latin1", "utf-16"]
    for enc in encodings:
        try:
            with open(file_path, encoding=enc) as f:
                f.read()
            return enc
        except UnicodeDecodeError:
            continue
    return "utf-8"  # 默认编码


def backup_hosts_file(log_func: LogFunc = print) -> bool:
    """
    备份 hosts 文件

    参数:
        log_func: 日志输出函数

    返回:
        成功返回 True，失败返回 False
    """
    hosts_file = get_hosts_file_path(log_func)
    backup_file = get_backup_file_path()

    log_func("开始备份 hosts 文件...")

    if not os.path.exists(hosts_file):
        log_func(f"错误: hosts 文件不存在: {hosts_file}")
        return False

    try:
        shutil.copy2(hosts_file, backup_file)
        log_func(f"hosts 文件已备份到: {backup_file}")
        return True
    except Exception as e:
        log_func(f"备份 hosts 文件失败: {e}")
        return False


def restore_hosts_file(log_func: LogFunc = print) -> bool:  # noqa: PLR0911
    """
    还原 hosts 文件

    参数:
        log_func: 日志输出函数

    返回:
        成功返回 True，失败返回 False
    """
    hosts_file = get_hosts_file_path(log_func)
    backup_file = get_backup_file_path()

    log_func("开始还原 hosts 文件...")
    if not guard_hosts_modify("restore", log_func=log_func):
        return False

    if not os.path.exists(backup_file):
        log_func(f"错误: 备份文件不存在: {backup_file}")
        return False

    try:
        if sys.platform == "darwin":
            session = get_mac_privileged_session(log_func=log_func)
            if not session:
                return False
            if session.copy_file(backup_file, hosts_file, log_func=log_func):
                log_func("hosts 文件已还原")
                return True
            return False

        shutil.copy2(backup_file, hosts_file)
        log_func("hosts 文件已还原")
        return True
    except Exception as e:
        log_func(f"还原 hosts 文件失败: {e}")
        return False


def write_hosts_file_with_permission(
    hosts_file: str, content: str, encoding: str, log_func: LogFunc = print
) -> bool:
    """
    使用适当的权限写入 hosts 文件

    参数:
        hosts_file: hosts 文件路径
        content: 要写入的内容
        encoding: 文件编码
        log_func: 日志输出函数

    返回:
        成功返回 True，失败返回 False
    """
    if sys.platform == "darwin":
        session = get_mac_privileged_session(log_func=log_func)
        if not session:
            return False
        if session.write_file(hosts_file, content, encoding, log_func=log_func):
            log_func("✅ hosts 文件写入成功")
            return True
        return False
    else:
        # Windows 和其他系统：直接写入
        try:
            if os.name == "nt":
                check_file_operability(hosts_file, log_func=log_func)
                ensure_windows_file_writable(hosts_file, log_func=log_func)
            with open(hosts_file, "w", encoding=encoding) as f:
                f.write(content)
            return True
        except PermissionError as e:
            if os.name == "nt":
                is_admin = is_windows_admin()
                winerror = getattr(e, "winerror", None)
                log_func(
                    f"❌ 权限不足，请以管理员身份运行 "
                    f"(is_admin={is_admin}, winerror={winerror})"
                )
                log_func("⚠️ 如果已是管理员，可能是安全软件或只读属性锁定了 hosts，请解除后重试")
            else:
                log_func("❌ 权限不足，请以管理员身份运行或使用 sudo")
            return False
        except OSError as e:
            log_func(f"❌ 写入 hosts 文件失败: {e}")
            return False


def add_hosts_entry(  # noqa: PLR0911
    domain: str,
    ip: str | Iterable[object] | object | None = DEFAULT_HOSTS_IPS,
    log_func: LogFunc = print,
) -> bool:
    """
    添加 hosts 条目

    参数:
        domain: 域名
        ip: 单个 IP 字符串或可迭代的多个 IP
        log_func: 日志输出函数

    返回:
        成功返回 True，失败返回 False
    """
    ip_list = normalize_ip_list(ip)
    if not ip_list:
        log_func("未提供有效 IP，取消 hosts 修改")
        return False

    hosts_file = get_hosts_file_path(log_func)
    backup_file = get_backup_file_path()

    ip_text = ", ".join(f"{addr} {domain}" for addr in ip_list)
    log_func(f"开始添加 hosts 条目: {ip_text}")

    if not os.path.exists(hosts_file):
        log_func(f"错误: hosts 文件不存在: {hosts_file}")
        return False

    try:
        # 先备份（如果备份文件不存在）
        if not os.path.exists(backup_file):
            shutil.copy2(hosts_file, backup_file)
            log_func(f"hosts 文件已自动备份到: {backup_file}")

        # 检测文件编码
        encoding = detect_file_encoding(hosts_file)
        log_func(f"检测到 hosts 文件编码: {encoding}")

        # 读取 hosts 文件内容
        with open(hosts_file, encoding=encoding, errors="replace") as f:
            content = f.read()

        hosts_block = build_hosts_block(domain, ip_list)
        if not hosts_block:
            log_func("未能构造 hosts 写入数据，取消操作")
            return False

        if (
            hosts_block in content
            or f"\n{hosts_block}" in content
            or f"\n\n{hosts_block}" in content
        ):
            log_func("hosts 文件已包含目标记录，无需修改")
            return True

        state = get_hosts_modify_block_state()
        if state.blocked:
            reason = state.reason or (state.report.status.value if state.report else "unknown")
            return _fallback_to_append(
                hosts_file=hosts_file,
                hosts_block=hosts_block,
                encoding=encoding,
                log_func=log_func,
                reason=f"当前环境 hosts 写入受限（reason={reason}），将回退为追加写入模式。",
            )

        # 移除旧记录，保证写入是原子块
        content, removed_entries = remove_hosts_block_from_content(content, domain, ip_list)
        if removed_entries:
            log_func(f"检测到重复记录，已移除 {removed_entries} 个 {domain} 条目")

        # 添加统一的文本块并保留一个空行
        content = append_hosts_block(content, hosts_block)

        # 使用权限写入
        write_success = write_hosts_file_with_permission(hosts_file, content, encoding, log_func)
        if write_success:
            log_func("hosts 文件修改成功！")
            return True

        if os.name == "nt":
            return _fallback_to_append(
                hosts_file=hosts_file,
                hosts_block=hosts_block,
                encoding=encoding,
                log_func=log_func,
                reason="原子写入 hosts 失败，尝试回退为追加写入模式（无法保证原子性增删/去重）。",
                removed_entries=removed_entries,
            )

        return False

    except Exception as e:
        log_func(f"修改 hosts 文件失败: {e}")
        return False


def remove_hosts_entry(
    domain: str, log_func: LogFunc = print, *, ip: str | Iterable[object] | object | None = None
) -> bool:
    """
    删除 hosts 条目

    参数:
        domain: 要删除的域名
        ip: 需要删除的 IP 列表（默认删除模块写入的两个地址）
        log_func: 日志输出函数

    返回:
        成功返回 True，失败返回 False
    """
    if not guard_hosts_modify("remove", log_func=log_func):
        return False
    ip_list = normalize_ip_list(ip)

    hosts_file = get_hosts_file_path(log_func)

    log_func(f"开始删除 hosts 条目: {domain}")

    if not os.path.exists(hosts_file):
        log_func(f"错误: hosts 文件不存在: {hosts_file}")
        return False

    try:
        # 检测文件编码
        encoding = detect_file_encoding(hosts_file)
        log_func(f"检测到 hosts 文件编码: {encoding}")

        with open(hosts_file, encoding=encoding, errors="replace") as f:
            content = f.read()

        new_content, removed_count = remove_hosts_block_from_content(content, domain, ip_list)

        if removed_count > 0:
            if write_hosts_file_with_permission(hosts_file, new_content, encoding, log_func):
                log_func(f"hosts 文件已重置，删除了 {removed_count} 个 {domain} 条目")
            else:
                return False
        else:
            log_func(f"hosts 文件中未找到 {domain} 条目")

        return True

    except Exception as e:
        log_func(f"删除 hosts 条目失败: {e}")
        return False


def open_hosts_file(log_func: LogFunc = print) -> bool:
    """
    根据平台打开 hosts 文件

    参数:
        log_func: 日志输出函数

    返回:
        成功返回 True，失败返回 False
    """
    hosts_file = get_hosts_file_path(log_func)
    result = False

    try:
        if os.name == "nt":  # Windows
            subprocess.run(["notepad", hosts_file], check=True)
            log_func("已使用记事本打开 hosts 文件")
            result = True
        elif sys.platform == "darwin":  # macOS
            session = get_mac_privileged_session(log_func=log_func)
            if session:
                success, data = session.run_command(["open", "-t", hosts_file], log_func=log_func)
                data_dict = data
                if success:
                    log_func("已使用默认文本编辑器打开 hosts 文件")
                    result = True
                else:
                    error_msg = (
                        data_dict.get("stderr")
                        or data_dict.get("error")
                        or data_dict.get("stdout")
                        or ""
                    )
                    log_func(f"打开 hosts 文件失败: {error_msg or '未知错误'}")
            else:
                log_func("⚠️ 打开 hosts 文件需要管理员权限，已取消操作")
        else:  # Linux
            editors = ["gedit", "nano", "vim"]
            for editor in editors:
                try:
                    subprocess.run([editor, hosts_file], check=True)
                    log_func(f"已使用 {editor} 打开 hosts 文件")
                    result = True
                    break
                except (subprocess.CalledProcessError, FileNotFoundError):
                    continue
            if not result:
                log_func("未找到合适的文本编辑器")

        return result

    except Exception as e:
        log_func(f"打开 hosts 文件失败: {e}")
        return False


def modify_hosts_file(
    domain: str = "api.openai.com",
    action: str = "add",
    ip: str | Iterable[object] | object | None = DEFAULT_HOSTS_IPS,
    log_func: LogFunc = print,
) -> bool:
    """
    修改 hosts 文件的主函数

    参数:
        domain: 域名
        action: 操作类型 ("add", "remove", "backup", "restore")
        ip: 单个 IP 字符串或可迭代的多个 IP（仅在 action="add" 时使用）
        log_func: 日志输出函数

    返回:
        成功返回 True，失败返回 False
    """
    action_names = {
        "add": "添加条目",
        "remove": "删除条目",
        "backup": "备份文件",
        "restore": "还原文件",
    }

    log_func(f"开始执行 hosts 文件操作: {action_names.get(action, action)}")

    if action == "backup":
        return backup_hosts_file(log_func)
    elif action == "restore":
        return restore_hosts_file(log_func)
    elif action == "add":
        return add_hosts_entry(domain, ip=ip, log_func=log_func)
    elif action == "remove":
        return remove_hosts_entry(domain, log_func=log_func, ip=ip)
    else:
        log_func(f"错误: 不支持的操作类型: {action}")
        return False
