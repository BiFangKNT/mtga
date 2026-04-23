from __future__ import annotations

import argparse
import ctypes
import json
from ctypes import wintypes
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .hook_candidates import AI_AGENT_DLL

TH32CS_SNAPPROCESS = 0x00000002
TH32CS_SNAPMODULE = 0x00000008
TH32CS_SNAPMODULE32 = 0x00000010
INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value
MAX_PATH = 260
ERROR_NOT_ALL_ASSIGNED = 1300
SE_PRIVILEGE_ENABLED = 0x00000002
TOKEN_ADJUST_PRIVILEGES = 0x0020
TOKEN_QUERY = 0x0008

DEFAULT_RVAS = {
    "update_boot_config_log_anchor": 0x951127,
    "tunnel_url_builder_http_fallback_anchor": 0x28A5995,
    "tunnel_url_builder_error_anchor": 0x28A599C,
    "tunnel_url_builder_result_ready_anchor": 0x28A59AB,
}


class PROCESSENTRY32W(ctypes.Structure):
    _fields_ = [
        ("dwSize", wintypes.DWORD),
        ("cntUsage", wintypes.DWORD),
        ("th32ProcessID", wintypes.DWORD),
        ("th32DefaultHeapID", ctypes.c_size_t),
        ("th32ModuleID", wintypes.DWORD),
        ("cntThreads", wintypes.DWORD),
        ("th32ParentProcessID", wintypes.DWORD),
        ("pcPriClassBase", wintypes.LONG),
        ("dwFlags", wintypes.DWORD),
        ("szExeFile", wintypes.WCHAR * MAX_PATH),
    ]


class MODULEENTRY32W(ctypes.Structure):
    _fields_ = [
        ("dwSize", wintypes.DWORD),
        ("th32ModuleID", wintypes.DWORD),
        ("th32ProcessID", wintypes.DWORD),
        ("GlblcntUsage", wintypes.DWORD),
        ("ProccntUsage", wintypes.DWORD),
        ("modBaseAddr", ctypes.POINTER(wintypes.BYTE)),
        ("modBaseSize", wintypes.DWORD),
        ("hModule", wintypes.HMODULE),
        ("szModule", wintypes.WCHAR * 256),
        ("szExePath", wintypes.WCHAR * MAX_PATH),
    ]


class LUID(ctypes.Structure):
    _fields_ = [
        ("LowPart", wintypes.DWORD),
        ("HighPart", wintypes.LONG),
    ]


class LUID_AND_ATTRIBUTES(ctypes.Structure):
    _fields_ = [
        ("Luid", LUID),
        ("Attributes", wintypes.DWORD),
    ]


class TOKEN_PRIVILEGES(ctypes.Structure):
    _fields_ = [
        ("PrivilegeCount", wintypes.DWORD),
        ("Privileges", LUID_AND_ATTRIBUTES * 1),
    ]


kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
advapi32 = ctypes.WinDLL("advapi32", use_last_error=True)
CreateToolhelp32Snapshot = kernel32.CreateToolhelp32Snapshot
CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
CreateToolhelp32Snapshot.restype = wintypes.HANDLE

Process32FirstW = kernel32.Process32FirstW
Process32FirstW.argtypes = [wintypes.HANDLE, ctypes.POINTER(PROCESSENTRY32W)]
Process32FirstW.restype = wintypes.BOOL

Process32NextW = kernel32.Process32NextW
Process32NextW.argtypes = [wintypes.HANDLE, ctypes.POINTER(PROCESSENTRY32W)]
Process32NextW.restype = wintypes.BOOL

Module32FirstW = kernel32.Module32FirstW
Module32FirstW.argtypes = [wintypes.HANDLE, ctypes.POINTER(MODULEENTRY32W)]
Module32FirstW.restype = wintypes.BOOL

Module32NextW = kernel32.Module32NextW
Module32NextW.argtypes = [wintypes.HANDLE, ctypes.POINTER(MODULEENTRY32W)]
Module32NextW.restype = wintypes.BOOL

CloseHandle = kernel32.CloseHandle
CloseHandle.argtypes = [wintypes.HANDLE]
CloseHandle.restype = wintypes.BOOL
GetCurrentProcess = kernel32.GetCurrentProcess
GetCurrentProcess.argtypes = []
GetCurrentProcess.restype = wintypes.HANDLE

