from __future__ import annotations

import contextlib
import hashlib
import json
import plistlib
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, cast

from .compatibility import parse_macho_layout

MACOS_AI_AGENT_RELATIVE_PATH = Path("Contents/Resources/app/modules/ai-agent/libai_agent.dylib")
DEFAULT_MANIFEST_PATH = Path(__file__).with_name("url_patch_manifest.json")
DEFAULT_PATCH_APP_NAME = "Trae-MTGA.app"
DEFAULT_PATCH_ROOT_RELATIVE_PATH = Path("trae-native") / "macos"
DEFAULT_PATCH_STATE_FILENAME = "patch_state.json"
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
ARM64_ADR_BASE = 0x10000000
ARM64_MOVZ_X_BASE = 0xD2800000
ARM64_INSTRUCTION_SIZE = 4
MAX_MOVZ_IMMEDIATE = 0xFFFF
MAX_GENERAL_REGISTER = 30
RET_BYTES = bytes.fromhex("c0 03 5f d6")
NOP_BYTES = bytes.fromhex("1f 20 03 d5")


def _run_command(
    command: list[str],
    *,
    timeout: float | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )


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


def _u32le(value: int) -> bytes:
    return int(value & 0xFFFFFFFF).to_bytes(4, "little")


def _parse_x_register(register_name: str) -> int:
    normalized = register_name.strip().lower()
    if not normalized.startswith("x"):
        raise RuntimeError(f"当前仅支持 xN 通用寄存器: {register_name}")
    try:
        register_index = int(normalized[1:], 10)
    except ValueError as exc:
        raise RuntimeError(f"寄存器格式无效: {register_name}") from exc
    if not 0 <= register_index <= MAX_GENERAL_REGISTER:
        raise RuntimeError(f"寄存器编号超出范围: {register_name}")
    return register_index


def _encode_adr(register_name: str, imm: int) -> bytes:
    if not -(1 << 20) <= imm < (1 << 20):
        raise RuntimeError(f"ADR 偏移超出 +/-1MiB: {imm}")
    immlo = imm & 0x3
    immhi = (imm >> 2) & 0x7FFFF
    instruction = (
        ARM64_ADR_BASE
        | (immlo << 29)
        | (immhi << 5)
        | _parse_x_register(register_name)
    )
    return _u32le(instruction)


def _encode_movz(register_name: str, imm: int) -> bytes:
    if not 0 <= imm <= MAX_MOVZ_IMMEDIATE:
        raise RuntimeError(f"MOVZ 立即数超出范围: {imm}")
    instruction = ARM64_MOVZ_X_BASE | (imm << 5) | _parse_x_register(register_name)
    return _u32le(instruction)


def _assemble_url_override_trampoline(
    new_url: str,
    *,
    pointer_register: str,
    length_register: str,
) -> dict[str, Any]:
    new_url_bytes = new_url.encode("utf-8")
    if len(new_url_bytes) > MAX_MOVZ_IMMEDIATE:
        raise RuntimeError(f"new_url 长度超出 MOVZ 立即数范围: {len(new_url_bytes)}")
    blob = (
        _encode_adr(pointer_register, 16)
        + _encode_movz(length_register, len(new_url_bytes))
        + RET_BYTES
        + NOP_BYTES
        + new_url_bytes
    )
    padding = (-len(blob)) % 4
    if padding:
        blob += b"\x00" * padding
    return {
        "blob": blob,
        "blob_hex": blob.hex(" "),
        "blob_len": len(blob),
        "new_url_text": new_url,
        "new_url_length": len(new_url_bytes),
        "new_url_offset": 16,
        "code_size": 12,
    }


def _find_macos_app_bundle(path: Path) -> Path | None:
    candidates = (path, *path.parents)
    for candidate in candidates:
        if candidate.suffix.lower() == ".app" and candidate.is_dir():
            return candidate
    return None


