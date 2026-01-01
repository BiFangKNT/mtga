from __future__ import annotations

import tkinter as tk
from collections.abc import Callable
from dataclasses import dataclass
from tkinter import ttk

from modules.services.config_service import ConfigStore


@dataclass(frozen=True)
class GlobalConfigPanelDeps:
    parent: ttk.Frame
    log: Callable[[str], None]
    tooltip: Callable[..., None]
    config_store: ConfigStore


def build_global_config_panel(deps: GlobalConfigPanelDeps) -> ttk.LabelFrame:
    global_config_frame = ttk.LabelFrame(deps.parent, text="全局配置")
    global_config_frame.pack(fill=tk.X, padx=5, pady=5)

    mtga_auth_frame = ttk.Frame(global_config_frame)
    mtga_auth_frame.pack(fill=tk.X, padx=5, pady=2)
    ttk.Label(mtga_auth_frame, text="MTGA鉴权Key", width=12).pack(side=tk.LEFT)
    mtga_auth_var = tk.StringVar()
    mtga_auth_entry = ttk.Entry(mtga_auth_frame, textvariable=mtga_auth_var, width=25, show="*")
    mtga_auth_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 10))  # 右侧留出间距
    deps.tooltip(
        mtga_auth_entry,
        "必填：MTGA鉴权Key\n"
        "对应 Trae 端填写的 API 密钥，自定义，\n与实际 API Key 是互相独立的概念。\n"
        "作为 MTGA 代理服务的全局密钥。\n"
        "示例：111",
        wraplength=360,
    )

    def load_global_config_values() -> None:
        _, mtga_auth_key = deps.config_store.load_global_config()
        mtga_auth_var.set(mtga_auth_key)

    def save_global_config_values() -> bool:
        mtga_auth_key = mtga_auth_var.get().strip()

        if not mtga_auth_key:
            deps.log("错误: MTGA鉴权Key是必填项")
            return False

        config_groups, current_config_index = deps.config_store.load_config_groups()

        if deps.config_store.save_config_groups(
            config_groups,
            current_config_index,
            "",  # 映射模型ID不再在全局配置中
            mtga_auth_key,
        ):
            deps.log("全局配置已保存")
            return True
        deps.log("保存全局配置失败")
        return False

    load_global_config_values()

    # 保存按钮移到同一行
    global_save_btn = ttk.Button(
        mtga_auth_frame,
        text="保存",
        width=8,
        command=save_global_config_values,
    )
    global_save_btn.pack(side=tk.LEFT, padx=(0, 5))

    return global_config_frame
