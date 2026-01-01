from __future__ import annotations

import tkinter as tk
from collections.abc import Callable
from dataclasses import dataclass
from tkinter import ttk


@dataclass(frozen=True)
class RuntimeOptions:
    debug_mode_var: tk.BooleanVar
    disable_ssl_strict_var: tk.BooleanVar
    stream_mode_var: tk.BooleanVar
    stream_mode_combo: ttk.Combobox


@dataclass(frozen=True)
class RuntimeOptionsPanelDeps:
    parent: ttk.Frame
    tooltip: Callable[..., None]
    on_debug_mode_toggle: Callable[[], None]


def build_runtime_options_panel(deps: RuntimeOptionsPanelDeps) -> RuntimeOptions:
    # ========== 运行时选项（所有选项在同一行）==========
    options_frame = ttk.Frame(deps.parent)
    options_frame.pack(fill=tk.X, padx=5, pady=2)
    
    debug_mode_var = tk.BooleanVar(value=False)

    debug_mode_check = ttk.Checkbutton(
        options_frame,
        text="开启调试模式",
        variable=debug_mode_var,
        command=deps.on_debug_mode_toggle,
    )
    debug_mode_check.pack(side=tk.LEFT)
    deps.tooltip(
        debug_mode_check,
        "开启后：\n"
        "1) 代理服务器输出更详细的调试日志，便于排查问题；\n"
        "2) 启动代理服务器前会额外检查系统/环境变量的显式代理配置\n并提示其可能绕过 hosts 导流。\n"
        "（默认不做第 2 项检查，仅在调试模式下启用）",
        wraplength=500,
    )
    
    disable_ssl_strict_var = tk.BooleanVar(value=False)
    disable_ssl_strict_check = ttk.Checkbutton(
        options_frame,
        text="关闭SSL严格模式",
        variable=disable_ssl_strict_var,
    )
    disable_ssl_strict_check.pack(side=tk.LEFT, padx=(20, 0))

    # 强制流模式（与其他选项在同一行）
    stream_mode_var = tk.BooleanVar(value=False)
    stream_mode_check = ttk.Checkbutton(
        options_frame,
        text="强制流模式:",
        variable=stream_mode_var,
        command=lambda: stream_mode_combo.config(
            state="readonly" if stream_mode_var.get() else "disabled"
        ),
    )
    stream_mode_check.pack(side=tk.LEFT, padx=(20, 0))
    
    stream_mode_combo = ttk.Combobox(
        options_frame, values=["true", "false"], state="disabled", width=10
    )
    stream_mode_combo.pack(side=tk.LEFT, padx=(5, 0))
    stream_mode_combo.set("true")

    return RuntimeOptions(
        debug_mode_var=debug_mode_var,
        disable_ssl_strict_var=disable_ssl_strict_var,
        stream_mode_var=stream_mode_var,
        stream_mode_combo=stream_mode_combo,
    )
