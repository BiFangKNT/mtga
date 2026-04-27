from __future__ import annotations

import contextlib
import os
import plistlib
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

from .common.types import (
    CompatibilityReport,
    LaunchPreparationRequest,
    LaunchPreparationResult,
    NativeBackend,
    NativeProcessInfo,
    RewriterConfigRequest,
)

WINDOWS_REWRITER_MODULE = "modules.trae_patch.windows.sse_open_url_rewriter"
MACOS_REWRITER_MODULE = "modules.trae_patch.macos.sse_open_url_rewriter"
WINDOWS_AI_AGENT_RELATIVE_PATH = Path("resources/app/modules/ai-agent/ai_agent.dll")
MACOS_AI_AGENT_RELATIVE_PATH = Path("Contents/Resources/app/modules/ai-agent/libai_agent.dylib")
MACOS_CONTENTS_AI_AGENT_RELATIVE_PATH = Path("Resources/app/modules/ai-agent/libai_agent.dylib")
WINDOWS_TRAE_PROCESS_NAME = "trae.exe"
WINDOWS_TASKLIST_MIN_COLUMNS = 2
MACOS_TRAE_APP_SUFFIX = ".app"
MACOS_TRAE_FALLBACK_EXECUTABLE = "Electron"
MACOS_PS_MIN_COLUMNS = 3


class UnsupportedNativeBackendError(RuntimeError):
    pass


def _expand_user_path(raw_path: str) -> Path:
    return Path(os.path.expanduser(os.path.expandvars(raw_path.strip()))).resolve()


@dataclass(frozen=True)
class WindowsNativeBackend:
    name: str = "windows"
    rewriter_module: str = WINDOWS_REWRITER_MODULE
    module_display_name: str = "ai_agent.dll"
    path_prompt_name: str = "Trae.exe"

    def resolve_trae_executable(self, raw_path: str) -> Path:
        return _expand_user_path(raw_path)

    def resolve_module_path(self, trae_executable: Path) -> Path:
        return trae_executable.parent / WINDOWS_AI_AGENT_RELATIVE_PATH

    def build_launch_command(
        self,
        trae_executable: Path,
        *,
        cdp_port: int,
    ) -> tuple[list[str], Path]:
        return [str(trae_executable), f"--remote-debugging-port={cdp_port}"], trae_executable.parent

    def list_existing_trae_processes(self) -> list[NativeProcessInfo]:
        try:
            completed = subprocess.run(
                [
                    "tasklist",
                    "/FI",
                    "IMAGENAME eq Trae.exe",
                    "/FO",
                    "CSV",
                    "/NH",
                ],
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=3,
            )
        except Exception:
            return []

        processes: list[NativeProcessInfo] = []
        for raw_line in completed.stdout.splitlines():
            line = raw_line.strip()
            if not line or "INFO:" in line:
                continue
            columns = [part.strip().strip('"') for part in line.split(",")]
            if (
                len(columns) < WINDOWS_TASKLIST_MIN_COLUMNS
                or columns[0].lower() != WINDOWS_TRAE_PROCESS_NAME
            ):
                continue
            with contextlib.suppress(ValueError):
                pid = int(columns[1])
                processes.append(
                    NativeProcessInfo(
                        pid=pid,
                        name=columns[0],
                        command=columns[0],
                    )
                )
        return sorted(processes, key=lambda item: item.pid)

    def build_compatibility_report(self, module_path: Path) -> CompatibilityReport:
        from .windows.compatibility import build_compatibility_report  # noqa: PLC0415

        return build_compatibility_report(module_path)

    def prepare_launch(self, request: LaunchPreparationRequest) -> LaunchPreparationResult:
        return LaunchPreparationResult(
            trae_executable=request.trae_executable,
            requires_runtime_rewriter=True,
            summary=None,
        )

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


def _find_macos_app_bundle(path: Path) -> Path | None:
    candidates = (path, *path.parents)
    for candidate in candidates:
        if candidate.suffix.lower() == MACOS_TRAE_APP_SUFFIX and candidate.is_dir():
            return candidate
    return None


def _read_macos_bundle_executable(app_path: Path) -> str:
    info_plist = app_path / "Contents" / "Info.plist"
    try:
        raw: object = plistlib.loads(info_plist.read_bytes())
    except Exception:
        return MACOS_TRAE_FALLBACK_EXECUTABLE
    executable = (
        cast("dict[str, object]", raw).get("CFBundleExecutable")
        if isinstance(raw, dict)
        else None
    )
    if isinstance(executable, str) and executable.strip():
        return executable.strip()
    return MACOS_TRAE_FALLBACK_EXECUTABLE


