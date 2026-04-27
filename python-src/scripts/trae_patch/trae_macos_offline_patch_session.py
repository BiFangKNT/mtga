from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import shutil
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

PYTHON_SRC_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(PYTHON_SRC_DIR))

from modules.trae_patch.backends import MacOSNativeBackend  # noqa: E402
from modules.trae_patch.macos.compatibility import (  # noqa: E402
    CHAT_COMPLETIONS_MARKER,
    DEFAULT_OLD_URL,
    build_compatibility_report,
    parse_macho_layout,
)

DEFAULT_HOST = "127.0.0.1"
DEFAULT_LOOPBACK_PORT = 18083
DEFAULT_CDP_PORT = 9330
DEFAULT_CDP_WAIT_SECONDS = 20
DEFAULT_LOOPBACK_WAIT_SECONDS = 20
DEFAULT_LOOPBACK_HIT_WAIT_SECONDS = 20
DEFAULT_VERDICT_WAIT_SECONDS = 6
DEFAULT_WAIT_AFTER_SEND_SECONDS = 0.5
DEFAULT_TARGET_URL_SUBSTRING = "workbench/workbench.html"
DEFAULT_TARGET_TITLE_SUBSTRING = ""
DEFAULT_CDP_MODE = "current"
DEFAULT_CDP_AGENT_NAME = "current"
DEFAULT_TEST_MESSAGE = "请只回复：mtga-macos-offline-patch-smoke"
DEFAULT_MARKER_WINDOW_BYTES = 48
DEFAULT_ARTIFACT_ROOT = Path("python-src/artifacts/trae_macos_offline_patch_session")
DEFAULT_CLONE_ROOT = Path("/tmp/mtga-trae-offline-patch")
DEFAULT_CLONE_APP = DEFAULT_CLONE_ROOT / "Trae-MTGA.app"
ASCII_PRINTABLE_MIN = 32
ASCII_PRINTABLE_MAX = 127
MACHO_MAGIC_HEADERS = {
    b"\xca\xfe\xba\xbe",
    b"\xbe\xba\xfe\xca",
    b"\xca\xfe\xba\xbf",
    b"\xbf\xba\xfe\xca",
    b"\xfe\xed\xfa\xce",
    b"\xce\xfa\xed\xfe",
    b"\xfe\xed\xfa\xcf",
    b"\xcf\xfa\xed\xfe",
}


def _script_path(name: str) -> Path:
    return Path(__file__).with_name(name)


def _project_python() -> str:
    candidates = [
        PYTHON_SRC_DIR / ".venv" / "bin" / "python",
        PYTHON_SRC_DIR / ".venv" / "Scripts" / "python.exe",
    ]
    for candidate in candidates:
        if candidate.is_file():
            return str(candidate)
    return sys.executable


def _now_stamp() -> str:
    return time.strftime("%Y%m%dT%H%M%S")


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fp:
        while True:
            chunk = fp.read(1024 * 1024)
            if not chunk:
                return digest.hexdigest()
            digest.update(chunk)


def _normalize_hex(value: str) -> bytes:
    normalized = "".join(value.split()).replace("0x", "")
    if len(normalized) % 2 != 0:
        raise ValueError("hex pattern 长度必须是偶数")
    return bytes.fromhex(normalized)


def _find_app_bundle(path: Path) -> Path | None:
    candidates = (path, *path.parents)
    for candidate in candidates:
        if candidate.suffix.lower() == ".app" and candidate.is_dir():
            return candidate
    return None


def _ascii_preview(data: bytes) -> str:
    return "".join(
        chr(byte) if ASCII_PRINTABLE_MIN <= byte < ASCII_PRINTABLE_MAX else "."
        for byte in data
    )


def _relative_to(path: Path, root: Path) -> str:
    with contextlib.suppress(ValueError):
        return str(path.relative_to(root))
    return str(path)


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError(f"JSON 根节点必须是对象: {path}")
    return payload


def _resolve_paths(trae_path: str) -> dict[str, Path]:
    backend = MacOSNativeBackend()
    executable = backend.resolve_trae_executable(trae_path)
    if not executable.is_file():
        raise RuntimeError(f"Trae 路径无效: {executable}")
    app_bundle = _find_app_bundle(executable)
    if app_bundle is None:
        raise RuntimeError(f"无法从路径推导 Trae.app: {executable}")
    module_path = backend.resolve_module_path(executable)
    if not module_path.is_file():
        raise RuntimeError(f"未找到 libai_agent.dylib: {module_path}")
    return {
        "app_bundle": app_bundle,
        "executable": executable,
        "module_path": module_path,
    }


