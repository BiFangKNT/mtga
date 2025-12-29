"""
macOS 管理员权限持久化辅助模块。

该模块会在第一次需要提权时通过 osascript 启动一个以 root 运行的
Python helper，后续通过 Unix Socket 与其通信，在 GUI 关闭时主动释放。
"""

from __future__ import annotations

import argparse
import atexit
import json
import os
import shlex
import shutil
import socket
import subprocess
import sys
import threading
import time
import uuid
from collections.abc import Mapping
from contextlib import suppress
from pathlib import Path
from typing import Any

try:
    from modules.runtime.resource_manager import is_packaged
except ImportError:
    # 作为脚本运行时，没有包上下文，补充模块搜索路径
    import sys

    project_root = Path(__file__).resolve().parents[2]
    if str(project_root) not in sys.path:
        sys.path.append(str(project_root))
    from modules.runtime.resource_manager import is_packaged

JsonDict = dict[str, Any]
JsonMapping = Mapping[str, Any]

REQUEST_TERMINATOR = b"\n"
CONNECT_TIMEOUT = 12.0
RETRY_DELAY = 0.15
HELPER_FLAG = "--run-macos-helper"
_SOCKET_FAMILY_UNIX = getattr(socket, "AF_UNIX", None)


class MacPrivilegeSessionError(RuntimeError):
    """代表持久化提权通信过程中的错误。"""


