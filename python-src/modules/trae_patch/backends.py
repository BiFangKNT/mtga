from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .common.types import CompatibilityReport, NativeBackend, RewriterConfigRequest

WINDOWS_REWRITER_MODULE = "modules.trae_patch.windows.sse_open_url_rewriter"


class UnsupportedNativeBackendError(RuntimeError):
    pass


@dataclass(frozen=True)
class WindowsNativeBackend:
    name: str = "windows"
    rewriter_module: str = WINDOWS_REWRITER_MODULE

    def build_compatibility_report(self, module_path: Path) -> CompatibilityReport:
        from .windows.compatibility import build_compatibility_report  # noqa: PLC0415

        return build_compatibility_report(module_path)

    def create_rewriter_config(self, request: RewriterConfigRequest) -> object:
        from .windows.sse_open_url_rewriter import RewriterConfig  # noqa: PLC0415

        return RewriterConfig(
            module_path=request.module_path,
            new_url=request.new_url,
            compatibility_report=request.compatibility_report,
            duration_seconds=request.duration_seconds,
            output_path=request.output_path,
            stop_file=request.stop_file,
            quiet=request.quiet,
        )

    def run_rewriter_config(self, config: object) -> dict[str, Any]:
        from .windows.sse_open_url_rewriter import (  # noqa: PLC0415
            RewriterConfig,
            run_rewriter_config,
        )

        if not isinstance(config, RewriterConfig):
            raise TypeError(f"unexpected Windows rewriter config: {type(config).__name__}")
        return run_rewriter_config(config)


def get_native_backend() -> NativeBackend:
    if sys.platform == "win32":
        return WindowsNativeBackend()
    raise UnsupportedNativeBackendError(
        f"Trae native route does not support platform: {sys.platform}"
    )


__all__ = [
    "UnsupportedNativeBackendError",
    "WINDOWS_REWRITER_MODULE",
    "WindowsNativeBackend",
    "get_native_backend",
]