def _marker_contexts(
    module_path: Path,
    *,
    marker_window_bytes: int,
) -> list[dict[str, Any]]:
    data = module_path.read_bytes()
    layout = parse_macho_layout(data)
    offsets: list[int] = []
    start = 0
    while True:
        offset = data.find(CHAT_COMPLETIONS_MARKER, start)
        if offset < 0:
            break
        offsets.append(offset)
        start = offset + 1

    contexts: list[dict[str, Any]] = []
    for offset in offsets[:20]:
        window_start = max(0, offset - marker_window_bytes)
        window_end = min(len(data), offset + len(CHAT_COMPLETIONS_MARKER) + marker_window_bytes)
        window = data[window_start:window_end]
        contexts.append(
            {
                "file_offset": hex(offset),
                "location": layout.locate_file_offset(offset),
                "window_start": hex(window_start),
                "window_end": hex(window_end),
                "window_hex": window.hex(" "),
                "window_ascii": _ascii_preview(window),
            }
        )
    return contexts


def _run_command(
    command: list[str],
    *,
    timeout: float | None = None,
    cwd: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        cwd=str(cwd) if cwd is not None else None,
    )


def _remove_path(path: Path) -> None:
    if not path.exists():
        return
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
        return
    path.unlink()


def _clone_app_bundle(source: Path, destination: Path) -> dict[str, Any]:
    destination.parent.mkdir(parents=True, exist_ok=True)
    _remove_path(destination)

    clone_command = ["/bin/cp", "-cR", str(source), str(destination)]
    completed = _run_command(clone_command, timeout=120)
    mode = "cp_clone"
    if completed.returncode != 0:
        shutil.copytree(source, destination, symlinks=True)
        mode = "copytree_fallback"
    return {
        "mode": mode,
        "source": str(source),
        "destination": str(destination),
        "cp_returncode": completed.returncode,
        "cp_stderr_tail": completed.stderr[-1000:].strip(),
    }


def _reuse_existing_app_bundle(source: Path, destination: Path) -> dict[str, Any]:
    if not destination.is_dir():
        raise RuntimeError(f"--reuse-clone 指定的副本不存在: {destination}")
    return {
        "mode": "reuse_existing",
        "source": str(source),
        "destination": str(destination),
        "cp_returncode": None,
        "cp_stderr_tail": "",
    }


def _read_recipe(path: Path) -> dict[str, Any]:
    recipe = _load_json(path)
    replacements = recipe.get("replacements")
    if not isinstance(replacements, list):
        raise RuntimeError("recipe.replacements 必须是数组")
    return recipe


def _generate_url_patch_recipe(
    *,
    trae_path: str,
    artifact_root: Path,
) -> dict[str, Any]:
    generated_root = artifact_root / "generated_url_patch_recipe"
    report_root = artifact_root / "native_symbol_report"
    command = [
        _project_python(),
        str(_script_path("trae_macos_url_patch_recipe.py")),
        "--trae-path",
        trae_path,
        "--artifact-root",
        str(generated_root),
        "--report-artifact-root",
        str(report_root),
        "--json",
    ]
    completed = _run_command(command, timeout=120)
    if completed.returncode != 0:
        raise RuntimeError(
            completed.stderr.strip() or completed.stdout.strip() or "自动生成 recipe 失败"
        )
    payload = json.loads(completed.stdout or "{}")
    if not isinstance(payload, dict):
        raise RuntimeError("自动生成 recipe 返回格式无效")
    recipe_path = payload.get("recipe_path")
    if not isinstance(recipe_path, str) or not recipe_path.strip():
        raise RuntimeError("自动生成 recipe 未返回 recipe_path")
    return {
        "recipe_path": recipe_path,
        "report_root": str(report_root),
        "generated_root": str(generated_root),
        "payload": payload,
    }


def _replace_all(data: bytearray, needle: bytes, replacement: bytes) -> list[int]:
    offsets: list[int] = []
    start = 0
    while True:
        offset = bytes(data).find(needle, start)
        if offset < 0:
            return offsets
        data[offset : offset + len(needle)] = replacement
        offsets.append(offset)
        start = offset + len(replacement)


def _find_exact_offsets(data: bytes, needle: bytes) -> list[int]:
    offsets: list[int] = []
    start = 0
    while True:
        offset = data.find(needle, start)
        if offset < 0:
            return offsets
        offsets.append(offset)
        start = offset + len(needle)