class MacPrivilegeSession:
    """与 root helper 通信的客户端，实现写文件/复制/运行命令等能力。"""

    def __init__(self) -> None:
        self.owner_uid = getattr(os, "getuid", lambda: 0)()
        self.owner_gid = getattr(os, "getgid", lambda: 0)()
        base_dir = Path("/tmp/mtga_gui_privileged") / str(self.owner_uid)
        base_dir.mkdir(parents=True, exist_ok=True)
        base_dir.chmod(0o700)
        unique = f"{os.getpid()}_{uuid.uuid4().hex}"
        self.base_dir = base_dir
        self.socket_path = str(base_dir / f"hosts_helper_{unique}.sock")
        self.helper_log_path = str(base_dir / f"hosts_helper_{uuid.uuid4().hex}.log")
        self._connection: socket.socket | None = None
        self._recv_buffer = b""
        self._helper_started = False
        self._lock = threading.Lock()
        self._atexit_registered = False
        self._connect_logged_wait = False
        self._security_session = os.environ.get("SECURITYSESSIONID")

    def ensure_ready(self, log_func=print) -> bool:
        """确保 helper 已经启动并建立 socket 连接。"""
        if sys.platform != "darwin":
            log_func("⚠️ macOS 持久化提权仅在 macOS 平台生效")
            return False

        if self._connection:
            return True

        if self._helper_started and not os.path.exists(self.socket_path):
            # helper 异常退出，需重新启动
            self._helper_started = False

        if not self._helper_started:
            if not self._start_helper(log_func):
                return False
            self._helper_started = True

        return self._connect(log_func)

    def write_file(self, path: str, content: str, encoding: str, log_func=print) -> bool:
        """以管理员权限写入文本文件。"""
        payload = {
            "action": "write_file",
            "path": path,
            "content": content,
            "encoding": encoding,
        }
        response = self._send_payload(payload, log_func)
        if not response:
            return False
        if response.get("ok"):
            return True
        log_func(f"⚠️ 写入 {path} 失败: {response.get('error')}")
        return False

    def copy_file(self, src: str, dst: str, log_func=print) -> bool:
        """复制文件，可用于 hosts 备份/还原等场景。"""
        payload = {"action": "copy_file", "src": src, "dst": dst}
        response = self._send_payload(payload, log_func)
        if not response:
            return False
        if response.get("ok"):
            return True
        log_func(f"⚠️ 复制 {src} -> {dst} 失败: {response.get('error')}")
        return False

    def run_command(self, cmd: list[str], log_func=print) -> tuple[bool, JsonDict]:
        """运行命令（例如 open -t /etc/hosts），返回 (success, data)。"""
        payload = {"action": "run_command", "cmd": cmd}
        response = self._send_payload(payload, log_func)
        if not response:
            return False, {"error": "通信失败"}
        if response.get("ok"):
            return True, response.get("data", {})
        raw_data = response.get("data")
        data: JsonDict = raw_data if isinstance(raw_data, dict) else {}
        data.setdefault("error", response.get("error", "未知错误"))
        return False, data

    def install_trusted_cert(
        self,
        cert_path: str,
        *,
        keychain: str = "/Library/Keychains/System.keychain",
        log_func=print,
    ) -> tuple[bool, JsonDict]:
        """使用管理员权限安装并信任 CA 证书，返回 (success, data)。"""
        if not cert_path:
            return False, {"error": "证书路径为空"}

        base_cmd: list[str] = [
            "security",
            "add-trusted-cert",
            "-d",
            "-r",
            "trustRoot",
            "-k",
            keychain,
            cert_path,
        ]
        cmd = base_cmd
        if sys.platform == "darwin" and self.owner_uid:
            cmd = ["launchctl", "asuser", str(self.owner_uid)]
            if self._security_session:
                cmd.extend(["env", f"SECURITYSESSIONID={self._security_session}"])
            cmd.extend(base_cmd)
        success, data = self.run_command(cmd, log_func=log_func)
        if success or cmd == base_cmd:
            return success, data

        # 回退使用直接 security 命令，避免 launchctl 不可用时失败
        return self.run_command(base_cmd, log_func=log_func)

    def shutdown(self) -> None:
        """GUI 退出时关闭 helper。"""
        if not self._helper_started:
            return
        payload = {"action": "shutdown"}
        try:
            self._send_payload(payload, log_func=lambda *_: None, allow_retry=False)
        except MacPrivilegeSessionError:
            pass
        finally:
            self._cleanup_connection()
            self._helper_started = False

    def _start_helper(self, log_func) -> bool:
        if is_packaged():
            launcher = self._locate_packaged_launcher()
            if not launcher:
                log_func("⚠️ 无法找到打包后的可执行文件，无法申请管理员权限")
                return False
            cmd_parts = [
                shlex.quote(str(launcher)),
                HELPER_FLAG,
                "--socket",
                shlex.quote(self.socket_path),
                "--owner-uid",
                str(self.owner_uid),
                "--owner-gid",
                str(self.owner_gid),
            ]
        else:
            python_exec = self._locate_python_executable()
            if not python_exec:
                log_func(f"⚠️ 无法定位 Python 解释器: {sys.executable}")
                return False
            helper_path = Path(__file__).resolve()
            cmd_parts = [
                shlex.quote(str(python_exec)),
                shlex.quote(str(helper_path)),
                HELPER_FLAG,
                "--socket",
                shlex.quote(self.socket_path),
                "--owner-uid",
                str(self.owner_uid),
                "--owner-gid",
                str(self.owner_gid),
            ]

        log_func("🔐 正在请求管理员权限，请在弹窗中输入密码...")
        helper_cmd = " ".join(cmd_parts)
        if self._security_session:
            helper_cmd = f"SECURITYSESSIONID={shlex.quote(self._security_session)} " + helper_cmd
        helper_cmd += f" >> {shlex.quote(self.helper_log_path)} 2>&1 &"
        script = f'do shell script "{helper_cmd}" with administrator privileges'
        result = subprocess.run(
            ["osascript", "-e", script], capture_output=True, text=True, check=False
        )
        if result.returncode != 0:
            message = result.stderr.strip() or result.stdout.strip() or "未知错误"
            log_func(f"⚠️ 无法获取管理员权限: {message}")
            return False
        log_func("✅ 管理员权限已授权，正在建立通信通道...")
        return True

    def _locate_packaged_launcher(self) -> Path | None:
        argv0 = Path(sys.argv[0]).resolve()
        if argv0.is_file():
            return argv0

        exec_path = Path(sys.executable)
        exec_dir = exec_path.parent if exec_path.exists() else Path.cwd()
        candidates = sorted(exec_dir.glob("MTGA_GUI-*"))
        for candidate in candidates:
            if candidate.is_file() and os.access(candidate, os.X_OK):
                return candidate
        return None

    def _locate_python_executable(self) -> Path | None:
        candidates: list[Path] = []
        exec_path = Path(sys.executable)
        if exec_path.is_file():
            candidates.append(exec_path)
        for bin_name in ("python3", "python"):
            found = shutil.which(bin_name)
            if found:
                candidates.append(Path(found))
        for candidate in candidates:
            if candidate and candidate.is_file():
                return candidate
        return None

    def _connect(self, log_func) -> bool:
        if not self._connect_logged_wait:
            log_func("⌛ 正在初始化管理员通信通道，请稍候...")
            self._connect_logged_wait = True
        deadline = time.time() + CONNECT_TIMEOUT
        while time.time() < deadline:
            try:
                if _SOCKET_FAMILY_UNIX is None:
                    log_func("当前系统不支持 Unix Socket，无法建立连接")
                    break
                conn = socket.socket(_SOCKET_FAMILY_UNIX, socket.SOCK_STREAM)
                conn.connect(self.socket_path)
                self._connection = conn
                self._recv_buffer = b""
                self._register_atexit()
                self._connect_logged_wait = False
                log_func("🔗 管理员通信通道已就绪")
                return True
            except FileNotFoundError:
                time.sleep(RETRY_DELAY)
            except ConnectionRefusedError:
                time.sleep(RETRY_DELAY)
            except OSError:
                time.sleep(RETRY_DELAY)

        self._connect_logged_wait = False
        log_func(f"⚠️ 管理员权限通道初始化失败，请重试（日志: {self.helper_log_path}）")
        self._cleanup_connection()
        return False

    def _send_payload(
        self,
        payload: JsonMapping,
        log_func,
        *,
        allow_retry: bool = True,
    ) -> JsonDict | None:
        with self._lock:
            attempts = 2 if allow_retry else 1
            payload_json = dict(payload)
            data = json.dumps(payload_json, ensure_ascii=False).encode("utf-8") + REQUEST_TERMINATOR
            for _ in range(attempts):
                if not self.ensure_ready(log_func):
                    return None
                try:
                    assert self._connection is not None
                    self._connection.sendall(data)
                    line = self._readline()
                    return json.loads(line.decode("utf-8"))
                except (OSError, ConnectionError, json.JSONDecodeError):
                    self._cleanup_connection()
                    time.sleep(RETRY_DELAY)

        raise MacPrivilegeSessionError("无法与管理员权限 helper 通信")

    def _readline(self) -> bytes:
        if not self._connection:
            raise ConnectionError("连接尚未建立")

        while True:
            if REQUEST_TERMINATOR in self._recv_buffer:
                line, self._recv_buffer = self._recv_buffer.split(REQUEST_TERMINATOR, 1)
                return line
            chunk = self._connection.recv(4096)
            if not chunk:
                raise ConnectionError("helper 已关闭连接")
            self._recv_buffer += chunk

    def _cleanup_connection(self) -> None:
        if self._connection:
            with suppress(OSError):
                self._connection.close()
        self._connection = None
        self._recv_buffer = b""
        self._connect_logged_wait = False

    def _register_atexit(self) -> None:
        if self._atexit_registered:
            return
        self._atexit_registered = True
        atexit.register(self.shutdown)