OpenProcessToken = advapi32.OpenProcessToken
OpenProcessToken.argtypes = [
    wintypes.HANDLE,
    wintypes.DWORD,
    ctypes.POINTER(wintypes.HANDLE),
]
OpenProcessToken.restype = wintypes.BOOL
LookupPrivilegeValueW = advapi32.LookupPrivilegeValueW
LookupPrivilegeValueW.argtypes = [
    wintypes.LPCWSTR,
    wintypes.LPCWSTR,
    ctypes.POINTER(LUID),
]
LookupPrivilegeValueW.restype = wintypes.BOOL
AdjustTokenPrivileges = advapi32.AdjustTokenPrivileges
AdjustTokenPrivileges.argtypes = [
    wintypes.HANDLE,
    wintypes.BOOL,
    ctypes.POINTER(TOKEN_PRIVILEGES),
    wintypes.DWORD,
    ctypes.c_void_p,
    ctypes.c_void_p,
]
AdjustTokenPrivileges.restype = wintypes.BOOL


@dataclass(frozen=True)
class ProcessInfo:
    pid: int
    name: str
    parent_pid: int


@dataclass(frozen=True)
class ModuleInfo:
    pid: int
    process_name: str
    parent_pid: int
    module_name: str
    module_path: str
    base_address: int
    size: int


@dataclass(frozen=True)
class ModuleSnapshotFailure:
    pid: int
    process_name: str
    stage: str
    error_code: int


def _raise_last_error(message: str) -> None:
    error_code = ctypes.get_last_error()
    raise OSError(error_code, f"{message}: WinError {error_code}")


def _handle_value(handle: wintypes.HANDLE) -> int:
    value = getattr(handle, "value", handle)
    if value is None:
        return 0
    return int(value)


def _close_handle(handle: wintypes.HANDLE) -> None:
    if _handle_value(handle) not in (0, INVALID_HANDLE_VALUE):
        CloseHandle(handle)


def enable_debug_privilege() -> dict[str, Any]:
    token = wintypes.HANDLE()
    if not OpenProcessToken(
        GetCurrentProcess(),
        TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY,
        ctypes.byref(token),
    ):
        return {"ok": False, "stage": "OpenProcessToken", "error_code": ctypes.get_last_error()}

    try:
        luid = LUID()
        if not LookupPrivilegeValueW(None, "SeDebugPrivilege", ctypes.byref(luid)):
            return {
                "ok": False,
                "stage": "LookupPrivilegeValueW",
                "error_code": ctypes.get_last_error(),
            }

        privileges = TOKEN_PRIVILEGES()
        privileges.PrivilegeCount = 1
        privileges.Privileges[0].Luid = luid
        privileges.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED
        ctypes.set_last_error(0)
        if not AdjustTokenPrivileges(
            token,
            False,
            ctypes.byref(privileges),
            0,
            None,
            None,
        ):
            return {
                "ok": False,
                "stage": "AdjustTokenPrivileges",
                "error_code": ctypes.get_last_error(),
            }
        error_code = ctypes.get_last_error()
        return {
            "ok": error_code == 0,
            "stage": "AdjustTokenPrivileges",
            "error_code": error_code,
            "not_all_assigned": error_code == ERROR_NOT_ALL_ASSIGNED,
        }
    finally:
        _close_handle(token)


def iter_processes() -> list[ProcessInfo]:
    snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    if _handle_value(snapshot) == INVALID_HANDLE_VALUE:
        _raise_last_error("CreateToolhelp32Snapshot(process) 失败")

    try:
        entry = PROCESSENTRY32W()
        entry.dwSize = ctypes.sizeof(PROCESSENTRY32W)
        processes: list[ProcessInfo] = []
        if not Process32FirstW(snapshot, ctypes.byref(entry)):
            return processes
        while True:
            processes.append(
                ProcessInfo(
                    pid=int(entry.th32ProcessID),
                    name=entry.szExeFile,
                    parent_pid=int(entry.th32ParentProcessID),
                )
            )
            if not Process32NextW(snapshot, ctypes.byref(entry)):
                break
        return processes
    finally:
        _close_handle(snapshot)