@dataclass(frozen=True)
class MacOSNativeBackend:
    name: str = "macos"
    rewriter_module: str = MACOS_REWRITER_MODULE
    module_display_name: str = "libai_agent.dylib"
    path_prompt_name: str = "Trae.app 或 Trae 可执行文件"

    def resolve_trae_executable(self, raw_path: str) -> Path:
        path = _expand_user_path(raw_path)
        app_path = _find_macos_app_bundle(path)
        if app_path is None:
            return path
        executable_name = _read_macos_bundle_executable(app_path)
        return app_path / "Contents" / "MacOS" / executable_name

    def resolve_module_path(self, trae_executable: Path) -> Path:
        app_path = _find_macos_app_bundle(trae_executable)
        if app_path is not None:
            return app_path / MACOS_AI_AGENT_RELATIVE_PATH
        contents_dir = trae_executable.parent.parent
        return contents_dir / MACOS_CONTENTS_AI_AGENT_RELATIVE_PATH

    def build_launch_command(
        self,
        trae_executable: Path,
        *,
        cdp_port: int,
    ) -> tuple[list[str], Path]:
        app_path = _find_macos_app_bundle(trae_executable)
        cwd = (
            app_path / "Contents" / "Resources" / "app"
            if app_path is not None
            else trae_executable.parent
        )
        return [str(trae_executable), f"--remote-debugging-port={cdp_port}"], cwd

    def list_existing_trae_processes(self) -> list[NativeProcessInfo]:
        try:
            completed = subprocess.run(
                ["ps", "-axo", "pid=,comm=,args="],
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=3,
            )
        except Exception:
            return []

        processes: list[NativeProcessInfo] = []
        for raw_line in completed.stdout.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            parts = line.split(None, 2)
            if len(parts) < MACOS_PS_MIN_COLUMNS:
                continue
            raw_pid, name, command = parts
            command_path = command.split(None, 1)[0]
            if ".app/Contents/MacOS/" not in command_path:
                continue
            if "Trae" not in command_path:
                continue
            with contextlib.suppress(ValueError):
                processes.append(
                    NativeProcessInfo(
                        pid=int(raw_pid),
                        name=Path(name).name,
                        command=command,
                    )
                )
        return sorted(processes, key=lambda item: item.pid)

    def build_compatibility_report(self, module_path: Path) -> CompatibilityReport:
        from .macos.compatibility import build_compatibility_report  # noqa: PLC0415

        return build_compatibility_report(module_path)

    def prepare_launch(self, request: LaunchPreparationRequest) -> LaunchPreparationResult:
        from .macos.offline_patch import prepare_patched_copy  # noqa: PLC0415

        summary = prepare_patched_copy(
            request.trae_executable,
            new_url=request.new_url,
            user_data_dir=request.user_data_dir,
            logs_dir=request.logs_dir,
        )
        prepared_executable = Path(str(summary.get("prepared_executable") or "")).resolve()
        if not prepared_executable.is_file():
            raise RuntimeError(f"patched copy 可执行文件不存在: {prepared_executable}")
        return LaunchPreparationResult(
            trae_executable=prepared_executable,
            requires_runtime_rewriter=False,
            summary=summary,
        )

    def create_rewriter_config(self, request: RewriterConfigRequest) -> object:
        from .macos.sse_open_url_rewriter import RewriterConfig  # noqa: PLC0415

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
        from .macos.sse_open_url_rewriter import (  # noqa: PLC0415
            RewriterConfig,
            run_rewriter_config,
        )

        if not isinstance(config, RewriterConfig):
            raise TypeError(f"unexpected macOS rewriter config: {type(config).__name__}")
        return run_rewriter_config(config)


def get_native_backend() -> NativeBackend:
    if sys.platform == "win32":
        return WindowsNativeBackend()
    if sys.platform == "darwin":
        return MacOSNativeBackend()
    raise UnsupportedNativeBackendError(
        f"Trae native route does not support platform: {sys.platform}"
    )


__all__ = [
    "UnsupportedNativeBackendError",
    "MACOS_REWRITER_MODULE",
    "MacOSNativeBackend",
    "WINDOWS_REWRITER_MODULE",
    "WindowsNativeBackend",
    "get_native_backend",
]
