from __future__ import annotations

import tkinter as tk
from collections.abc import Callable
from dataclasses import dataclass
from tkinter import messagebox, ttk
from typing import Any

import requests

from modules.proxy.proxy_config import DEFAULT_MIDDLE_ROUTE, normalize_middle_route
from modules.services.config_service import ConfigStore


@dataclass(frozen=True)
class ConfigGroupPanelDeps:
    parent: ttk.Frame
    window: tk.Tk
    log: Callable[[str], None]
    tooltip: Callable[..., None]
    center_window: Callable[[tk.Toplevel | tk.Tk], None]
    get_preferred_font: Callable[..., Any]
    config_store: ConfigStore
    thread_manager: Any
    api_key_visible_chars: int
    test_chat_completion: Callable[..., None]
    test_model_in_list: Callable[..., None]


class ConfigGroupPanel:
    def __init__(self, deps: ConfigGroupPanelDeps) -> None:
        self._deps = deps
        self._config_groups: list[dict[str, Any]] = []
        self._current_config_index = 0
        self._build()
        self.refresh_config_list()

    def refresh_config_list(self) -> None:
        self._refresh_config_tree()
        self._deps.log("已刷新配置组列表")

    def _build(self) -> None:
        config_frame = ttk.LabelFrame(self._deps.parent, text="代理服务器配置组")
        config_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        config_paned = ttk.PanedWindow(config_frame, orient=tk.HORIZONTAL)
        config_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        config_list_frame = ttk.Frame(config_paned)
        config_paned.add(config_list_frame, weight=3)

        list_header_frame = ttk.Frame(config_list_frame)
        list_header_frame.pack(fill=tk.X, padx=5, pady=(5, 0))

        ttk.Label(list_header_frame, text="配置组列表:").pack(side=tk.LEFT)

        test_btn = ttk.Button(
            list_header_frame,
            text="测活",
            command=self._test_selected_config,
            width=6,
        )
        test_btn.pack(side=tk.RIGHT, padx=5)
        self._deps.tooltip(
            test_btn,
            "测试选中配置组的实际对话功能\n会发送最小请求并消耗少量tokens\n请确保配置正确后使用",
            wraplength=250,
        )

        refresh_btn = ttk.Button(
            list_header_frame,
            text="刷新",
            command=self.refresh_config_list,
            width=6,
        )
        refresh_btn.pack(side=tk.RIGHT, padx=16)
        self._deps.tooltip(
            refresh_btn,
            "重新加载配置文件中的配置组\n用于同步外部修改或恢复意外更改",
            wraplength=250,
        )

        tree_frame = ttk.Frame(config_list_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        columns = ("序号", "API URL", "实际模型ID", "映射模型ID", "API Key")
        self._config_tree = ttk.Treeview(
            tree_frame, columns=columns, show="headings", height=6
        )

        v_scrollbar = ttk.Scrollbar(
            tree_frame,
            orient=tk.VERTICAL,
            command=self._config_tree.yview,
        )
        self._config_tree.configure(yscrollcommand=v_scrollbar.set)
        h_scrollbar = ttk.Scrollbar(
            tree_frame,
            orient=tk.HORIZONTAL,
            command=self._config_tree.xview,
        )
        self._config_tree.configure(xscrollcommand=h_scrollbar.set)

        self._config_tree.heading("序号", text="序号")
        self._config_tree.heading("API URL", text="API URL")
        self._config_tree.heading("实际模型ID", text="实际模型ID")
        self._config_tree.heading("映射模型ID", text="映射模型ID")
        self._config_tree.heading("API Key", text="API Key")

        self._config_tree.column("序号", width=30, anchor=tk.CENTER)
        self._config_tree.column("API URL", width=150)
        self._config_tree.column("实际模型ID", width=120)
        self._config_tree.column("映射模型ID", width=120)
        self._config_tree.column("API Key", width=100)

        self._config_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        config_buttons_frame = ttk.Frame(config_paned)
        config_paned.add(config_buttons_frame, weight=1)

        ttk.Label(config_buttons_frame, text="操作:").pack(anchor=tk.W, padx=5, pady=(5, 0))

        ttk.Button(config_buttons_frame, text="新增", command=self._add_config_group).pack(
            fill=tk.X, padx=5, pady=2
        )
        ttk.Button(config_buttons_frame, text="修改", command=self._edit_config_group).pack(
            fill=tk.X, padx=5, pady=2
        )
        ttk.Button(config_buttons_frame, text="删除", command=self._delete_config_group).pack(
            fill=tk.X, padx=5, pady=2
        )
        ttk.Button(config_buttons_frame, text="上移", command=self._move_config_up).pack(
            fill=tk.X, padx=5, pady=2
        )
        ttk.Button(config_buttons_frame, text="下移", command=self._move_config_down).pack(
            fill=tk.X, padx=5, pady=2
        )

        self._config_tree.bind("<<TreeviewSelect>>", self._on_config_select)

    def _test_selected_config(self) -> None:
        selected_index = self._get_selected_index()
        if selected_index < 0:
            self._deps.log("请先选择要测活的配置组")
            return

        config_group = self._config_groups[selected_index]
        self._deps.test_chat_completion(
            config_group,
            log_func=self._deps.log,
            thread_manager=self._deps.thread_manager,
        )

    def _refresh_config_tree(self) -> None:
        (
            self._config_groups,
            self._current_config_index,
        ) = self._deps.config_store.load_config_groups()

        for item in self._config_tree.get_children():
            self._config_tree.delete(item)

        for i, group in enumerate(self._config_groups):
            # API Key 显示（部分隐藏）
            if "target_model_id" in group:
                fifth_col = group.get("target_model_id", "") or "(无)"
            else:
                api_key = group.get("api_key", "")
                if api_key:
                    if len(api_key) > self._deps.api_key_visible_chars:
                        mask = "*" * (len(api_key) - self._deps.api_key_visible_chars)
                        suffix = api_key[-self._deps.api_key_visible_chars :]
                        fifth_col = f"{mask}{suffix}"
                    else:
                        fifth_col = "***"
                else:
                    fifth_col = "(无)"
            
            # 映射模型ID（默认与实际ID相同）
            mapped_model_id = group.get("mapped_model_id", "") or group.get("model_id", "") or "(无)"

            self._config_tree.insert(
                "",
                "end",
                values=(
                    i + 1,
                    group.get("api_url", ""),
                    group.get("model_id", ""),
                    mapped_model_id,
                    fifth_col
                ),
            )

        if self._config_groups and 0 <= self._current_config_index < len(self._config_groups):
            children = self._config_tree.get_children()
            if self._current_config_index < len(children):
                self._config_tree.selection_set(children[self._current_config_index])
                self._config_tree.focus(children[self._current_config_index])

    def _get_selected_index(self) -> int:
        selection = self._config_tree.selection()
        if selection:
            item = selection[0]
            return self._config_tree.index(item)
        return -1

    def _on_config_select(self, _event) -> None:
        selected_index = self._get_selected_index()
        if selected_index >= 0:
            self._current_config_index = selected_index
            self._deps.config_store.save_config_groups(
                self._config_groups,
                self._current_config_index,
            )

    def _open_config_group_window(  # noqa: PLR0915
        self,
        title: str,
        initial_group: dict[str, Any] | None,
        on_save: Callable[[dict[str, str]], bool],
        on_saved: Callable[[dict[str, str]], None] | None = None,
    ) -> None:
        def handle_save() -> None:
            name = name_var.get().strip()
            api_url = api_url_var.get().strip()
            model_id = model_id_var.get().strip()
            mapped_model_id = mapped_model_id_var.get().strip()
            api_key = api_key_var.get().strip()
            middle_route_value = ""
            if middle_route_enabled_var.get() and not placeholder_active:
                middle_route_value = middle_route_var.get().strip()

            if not api_url or not model_id or not api_key:
                self._deps.log("错误: API URL、实际模型ID和API Key都是必填项")
                return

            payload = {
                "name": name,
                "api_url": api_url,
                "model_id": model_id,
                "mapped_model_id": mapped_model_id if mapped_model_id else model_id,  # 默认与实际ID相同
                "api_key": api_key,
            }
            if middle_route_value:
                payload["middle_route"] = normalize_middle_route(middle_route_value)

            if on_save(payload):
                window.destroy()
                if on_saved:
                    on_saved(payload)

        window = tk.Toplevel(self._deps.window)
        window.title(title)
        window.geometry("450x360")  # 增加高度以容纳获取模型按钮
        window.resizable(False, False)
        window.transient(self._deps.window)

        main_frame = ttk.Frame(window, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        name_value = initial_group.get("name", "") if initial_group else ""
        api_url_value = initial_group.get("api_url", "") if initial_group else ""
        model_id_value = initial_group.get("model_id", "") if initial_group else ""
        mapped_model_id_value = initial_group.get("mapped_model_id", model_id_value) if initial_group else ""  # 默认值为实际模型ID
        api_key_value = initial_group.get("api_key", "") if initial_group else ""

        ttk.Label(main_frame, text="配置组名称 (可选):").grid(row=0, column=0, sticky=tk.W, pady=5)
        name_var = tk.StringVar(value=name_value)
        name_entry = ttk.Entry(main_frame, textvariable=name_var, width=35)
        name_entry.grid(row=0, column=1, sticky=tk.EW, padx=(10, 0), pady=5)

        ttk.Label(main_frame, text="* API URL:").grid(row=1, column=0, sticky=tk.W, pady=5)
        api_url_var = tk.StringVar(value=api_url_value)
        api_url_entry = ttk.Entry(main_frame, textvariable=api_url_var, width=35)
        api_url_entry.grid(row=1, column=1, sticky=tk.EW, padx=(10, 0), pady=5)

        ttk.Label(main_frame, text="* API Key:").grid(row=2, column=0, sticky=tk.W, pady=5)
        api_key_var = tk.StringVar(value=api_key_value)
        api_key_entry = ttk.Entry(main_frame, textvariable=api_key_var, width=35, show="*")
        api_key_entry.grid(row=2, column=1, sticky=tk.EW, padx=(10, 0), pady=5)

        middle_route_value = initial_group.get("middle_route", "").strip() if initial_group else ""
        middle_route_enabled_var = tk.BooleanVar(value=bool(middle_route_value))
        middle_route_var = tk.StringVar(value=middle_route_value)
        middle_route_custom_value = middle_route_value
        placeholder_active = False

        placeholder_style = "ConfigGroupPlaceholder.TEntry"
        ttk.Style().configure(placeholder_style, foreground="gray")

        middle_route_toggle = ttk.Checkbutton(
            main_frame,
            text="修改中间路由",
            variable=middle_route_enabled_var,
        )
        middle_route_toggle.grid(row=3, column=0, sticky=tk.W, pady=5)

        middle_route_entry = ttk.Entry(main_frame, textvariable=middle_route_var, width=35)
        middle_route_entry.grid(row=3, column=1, sticky=tk.EW, padx=(10, 0), pady=5)

        # 实际模型ID行（支持智能下拉选择）
        ttk.Label(main_frame, text="* 实际模型ID:").grid(row=4, column=0, sticky=tk.W, pady=5)
        
        # 模型ID容器（包含下拉框和刷新按钮）
        model_id_container = ttk.Frame(main_frame)
        model_id_container.grid(row=4, column=1, sticky=tk.EW, padx=(10, 0), pady=5)
        
        # 模型ID变量
        model_id_var = tk.StringVar(value=model_id_value)
        
        # 创建智能下拉框（可输入 + 可选择）
        model_id_combobox = ttk.Combobox(
            model_id_container,
            textvariable=model_id_var,
            width=28  # 减小宽度为刷新按钮留空间
        )
        model_id_combobox.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 设置初始值
        if model_id_value:
            model_id_combobox.set(model_id_value)
        
        # 刷新按钮
        refresh_btn = ttk.Button(
            model_id_container,
            text="🔄",
            width=3,
            command=lambda: self._fetch_models_list(
                api_url_var.get().strip(),
                api_key_var.get().strip(),
                model_id_var,
                model_id_combobox,
                window,
                force_refresh=True  # 强制刷新
            )
        )
        refresh_btn.pack(side=tk.LEFT, padx=(5, 0))
        self._deps.tooltip(
            refresh_btn,
            "刷新模型列表\n从API获取最新可用模型",
            wraplength=150,
        )
        
        # 绑定下拉框打开事件，自动获取模型列表
        def on_combobox_click(event):
            # 只在列表为空时才显示加载弹窗并获取
            if not model_id_combobox['values']:
                # 阻止默认的下拉行为
                model_id_combobox.selection_clear()
                # 触发异步获取（显示加载弹窗）
                self._fetch_models_list(
                    api_url_var.get().strip(),
                    api_key_var.get().strip(),
                    model_id_var,
                    model_id_combobox,
                    window
                )
                return 'break'  # 阻止默认行为
            # 如果列表已有数据，允许正常展开
        
        # 实际模型ID变化时，自动同步到映射ID（如果映射ID为空或与旧实际ID相同）
        def on_model_id_change(*args):
            current_model_id = model_id_var.get().strip()
            current_mapped_id = mapped_model_id_var.get().strip()
            
            # 如果映射ID为空，或者映射ID等于之前的实际ID，则自动同步
            if not current_mapped_id or current_mapped_id == model_id_value:
                mapped_model_id_var.set(current_model_id)
        
        model_id_var.trace_add('write', on_model_id_change)
        
        model_id_combobox.bind('<Button-1>', on_combobox_click)
        model_id_combobox.bind('<<ComboboxSelected>>', lambda e: None)  # 占位符
        
        # 添加提示文本
        self._deps.tooltip(
            model_id_combobox,
            "点击下拉箭头自动从API获取可用模型列表\n也可以直接手动输入模型ID",
            wraplength=250,
        )

        # 映射模型ID行（客户端使用的模型名）
        ttk.Label(main_frame, text="映射模型ID:").grid(row=5, column=0, sticky=tk.W, pady=5)
        mapped_model_id_var = tk.StringVar(value=mapped_model_id_value)
        mapped_model_id_entry = ttk.Entry(main_frame, textvariable=mapped_model_id_var, width=35)
        mapped_model_id_entry.grid(row=5, column=1, sticky=tk.EW, padx=(10, 0), pady=5)
        self._deps.tooltip(
            mapped_model_id_entry,
            "映射模型ID（客户端使用的模型名）\n默认与实际模型ID相同\n示例：gpt-4o-mini",
            wraplength=250,
        )

        def set_middle_route_placeholder() -> None:
            nonlocal placeholder_active
            middle_route_var.set(DEFAULT_MIDDLE_ROUTE)
            middle_route_entry.configure(style=placeholder_style)
            placeholder_active = True

        def clear_middle_route_placeholder() -> None:
            nonlocal placeholder_active
            if placeholder_active:
                middle_route_var.set("")
                middle_route_entry.configure(style="TEntry")
                placeholder_active = False

        def apply_middle_route_state() -> None:
            nonlocal middle_route_custom_value, placeholder_active
            if middle_route_enabled_var.get():
                middle_route_entry.configure(state="normal")
                if middle_route_custom_value:
                    middle_route_var.set(middle_route_custom_value)
                    middle_route_entry.configure(style="TEntry")
                    placeholder_active = False
                else:
                    set_middle_route_placeholder()
            else:
                if not placeholder_active:
                    middle_route_custom_value = middle_route_var.get().strip()
                middle_route_entry.configure(state="disabled")
                set_middle_route_placeholder()

        def on_middle_route_focus_in(_event: tk.Event) -> None:
            if middle_route_enabled_var.get() and placeholder_active:
                clear_middle_route_placeholder()

        def on_middle_route_focus_out(_event: tk.Event) -> None:
            if not middle_route_enabled_var.get():
                return
            if not middle_route_var.get().strip():
                set_middle_route_placeholder()

        def on_middle_route_key_release(_event: tk.Event) -> None:
            nonlocal middle_route_custom_value
            if not middle_route_enabled_var.get() or placeholder_active:
                return
            middle_route_custom_value = middle_route_var.get().strip()

        middle_route_toggle.configure(command=apply_middle_route_state)
        middle_route_entry.bind("<FocusIn>", on_middle_route_focus_in)
        middle_route_entry.bind("<FocusOut>", on_middle_route_focus_out)
        middle_route_entry.bind("<KeyRelease>", on_middle_route_key_release)
        apply_middle_route_state()

        info_label = ttk.Label(
            main_frame,
            text="* 为必填项",
            font=self._deps.get_preferred_font(size=8),
            foreground="gray",
        )
        info_label.grid(row=7, column=0, columnspan=2, sticky=tk.W, pady=5)

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=8, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="保存", command=handle_save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="取消", command=window.destroy).pack(
            side=tk.LEFT, padx=5
        )

        main_frame.columnconfigure(1, weight=1)
        self._deps.center_window(window)
        window.grab_set()
        name_entry.focus()

    def _add_config_group(self) -> None:
        def save_new_config(payload: dict[str, str]) -> bool:
            self._config_groups.append(payload)
            if self._deps.config_store.save_config_groups(
                self._config_groups, self._current_config_index
            ):
                display_name = payload["name"] or f"配置组 {len(self._config_groups)}"
                self._deps.log(f"已添加配置组: {display_name}")
                self.refresh_config_list()
                return True

            self._deps.log("保存配置组失败")
            return False

        def after_save(payload: dict[str, str]) -> None:
            self._deps.test_model_in_list(
                payload,
                log_func=self._deps.log,
                thread_manager=self._deps.thread_manager,
            )

        self._open_config_group_window(
            title="新增配置组",
            initial_group=None,
            on_save=save_new_config,
            on_saved=after_save,
        )

    def _edit_config_group(self) -> None:
        selected_index = self._get_selected_index()
        if selected_index < 0:
            self._deps.log("请先选择要修改的配置组")
            return

        current_group = self._config_groups[selected_index]

        def save_edited_config(payload: dict[str, str]) -> bool:
            self._config_groups[selected_index] = payload
            if self._deps.config_store.save_config_groups(
                self._config_groups, self._current_config_index
            ):
                display_name = payload["name"] or f"配置组 {selected_index + 1}"
                self._deps.log(f"已修改配置组: {display_name}")
                self.refresh_config_list()
                return True

            self._deps.log("保存配置组失败")
            return False

        def after_save(payload: dict[str, str]) -> None:
            self._deps.test_model_in_list(
                payload,
                log_func=self._deps.log,
                thread_manager=self._deps.thread_manager,
            )

        self._open_config_group_window(
            title="修改配置组",
            initial_group=current_group,
            on_save=save_edited_config,
            on_saved=after_save,
        )

    def _delete_config_group(self) -> None:
        selected_index = self._get_selected_index()
        if selected_index < 0:
            self._deps.log("请先选择要删除的配置组")
            return

        if len(self._config_groups) <= 1:
            self._deps.log("至少需要保留一个配置组")
            return

        group_name = self._config_groups[selected_index].get(
            "name", f"配置组{selected_index + 1}"
        )

        if messagebox.askyesno("确认删除", f"确定要删除配置组 '{group_name}' 吗？"):
            del self._config_groups[selected_index]

            if self._current_config_index >= len(self._config_groups):
                self._current_config_index = len(self._config_groups) - 1
            elif self._current_config_index > selected_index:
                self._current_config_index -= 1

            if self._deps.config_store.save_config_groups(
                self._config_groups, self._current_config_index
            ):
                self._deps.log(f"已删除配置组: {group_name}")
                self.refresh_config_list()
            else:
                self._deps.log("保存配置组失败")

    def _move_config_up(self) -> None:
        selected_index = self._get_selected_index()
        if selected_index <= 0:
            return

        self._config_groups[selected_index], self._config_groups[selected_index - 1] = (
            self._config_groups[selected_index - 1],
            self._config_groups[selected_index],
        )

        if self._current_config_index == selected_index:
            self._current_config_index = selected_index - 1
        elif self._current_config_index == selected_index - 1:
            self._current_config_index = selected_index

        if self._deps.config_store.save_config_groups(
            self._config_groups, self._current_config_index
        ):
            self.refresh_config_list()
            children = self._config_tree.get_children()
            if selected_index - 1 < len(children):
                self._config_tree.selection_set(children[selected_index - 1])
                self._config_tree.focus(children[selected_index - 1])
        else:
            self._deps.log("保存配置组失败")

    def _move_config_down(self) -> None:
        selected_index = self._get_selected_index()
        if selected_index < 0 or selected_index >= len(self._config_groups) - 1:
            return

        self._config_groups[selected_index], self._config_groups[selected_index + 1] = (
            self._config_groups[selected_index + 1],
            self._config_groups[selected_index],
        )

        if self._current_config_index == selected_index:
            self._current_config_index = selected_index + 1
        elif self._current_config_index == selected_index + 1:
            self._current_config_index = selected_index

        if self._deps.config_store.save_config_groups(
            self._config_groups, self._current_config_index
        ):
            self.refresh_config_list()
            children = self._config_tree.get_children()
            if selected_index + 1 < len(children):
                self._config_tree.selection_set(children[selected_index + 1])
                self._config_tree.focus(children[selected_index + 1])
        else:
            self._deps.log("保存配置组失败")

    def _fetch_models_list(
        self,
        api_url: str,
        api_key: str,
        model_id_var: tk.StringVar,
        model_id_combobox: ttk.Combobox,
        parent_window: tk.Toplevel,
        force_refresh: bool = False,
    ) -> None:
        """从API获取模型列表并更新下拉框选项
        
        Args:
            force_refresh: 是否强制刷新（清空现有列表）
        """
        if not api_url or not api_key:
            self._deps.log("⚠️ 请先填写 API URL 和 API Key 后再获取模型列表")
            return
        
        # 如果是强制刷新，先清空列表
        if force_refresh:
            model_id_combobox['values'] = []
            self._deps.log("🔄 正在刷新模型列表...")

        # 构建完整的模型列表URL
        api_url = api_url.rstrip('/')
        if not api_url.startswith('http://') and not api_url.startswith('https://'):
            api_url = f'https://{api_url}'
        
        models_url = f"{api_url}/v1/models"
        
        self._deps.log(f"🔄 正在从 {models_url} 获取模型列表...")
        
        # 创建加载弹窗
        loading_dialog = tk.Toplevel(parent_window)
        loading_dialog.title("加载中")
        loading_dialog.geometry("300x100")
        loading_dialog.resizable(False, False)
        loading_dialog.transient(parent_window)
        loading_dialog.grab_set()
        
        # 居中显示
        self._deps.center_window(loading_dialog)
        
        # 添加加载提示
        loading_frame = ttk.Frame(loading_dialog, padding=20)
        loading_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(
            loading_frame,
            text="🔄 正在获取模型列表...",
            font=self._deps.get_preferred_font(size=11)
        ).pack(pady=(10, 5))
        
        ttk.Label(
            loading_frame,
            text="请稍候",
            font=self._deps.get_preferred_font(size=9),
            foreground="gray"
        ).pack()
        
        def fetch_in_thread():
            try:
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                
                response = requests.get(
                    models_url,
                    headers=headers,
                    timeout=10,
                    verify=False  # 跳过SSL验证，与代理服务器行为一致
                )
                response.raise_for_status()
                
                data = response.json()
                models_data = data.get('data', [])
                
                if not models_data:
                    self._deps.log("⚠️ API 返回的模型列表为空（可手动输入模型ID）")
                    return
                
                # 提取模型ID列表
                model_ids = [model.get('id', '') for model in models_data if model.get('id')]
                
                if not model_ids:
                    self._deps.log("⚠️ 未找到有效的模型ID（可手动输入模型ID）")
                    return
                
                self._deps.log(f"✅ 成功获取 {len(model_ids)} 个模型")
                
                # 在主线程中关闭加载弹窗并更新下拉框
                parent_window.after(0, lambda: self._close_loading_and_update(
                    loading_dialog,
                    model_id_combobox,
                    model_id_var,
                    model_ids
                ))
                
            except requests.exceptions.Timeout:
                self._deps.log("⚠️ 获取模型列表超时，请检查网络连接（可手动输入模型ID）")
                parent_window.after(0, lambda: loading_dialog.destroy())
            except requests.exceptions.RequestException as e:
                error_msg = f"⚠️ 获取模型列表失败: {str(e)}（可手动输入模型ID）"
                self._deps.log(error_msg)
                parent_window.after(0, lambda: loading_dialog.destroy())
            except Exception as e:
                error_msg = f"⚠️ 发生未知错误: {str(e)}（可手动输入模型ID）"
                self._deps.log(error_msg)
                parent_window.after(0, lambda: loading_dialog.destroy())
        
        # 在后台线程中执行请求
        self._deps.thread_manager.run(
            "fetch_models",
            fetch_in_thread,
            allow_parallel=True
        )

    def _update_combobox_values(
        self,
        combobox: ttk.Combobox,
        model_id_var: tk.StringVar,
        model_ids: list[str],
    ) -> None:
        """更新下拉框的可选值列表"""
        # 保存当前值
        current_value = model_id_var.get()
        
        # 更新下拉框选项
        combobox['values'] = model_ids
        
        # 如果当前值在列表中，保持选中；否则选择第一个
        if current_value and current_value in model_ids:
            combobox.set(current_value)
        elif model_ids:
            combobox.current(0)  # 选择第一个
        
        # 延迟50ms后展开下拉列表，确保数据已加载
        combobox.after(50, lambda: combobox.event_generate('<Down>'))
        
        self._deps.log(f"✅ 已加载 {len(model_ids)} 个可选模型，您也可以直接输入")


    def _close_loading_and_update(
        self,
        loading_dialog: tk.Toplevel,
        combobox: ttk.Combobox,
        model_id_var: tk.StringVar,
        model_ids: list[str],
    ) -> None:
        """关闭加载弹窗并更新下拉框"""
        try:
            # 关闭加载弹窗
            loading_dialog.destroy()
        except Exception:
            pass  # 弹窗可能已关闭
        
        # 更新下拉框
        self._update_combobox_values(combobox, model_id_var, model_ids)


def build_config_group_panel(deps: ConfigGroupPanelDeps) -> ConfigGroupPanel:
    return ConfigGroupPanel(deps)
