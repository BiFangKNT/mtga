from __future__ import annotations

import os
import sys
import tkinter as tk
from collections.abc import Callable
from dataclasses import dataclass
from tkinter import font as tkfont
from typing import Literal

from modules.ui.tk_fonts import FontManager, apply_global_font


@dataclass(frozen=True)
class WindowSetupResult:
    font_manager: FontManager
    get_preferred_font: Callable[..., tkfont.Font]


def setup_main_window(
    window: tk.Tk,
    *,
    get_icon_file: Callable[[str], str] | None = None,
) -> WindowSetupResult:
    window.title("MTGA GUI")
    window.geometry("1250x680")  # 减小高度，让布局更紧凑
    window.resizable(False, False)  # 固定窗口大小，不允许调整

    if sys.platform == "darwin":
        try:
            scaling = window.winfo_fpixels("1i") / 72.0
            if scaling > 0:
                window.tk.call("tk", "scaling", scaling)
        except tk.TclError:
            pass

    font_manager = FontManager()

    def get_preferred_font(
        size: int = 10,
        weight: Literal["normal", "bold"] = "normal",
    ) -> tkfont.Font:
        return font_manager.get_preferred_font(size=size, weight=weight)

    default_font = get_preferred_font()
    apply_global_font(root=window, default_font=default_font)

    try:
        if os.name == "nt" and get_icon_file is not None:
            icon_path = get_icon_file("f0bb32_bg-black.ico")
            if os.path.exists(icon_path):
                window.iconbitmap(icon_path)
    except Exception:
        pass

    return WindowSetupResult(
        font_manager=font_manager,
        get_preferred_font=get_preferred_font,
    )
