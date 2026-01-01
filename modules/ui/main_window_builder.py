from __future__ import annotations

import os
import sys
import tkinter as tk
from contextlib import suppress
from dataclasses import dataclass
from typing import Any

from modules.actions import (
    hosts_actions,
    model_tests,
    shutdown_actions,
)
from modules.services.config_service import ConfigStore
from modules.ui import (
    config_group_panel,
    footer_actions,
    global_config_panel,
    layout_builders,
    proxy_context,
    tab_builders,
    window_context,
    window_lifecycle,
)


@dataclass(frozen=True)
class MainWindowDeps:
    get_icon_file: Any
    thread_manager: Any
    config_store: ConfigStore
    log_error: Any
    check_environment: Any
    is_packaged: Any
    check_network_environment: Any
    modify_hosts_file: Any
    open_hosts_file: Any
    get_user_data_dir: Any
    copy_template_files: Any
    app_metadata: Any
    app_version: str
    update_service: Any
    update_dialog: Any
    create_tkinterweb_html_widget: Any
    program_resource_dir: str
    startup_context: Any
    generate_certificates: Any
    install_ca_cert: Any
    has_existing_ca_cert: Any
    center_window: Any
    get_proxy_instance: Any
    set_proxy_instance: Any
    messagebox: Any


def build_main_window(deps: MainWindowDeps) -> tk.Tk | None:  # noqa: PLR0915
    if sys.platform == "darwin" and os.getcwd() == "/":
        with suppress(OSError):
            os.chdir(os.path.expanduser("~"))

    window_context_result = window_context.build_window_context(
        log_error=deps.log_error,
        get_icon_file=deps.get_icon_file,
    )
    window = window_context_result.window
    get_preferred_font = window_context_result.get_preferred_font
    default_font = window_context_result.default_font
    main_frame = window_context_result.main_frame
    main_paned = window_context_result.main_paned
    left_frame = window_context_result.left_frame
    left_content = window_context_result.left_content
    log = window_context_result.log
    tooltip = window_context_result.tooltip

    hosts_runner = hosts_actions.HostsTaskRunner(
        log_func=log,
        thread_manager=deps.thread_manager,
        modify_hosts_file=deps.modify_hosts_file,
        open_hosts_file=deps.open_hosts_file,
    )

    shutdown_state = shutdown_actions.ShutdownState()

    deps.startup_context.emit_logs(
        log=log,
        check_environment=deps.check_environment,
        is_packaged=deps.is_packaged,
    )

    config_group_panel.build_config_group_panel(
        config_group_panel.ConfigGroupPanelDeps(
            parent=left_content,
            window=window,
            log=log,
            tooltip=tooltip,
            center_window=deps.center_window,
            get_preferred_font=get_preferred_font,
            config_store=deps.config_store,
            thread_manager=deps.thread_manager,
            api_key_visible_chars=deps.app_metadata.api_key_visible_chars,
            test_chat_completion=model_tests.test_chat_completion,
            test_model_in_list=model_tests.test_model_in_list,
        )
    )

    global_config_panel.build_global_config_panel(
        global_config_panel.GlobalConfigPanelDeps(
            parent=left_content,
            log=log,
            tooltip=tooltip,
            config_store=deps.config_store,
        )
    )

    proxy_context_result = proxy_context.build_proxy_context(
        proxy_context.ProxyContextDeps(
            parent=left_content,
            tooltip=tooltip,
            log=log,
            config_store=deps.config_store,
            thread_manager=deps.thread_manager,
            check_network_environment=deps.check_network_environment,
            modify_hosts_file=deps.modify_hosts_file,
            get_proxy_instance=deps.get_proxy_instance,
            set_proxy_instance=deps.set_proxy_instance,
            hosts_runner=hosts_runner,
            has_existing_ca_cert=deps.has_existing_ca_cert,
            generate_certificates=deps.generate_certificates,
            install_ca_cert=deps.install_ca_cert,
            ca_common_name=deps.app_metadata.ca_common_name,
        )
    )

    proxy_ui = proxy_context_result.proxy_ui
    proxy_runner = proxy_context_result.proxy_runner

    # 移除更新检查功能
    tab_builders.build_main_tabs(
        tab_builders.MainTabsDeps(
            parent=left_content,
            window=window,
            log=log,
            tooltip=tooltip,
            center_window=deps.center_window,
            ca_common_name=deps.app_metadata.ca_common_name,
            thread_manager=deps.thread_manager,
            hosts_runner=hosts_runner,
            proxy_runner=proxy_runner,
            is_packaged=deps.is_packaged,
            get_user_data_dir=deps.get_user_data_dir,
            copy_template_files=deps.copy_template_files,
            error_log_filename=deps.app_metadata.error_log_filename,
            app_display_name=deps.app_metadata.display_name,
            app_version=deps.app_version,
            get_preferred_font=get_preferred_font,
        )
    )

    footer_actions.build_footer_actions(
        footer_actions.FooterActionsDeps(
            left_frame=left_frame,
            start_all=proxy_runner.start_all,
        )
    )
    window_lifecycle.bind_window_close(
        window_lifecycle.WindowLifecycleDeps(
            window=window,
            log=log,
            thread_manager=deps.thread_manager,
            stop_proxy_and_restore=proxy_ui.stop_proxy_and_restore,
            proxy_runner=proxy_runner,
            shutdown_state=shutdown_state,
        )
    )

    layout_builders.init_paned_layout(main_paned, main_frame, window)

    log("MTGA GUI 已启动")
    log("请选择操作或直接使用一键启动...")
    # 移除启动时自动检查更新

    return window