def _apply_replacements(  # noqa: PLR0912, PLR0915
    app_bundle: Path,
    recipe: dict[str, Any],
) -> list[dict[str, Any]]:
    replacements = recipe.get("replacements")
    if not isinstance(replacements, list):
        raise RuntimeError("recipe.replacements 必须是数组")

    records: list[dict[str, Any]] = []
    for index, raw_item in enumerate(replacements, start=1):
        if not isinstance(raw_item, dict):
            raise RuntimeError(f"replacement[{index}] 必须是对象")
        item = raw_item
        relative_path = item.get("path")
        if not isinstance(relative_path, str) or not relative_path.strip():
            raise RuntimeError(f"replacement[{index}].path 缺失")
        target_path = app_bundle / relative_path
        if not target_path.is_file():
            raise RuntimeError(f"replacement[{index}] 目标文件不存在: {target_path}")

        mode = str(item.get("mode") or "").strip()
        if not mode:
            raise RuntimeError(f"replacement[{index}].mode 缺失")

        original = target_path.read_bytes()
        patched = bytearray(original)
        before_sha256 = hashlib.sha256(original).hexdigest()

        replaced_offsets: list[int] = []
        already_patched_offsets: list[int] = []
        if mode == "find_hex":
            needle = _normalize_hex(str(item.get("find") or ""))
            replacement = _normalize_hex(str(item.get("replace") or ""))
            if len(needle) != len(replacement):
                raise RuntimeError(f"replacement[{index}] find_hex 只支持等长替换")
            replaced_offsets = _replace_all(patched, needle, replacement)
            expect_count = item.get("expect_count")
            if expect_count is not None:
                expected_count = int(expect_count)
                if len(replaced_offsets) != expected_count:
                    already_patched_offsets = _find_exact_offsets(original, replacement)
                    if len(replaced_offsets) + len(already_patched_offsets) != expected_count:
                        raise RuntimeError(
                            "replacement["
                            f"{index}] 命中次数不符: expect={expected_count} "
                            f"actual={len(replaced_offsets)} "
                            f"already_patched={len(already_patched_offsets)}"
                        )
        elif mode == "find_text":
            needle_text = str(item.get("find") or "")
            replacement_text = str(item.get("replace") or "")
            needle = needle_text.encode("utf-8")
            replacement = replacement_text.encode("utf-8")
            if len(needle) != len(replacement):
                raise RuntimeError(f"replacement[{index}] find_text 只支持等长替换")
            replaced_offsets = _replace_all(patched, needle, replacement)
            expect_count = item.get("expect_count")
            if expect_count is not None:
                expected_count = int(expect_count)
                if len(replaced_offsets) != expected_count:
                    already_patched_offsets = _find_exact_offsets(original, replacement)
                    if len(replaced_offsets) + len(already_patched_offsets) != expected_count:
                        raise RuntimeError(
                            "replacement["
                            f"{index}] 命中次数不符: expect={expected_count} "
                            f"actual={len(replaced_offsets)} "
                            f"already_patched={len(already_patched_offsets)}"
                        )
        elif mode == "offset_hex":
            raw_offset = item.get("offset")
            if raw_offset is None:
                raise RuntimeError(f"replacement[{index}].offset 缺失")
            offset = int(raw_offset, 0) if isinstance(raw_offset, str) else int(raw_offset)
            replacement = _normalize_hex(str(item.get("replace") or ""))
            expected = item.get("expected")
            if expected is not None:
                expected_bytes = _normalize_hex(str(expected))
                actual = bytes(patched[offset : offset + len(expected_bytes)])
                if actual == replacement:
                    already_patched_offsets = [offset]
                elif actual != expected_bytes:
                    raise RuntimeError(
                        f"replacement[{index}] 预期字节不匹配: "
                        f"offset={hex(offset)} actual={actual.hex(' ')} "
                        f"expected={expected_bytes.hex(' ')}"
                    )
            if not already_patched_offsets:
                patched[offset : offset + len(replacement)] = replacement
                replaced_offsets = [offset]
        else:
            raise RuntimeError(f"replacement[{index}] 不支持的 mode: {mode}")

        if bytes(patched) != original:
            target_path.write_bytes(bytes(patched))

        after_sha256 = _sha256_file(target_path)
        records.append(
            {
                "index": index,
                "mode": mode,
                "path": relative_path,
                "replaced_offsets": [hex(offset) for offset in replaced_offsets],
                "already_patched_offsets": [hex(offset) for offset in already_patched_offsets],
                "replacement_count": len(replaced_offsets),
                "before_sha256": before_sha256,
                "after_sha256": after_sha256,
            }
        )
    return records


def _pick_codesign_identity() -> str:
    security_path = shutil.which("security")
    if not security_path:
        return "-"
    completed = _run_command(
        [security_path, "find-identity", "-v", "-p", "codesigning"],
        timeout=15,
    )
    lines = [line.strip() for line in completed.stdout.splitlines() if '"' in line]
    if not lines:
        return "-"

    identities: list[str] = []
    for line in lines:
        start = line.find('"')
        end = line.rfind('"')
        if start < 0 or end <= start:
            continue
        identities.append(line[start + 1 : end].strip())
    if not identities:
        return "-"

    for identity in identities:
        if identity.startswith("Apple Development:"):
            return identity
    return identities[0]