def iter_modules(
    process: ProcessInfo,
    failures: list[ModuleSnapshotFailure] | None = None,
) -> list[ModuleInfo]:
    snapshot = CreateToolhelp32Snapshot(
        TH32CS_SNAPMODULE | TH32CS_SNAPMODULE32,
        process.pid,
    )
    if _handle_value(snapshot) == INVALID_HANDLE_VALUE:
        if failures is not None:
            failures.append(
                ModuleSnapshotFailure(
                    pid=process.pid,
                    process_name=process.name,
                    stage="CreateToolhelp32Snapshot(module)",
                    error_code=ctypes.get_last_error(),
                )
            )
        return []

    try:
        entry = MODULEENTRY32W()
        entry.dwSize = ctypes.sizeof(MODULEENTRY32W)
        modules: list[ModuleInfo] = []
        if not Module32FirstW(snapshot, ctypes.byref(entry)):
            if failures is not None:
                failures.append(
                    ModuleSnapshotFailure(
                        pid=process.pid,
                        process_name=process.name,
                        stage="Module32FirstW",
                        error_code=ctypes.get_last_error(),
                    )
                )
            return modules
        while True:
            modules.append(
                ModuleInfo(
                    pid=process.pid,
                    process_name=process.name,
                    parent_pid=process.parent_pid,
                    module_name=entry.szModule,
                    module_path=entry.szExePath,
                    base_address=ctypes.addressof(entry.modBaseAddr.contents),
                    size=int(entry.modBaseSize),
                )
            )
            if not Module32NextW(snapshot, ctypes.byref(entry)):
                break
        return modules
    finally:
        _close_handle(snapshot)


def collect_ai_agent_modules(
    target_module: Path,
) -> tuple[list[ModuleInfo], list[ProcessInfo], list[ModuleSnapshotFailure], dict[str, Any]]:
    privilege = enable_debug_privilege()
    target_name = target_module.name.lower()
    processes = [
        process
        for process in iter_processes()
        if process.name.lower().startswith("trae")
    ]
    failures: list[ModuleSnapshotFailure] = []
    modules: list[ModuleInfo] = []
    for process in processes:
        for module in iter_modules(process, failures):
            if module.module_name.lower() == target_name:
                modules.append(module)
    return modules, processes, failures, privilege


def find_ai_agent_modules(target_module: Path) -> list[ModuleInfo]:
    modules, _, _, _ = collect_ai_agent_modules(target_module)
    return modules


def build_report(target_module: Path, rvas: dict[str, int]) -> dict[str, Any]:
    modules, processes, failures, privilege = collect_ai_agent_modules(target_module)
    return {
        "target_module": str(target_module),
        "module_count": len(modules),
        "trae_process_count": len(processes),
        "debug_privilege": privilege,
        "module_snapshot_failures": [
            {
                "pid": failure.pid,
                "process_name": failure.process_name,
                "stage": failure.stage,
                "error_code": failure.error_code,
            }
            for failure in failures[:20]
        ],
        "module_snapshot_failure_count": len(failures),
        "rvas": {name: hex(rva) for name, rva in rvas.items()},
        "processes": [
            {
                "pid": module.pid,
                "process_name": module.process_name,
                "parent_pid": module.parent_pid,
                "module_path": module.module_path,
                "module_base": hex(module.base_address),
                "module_size": hex(module.size),
                "breakpoints": {
                    name: hex(module.base_address + rva)
                    for name, rva in rvas.items()
                },
                "x64dbg_commands": [
                    f"bp {hex(module.base_address + rva)}"
                    for rva in rvas.values()
                ],
            }
            for module in modules
        ],
    }


def parse_rva_pairs(values: list[str]) -> dict[str, int]:
    if not values:
        return dict(DEFAULT_RVAS)

    result: dict[str, int] = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"RVA 参数必须是 name=value: {value}")
        name, raw_rva = value.split("=", 1)
        result[name] = int(raw_rva, 0)
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="枚举加载 ai_agent.dll 的 Trae 进程，并把 RVA 转成运行时断点地址。"
    )
    parser.add_argument("--module-path", type=Path, default=AI_AGENT_DLL, help="目标模块")
    parser.add_argument(
        "--rva",
        action="append",
        default=[],
        help="追加断点 RVA，格式 name=0x1234；不传则使用当前 native 锚点",
    )
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    report = build_report(args.module_path, parse_rva_pairs(args.rva))

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    print(f"target_module: {report['target_module']}")
    print(f"module_count: {report['module_count']}")
    for process in report["processes"]:
        print(
            f"- pid={process['pid']} base={process['module_base']} "
            f"path={process['module_path']}"
        )
        print(f"  breakpoints: {process['breakpoints']}")
        print(f"  x64dbg_commands: {process['x64dbg_commands']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

