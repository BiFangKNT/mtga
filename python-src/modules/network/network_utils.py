from __future__ import annotations

import contextlib
import os
import socket
import subprocess

DEFAULT_PORT_SCAN_ATTEMPTS = 16
TASKLIST_MIN_COLUMNS = 2
NETSTAT_LISTEN_COLUMNS = 5


def is_host_port_open(host: str, port: int, *, timeout: float = 0.2) -> bool:
    with contextlib.suppress(OSError), socket.create_connection((host, port), timeout=timeout):
        return True
    return False


def iter_port_candidates(
    preferred_port: int,
    *,
    max_tries: int = DEFAULT_PORT_SCAN_ATTEMPTS,
) -> range:
    return range(preferred_port, preferred_port + max_tries)


def is_port_in_use(port: int) -> bool:
    checks = [("127.0.0.1", socket.AF_INET)]
    if socket.has_ipv6:
        checks.append(("::1", socket.AF_INET6))

    for host, family in checks:
        with socket.socket(family, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.2)
            try:
                if sock.connect_ex((host, port)) == 0:
                    return True
            except OSError:
                continue
    return False


def get_tcp_listener_pids(port: int) -> list[int]:
    if os.name != "nt":
        return []

    pids = _get_tcp_listener_pids_from_powershell(port)
    if pids:
        return pids
    return _get_tcp_listener_pids_from_netstat(port)


def get_process_name(pid: int) -> str | None:
    if os.name != "nt":
        return None

    try:
        completed = subprocess.run(
            [
                "tasklist",
                "/FI",
                f"PID eq {pid}",
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
        return None

    for raw_line in completed.stdout.splitlines():
        line = raw_line.strip()
        if not line or "INFO:" in line:
            continue
        columns = [part.strip().strip('"') for part in line.split(",")]
        if len(columns) < TASKLIST_MIN_COLUMNS:
            continue
        return columns[0] or None
    return None


def get_tcp_listener_process_names(port: int) -> list[str]:
    names: list[str] = []
    for pid in get_tcp_listener_pids(port):
        name = get_process_name(pid)
        if name and name not in names:
            names.append(name)
    return names


def _get_tcp_listener_pids_from_powershell(port: int) -> list[int]:
    command = (
        f"$items = @(Get-NetTCPConnection -State Listen -LocalPort {port} "
        "-ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess); "
        "$items | ForEach-Object { $_ }"
    )
    try:
        completed = subprocess.run(
            ["powershell.exe", "-Command", command],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=4,
        )
    except Exception:
        return []

    pids: list[int] = []
    for raw_line in completed.stdout.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        with contextlib.suppress(ValueError):
            pid = int(line)
            if pid not in pids:
                pids.append(pid)
    return pids


def _get_tcp_listener_pids_from_netstat(port: int) -> list[int]:
    try:
        completed = subprocess.run(
            ["netstat", "-ano", "-p", "tcp"],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=4,
        )
    except Exception:
        return []

    pids: list[int] = []
    for raw_line in completed.stdout.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        columns = line.split()
        if len(columns) < NETSTAT_LISTEN_COLUMNS or columns[0].upper() != "TCP":
            continue
        local_endpoint = columns[1]
        foreign_endpoint = columns[2]
        pid_text = columns[-1]
        local_port = _extract_endpoint_port(local_endpoint)
        foreign_port = _extract_endpoint_port(foreign_endpoint)
        if local_port != port or foreign_port != 0:
            continue
        with contextlib.suppress(ValueError):
            pid = int(pid_text)
            if pid not in pids:
                pids.append(pid)
    return pids


def _extract_endpoint_port(endpoint: str) -> int | None:
    if endpoint.startswith("["):
        closing = endpoint.rfind("]:")
        if closing >= 0:
            with contextlib.suppress(ValueError):
                return int(endpoint[closing + 2 :])
        return None
    if ":" not in endpoint:
        return None
    with contextlib.suppress(ValueError):
        return int(endpoint.rsplit(":", maxsplit=1)[1])
    return None