def _extract_entitlements(codesign_path: str, target: Path) -> bytes | None:
    completed = _run_command(
        [codesign_path, "-d", "--entitlements", ":-", str(target)],
        timeout=30,
    )
    text = ""
    if completed.stdout:
        text += completed.stdout
    if completed.stderr:
        if text:
            text += "\n"
        text += completed.stderr
    start = text.find("<?xml")
    if start < 0:
        start = text.find("<plist")
    if start < 0:
        return None
    end = text.find("</plist>", start)
    if end < 0:
        return None
    payload = text[start : end + len("</plist>")].encode("utf-8")
    return payload


def _is_macho_file(path: Path) -> bool:
    if not path.is_file() or path.is_symlink():
        return False
    with path.open("rb") as fp:
        return fp.read(4) in MACHO_MAGIC_HEADERS


def _iter_macho_leaf_files(app_bundle: Path) -> list[Path]:
    files: list[Path] = []
    for path in app_bundle.rglob("*"):
        if "_CodeSignature" in path.parts or path.name.endswith(".cstemp"):
            continue
        if path.suffix.lower() not in {".dylib", ".so", ".node"}:
            continue
        if _is_macho_file(path):
            files.append(path)
    return sorted(files, key=lambda item: (len(item.parts), str(item)), reverse=True)


def _write_entitlements_file(
    temp_dir: Path,
    *,
    key: str,
    payload: bytes | None,
) -> Path | None:
    if payload is None:
        return None
    path = temp_dir / f"{key}.entitlements.plist"
    path.write_bytes(payload)
    return path


def _remove_codesign_temp_files(root: Path) -> None:
    for path in root.rglob("*.cstemp"):
        if path.is_file() or path.is_symlink():
            path.unlink(missing_ok=True)


