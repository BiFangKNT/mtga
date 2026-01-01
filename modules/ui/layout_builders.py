from __future__ import annotations

import tkinter as tk
from collections.abc import Callable
from dataclasses import dataclass
from tkinter import scrolledtext, ttk
from typing import Any

from modules.ui.ui_helpers import build_text_logger


@dataclass(frozen=True)
class WindowLayout:
    main_frame: ttk.Frame
    main_paned: ttk.PanedWindow
    left_frame: ttk.Frame
    left_content: ttk.Frame
    right_frame: ttk.Frame
    log_text: scrolledtext.ScrolledText
    log: Callable[[str], None]


def build_main_layout(
    window: tk.Tk,
    *,
    get_preferred_font: Callable[..., Any] | None = None,
) -> WindowLayout:
    main_frame = ttk.Frame(window, padding=15)  # 增加内边距
    main_frame.pack(fill=tk.BOTH, expand=True)

    # ========== 标题区域 ==========
    title_frame = ttk.Frame(main_frame)
    title_frame.pack(fill=tk.X, pady=(0, 15))  # 增加底部间距
    
    title_font = (
        get_preferred_font(size=18, weight="bold")  # 增加字体大小
        if get_preferred_font is not None
        else ("TkDefaultFont", 18, "bold")
    )
    title_label = ttk.Label(
        title_frame,
        text="🚀 MTGA - 代理服务器管理工具",  # 添加图标
        font=title_font,
    )
    title_label.pack(side=tk.LEFT)
    
    # 版本信息（可选）
    version_font = (
        get_preferred_font(size=9)
        if get_preferred_font is not None
        else ("TkDefaultFont", 9)
    )
    version_label = ttk.Label(
        title_frame,
        text="v1.2.0",
        font=version_font,
        foreground="gray",
    )
    version_label.pack(side=tk.LEFT, padx=(10, 0))

    # 分隔线
    separator = ttk.Separator(main_frame, orient=tk.HORIZONTAL)
    separator.pack(fill=tk.X, pady=(0, 15))

    main_paned = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
    main_paned.pack(fill=tk.BOTH, expand=True)

    # ========== 左侧面板（配置区域）==========
    left_frame = ttk.Frame(main_paned)
    main_paned.add(left_frame, weight=1)

    left_frame.grid_rowconfigure(0, weight=1)
    left_frame.grid_columnconfigure(0, weight=1)
    left_content = ttk.Frame(left_frame, padding=5)  # 添加内边距
    left_content.grid(row=0, column=0, sticky="nsew")

    # ========== 右侧面板（日志区域）==========
    right_frame = ttk.Frame(main_paned)
    main_paned.add(right_frame, weight=1)

    log_frame = ttk.LabelFrame(right_frame, text="📜 日志输出", padding=5)  # 添加图标和内边距
    log_frame.pack(fill=tk.BOTH, expand=True)
    
    log_text = scrolledtext.ScrolledText(
        log_frame,
        height=10,
        width=1,
        wrap=tk.WORD,  # 按单词换行
        font=("Consolas", 9) if get_preferred_font is None else get_preferred_font(size=9),  # 使用等宽字体
    )
    log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    log = build_text_logger(log_text)

    return WindowLayout(
        main_frame=main_frame,
        main_paned=main_paned,
        left_frame=left_frame,
        left_content=left_content,
        right_frame=right_frame,
        log_text=log_text,
        log=log,
    )


def init_paned_layout(main_paned: ttk.PanedWindow, main_frame: ttk.Frame, window: tk.Tk) -> None:
    first_layout_done = {"value": False}

    def on_main_paned_configure(_event) -> None:
        if first_layout_done["value"]:
            return
        window.update_idletasks()
        total_width = main_paned.winfo_width() or main_frame.winfo_width() or window.winfo_width()
        if total_width > 0:
            main_paned.sashpos(0, total_width // 2)
            first_layout_done["value"] = True
            main_paned.unbind("<Configure>")

    main_paned.bind("<Configure>", on_main_paned_configure)
