from __future__ import annotations

import os
import sys
import tkinter as tk
from collections.abc import Callable
from contextlib import suppress
from dataclasses import dataclass
from tkinter import font as tkfont
from tkinter import messagebox, ttk
from typing import Any

from platformdirs import user_data_dir as platform_user_data_dir

from modules.actions import cert_actions, network_actions
from modules.runtime.error_codes import ErrorCode
from modules.runtime.result_messages import describe_result
from modules.services.user_data_service import (
    backup_user_data_result,
    clear_user_data_result,
    find_latest_backup_result,
    restore_backup_result,
)


@dataclass(frozen=True)
class CertTabDeps:
    notebook: ttk.Notebook
    window: tk.Tk
    log: Callable[[str], None]
    tooltip: Callable[..., None]
    center_window: Callable[[tk.Toplevel | tk.Tk], None]
    ca_common_name: str
    thread_manager: Any


def build_cert_tab(deps: CertTabDeps) -> ttk.Frame:
    cert_tab = ttk.Frame(deps.notebook)
    deps.notebook.add(cert_tab, text="证书管理")

    def generate_certs_task():
        cert_actions.run_generate_certificates(
            ca_common_name=deps.ca_common_name,
            log_func=deps.log,
            thread_manager=deps.thread_manager,
        )

    def install_certs_task():
        cert_actions.run_install_ca_cert(
            log_func=deps.log,
            thread_manager=deps.thread_manager,
        )

    def clear_ca_cert_task(ca_common_name: str):
        cert_actions.run_clear_ca_cert(
            ca_common_name=ca_common_name,
            log_func=deps.log,
            thread_manager=deps.thread_manager,
        )

    def confirm_clear_ca_cert():
        dialog = tk.Toplevel(deps.window)
        dialog.title("确认清除 CA 证书")
        dialog.transient(deps.window)

        ttk.Label(
            dialog,
            text="将从系统信任存储中删除匹配的 CA 证书，是否继续？",
            anchor="w",
            justify="left",
        ).pack(fill=tk.X, padx=12, pady=(12, 6))

        ttk.Label(dialog, text="Common Name:", anchor="w").pack(
            fill=tk.X, padx=12, pady=(0, 4)
        )
        cn_var = tk.StringVar(value=deps.ca_common_name)
        ttk.Entry(dialog, textvariable=cn_var).pack(fill=tk.X, padx=12, pady=(0, 12))

        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=12, pady=(0, 12))

        def on_cancel():
            dialog.destroy()

        def on_confirm():
            cn_value = cn_var.get().strip() or deps.ca_common_name
            dialog.destroy()
            deps.log(f"准备清除 CA 证书，Common Name: {cn_value}")
            clear_ca_cert_task(cn_value)

        ttk.Button(button_frame, text="取消", command=on_cancel).pack(side=tk.RIGHT, padx=(8, 0))
        ttk.Button(button_frame, text="确定", command=on_confirm).pack(side=tk.RIGHT)
        deps.center_window(dialog)
        dialog.grab_set()

    ttk.Button(cert_tab, text="生成CA和服务器证书", command=generate_certs_task).pack(
        fill=tk.X, padx=5, pady=5
    )
    ttk.Button(cert_tab, text="安装CA证书", command=install_certs_task).pack(
        fill=tk.X, padx=5, pady=5
    )
    clear_ca_btn = ttk.Button(cert_tab, text="清除系统CA证书", command=confirm_clear_ca_cert)
    clear_ca_btn.pack(fill=tk.X, padx=5, pady=5)
    deps.tooltip(
        clear_ca_btn,
        "macOS: 删除系统钥匙串中匹配的CA证书；\n"
        "Windows: 删除本地计算机/Root 中匹配的CA证书\n"
        f"Common Name: {deps.ca_common_name}\n"
        "需要管理员权限，建议仅在需要重置证书时使用",
        wraplength=280,
    )
    return cert_tab