def _sign_code_object(  # noqa: PLR0913
    codesign_path: str,
    target: Path,
    *,
    identity: str,
    deep: bool = False,
    runtime: bool = False,
    entitlements_path: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    command = [
        codesign_path,
        "--force",
        "--sign",
        identity,
        "--timestamp=none",
        "--preserve-metadata=identifier",
    ]
    if deep:
        command.append("--deep")
    if runtime:
        command.extend(["--options", "runtime"])
    if entitlements_path is not None:
        command.extend(["--entitlements", str(entitlements_path)])
    command.append(str(target))
    return _run_command(command, timeout=180)


def _codesign_app_bundle(app_bundle: Path) -> dict[str, Any]:
    xattr_path = shutil.which("xattr")
    if xattr_path:
        _run_command([xattr_path, "-cr", str(app_bundle)], timeout=30)

    codesign_path = shutil.which("codesign")
    if not codesign_path:
        raise RuntimeError("未找到 codesign")
    identity = _pick_codesign_identity()

    framework_dirs = sorted(
        [path for path in app_bundle.rglob("*.framework") if path.is_dir()],
        key=lambda item: (len(item.parts), str(item)),
        reverse=True,
    )
    helper_app_dirs = sorted(
        [path for path in app_bundle.rglob("*.app") if path.is_dir() and path != app_bundle],
        key=lambda item: (len(item.parts), str(item)),
        reverse=True,
    )
    macho_leaf_files = _iter_macho_leaf_files(app_bundle)

    sign_logs: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="mtga-trae-codesign-") as temp_dir_raw:
        temp_dir = Path(temp_dir_raw)
        entitlements_map: dict[Path, Path | None] = {
            app_bundle: _write_entitlements_file(
                temp_dir,
                key="main_app",
                payload=_extract_entitlements(codesign_path, app_bundle),
            )
        }
        for index, helper_path in enumerate(helper_app_dirs, start=1):
            entitlements_map[helper_path] = _write_entitlements_file(
                temp_dir,
                key=f"helper_{index}",
                payload=_extract_entitlements(codesign_path, helper_path),
            )

        for target in macho_leaf_files:
            completed = _sign_code_object(
                codesign_path,
                target,
                identity=identity,
                runtime=True,
            )
            sign_logs.append(
                {
                    "path": str(target),
                    "kind": "macho_leaf",
                    "returncode": completed.returncode,
                    "stderr_tail": completed.stderr[-400:].strip(),
                    "stdout_tail": completed.stdout[-400:].strip(),
                }
            )
            if completed.returncode != 0:
                raise RuntimeError(
                    "codesign leaf 失败: "
                    f"{target} :: {completed.stderr.strip() or completed.stdout.strip()}"
                )

        for target in framework_dirs:
            _remove_codesign_temp_files(target)
            completed = _sign_code_object(
                codesign_path,
                target,
                identity=identity,
                deep=True,
                runtime=True,
            )
            sign_logs.append(
                {
                    "path": str(target),
                    "kind": "framework",
                    "returncode": completed.returncode,
                    "stderr_tail": completed.stderr[-400:].strip(),
                    "stdout_tail": completed.stdout[-400:].strip(),
                }
            )
            if completed.returncode != 0:
                raise RuntimeError(
                    "codesign framework 失败: "
                    f"{target} :: {completed.stderr.strip() or completed.stdout.strip()}"
                )

        for target in helper_app_dirs:
            _remove_codesign_temp_files(target)
            completed = _sign_code_object(
                codesign_path,
                target,
                identity=identity,
                deep=True,
                runtime=True,
                entitlements_path=entitlements_map.get(target),
            )
            sign_logs.append(
                {
                    "path": str(target),
                    "kind": "helper_app",
                    "returncode": completed.returncode,
                    "stderr_tail": completed.stderr[-400:].strip(),
                    "stdout_tail": completed.stdout[-400:].strip(),
                }
            )
            if completed.returncode != 0:
                raise RuntimeError(
                    "codesign helper 失败: "
                    f"{target} :: {completed.stderr.strip() or completed.stdout.strip()}"
                )

        _remove_codesign_temp_files(app_bundle)
        sign = _sign_code_object(
            codesign_path,
            app_bundle,
            identity=identity,
            runtime=True,
            entitlements_path=entitlements_map.get(app_bundle),
        )
        sign_logs.append(
            {
                "path": str(app_bundle),
                "kind": "main_app",
                "returncode": sign.returncode,
                "stderr_tail": sign.stderr[-400:].strip(),
                "stdout_tail": sign.stdout[-400:].strip(),
            }
        )
        if sign.returncode != 0:
            raise RuntimeError(f"codesign 失败: {sign.stderr.strip() or sign.stdout.strip()}")

    verify = _run_command(
        [codesign_path, "--verify", "--deep", "--strict", "--verbose=4", str(app_bundle)],
        timeout=120,
    )
    if verify.returncode != 0:
        raise RuntimeError(
            "codesign verify 失败: "
            f"{verify.stderr.strip() or verify.stdout.strip()}"
        )

    return {
        "identity": identity,
        "macho_leaf_count": len(macho_leaf_files),
        "framework_count": len(framework_dirs),
        "helper_app_count": len(helper_app_dirs),
        "sign_stdout_tail": sign.stdout[-1000:].strip(),
        "sign_stderr_tail": sign.stderr[-1000:].strip(),
        "verify_stdout_tail": verify.stdout[-1000:].strip(),
        "verify_stderr_tail": verify.stderr[-1000:].strip(),
        "sign_log_tail": sign_logs[-20:],
    }


def _is_port_open(host: str, port: int) -> bool:
    with contextlib.suppress(OSError), socket.create_connection((host, port), timeout=0.5):
        return True
    return False


def _wait_port(host: str, port: int, timeout_seconds: float) -> bool:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        if _is_port_open(host, port):
            return True
        time.sleep(0.2)
    return _is_port_open(host, port)


def _start_loopback(  # noqa: PLR0913
    *,
    host: str,
    port: int,
    current_config_index: int | None,
    debug_mode: bool,
    disable_ssl_strict_mode: bool,
    log_path: Path,
) -> tuple[subprocess.Popen[bytes] | None, Any | None]:
    if _is_port_open(host, port):
        return None, None

    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_fp = log_path.open("w", encoding="utf-8", errors="replace")
    command = [
        _project_python(),
        "-u",
        str(_script_path("trae_local_model_loopback.py")),
        "--host",
        host,
        "--port",
        str(port),
        "--json",
    ]
    if current_config_index is not None:
        command.extend(["--current-config-index", str(current_config_index)])
    if debug_mode:
        command.append("--debug-mode")
    if disable_ssl_strict_mode:
        command.append("--disable-ssl-strict-mode")

    process = subprocess.Popen(command, stdout=log_fp, stderr=log_fp)
    if not _wait_port(host, port, DEFAULT_LOOPBACK_WAIT_SECONDS):
        process.terminate()
        with contextlib.suppress(subprocess.TimeoutExpired):
            process.wait(timeout=3)
        log_fp.close()
        raise RuntimeError(f"loopback 未在 {DEFAULT_LOOPBACK_WAIT_SECONDS}s 内就绪: {log_path}")
    return process, log_fp


