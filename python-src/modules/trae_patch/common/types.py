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


class NativeBackend(Protocol):
    @property
    def name(self) -> str: ...

    @property
    def rewriter_module(self) -> str: ...

    def build_compatibility_report(self, module_path: Path) -> CompatibilityReport: ...

    def create_rewriter_config(self, request: RewriterConfigRequest) -> object: ...

    def run_rewriter_config(self, config: object) -> dict[str, Any]: ...


__all__ = [
    "CompatibilityReport",
    "CompatibilityStatusLike",
    "NativeBackend",
    "RewriterConfigRequest",
]
