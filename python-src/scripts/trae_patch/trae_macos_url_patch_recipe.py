from __future__ import annotations

import argparse
import hashlib
import json
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
from modules.trae_patch.macos.compatibility import parse_macho_layout  # noqa: E402

DEFAULT_TRAE_PATH = "/Applications/Trae.app"
DEFAULT_NEW_URL = "http://127.0.0.1:18083/v1/chat/completions"
DEFAULT_ARTIFACT_ROOT = Path("python-src/artifacts/trae_macos_url_patch_recipe")
DEFAULT_REPORT_ARTIFACT_ROOT = Path("python-src/artifacts/trae_macos_native_symbol_report")
DEFAULT_MANIFEST_PATH = (
    PYTHON_SRC_DIR / "modules" / "trae_patch" / "macos" / "url_patch_manifest.json"
)
DEFAULT_PRIMARY_SITE_LABEL = "default_handler_final_request_url_load"
DEFAULT_PRIMARY_SITE_ADDRESS = 0x1204B3C
DEFAULT_PRIMARY_SITE_SYMBOL = "default_handler_handle_sse_closure"
DEFAULT_PRIMARY_SITE_KIND = "reqwest_request_url_pair_load"
DEFAULT_PRIMARY_SITE_WHY = (
    "DefaultSseProxyHandler 在 reqwest::Client::request 前最后一次装入 URL 对。"
)
ARM64_BL_BASE = 0x94000000
ARM64_INSTRUCTION_SIZE = 4
ARM64_BL_RANGE = 1 << 27
MAX_MOVZ_IMMEDIATE = 0xFFFF
RET_BYTES = bytes.fromhex("c0 03 5f d6")
SITE_KIND_REGISTER_SPECS: dict[str, dict[str, str]] = {
    "reqwest_request_url_pair_load": {
        "pointer_register": "x3",
        "length_register": "x4",
        "instruction_hint": "ldp x3, x4, [x28, #0x8]",
        "path_scope": "DefaultSseProxyHandler -> reqwest::Client::request",
    },
    "url_pair_load": {
        "pointer_register": "x3",
        "length_register": "x4",
        "instruction_hint": "ldp x3, x4, [...]",
        "path_scope": "generic reqwest::Client::request bridge",
    },
    "builder_url_source_load": {
        "pointer_register": "x1",
        "length_register": "x2",
        "instruction_hint": "ldp x1, x2, [x19, #0x88]",
        "path_scope": "custom_model HttpRequest -> RequestBuilder",
    },
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


def _find_app_bundle(path: Path) -> Path | None:
    candidates = (path, *path.parents)
    for candidate in candidates:
        if candidate.suffix.lower() == ".app" and candidate.is_dir():
            return candidate
    return None


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


def _load_report(trae_path: str, artifact_root: Path) -> dict[str, Any]:
    command = [
        _project_python(),
        str(_script_path("trae_macos_native_symbol_report.py")),
        "--trae-path",
        trae_path,
        "--artifact-root",
        str(artifact_root),
        "--json",
    ]
    completed = _run_command(command, timeout=90)
    if completed.returncode != 0:
        raise RuntimeError(
            completed.stderr.strip() or completed.stdout.strip() or "symbol report 执行失败"
        )
    payload = json.loads(completed.stdout)
    if not isinstance(payload, dict):
        raise RuntimeError("symbol report JSON 根节点不是对象")
    return payload


def _load_manifest_entry(
    module_path: Path,
    *,
    manifest_path: Path,
) -> dict[str, Any] | None:
    if not manifest_path.is_file():
        return None

    raw_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(raw_manifest, dict):
        raise RuntimeError("manifest 根节点不是对象")
    raw_entries = raw_manifest.get("entries")
    if not isinstance(raw_entries, list):
        raise RuntimeError("manifest entries 不是数组")

    module_sha256 = _sha256_file(module_path)
    for raw_entry in raw_entries:
        if not isinstance(raw_entry, dict):
            continue
        entry_sha256 = raw_entry.get("module_sha256")
        if isinstance(entry_sha256, str) and entry_sha256 == module_sha256:
            return raw_entry
    return None


def _rva_to_file_offset(layout: Any, rva: int) -> int:
    for section in layout.sections:
        if section.address <= rva < section.address + section.size:
            return section.offset + (rva - section.address)
    raise RuntimeError(f"RVA 未命中任何 section: {hex(rva)}")


def _u32le(value: int) -> bytes:
    return int(value & 0xFFFFFFFF).to_bytes(4, "little")


def _encode_bl(src_rva: int, target_rva: int) -> bytes:
    offset = target_rva - src_rva
    if offset % ARM64_INSTRUCTION_SIZE != 0:
        raise RuntimeError(f"BL 偏移未按 4 字节对齐: {offset}")
    if not -(ARM64_BL_RANGE // 2) <= offset < (ARM64_BL_RANGE // 2):
        raise RuntimeError(
            f"BL 目标超出 +/-128MiB 范围: src={hex(src_rva)} target={hex(target_rva)}"
        )
    imm26 = (offset >> 2) & 0x03FFFFFF
    return _u32le(ARM64_BL_BASE | imm26)


def _hex_bytes(data: bytes) -> str:
    return data.hex(" ")


def _candidate_site(summary: dict[str, Any], label: str) -> dict[str, Any]:
    recommended_plan = summary.get("recommended_patch_plan")
    if isinstance(recommended_plan, dict):
        primary = recommended_plan.get("primary")
        if isinstance(primary, dict):
            site = primary.get("site")
            if isinstance(site, dict):
                recommended_label = str(site.get("label") or "")
                if recommended_label == label:
                    return site

    raw_sites = summary.get("candidate_patch_sites")
    if not isinstance(raw_sites, list):
        raise RuntimeError("summary 缺少 candidate_patch_sites")
    for item in raw_sites:
        if isinstance(item, dict) and str(item.get("label")) == label:
            return item
    if label == DEFAULT_PRIMARY_SITE_LABEL:
        return {
            "label": DEFAULT_PRIMARY_SITE_LABEL,
            "symbol": DEFAULT_PRIMARY_SITE_SYMBOL,
            "address": hex(DEFAULT_PRIMARY_SITE_ADDRESS),
            "kind": DEFAULT_PRIMARY_SITE_KIND,
            "why": DEFAULT_PRIMARY_SITE_WHY,
        }
    raise RuntimeError(f"未在 summary 中找到 patch site: {label}")


def _candidate_cave(
    summary: dict[str, Any],
    *,
    site_rva: int,
    required_length: int,
) -> dict[str, Any]:
    raw_caves = summary.get("text_code_caves")
    if not isinstance(raw_caves, list):
        raise RuntimeError("summary 缺少 text_code_caves")

    for raw_cave in raw_caves:
        if not isinstance(raw_cave, dict):
            continue
        usable_length = int(raw_cave.get("usable_length_bytes", 0))
        if usable_length < required_length:
            continue
        aligned_file_offset = int(str(raw_cave.get("aligned_file_offset", "0x0")), 16)
        location = raw_cave.get("location")
        if not isinstance(location, dict):
            continue
        base_file_offset = int(str(location.get("file_offset", "0x0")), 16)
        base_rva = int(str(location.get("rva", "0x0")), 16)
        selected_rva = base_rva + (aligned_file_offset - base_file_offset)
        distance = selected_rva - site_rva
        if not -(ARM64_BL_RANGE // 2) <= distance < (ARM64_BL_RANGE // 2):
            continue
        return {
            **raw_cave,
            "selected_file_offset": hex(aligned_file_offset),
            "selected_rva": hex(selected_rva),
            "branch_distance_bytes": distance,
        }
    raise RuntimeError(
        "未找到可用的 __TEXT,__text cave: "
        f"site={hex(site_rva)} required_length={required_length}"
    )


def _extract_text_section_bytes(object_path: Path) -> bytes:
    completed = _run_command(
        ["otool", "-s", "__TEXT", "__text", str(object_path)],
        timeout=10,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            completed.stderr.strip() or completed.stdout.strip() or "otool 提取 __text 失败"
        )

    blob = bytearray()
    for raw_line in completed.stdout.splitlines():
        line = raw_line.strip()
        if not line or line.endswith("section") or line.endswith(":"):
            continue
        parts = line.split()
        for token in parts[1:]:
            if len(token) % 2 == 0 and all(ch in "0123456789abcdefABCDEF" for ch in token):
                blob.extend(bytes.fromhex(token)[::-1])
            else:
                break
    if not blob:
        raise RuntimeError(f"未从 {object_path} 提取到 __text section 原始字节")
    return bytes(blob)


def _site_register_spec(kind: str) -> dict[str, str]:
    spec = SITE_KIND_REGISTER_SPECS.get(kind)
    if spec is None:
        raise RuntimeError(f"当前 recipe 暂不支持该 site.kind: {kind}")
    return spec


def _validated_manifest_site(entry: dict[str, Any]) -> dict[str, Any]:
    raw_site = entry.get("site")
    if not isinstance(raw_site, dict):
        raise RuntimeError("manifest entry 缺少 site")
    site = dict(raw_site)
    if str(site.get("label") or "") != DEFAULT_PRIMARY_SITE_LABEL:
        raise RuntimeError(
            "manifest site.label 与当前默认 primary 不一致: "
            f"{site.get('label')}"
        )
    if str(site.get("kind") or "") != DEFAULT_PRIMARY_SITE_KIND:
        raise RuntimeError(
            "manifest site.kind 与当前 recipe 预期不一致: "
            f"{site.get('kind')}"
        )
    if "address" not in site or "file_offset" not in site:
        raise RuntimeError("manifest site 缺少 address/file_offset")
    return site


def _validated_manifest_trampoline(entry: dict[str, Any]) -> dict[str, Any]:
    raw_trampoline = entry.get("trampoline")
    if not isinstance(raw_trampoline, dict):
        raise RuntimeError("manifest entry 缺少 trampoline")
    trampoline = dict(raw_trampoline)
    if "stub_rva" not in trampoline or "file_offset" not in trampoline:
        raise RuntimeError("manifest trampoline 缺少 stub_rva/file_offset")
    return trampoline


def _assemble_url_override_trampoline(
    new_url: str,
    *,
    pointer_register: str,
    length_register: str,
) -> dict[str, Any]:
    if len(new_url.encode("utf-8")) > MAX_MOVZ_IMMEDIATE:
        raise RuntimeError(f"new_url 长度超出 MOVZ 立即数范围: {len(new_url)}")

    assembly = f"""
.text
.globl _stub
.p2align 2
_stub:
  adr {pointer_register}, new_url
  movz {length_register}, #{len(new_url.encode("utf-8"))}
  ret
  .p2align 3
new_url:
  .ascii {json.dumps(new_url, ensure_ascii=False)}
"""
    with tempfile.TemporaryDirectory(prefix="mtga-macos-url-patch-") as temp_dir:
        stub_path = Path(temp_dir) / "stub.s"
        object_path = Path(temp_dir) / "stub.o"
        stub_path.write_text(assembly.strip() + "\n", encoding="utf-8")
        completed = _run_command(
            [
                "xcrun",
                "clang",
                "-target",
                "arm64-apple-macos",
                "-c",
                str(stub_path),
                "-o",
                str(object_path),
            ],
            timeout=30,
        )
        if completed.returncode != 0:
            raise RuntimeError(
                completed.stderr.strip() or completed.stdout.strip() or "clang 汇编 trampoline 失败"
            )
        blob = _extract_text_section_bytes(object_path)

    new_url_bytes = new_url.encode("utf-8")
    new_url_offset = blob.find(new_url_bytes)
    code_size = blob.find(RET_BYTES)
    return {
        "blob": blob,
        "blob_hex": blob.hex(" "),
        "blob_len": len(blob),
        "new_url_text": new_url,
        "new_url_length": len(new_url_bytes),
        "new_url_offset": new_url_offset,
        "code_size": code_size + len(RET_BYTES) if code_size >= 0 else None,
    }


def _relative_to(path: Path, root: Path) -> str:
    return str(path.relative_to(root))


def _build_recipe(  # noqa: PLR0913
    *,
    app_bundle: Path,
    module_path: Path,
    new_url: str,
    report_artifact_root: Path,
    summary: dict[str, Any] | None = None,
    manifest_entry: dict[str, Any] | None = None,
    manifest_path: Path | None = None,
) -> dict[str, Any]:
    data = module_path.read_bytes()
    if manifest_entry is not None:
        site = _validated_manifest_site(manifest_entry)
        site_kind = str(site["kind"])
        site_rva = int(str(site["address"]), 16)
        site_file_offset = int(str(site["file_offset"]), 16)
        register_spec = _site_register_spec(site_kind)
        manifest_trampoline = _validated_manifest_trampoline(manifest_entry)
        cave_file_offset = int(str(manifest_trampoline["file_offset"]), 16)
        cave_rva = int(str(manifest_trampoline["stub_rva"]), 16)
        compatibility_report = manifest_entry.get("compatibility_report")
        report_summary_path = None
        reference_notes = [
            "primary site/cave 来自已验证通过的 manifest，不再重新跑 symbol report 推导。",
        ]
    else:
        if summary is None:
            raise RuntimeError("缺少 summary 或 manifest_entry")
        layout = parse_macho_layout(data)
        site = _candidate_site(summary, DEFAULT_PRIMARY_SITE_LABEL)
        site_kind = str(site.get("kind") or "")
        if site_kind != DEFAULT_PRIMARY_SITE_KIND:
            raise RuntimeError(
                "primary site kind 不符合当前 recipe 预期: "
                f"expected={DEFAULT_PRIMARY_SITE_KIND} actual={site_kind}"
            )
        site_rva = int(str(site["address"]), 16)
        site_file_offset = _rva_to_file_offset(layout, site_rva)
        register_spec = _site_register_spec(site_kind)
        compatibility_report = summary.get("compatibility_report")
        report_summary_path = str(report_artifact_root / "summary.json")
        reference_notes = []

    trampoline = _assemble_url_override_trampoline(
        new_url,
        pointer_register=register_spec["pointer_register"],
        length_register=register_spec["length_register"],
    )
    if manifest_entry is None:
        cave = _candidate_cave(
            summary,
            site_rva=site_rva,
            required_length=int(trampoline["blob_len"]),
        )
        cave_file_offset = int(str(cave["selected_file_offset"]), 16)
        cave_rva = int(str(cave["selected_rva"]), 16)
        usable_length_bytes = cave["usable_length_bytes"]
        branch_distance_bytes = cave["branch_distance_bytes"]
    else:
        usable_length_bytes = manifest_trampoline.get("usable_length_bytes")
        branch_distance_bytes = cave_rva - site_rva
    branch = _encode_bl(site_rva, cave_rva)

    site_expected = data[site_file_offset : site_file_offset + ARM64_INSTRUCTION_SIZE]
    blob = bytes(trampoline["blob"])
    cave_expected = data[cave_file_offset : cave_file_offset + len(blob)]
    if len(cave_expected) != len(blob):
        raise RuntimeError("trampoline 写入区域越界")

    relative_module_path = _relative_to(module_path, app_bundle)
    module_sha256 = _sha256_file(module_path)
    return {
        "meta": {
            "ts": _now_stamp(),
            "strategy": "arm64_bl_trampoline_custom_model_url_override",
            "primary_site_label": site["label"],
            "module_relative_path": relative_module_path,
            "module_sha256": module_sha256,
            "new_url": new_url,
            "report_summary_path": report_summary_path,
            "manifest_path": str(manifest_path) if manifest_path is not None else None,
            "compatibility_report": compatibility_report,
            "notes": reference_notes + [
                "将 primary site 的 URL 装载指令改为 BL trampoline。",
                "trampoline 通过 ADR + MOVZ 直接设置 "
                f"{register_spec['pointer_register']}/{register_spec['length_register']}，"
                "并用 ret 返回到 "
                f"{hex(site_rva + ARM64_INSTRUCTION_SIZE)}。",
                f"该位点当前覆盖 {register_spec['path_scope']} 路径。",
            ],
        },
        "replacements": [
            {
                "path": relative_module_path,
                "mode": "offset_hex",
                "offset": hex(site_file_offset),
                "expected": _hex_bytes(site_expected),
                "replace": _hex_bytes(branch),
                "description": (
                    "用 BL trampoline 替换 URL 装载指令 "
                    f"{register_spec['instruction_hint']}"
                ),
            },
            {
                "path": relative_module_path,
                "mode": "offset_hex",
                "offset": hex(cave_file_offset),
                "expected": _hex_bytes(cave_expected),
                "replace": str(trampoline["blob_hex"]),
                "description": "向 __TEXT,__text cave 注入最小 URL override trampoline",
            },
        ],
        "plan": {
            "site": {
                **site,
                "file_offset": hex(site_file_offset),
                "expected_bytes": _hex_bytes(site_expected),
                "branch_bytes": _hex_bytes(branch),
                "return_rva": hex(site_rva + ARM64_INSTRUCTION_SIZE),
                "pointer_register": register_spec["pointer_register"],
                "length_register": register_spec["length_register"],
            },
            "trampoline": {
                key: value
                for key, value in trampoline.items()
                if key != "blob"
            }
            | {
                "file_offset": hex(cave_file_offset),
                "expected_bytes": _hex_bytes(cave_expected),
                "branch_distance_bytes": branch_distance_bytes,
                "usable_length_bytes": usable_length_bytes,
                "stub_rva": hex(cave_rva),
                "return_rva": hex(site_rva + ARM64_INSTRUCTION_SIZE),
                "pointer_register": register_spec["pointer_register"],
                "length_register": register_spec["length_register"],
            },
        },
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="生成 macOS Trae native URL override 的离线 patch recipe。"
    )
    parser.add_argument("--trae-path", default=DEFAULT_TRAE_PATH)
    parser.add_argument("--new-url", default=DEFAULT_NEW_URL)
    parser.add_argument("--artifact-root", type=Path, default=DEFAULT_ARTIFACT_ROOT)
    parser.add_argument(
        "--report-artifact-root",
        type=Path,
        default=DEFAULT_REPORT_ARTIFACT_ROOT,
    )
    parser.add_argument(
        "--manifest-path",
        type=Path,
        default=DEFAULT_MANIFEST_PATH,
    )
    parser.add_argument("--json", action="store_true", help="输出完整 JSON")
    return parser


def main() -> int:
    if sys.platform != "darwin":
        raise SystemExit("该脚本仅支持 macOS")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

    args = build_parser().parse_args()
    artifact_root = args.artifact_root.resolve()
    artifact_root.mkdir(parents=True, exist_ok=True)

    paths = _resolve_paths(args.trae_path)
    manifest_path = args.manifest_path.resolve()
    manifest_entry = _load_manifest_entry(paths["module_path"], manifest_path=manifest_path)
    report_root = args.report_artifact_root.resolve()
    summary = None if manifest_entry is not None else _load_report(args.trae_path, report_root)
    recipe = _build_recipe(
        app_bundle=paths["app_bundle"],
        module_path=paths["module_path"],
        new_url=args.new_url,
        report_artifact_root=report_root,
        summary=summary,
        manifest_entry=manifest_entry,
        manifest_path=manifest_path if manifest_entry is not None else None,
    )

    recipe_path = artifact_root / "recipe.json"
    plan_path = artifact_root / "plan.json"
    recipe_path.write_text(
        json.dumps(recipe, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    plan_path.write_text(
        json.dumps(recipe["plan"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    output = {
        "ts": recipe["meta"]["ts"],
        "recipe_path": str(recipe_path),
        "plan_path": str(plan_path),
        "module_path": str(paths["module_path"]),
        "module_sha256": recipe["meta"]["module_sha256"],
        "manifest_hit": manifest_entry is not None,
        "manifest_path": str(manifest_path) if manifest_entry is not None else None,
        "site": recipe["plan"]["site"],
        "trampoline": recipe["plan"]["trampoline"],
    }
    if args.json:
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return 0

    print(f"recipe_path: {recipe_path}")
    print(f"plan_path: {plan_path}")
    print(f"module_path: {paths['module_path']}")
    print(
        "site: "
        f"{output['site']['label']} file={output['site']['file_offset']} "
        f"branch={output['site']['branch_bytes']}"
    )
    print(
        "trampoline: "
        f"file={output['trampoline']['file_offset']} "
        f"len={output['trampoline']['blob_len']} "
        f"branch_distance={output['trampoline']['branch_distance_bytes']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