def _stop_process(process: subprocess.Popen[bytes] | None) -> None:
    if process is None or process.poll() is not None:
        return
    process.terminate()
    with contextlib.suppress(subprocess.TimeoutExpired):
        process.wait(timeout=5)
    if process.poll() is None:
        process.kill()
        with contextlib.suppress(subprocess.TimeoutExpired):
            process.wait(timeout=3)


def _launch_trae(executable: Path, *, cdp_port: int) -> subprocess.Popen[bytes]:
    backend = MacOSNativeBackend()
    command, cwd = backend.build_launch_command(executable, cdp_port=cdp_port)
    return subprocess.Popen(
        command,
        cwd=str(cwd),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def _run_cdp_send_chat(  # noqa: PLR0913
    *,
    host: str,
    port: int,
    message: str,
    target_url_substring: str,
    target_title_substring: str,
    target_wait_seconds: float,
    wait_after_send_seconds: float,
    mode: str,
    agent_name: str,
    log_path: Path,
) -> dict[str, Any]:
    command = [
        _project_python(),
        str(_script_path("trae_cdp_send_chat.py")),
        "--host",
        host,
        "--port",
        str(port),
        "--message",
        message,
        "--target-url-substring",
        target_url_substring,
        "--target-title-substring",
        target_title_substring,
        "--target-wait-seconds",
        str(target_wait_seconds),
        "--wait-after-send-seconds",
        str(wait_after_send_seconds),
        "--mode",
        mode,
        "--agent-name",
        agent_name,
        "--json",
    ]
    timeout_seconds = max(45.0, target_wait_seconds + wait_after_send_seconds + 25.0)
    try:
        completed = _run_command(command, timeout=timeout_seconds)
    except subprocess.TimeoutExpired as exc:
        output_text = ""
        if exc.stdout:
            output_text += exc.stdout
        if exc.stdout and exc.stderr:
            output_text += "\n"
        if exc.stderr:
            output_text += exc.stderr
        if output_text:
            output_text += "\n"
        output_text += (
            "error: CDP 发消息超时 "
            f"(timeout={timeout_seconds}s, target_wait={target_wait_seconds}s)"
        )
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.write_text(output_text, encoding="utf-8")
        raise RuntimeError(
            "CDP 发消息超时: "
            f"timeout={timeout_seconds}s "
            f"target_wait={target_wait_seconds}s "
            f"log={log_path}"
        ) from exc
    output_text = completed.stdout
    if completed.stdout and completed.stderr:
        output_text += "\n"
    output_text += completed.stderr
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(output_text, encoding="utf-8")
    if completed.returncode != 0:
        raise RuntimeError(
            completed.stderr.strip() or completed.stdout.strip() or "CDP 发消息失败"
        )
    payload = json.loads(completed.stdout or "{}")
    if not isinstance(payload, dict):
        raise RuntimeError("CDP 返回格式无效")
    return payload


def _wait_loopback_hit(log_path: Path, *, timeout_seconds: float) -> dict[str, Any] | None:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        if log_path.exists():
            lines = log_path.read_text(encoding="utf-8", errors="replace").splitlines()
            hits = [
                line
                for line in lines
                if "POST /v1/chat/completions" in line
                or '"/v1/chat/completions HTTP/' in line
            ]
            if hits:
                return {
                    "matched": True,
                    "line_count": len(hits),
                    "last_line": hits[-1],
                }
        time.sleep(0.2)
    return None


def _run_latest_verdict(
    *,
    wait_seconds: float,
    log_path: Path,
) -> dict[str, Any] | None:
    if wait_seconds > 0:
        time.sleep(wait_seconds)
    command = [
        _project_python(),
        str(_script_path("trae_ai_agent_latest_verdict.py")),
        "--json",
    ]
    completed = _run_command(command, timeout=20)
    output_text = completed.stdout
    if completed.stdout and completed.stderr:
        output_text += "\n"
    output_text += completed.stderr
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(output_text, encoding="utf-8")
    if completed.returncode != 0:
        return {
            "error": (
                completed.stderr.strip()
                or completed.stdout.strip()
                or "latest verdict failed"
            ),
        }
    payload = json.loads(completed.stdout or "{}")
    return payload if isinstance(payload, dict) else None


def _summary_paths(root: Path) -> dict[str, Path]:
    return {
        "summary": root / "session.summary.json",
        "loopback_log": root / "loopback.log",
        "cdp_log": root / "cdp_send_chat.log",
        "verdict_log": root / "latest_verdict.log",
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="macOS 离线 patch + clone + launch + CDP smoke 自动化会话脚本。"
    )
    parser.add_argument("--trae-path", required=True, help="官方 Trae.app 路径")
    parser.add_argument("--artifact-root", type=Path, default=DEFAULT_ARTIFACT_ROOT)
    parser.add_argument("--clone-app", type=Path, default=DEFAULT_CLONE_APP)
    parser.add_argument("--recipe", type=Path, help="离线 patch recipe JSON")
    parser.add_argument(
        "--auto-url-patch-recipe",
        action="store_true",
        help="自动生成 macOS native URL override recipe 并应用到 clone 副本",
    )
    parser.add_argument(
        "--skip-clone",
        action="store_true",
        help="直接使用官方 Trae，不复制副本",
    )
    parser.add_argument(
        "--reuse-clone",
        action="store_true",
        help="复用现有 clone 副本；适合固定副本反复 patch/smoke，避免重新复制",
    )
    parser.add_argument("--skip-sign", action="store_true", help="跳过副本 codesign")
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="准备后自动启动 loopback/Trae/CDP smoke",
    )
    parser.add_argument("--keep-running", action="store_true", help="smoke 后保留 Trae 运行")
    parser.add_argument("--loopback-host", default=DEFAULT_HOST)
    parser.add_argument("--loopback-port", type=int, default=DEFAULT_LOOPBACK_PORT)
    parser.add_argument("--cdp-host", default=DEFAULT_HOST)
    parser.add_argument("--cdp-port", type=int, default=DEFAULT_CDP_PORT)
    parser.add_argument(
        "--cdp-wait-seconds",
        type=float,
        default=DEFAULT_CDP_WAIT_SECONDS,
    )
    parser.add_argument(
        "--loopback-hit-wait-seconds",
        type=float,
        default=DEFAULT_LOOPBACK_HIT_WAIT_SECONDS,
    )
    parser.add_argument(
        "--verdict-wait-seconds",
        type=float,
        default=DEFAULT_VERDICT_WAIT_SECONDS,
    )
    parser.add_argument("--current-config-index", type=int)
    parser.add_argument("--debug-mode", action="store_true")
    parser.add_argument("--disable-ssl-strict-mode", action="store_true")
    parser.add_argument("--message", default=DEFAULT_TEST_MESSAGE)
    parser.add_argument("--target-url-substring", default=DEFAULT_TARGET_URL_SUBSTRING)
    parser.add_argument("--target-title-substring", default=DEFAULT_TARGET_TITLE_SUBSTRING)
    parser.add_argument(
        "--cdp-mode",
        choices=("ide", "solo", "current"),
        default=DEFAULT_CDP_MODE,
        help="CDP 发消息前优先切换的模式；主线默认保持 current",
    )
    parser.add_argument(
        "--cdp-agent-name",
        default=DEFAULT_CDP_AGENT_NAME,
        help="CDP 发消息前要求的已选 agent；传 current 跳过校验",
    )
    parser.add_argument(
        "--wait-after-send-seconds",
        type=float,
        default=DEFAULT_WAIT_AFTER_SEND_SECONDS,
    )
    parser.add_argument(
        "--marker-window-bytes",
        type=int,
        default=DEFAULT_MARKER_WINDOW_BYTES,
    )
    return parser


