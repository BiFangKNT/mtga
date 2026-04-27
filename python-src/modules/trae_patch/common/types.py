from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol


class CompatibilityStatusLike(Protocol):
    @property
    def value(self) -> str: ...


class CompatibilityReport(Protocol):
    @property
    def status(self) -> CompatibilityStatusLike: ...

    @property
    def reason(self) -> str: ...

    @property
    def dll_path(self) -> str: ...

    @property
    def dll_size(self) -> int | None: ...

    @property
    def dll_sha256(self) -> str | None: ...

    @property
    def pattern_count(self) -> int | None: ...

    @property
    def url_copy_call_rva(self) -> str | None: ...

    @property
    def manifest_error(self) -> str | None: ...

    @property
    def blocked(self) -> bool: ...

    def to_dict(self) -> dict[str, Any]: ...


@dataclass(frozen=True)
class RewriterConfigRequest:
    module_path: Path
    new_url: str
    compatibility_report: dict[str, Any] | None
    duration_seconds: int
    output_path: Path
    stop_file: Path
    quiet: bool


@dataclass(frozen=True)
class NativeProcessInfo:
    pid: int
    name: str
    command: str


@dataclass(frozen=True)
class LaunchPreparationRequest:
    trae_executable: Path
    new_url: str
    user_data_dir: Path
    logs_dir: Path


@dataclass(frozen=True)
class LaunchPreparationResult:
    trae_executable: Path
    requires_runtime_rewriter: bool
    summary: dict[str, Any] | None = None


class NativeBackend(Protocol):
    @property
    def name(self) -> str: ...

    @property
    def rewriter_module(self) -> str: ...

    @property
    def module_display_name(self) -> str: ...

    @property
    def path_prompt_name(self) -> str: ...

    def resolve_trae_executable(self, raw_path: str) -> Path: ...

    def resolve_module_path(self, trae_executable: Path) -> Path: ...

    def build_launch_command(
        self,
        trae_executable: Path,
        *,
        cdp_port: int,
    ) -> tuple[list[str], Path]: ...

    def list_existing_trae_processes(self) -> list[NativeProcessInfo]: ...

    def build_compatibility_report(self, module_path: Path) -> CompatibilityReport: ...

    def prepare_launch(self, request: LaunchPreparationRequest) -> LaunchPreparationResult: ...

    def create_rewriter_config(self, request: RewriterConfigRequest) -> object: ...

    def run_rewriter_config(self, config: object) -> dict[str, Any]: ...


__all__ = [
    "CompatibilityReport",
    "CompatibilityStatusLike",
    "LaunchPreparationRequest",
    "LaunchPreparationResult",
    "NativeBackend",
    "NativeProcessInfo",
    "RewriterConfigRequest",
]