@dataclass(frozen=True)
class HostsTabDeps:
    notebook: ttk.Notebook
    hosts_runner: Any


def build_hosts_tab(deps: HostsTabDeps) -> ttk.Frame:
    hosts_tab = ttk.Frame(deps.notebook)
    deps.notebook.add(hosts_tab, text="hosts文件管理")

    ttk.Button(
        hosts_tab,
        text="修改hosts文件",
        command=lambda: deps.hosts_runner.modify_hosts("add"),
    ).pack(fill=tk.X, padx=5, pady=5)

    hosts_buttons_frame = ttk.Frame(hosts_tab)
    hosts_buttons_frame.pack(fill=tk.X, padx=5, pady=5)

    ttk.Button(
        hosts_buttons_frame,
        text="备份hosts",
        command=lambda: deps.hosts_runner.modify_hosts("backup"),
    ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
    ttk.Button(
        hosts_buttons_frame,
        text="还原hosts",
        command=lambda: deps.hosts_runner.modify_hosts("restore"),
    ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

    ttk.Button(
        hosts_tab,
        text="打开hosts文件",
        command=deps.hosts_runner.open_hosts,
    ).pack(fill=tk.X, padx=5, pady=5)
    return hosts_tab


@dataclass(frozen=True)
class ProxyTabDeps:
    notebook: ttk.Notebook
    proxy_runner: Any
    log: Callable[[str], None]
    thread_manager: Any


def build_proxy_tab(deps: ProxyTabDeps) -> ttk.Frame:
    proxy_tab = ttk.Frame(deps.notebook)
    deps.notebook.add(proxy_tab, text="代理服务器操作")

    ttk.Button(proxy_tab, text="启动代理服务器", command=deps.proxy_runner.start_proxy).pack(
        fill=tk.X, padx=5, pady=5
    )
    ttk.Button(proxy_tab, text="停止代理服务器", command=deps.proxy_runner.stop_proxy).pack(
        fill=tk.X, padx=5, pady=5
    )

    ttk.Button(
        proxy_tab,
        text="检查网络环境",
        command=lambda: network_actions.run_network_environment_check(
            log_func=deps.log,
            thread_manager=deps.thread_manager,
        ),
    ).pack(fill=tk.X, padx=5, pady=5)
    return proxy_tab


@dataclass(frozen=True)
class DataManagementTabDeps:
    notebook: ttk.Notebook
    log: Callable[[str], None]
    tooltip: Callable[..., None]
    get_user_data_dir: Callable[[], str]
    copy_template_files: Callable[[], list[str]]
    error_log_filename: str


def _open_user_data_directory(deps: DataManagementTabDeps) -> None:
    try:
        user_data_dir = deps.get_user_data_dir()
        if os.name == "nt":
            os.startfile(user_data_dir)
        elif sys.platform == "darwin":
            os.system(f'open "{user_data_dir}"')
        else:
            os.system(f'xdg-open "{user_data_dir}"')
        deps.log(f"已打开用户数据目录: {user_data_dir}")
    except Exception as exc:
        deps.log(f"打开用户数据目录失败: {exc}")


def _backup_user_data_action(deps: DataManagementTabDeps) -> None:
    try:
        user_data_dir = deps.get_user_data_dir()
        result = backup_user_data_result(
            user_data_dir,
            error_log_filename=deps.error_log_filename,
        )
        if not result.ok:
            message = describe_result(result, "备份用户数据失败")
            deps.log(f"❌ {message}")
            return
        backup_result = result.details.get("backup_result") if result.details else None
        if backup_result and backup_result.item_count:
            deps.log(f"✅ 用户数据备份成功: {backup_result.backup_dir}")
            deps.log(f"备份了 {backup_result.item_count} 个项目")
        else:
            deps.log("没有需要备份的用户数据")
    except Exception as exc:
        deps.log(f"❌ 备份用户数据失败: {exc}")


def _clear_user_data_action(deps: DataManagementTabDeps) -> None:
    try:
        result = messagebox.askyesno(
            "确认清除",
            "此操作将删除所有用户数据（配置文件、证书等），但保留备份文件夹。\n\n确定要继续吗？",
            icon="warning",
        )
        if not result:
            deps.log("用户取消了清除操作")
            return

        user_data_dir = deps.get_user_data_dir()
        result = clear_user_data_result(
            user_data_dir,
            error_log_filename=deps.error_log_filename,
            copy_template_files_fn=deps.copy_template_files,
        )
        if not result.ok:
            message = describe_result(result, "清除用户数据失败")
            deps.log(f"❌ {message}")
            return
        clear_result = result.details.get("clear_result") if result.details else None
        if clear_result and clear_result.removed_count:
            deps.log(f"✅ 用户数据清除成功，删除了 {clear_result.removed_count} 个项目")
            deps.log("备份文件夹已保留")
            if clear_result.copied_files_count:
                deps.log(f"✅ 已复制 {clear_result.copied_files_count} 个模板文件")
            else:
                deps.log("模板文件已存在或复制完成")
        else:
            deps.log("没有需要清除的用户数据")
    except Exception as exc:
        deps.log(f"❌ 清除用户数据失败: {exc}")


def _restore_user_data_action(deps: DataManagementTabDeps) -> None:
    try:
        def warn_no_backup(log_message: str, dialog_message: str) -> None:
            deps.log(log_message)
            messagebox.showwarning("无备份", dialog_message)

        def show_restore_error(log_message: str, dialog_message: str) -> None:
            deps.log(log_message)
            messagebox.showerror("还原失败", dialog_message)

        user_data_dir = deps.get_user_data_dir()
        latest_result = find_latest_backup_result(user_data_dir)
        if not latest_result.ok:
            if latest_result.code == ErrorCode.BACKUP_DIR_MISSING:
                warn_no_backup("❌ 没有找到备份文件夹", "没有找到备份文件夹，无法执行还原操作。")
            elif latest_result.code == ErrorCode.NO_BACKUPS:
                warn_no_backup("❌ 没有找到任何备份", "没有找到任何备份文件，无法执行还原操作。")
            else:
                show_restore_error(
                    f"❌ {describe_result(latest_result, '读取备份失败')}",
                    f"无法读取备份：\n{describe_result(latest_result, '读取备份失败')}",
                )
            return

        latest_info = latest_result.details.get("latest_backup") if latest_result.details else None
        if not latest_info:
            warn_no_backup("❌ 未找到可用备份", "没有找到任何备份文件，无法执行还原操作。")
            return

        result = messagebox.askyesno(
            "确认还原",
            "将从最新备份还原数据：\n"
            f"{latest_info.backup_name}\n\n"
            "此操作将覆盖当前的配置文件、证书等数据。\n\n确定要继续吗？",
            icon="question",
        )
        if not result:
            deps.log("用户取消了还原操作")
            return

        restore_result = restore_backup_result(
            user_data_dir,
            backup_path=latest_info.backup_path,
        )
        if not restore_result.ok:
            message = describe_result(restore_result, "还原用户数据失败")
            show_restore_error(
                f"❌ {message}",
                f"还原操作失败：\n{message}",
            )
            return

        latest_restore = (
            restore_result.details.get("restore_result") if restore_result.details else None
        )
        if not latest_restore:
            show_restore_error("❌ 还原结果异常", "还原结果异常，请查看日志。")
            return
        deps.log(
            f"✅ 数据还原成功，从备份 {latest_restore.backup_name} "
            f"还原了 {latest_restore.restored_count} 个项目"
        )
        messagebox.showinfo(
            "还原成功",
            "数据还原完成！\n\n"
            f"从备份：{latest_restore.backup_name}\n"
            f"还原项目：{latest_restore.restored_count} 个",
        )
    except Exception as exc:
        deps.log(f"❌ 还原用户数据失败: {exc}")
        messagebox.showerror("还原失败", f"还原操作失败：\n{exc}")


def _build_data_management_buttons(
    deps: DataManagementTabDeps,
    data_mgmt_tab: ttk.Frame,
) -> None:
    button_frame = ttk.Frame(data_mgmt_tab)
    button_frame.pack(fill=tk.X, padx=5, pady=5)

    btn_open = ttk.Button(
        button_frame,
        text="打开目录",
        command=lambda: _open_user_data_directory(deps),
    )
    btn_open.pack(fill=tk.X, pady=2)
    default_user_data_dir = platform_user_data_dir("MTGA", appauthor=False, roaming=os.name == "nt")
    actual_user_data_dir = deps.get_user_data_dir()
    if os.path.normpath(actual_user_data_dir) != os.path.normpath(default_user_data_dir):
        open_dir_tooltip = (
            "使用系统文件管理器打开用户数据目录\n"
            f"当前：{actual_user_data_dir}\n"
            f"默认：{default_user_data_dir}"
        )
    else:
        open_dir_tooltip = f"使用系统文件管理器打开用户数据目录\n目录：{actual_user_data_dir}"
    deps.tooltip(btn_open, open_dir_tooltip)

    btn_backup = ttk.Button(
        button_frame,
        text="备份数据",
        command=lambda: _backup_user_data_action(deps),
    )
    btn_backup.pack(fill=tk.X, pady=2)
    deps.tooltip(
        btn_backup,
        "创建带时间戳的完整数据备份\n备份内容：配置文件、SSL证书、hosts备份\n"
        "备份位置：用户数据目录/backups/backup_时间戳/",
    )

    btn_restore = ttk.Button(
        button_frame,
        text="还原数据",
        command=lambda: _restore_user_data_action(deps),
    )
    btn_restore.pack(fill=tk.X, pady=2)
    deps.tooltip(
        btn_restore,
        "从最新备份恢复用户数据（覆盖现有数据）\n自动选择最新时间戳的备份进行还原\n"
        "注意：此操作会覆盖当前的配置和证书",
    )

    btn_clear = ttk.Button(
        button_frame,
        text="清除数据",
        command=lambda: _clear_user_data_action(deps),
    )
    btn_clear.pack(fill=tk.X, pady=2)
    deps.tooltip(
        btn_clear,
        "删除所有用户数据（保留历史备份）\n清除内容：配置文件、SSL证书、hosts备份\n"
        "保留内容：backups文件夹及其历史备份",
    )


def build_data_management_tab(deps: DataManagementTabDeps) -> ttk.Frame:
    data_mgmt_tab = ttk.Frame(deps.notebook)
    deps.notebook.add(data_mgmt_tab, text="用户数据管理")
    _build_data_management_buttons(deps, data_mgmt_tab)
    return data_mgmt_tab


@dataclass(frozen=True)
class AboutTabDeps:
    notebook: ttk.Notebook
    app_display_name: str
    app_version: str
    get_preferred_font: Callable[..., tkfont.Font]
    on_check_updates: Callable[[], None]


def build_about_tab(deps: AboutTabDeps) -> tuple[ttk.Frame, ttk.Button]:
    style = ttk.Style()
    style.configure("About.TFrame", background="#f0f0f0")
    style.configure(
        "AboutTitle.TLabel",
        background="#f0f0f0",
        font=deps.get_preferred_font(size=11, weight="bold"),
    )
    style.configure(
        "AboutFooter.TLabel",
        background="#f0f0f0",
        foreground="#666666",
        font=deps.get_preferred_font(size=9),
    )
    about_tab = ttk.Frame(deps.notebook, style="About.TFrame")
    deps.notebook.add(about_tab, text="关于")

    version_label = ttk.Label(
        about_tab,
        text=f"{deps.app_display_name} {deps.app_version}",
        style="AboutTitle.TLabel",
        anchor="w",
    )
    version_label.pack(anchor="w", fill=tk.X, padx=8, pady=(8, 4))

    check_updates_button = ttk.Button(about_tab, text="检查更新", command=deps.on_check_updates)
    check_updates_button.pack(anchor="w", padx=8, pady=(0, 8))

    about_footer = ttk.Label(
        about_tab,
        text="powered by BiFangKNT",
        style="AboutFooter.TLabel",
        anchor="center",
        justify="center",
    )
    about_footer.pack(side=tk.BOTTOM, fill=tk.X, padx=8, pady=(0, 8))

    return about_tab, check_updates_button


@dataclass(frozen=True)
class MainTabsDeps:
    parent: ttk.Frame
    window: tk.Tk
    log: Callable[[str], None]
    tooltip: Callable[..., None]
    center_window: Callable[[tk.Toplevel | tk.Tk], None]
    ca_common_name: str
    thread_manager: Any
    hosts_runner: Any
    proxy_runner: Any
    is_packaged: Callable[[], bool]
    get_user_data_dir: Callable[[], str]
    copy_template_files: Callable[[], list[str]]
    error_log_filename: str
    app_display_name: str
    app_version: str
    get_preferred_font: Callable[..., tkfont.Font]
    on_check_updates: Callable[[], None]


def build_main_tabs(deps: MainTabsDeps) -> tuple[ttk.Notebook, ttk.Button]:
    notebook = ttk.Notebook(deps.parent)
    notebook.pack(fill=tk.BOTH, expand=True, pady=0)
    if sys.platform == "darwin":
        # macOS 下 Notebook 点击同一标签会让焦点停留在标签栏，导致重绘延迟
        def _sync_tab_focus() -> None:
            try:
                tab_id = notebook.select()
                if not tab_id:
                    return
                tab_widget = notebook.nametowidget(tab_id)
            except tk.TclError:
                return

            focus_target: tk.Widget = tab_widget
            for child in tab_widget.winfo_children():
                if not child.winfo_viewable():
                    continue
                try:
                    takefocus = child.cget("takefocus")
                except tk.TclError:
                    takefocus = None
                if takefocus in (True, "1", 1, "true"):
                    focus_target = child
                    break
                if isinstance(child, ttk.Button | tk.Button):
                    focus_target = child
                    break

            with suppress(tk.TclError):
                focus_target.focus_set()
            focus_target.update_idletasks()

        def _schedule_refresh(_event=None) -> None:
            notebook.after_idle(_sync_tab_focus)

        notebook.bind("<<NotebookTabChanged>>", _schedule_refresh, add=True)
        notebook.bind("<ButtonRelease-1>", _schedule_refresh, add=True)
    build_cert_tab(
        CertTabDeps(
            notebook=notebook,
            window=deps.window,
            log=deps.log,
            tooltip=deps.tooltip,
            center_window=deps.center_window,
            ca_common_name=deps.ca_common_name,
            thread_manager=deps.thread_manager,
        )
    )
    build_hosts_tab(
        HostsTabDeps(
            notebook=notebook,
            hosts_runner=deps.hosts_runner,
        )
    )
    build_proxy_tab(
        ProxyTabDeps(
            notebook=notebook,
            proxy_runner=deps.proxy_runner,
            log=deps.log,
            thread_manager=deps.thread_manager,
        )
    )

    if deps.is_packaged():
        build_data_management_tab(
            DataManagementTabDeps(
                notebook=notebook,
                log=deps.log,
                tooltip=deps.tooltip,
                get_user_data_dir=deps.get_user_data_dir,
                copy_template_files=deps.copy_template_files,
                error_log_filename=deps.error_log_filename,
            )
        )

    _, check_updates_button = build_about_tab(
        AboutTabDeps(
            notebook=notebook,
            app_display_name=deps.app_display_name,
            app_version=deps.app_version,
            get_preferred_font=deps.get_preferred_font,
            on_check_updates=deps.on_check_updates,
        )
    )

    return notebook, check_updates_button