_mac_session_holder: dict[str, MacPrivilegeSession | None] = {"session": None}
_mac_session_lock = threading.Lock()


def get_mac_privileged_session(log_func=print) -> MacPrivilegeSession | None:
    """返回可用的 MacPrivilegeSession，没有可用权限时返回 None。"""
    if sys.platform != "darwin":
        return None

    with _mac_session_lock:
        session = _mac_session_holder["session"]
        if session is None:
            session = MacPrivilegeSession()
            _mac_session_holder["session"] = session

    if session.ensure_ready(log_func):
        return session
    return None


class _PrivilegeHelperServer:
    """运行在 root 下的 helper，实现具体的提权操作。"""

    def __init__(self, socket_path: str, owner_uid: int, owner_gid: int) -> None:
        self.socket_path = socket_path
        self.owner_uid = owner_uid
        self.owner_gid = owner_gid
        self._stop = False

    def run(self) -> None:
        with suppress(FileNotFoundError):
            os.remove(self.socket_path)

        if _SOCKET_FAMILY_UNIX is None:
            return

        server_socket = socket.socket(_SOCKET_FAMILY_UNIX, socket.SOCK_STREAM)
        server_socket.bind(self.socket_path)
        chown_fn = getattr(os, "chown", None)
        if callable(chown_fn):
            chown_fn(self.socket_path, self.owner_uid, self.owner_gid)
        os.chmod(self.socket_path, 0o600)
        server_socket.listen(1)

        try:
            while not self._stop:
                conn, _ = server_socket.accept()
                try:
                    self._handle_connection(conn)
                finally:
                    with suppress(OSError):
                        conn.close()
        finally:
            with suppress(FileNotFoundError):
                os.remove(self.socket_path)
            with suppress(OSError):
                server_socket.close()

    def _handle_connection(self, conn: socket.socket) -> None:
        buffer = b""
        while not self._stop:
            data = conn.recv(4096)
            if not data:
                break
            buffer += data
            while REQUEST_TERMINATOR in buffer:
                line, buffer = buffer.split(REQUEST_TERMINATOR, 1)
                if not line:
                    continue
                response = self._process_request(line)
                conn.sendall(response + REQUEST_TERMINATOR)
                if self._stop:
                    return

    def _process_request(self, line: bytes) -> bytes:
        try:
            payload = json.loads(line.decode("utf-8"))
        except json.JSONDecodeError:
            return json.dumps({"ok": False, "error": "无效的 JSON 请求"}).encode("utf-8")

        action = payload.get("action")
        try:
            if action == "write_file":
                path = payload["path"]
                encoding = payload.get("encoding", "utf-8")
                content = payload["content"]
                with open(path, "w", encoding=encoding) as fh:
                    fh.write(content)
                result = {"ok": True}
            elif action == "copy_file":
                shutil.copy2(payload["src"], payload["dst"])
                result = {"ok": True}
            elif action == "run_command":
                cmd = payload["cmd"]
                if not isinstance(cmd, list) or not all(isinstance(item, str) for item in cmd):
                    raise ValueError("cmd 必须是字符串列表")
                completed = subprocess.run(
                    cmd, capture_output=True, text=True, check=False
                )
                result = {
                    "ok": completed.returncode == 0,
                    "data": {
                        "returncode": completed.returncode,
                        "stdout": completed.stdout,
                        "stderr": completed.stderr,
                    },
                }
            elif action == "shutdown":
                self._stop = True
                result = {"ok": True}
            else:
                result = {"ok": False, "error": f"未知 action: {action}"}
        except Exception as exc:
            result = {"ok": False, "error": str(exc)}

        return json.dumps(result, ensure_ascii=False).encode("utf-8")


def _parse_server_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="macOS privileged helper")
    parser.add_argument(
        HELPER_FLAG,
        "--run-server",
        action="store_true",
        dest="run_helper",
        help="启动 helper",
    )
    parser.add_argument("--socket", dest="socket_path", required=True, help="Socket 路径")
    parser.add_argument("--owner-uid", type=int, required=True, help="原始用户 UID")
    parser.add_argument("--owner-gid", type=int, required=True, help="原始用户 GID")
    return parser.parse_args()


def main() -> None:
    """当以脚本方式运行时，启动 root helper。"""
    args = _parse_server_args()
    if not getattr(args, "run_helper", False):
        return

    server = _PrivilegeHelperServer(
        socket_path=args.socket_path, owner_uid=args.owner_uid, owner_gid=args.owner_gid
    )
    server.run()


if __name__ == "__main__":
    main()
