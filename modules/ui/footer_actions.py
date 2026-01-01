from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from tkinter import ttk


@dataclass(frozen=True)
class FooterActionsDeps:
    left_frame: ttk.Frame
    start_all: Callable[[], None]


def build_footer_actions(deps: FooterActionsDeps) -> ttk.Button:
    start_button = ttk.Button(
        deps.left_frame,
        text="一键启动全部服务",
        command=deps.start_all,
    )
    # 减小上侧间距，让按钮更靠近标签页
    start_button.grid(row=1, column=0, sticky="ew", padx=5, pady=(5, 0))

    return start_button