def _read_macos_bundle_executable(app_path: Path) -> str:
    info_plist = app_path / "Contents" / "Info.plist"
    try:
        raw = plistlib.loads(info_plist.read_bytes())
    except Exception:
        return "Electron"
    if isinstance(raw, dict):
        plist_payload = cast(dict[str, Any], raw)
        executable = plist_payload.get("CFBundleExecutable")
        if isinstance(executable, str) and executable.strip():
            return executable.strip()
    return "Electron"


def _prepared_executable_path(app_bundle: Path) -> Path:
    executable_name = _read_macos_bundle_executable(app_bundle)
    return app_bundle / "Contents" / "MacOS" / executable_name


def _remove_path(path: Path) -> None:
    if not path.exists():
        return
    if path.is_dir() and not path.is_symlink():
        with contextlib.suppress(FileNotFoundError):
            shutil.rmtree(path)
        return
    path.unlink()


def _load_json_dict(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    try:
        raw_payload = cast(object, json.loads(path.read_text(encoding="utf-8")))
    except Exception:
        return None
    if not isinstance(raw_payload, dict):
        return None
    return cast(dict[str, Any], raw_payload)


def _clone_app_bundle(source: Path, destination: Path) -> dict[str, Any]:
    destination.parent.mkdir(parents=True, exist_ok=True)
    _remove_path(destination)

    clone_command = ["/bin/cp", "-cR", str(source), str(destination)]
    completed = _run_command(clone_command, timeout=180)
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
    replacement_list = cast(list[object], replacements)

    records: list[dict[str, Any]] = []
    for index, raw_item in enumerate(replacement_list, start=1):
        if not isinstance(raw_item, dict):
            raise RuntimeError(f"replacement[{index}] 必须是对象")
        item = cast(dict[str, Any], raw_item)
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

        if mode == "offset_hex":
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
        elif mode == "find_hex":
            needle = _normalize_hex(str(item.get("find") or ""))
            replacement = _normalize_hex(str(item.get("replace") or ""))
            if len(needle) != len(replacement):
                raise RuntimeError(f"replacement[{index}] find_hex 只支持等长替换")
            replaced_offsets = _replace_all(patched, needle, replacement)
            expected_count = int(item.get("expect_count", len(replaced_offsets)))
            if len(replaced_offsets) != expected_count:
                already_patched_offsets = _find_exact_offsets(original, replacement)
                if len(replaced_offsets) + len(already_patched_offsets) != expected_count:
                    raise RuntimeError(
                        f"replacement[{index}] 命中次数不符: expect={expected_count} "
                        f"actual={len(replaced_offsets)} "
                        f"already_patched={len(already_patched_offsets)}"
                    )
        else:
            raise RuntimeError(f"replacement[{index}] 不支持的 mode: {mode}")

        if bytes(patched) != original:
            target_path.write_bytes(bytes(patched))

        records.append(
            {
                "index": index,
                "mode": mode,
                "path": relative_path,
                "replaced_offsets": [hex(offset) for offset in replaced_offsets],
                "already_patched_offsets": [hex(offset) for offset in already_patched_offsets],
                "replacement_count": len(replaced_offsets),
                "before_sha256": before_sha256,
                "after_sha256": _sha256_file(target_path),
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
    identities: list[str] = []
    for raw_line in completed.stdout.splitlines():
        line = raw_line.strip()
        if '"' not in line:
            continue
        start = line.find('"')
        end = line.rfind('"')
        if start >= 0 and end > start:
            identities.append(line[start + 1 : end].strip())
    for identity in identities:
        if identity.startswith("Apple Development:"):
            return identity
    return identities[0] if identities else "-"


def _extract_entitlements(codesign_path: str, target: Path) -> bytes | None:
    completed = _run_command(
        [codesign_path, "-d", "--entitlements", ":-", str(target)],
        timeout=30,
    )
    text = completed.stdout
    if completed.stderr:
        text = f"{text}\n{completed.stderr}" if text else completed.stderr
    start = text.find("<?xml")
    if start < 0:
        start = text.find("<plist")
    if start < 0:
        return None
    end = text.find("</plist>", start)
    if end < 0:
        return None
    return text[start : end + len("</plist>")].encode("utf-8")


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
                    f"codesign leaf 失败: {target} :: "
                    f"{completed.stderr.strip() or completed.stdout.strip()}"
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
                    f"codesign framework 失败: {target} :: "
                    f"{completed.stderr.strip() or completed.stdout.strip()}"
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
                    f"codesign helper 失败: {target} :: "
                    f"{completed.stderr.strip() or completed.stdout.strip()}"
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
        ["codesign", "--verify", "--deep", "--strict", "--verbose=4", str(app_bundle)],
        timeout=120,
    )
    if verify.returncode != 0:
        raise RuntimeError(
            f"codesign verify 失败: {verify.stderr.strip() or verify.stdout.strip()}"
        )

    return {
        "identity": identity,
        "macho_leaf_count": len(macho_leaf_files),
        "framework_count": len(framework_dirs),
        "helper_app_count": len(helper_app_dirs),
        "verify_stdout_tail": verify.stdout[-1000:].strip(),
        "verify_stderr_tail": verify.stderr[-1000:].strip(),
        "sign_log_tail": sign_logs[-20:],
    }


def load_manifest_entry(
    module_path: Path,
    *,
    manifest_path: Path = DEFAULT_MANIFEST_PATH,
) -> dict[str, Any] | None:
    if not manifest_path.is_file():
        raise RuntimeError(f"manifest 文件不存在: {manifest_path}")
    raw_manifest = cast(
        object,
        json.loads(manifest_path.read_text(encoding="utf-8")),
    )
    if not isinstance(raw_manifest, dict):
        raise RuntimeError("manifest 根节点不是对象")
    manifest = cast(dict[str, Any], raw_manifest)
    raw_entries = manifest.get("entries")
    if not isinstance(raw_entries, list):
        raise RuntimeError("manifest entries 不是数组")
    entries = cast(list[object], raw_entries)
    module_sha256 = _sha256_file(module_path)
    for raw_entry in entries:
        if not isinstance(raw_entry, dict):
            continue
        entry = cast(dict[str, Any], raw_entry)
        entry_sha256 = entry.get("module_sha256")
        if isinstance(entry_sha256, str) and entry_sha256 == module_sha256:
            return entry
    return None


def _reuse_copy_state_reason(  # noqa: PLR0911
    *,
    app_bundle: Path,
    module_path: Path,
    state_path: Path,
    source_app: Path,
    source_module_sha256: str,
) -> str | None:
    if not app_bundle.is_dir():
        return "prepared_app_missing"
    info_plist = app_bundle / "Contents" / "Info.plist"
    if not info_plist.is_file():
        return "prepared_info_plist_missing"
    prepared_executable = _prepared_executable_path(app_bundle)
    if not prepared_executable.is_file():
        return "prepared_executable_missing"
    if not module_path.is_file():
        return "prepared_module_missing"

    state = _load_json_dict(state_path)
    if state is None:
        return "patch_state_missing"

    state_source_app = state.get("source_app")
    if not isinstance(state_source_app, str) or state_source_app != str(source_app):
        return "source_app_changed"

    state_source_sha256 = state.get("module_sha256")
    if (
        not isinstance(state_source_sha256, str)
        or state_source_sha256 != source_module_sha256
    ):
        return "source_module_sha256_changed"

    state_patched_sha256 = state.get("patched_module_sha256")
    if not isinstance(state_patched_sha256, str) or not state_patched_sha256:
        return "patch_state_incomplete"
    current_patched_sha256 = _sha256_file(module_path)
    if state_patched_sha256 != current_patched_sha256:
        return "prepared_module_sha256_changed"
    return None


def build_recipe_from_manifest(
    module_path: Path,
    *,
    new_url: str,
    manifest_entry: dict[str, Any],
    manifest_path: Path = DEFAULT_MANIFEST_PATH,
) -> dict[str, Any]:
    raw_site = manifest_entry.get("site")
    raw_trampoline = manifest_entry.get("trampoline")
    if not isinstance(raw_site, dict) or not isinstance(raw_trampoline, dict):
        raise RuntimeError("manifest entry 缺少 site/trampoline")
    site = cast(dict[str, Any], raw_site)
    trampoline = cast(dict[str, Any], raw_trampoline)

    pointer_register = str(site.get("pointer_register") or "")
    length_register = str(site.get("length_register") or "")
    if not pointer_register or not length_register:
        raise RuntimeError("manifest site 缺少 pointer/length register")

    data = module_path.read_bytes()
    layout = parse_macho_layout(data)
    site_rva = int(str(site.get("address") or "0x0"), 16)
    site_file_offset = int(str(site.get("file_offset") or "0x0"), 16)
    if site_file_offset == 0:
        for section in layout.sections:
            if section.address <= site_rva < section.address + section.size:
                site_file_offset = section.offset + (site_rva - section.address)
                break
        if site_file_offset == 0:
            raise RuntimeError(f"无法根据 RVA 定位 site file offset: {hex(site_rva)}")

    cave_file_offset = int(str(trampoline.get("file_offset") or "0x0"), 16)
    cave_rva = int(str(trampoline.get("stub_rva") or "0x0"), 16)
    blob_info = _assemble_url_override_trampoline(
        new_url,
        pointer_register=pointer_register,
        length_register=length_register,
    )
    blob = bytes(blob_info["blob"])
    site_expected = data[site_file_offset : site_file_offset + ARM64_INSTRUCTION_SIZE]
    distance = cave_rva - site_rva
    if distance % ARM64_INSTRUCTION_SIZE != 0:
        raise RuntimeError(f"BL 偏移未按 4 字节对齐: {distance}")
    imm26 = (distance >> 2) & 0x03FFFFFF
    branch = _u32le(0x94000000 | imm26)
    cave_expected = data[cave_file_offset : cave_file_offset + len(blob)]
    if len(cave_expected) != len(blob):
        raise RuntimeError("manifest cave 写入区域越界")

    app_bundle = _find_macos_app_bundle(module_path)
    if app_bundle is None:
        raise RuntimeError(f"无法从 module_path 推导 app bundle: {module_path}")
    relative_module_path = str(module_path.relative_to(app_bundle))
    module_sha256 = _sha256_file(module_path)

    return {
        "meta": {
            "strategy": "arm64_bl_trampoline_custom_model_url_override",
            "primary_site_label": site.get("label"),
            "module_relative_path": relative_module_path,
            "module_sha256": module_sha256,
            "new_url": new_url,
            "manifest_path": str(manifest_path),
            "notes": [
                "primary site/cave 来自已验证通过的 manifest。",
                "将 primary site 的 URL 装载指令改为 BL trampoline。",
                f"trampoline 直接设置 {pointer_register}/{length_register}，"
                f"并返回到 {site.get('return_rva')}.",
            ],
        },
        "replacements": [
            {
                "path": relative_module_path,
                "mode": "offset_hex",
                "offset": hex(site_file_offset),
                "expected": site_expected.hex(" "),
                "replace": branch.hex(" "),
                "description": "用 BL trampoline 替换 manifest 主位点的 URL 装载指令",
            },
            {
                "path": relative_module_path,
                "mode": "offset_hex",
                "offset": hex(cave_file_offset),
                "expected": cave_expected.hex(" "),
                "replace": str(blob_info["blob_hex"]),
                "description": "向 manifest 指定的 __TEXT,__text cave 注入 URL override trampoline",
            },
        ],
        "plan": {
            "site": {
                **site,
                "file_offset": hex(site_file_offset),
                "expected_bytes": site_expected.hex(" "),
                "branch_bytes": branch.hex(" "),
                "pointer_register": pointer_register,
                "length_register": length_register,
            },
            "trampoline": {
                key: value
                for key, value in blob_info.items()
                if key != "blob"
            }
            | {
                "file_offset": hex(cave_file_offset),
                "expected_bytes": cave_expected.hex(" "),
                "branch_distance_bytes": distance,
                "usable_length_bytes": trampoline.get("usable_length_bytes"),
                "stub_rva": hex(cave_rva),
                "return_rva": site.get("return_rva"),
                "pointer_register": pointer_register,
                "length_register": length_register,
            },
        },
    }


def prepare_patched_copy(
    trae_executable: Path,
    *,
    new_url: str,
    user_data_dir: Path,
    logs_dir: Path,
    manifest_path: Path = DEFAULT_MANIFEST_PATH,
) -> dict[str, Any]:
    source_app = _find_macos_app_bundle(trae_executable)
    if source_app is None:
        raise RuntimeError(f"无法从路径推导 Trae.app: {trae_executable}")
    source_module_path = source_app / MACOS_AI_AGENT_RELATIVE_PATH
    if not source_module_path.is_file():
        raise RuntimeError(f"未找到 libai_agent.dylib: {source_module_path}")
    source_module_sha256 = _sha256_file(source_module_path)

    manifest_entry = load_manifest_entry(source_module_path, manifest_path=manifest_path)
    if manifest_entry is None:
        raise RuntimeError(
            "macOS url patch manifest 未命中当前版本: "
            f"sha={source_module_sha256} "
            f"manifest={manifest_path}"
        )
    recipe = build_recipe_from_manifest(
        source_module_path,
        new_url=new_url,
        manifest_entry=manifest_entry,
        manifest_path=manifest_path,
    )

    patch_root = user_data_dir / DEFAULT_PATCH_ROOT_RELATIVE_PATH
    app_bundle = patch_root / DEFAULT_PATCH_APP_NAME
    module_path = app_bundle / MACOS_AI_AGENT_RELATIVE_PATH
    state_path = patch_root / DEFAULT_PATCH_STATE_FILENAME
    summary_path = logs_dir / "trae_native_macos_patch.json"

    reuse_reason = _reuse_copy_state_reason(
        app_bundle=app_bundle,
        module_path=module_path,
        state_path=state_path,
        source_app=source_app,
        source_module_sha256=source_module_sha256,
    )
    if reuse_reason is not None:
        clone_summary = _clone_app_bundle(source_app, app_bundle)
        clone_summary["reason"] = reuse_reason
    else:
        clone_summary = {
            "mode": "reuse_existing",
            "source": str(source_app),
            "destination": str(app_bundle),
            "reason": "source_match",
        }

    try:
        patch_records = _apply_replacements(app_bundle, recipe)
    except Exception:
        clone_summary = _clone_app_bundle(source_app, app_bundle)
        clone_summary["reason"] = "patch_apply_retry_after_reclone"
        patch_records = _apply_replacements(app_bundle, recipe)

    changed = any(record.get("replacement_count") for record in patch_records)
    codesign_summary = None
    if str(clone_summary.get("mode") or "") != "reuse_existing" or changed:
        codesign_summary = _codesign_app_bundle(app_bundle)

    prepared_executable = _prepared_executable_path(app_bundle)
    summary = {
        "source_app": str(source_app),
        "prepared_app": str(app_bundle),
        "prepared_executable": str(prepared_executable),
        "manifest_path": str(manifest_path),
        "patch_state_path": str(state_path),
        "module_sha256": source_module_sha256,
        "recipe": {
            "site": recipe["plan"]["site"],
            "trampoline": recipe["plan"]["trampoline"],
        },
        "clone": clone_summary,
        "patch_records": patch_records,
        "codesign": codesign_summary,
        "patched_module_sha256": _sha256_file(module_path),
    }
    patch_root.mkdir(parents=True, exist_ok=True)
    state_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return summary


__all__ = [
    "DEFAULT_MANIFEST_PATH",
    "DEFAULT_PATCH_APP_NAME",
    "DEFAULT_PATCH_ROOT_RELATIVE_PATH",
    "build_recipe_from_manifest",
    "load_manifest_entry",
    "prepare_patched_copy",
]