def main() -> int:  # noqa: PLR0912, PLR0915
    if sys.platform != "darwin":
        raise SystemExit("该脚本仅支持 macOS")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

    args = build_parser().parse_args()
    if args.recipe is not None and args.auto_url_patch_recipe:
        raise RuntimeError("--recipe 与 --auto-url-patch-recipe 不能同时使用")
    artifact_root = args.artifact_root.resolve()
    artifact_root.mkdir(parents=True, exist_ok=True)
    paths = _summary_paths(artifact_root)

    generated_recipe: dict[str, Any] | None = None
    recipe_path = args.recipe.resolve() if args.recipe is not None else None
    if args.auto_url_patch_recipe:
        generated_recipe = _generate_url_patch_recipe(
            trae_path=args.trae_path,
            artifact_root=artifact_root,
        )
        recipe_path = Path(str(generated_recipe["recipe_path"])).resolve()

    source_paths = _resolve_paths(args.trae_path)
    report = build_compatibility_report(source_paths["module_path"], old_url=DEFAULT_OLD_URL)
    summary: dict[str, Any] = {
        "ts": _now_stamp(),
        "source": {
            "app_bundle": str(source_paths["app_bundle"]),
            "executable": str(source_paths["executable"]),
            "module_path": str(source_paths["module_path"]),
            "module_sha256": _sha256_file(source_paths["module_path"]),
            "compatibility_report": report.to_dict(),
            "marker_contexts": _marker_contexts(
                source_paths["module_path"],
                marker_window_bytes=args.marker_window_bytes,
            ),
        },
        "prepared": None,
        "smoke": None,
        "generated_recipe": generated_recipe,
    }

    prepared_app = source_paths["app_bundle"]
    prepared_executable = source_paths["executable"]
    prepared_module_path = source_paths["module_path"]
    if args.skip_clone and args.reuse_clone:
        raise RuntimeError("--skip-clone 与 --reuse-clone 不能同时使用")
    if not args.skip_clone:
        clone_destination = args.clone_app.resolve()
        clone_record = (
            _reuse_existing_app_bundle(source_paths["app_bundle"], clone_destination)
            if args.reuse_clone
            else _clone_app_bundle(source_paths["app_bundle"], clone_destination)
        )
        prepared_paths = _resolve_paths(str(clone_destination))
        patch_records: list[dict[str, Any]] = []
        recipe_payload: dict[str, Any] | None = None
        if recipe_path is not None:
            recipe_payload = _read_recipe(recipe_path)
            patch_records = _apply_replacements(prepared_paths["app_bundle"], recipe_payload)
        codesign_record: dict[str, Any] | None = None
        if not args.skip_sign:
            codesign_record = _codesign_app_bundle(prepared_paths["app_bundle"])

        prepared_app = prepared_paths["app_bundle"]
        prepared_executable = prepared_paths["executable"]
        prepared_module_path = prepared_paths["module_path"]
        summary["prepared"] = {
            "clone": clone_record,
            "recipe_path": str(recipe_path) if recipe_path is not None else None,
            "recipe": recipe_payload,
            "patch_records": patch_records,
            "app_bundle": str(prepared_app),
            "executable": str(prepared_executable),
            "module_path": str(prepared_module_path),
            "module_sha256": _sha256_file(prepared_module_path),
            "codesign": codesign_record,
        }
    else:
        summary["prepared"] = {
            "clone": None,
            "recipe_path": None,
            "recipe": None,
            "patch_records": [],
            "app_bundle": str(prepared_app),
            "executable": str(prepared_executable),
            "module_path": str(prepared_module_path),
            "module_sha256": _sha256_file(prepared_module_path),
            "codesign": None,
        }

    loopback_process: subprocess.Popen[bytes] | None = None
    loopback_log_fp: Any | None = None
    trae_process: subprocess.Popen[bytes] | None = None
    try:
        if args.smoke:
            if _is_port_open(args.cdp_host, args.cdp_port):
                raise RuntimeError(
                    f"CDP 端口已被占用: {args.cdp_host}:{args.cdp_port}；请先关闭现有 Trae"
                )
            loopback_process, loopback_log_fp = _start_loopback(
                host=args.loopback_host,
                port=args.loopback_port,
                current_config_index=args.current_config_index,
                debug_mode=args.debug_mode,
                disable_ssl_strict_mode=args.disable_ssl_strict_mode,
                log_path=paths["loopback_log"],
            )
            trae_process = _launch_trae(prepared_executable, cdp_port=args.cdp_port)
            if not _wait_port(args.cdp_host, args.cdp_port, args.cdp_wait_seconds):
                raise RuntimeError(
                    f"Trae 未在 {args.cdp_wait_seconds}s 内开放 CDP: "
                    f"{args.cdp_host}:{args.cdp_port}"
                )
            cdp_send = _run_cdp_send_chat(
                host=args.cdp_host,
                port=args.cdp_port,
                message=args.message,
                target_url_substring=args.target_url_substring,
                target_title_substring=args.target_title_substring,
                target_wait_seconds=args.cdp_wait_seconds,
                wait_after_send_seconds=args.wait_after_send_seconds,
                mode=args.cdp_mode,
                agent_name=args.cdp_agent_name,
                log_path=paths["cdp_log"],
            )
            loopback_hit = _wait_loopback_hit(
                paths["loopback_log"],
                timeout_seconds=args.loopback_hit_wait_seconds,
            )
            verdict = _run_latest_verdict(
                wait_seconds=args.verdict_wait_seconds,
                log_path=paths["verdict_log"],
            )
            summary["smoke"] = {
                "loopback_log": str(paths["loopback_log"]),
                "cdp_log": str(paths["cdp_log"]),
                "verdict_log": str(paths["verdict_log"]),
                "cdp_send": cdp_send,
                "loopback_hit": loopback_hit,
                "latest_verdict": verdict,
                "launched_executable": str(prepared_executable),
                "cdp_endpoint": f"http://{args.cdp_host}:{args.cdp_port}",
                "cdp_mode": args.cdp_mode,
                "cdp_agent_name": args.cdp_agent_name,
            }

        paths["summary"].write_text(
            json.dumps(summary, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)
        return 0
    finally:
        if not args.keep_running:
            _stop_process(trae_process)
        if loopback_log_fp is not None:
            loopback_log_fp.close()
        _stop_process(loopback_process)


if __name__ == "__main__":
    raise SystemExit(main())
