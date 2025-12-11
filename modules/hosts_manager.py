"""
hosts 文件管理模块
处理 hosts 文件的备份、修改、还原等操作
"""

import ctypes
import os
import shutil
import stat
import subprocess
import sys

from .macos_privileged_helper import get_mac_privileged_session
from .resource_manager import ResourceManager

HOSTS_ENTRY_MARKER = "# Added by MTGA GUI"
DEFAULT_HOSTS_IPS = ("127.0.0.1", "::1")


def _normalize_ip_list(ip):
    """将 IP 参数转换为去重后的字符串列表。"""
    if ip is None:
        iterable = DEFAULT_HOSTS_IPS
    elif isinstance(ip, str):
        iterable = [ip]
    elif isinstance(ip, (list, tuple, set)):
        iterable = list(ip)
    else:
        iterable = [ip]

    normalized = []
    for addr in iterable:
        if not addr:
            continue
        addr_str = str(addr).strip()
        if addr_str and addr_str not in normalized:
            normalized.append(addr_str)
    return normalized


def _build_hosts_block(domain, ip_list):
    """根据域名与 IP 列表构建统一的 hosts 文本块。"""
    domain = str(domain).strip()
    valid_ips = [ip for ip in ip_list if ip]
    if not domain or not valid_ips:
        return ""
    entries = "\n".join(f"{ip} {domain}" for ip in valid_ips)
    return f"{HOSTS_ENTRY_MARKER}\n{entries}\n"


def _append_hosts_block(content, hosts_block):
    """在原有内容后追加 hosts 文本块，并保留一个空行分隔。"""
    content = content.rstrip("\n")
    if not content:
        return hosts_block
    return f"{content}\n\n{hosts_block}"


def _remove_legacy_hosts_entries(content, domain):
    """
    移除旧版本逐条写入的 hosts 记录，返回新内容与删除数量。
    旧格式为一条注释配合单个域名记录。
    """
    lines = content.splitlines()
    new_lines = []
    skip_block = False
    removed_entries = 0

    for line in lines:
        if skip_block:
            if domain in line:
                removed_entries += 1
                continue
            if not line.strip():
                skip_block = False
                continue
            skip_block = False
        if HOSTS_ENTRY_MARKER in line:
            if new_lines and not new_lines[-1].strip():
                new_lines.pop()
            skip_block = True
            continue
        new_lines.append(line)

    trailing_newline = content.endswith("\n")
    new_content = "\n".join(new_lines)
    if trailing_newline:
        new_content += "\n"
    return new_content, removed_entries


def _remove_hosts_block_from_content(content, domain, ip_list):
    """移除当前版本写入的文本块，并返回新内容和删除的条目数量。"""
    normalized_ips = _normalize_ip_list(ip_list)
    removed_entries = 0
    block_text = _build_hosts_block(domain, normalized_ips)

    if block_text:
        variants = [
            ("\n\n" + block_text, "\n"),
            ("\n" + block_text, "\n"),
            (block_text, ""),
        ]
        for target, replacement in variants:
            while target in content:
                content = content.replace(target, replacement, 1)
                removed_entries += len(normalized_ips)

    content, legacy_removed = _remove_legacy_hosts_entries(content, domain)
    removed_entries += legacy_removed
    return content, removed_entries


def _is_windows_admin():
    """检测当前进程是否以管理员身份运行（仅 Windows 使用）。"""
    if os.name != "nt":
        return False
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def _ensure_windows_hosts_writable(hosts_file, log_func=print):
    """
    尝试清理 Windows hosts 文件的只读属性，避免因文件被锁导致写入失败。
    """
    if os.name != "nt":
        return
    try:
        os.chmod(hosts_file, stat.S_IWRITE)
    except PermissionError as e:
        log_func(f"⚠️ 无法移除 hosts 文件只读属性: {e}")
    except OSError as e:
        log_func(f"⚠️ 调整 hosts 文件权限时出错: {e}")


def get_hosts_file_path():
    """获取 hosts 文件路径"""
    if os.name == "nt":  # Windows
        return r"C:\Windows\System32\drivers\etc\hosts"
    else:  # Unix/Linux/macOS
        return "/etc/hosts"


def get_backup_file_path():
    """获取备份文件路径（持久化到用户数据目录）"""
    resource_manager = ResourceManager()
    return resource_manager.get_hosts_backup_file()


def detect_file_encoding(file_path):
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


def backup_hosts_file(log_func=print):
    """
    备份 hosts 文件

    参数:
        log_func: 日志输出函数

    返回:
        成功返回 True，失败返回 False
    """
    hosts_file = get_hosts_file_path()
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


def restore_hosts_file(log_func=print):
    """
    还原 hosts 文件

    参数:
        log_func: 日志输出函数

    返回:
        成功返回 True，失败返回 False
    """
    hosts_file = get_hosts_file_path()
    backup_file = get_backup_file_path()

    log_func("开始还原 hosts 文件...")

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


def write_hosts_file_with_permission(hosts_file, content, encoding, log_func=print):
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
            _ensure_windows_hosts_writable(hosts_file, log_func=log_func)
            with open(hosts_file, "w", encoding=encoding) as f:
                f.write(content)
            return True
        except PermissionError as e:
            if os.name == "nt":
                is_admin = _is_windows_admin()
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


def add_hosts_entry(domain, ip=DEFAULT_HOSTS_IPS, log_func=print):
    """
    添加 hosts 条目

    参数:
        domain: 域名
        ip: 单个 IP 字符串或可迭代的多个 IP
        log_func: 日志输出函数

    返回:
        成功返回 True，失败返回 False
    """
    ip_list = _normalize_ip_list(ip)
    if not ip_list:
        log_func("未提供有效 IP，取消 hosts 修改")
        return False

    hosts_file = get_hosts_file_path()
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

        # 移除旧记录，保证写入是原子块
        content, removed_entries = _remove_hosts_block_from_content(content, domain, ip_list)
        if removed_entries:
            log_func(f"检测到重复记录，已移除 {removed_entries} 个 {domain} 条目")

        hosts_block = _build_hosts_block(domain, ip_list)
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

        # 添加统一的文本块并保留一个空行
        content = _append_hosts_block(content, hosts_block)

        # 使用权限写入
        write_success = write_hosts_file_with_permission(hosts_file, content, encoding, log_func)
        if write_success:
            log_func("hosts 文件修改成功！")
        return write_success

    except Exception as e:
        log_func(f"修改 hosts 文件失败: {e}")
        return False


def remove_hosts_entry(domain, log_func=print, *, ip=None):
    """
    删除 hosts 条目

    参数:
        domain: 要删除的域名
        ip: 需要删除的 IP 列表（默认删除模块写入的两个地址）
        log_func: 日志输出函数

    返回:
        成功返回 True，失败返回 False
    """
    ip_list = _normalize_ip_list(ip)

    hosts_file = get_hosts_file_path()

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

        new_content, removed_count = _remove_hosts_block_from_content(content, domain, ip_list)

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


def open_hosts_file(log_func=print):
    """
    根据平台打开 hosts 文件

    参数:
        log_func: 日志输出函数

    返回:
        成功返回 True，失败返回 False
    """
    hosts_file = get_hosts_file_path()
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
                if success:
                    log_func("已使用默认文本编辑器打开 hosts 文件")
                    result = True
                else:
                    error_msg = data.get("stderr") or data.get("error") or data.get("stdout") or ""
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


def modify_hosts_file(domain="api.openai.com", action="add", ip=DEFAULT_HOSTS_IPS, log_func=print):
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
