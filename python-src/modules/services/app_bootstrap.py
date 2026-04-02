from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from modules.services import app_metadata, app_version, bootstrap, logging_service, startup_context


@dataclass(frozen=True)
class AppBootstrapResult:
    app_context: bootstrap.AppContext
    app_metadata: app_metadata.AppMetadata
    app_version: str
    startup_context: startup_context.StartupContext
    error_log_path: str
    log_error: Callable[..., None]


def build_app_bootstrap(
    *, project_root: Path, get_log_path: Callable[[str], str]
) -> AppBootstrapResult:
    app_context = bootstrap.build_app_context()
    metadata = app_metadata.DEFAULT_METADATA
    error_log_path = logging_service.setup_error_logging(
        get_log_path=get_log_path,
        error_log_filename=metadata.error_log_filename,
    )
    log_error = logging_service.log_error
    logging_service.install_global_exception_hook(log_error=log_error)
    startup = startup_context.build_startup_context()
    version = app_version.resolve_app_version(project_root=project_root)
    return AppBootstrapResult(
        app_context=app_context,
        app_metadata=metadata,
        app_version=version,
        startup_context=startup,
        error_log_path=error_log_path,
        log_error=log_error,
    )
