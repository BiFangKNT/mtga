"""
资源路径管理模块（tauri 统一实现）
处理开发环境和 tauri 打包环境的资源路径问题。
"""

import os
import shutil
import sys
import tempfile
from collections.abc import Callable
from importlib import resources
from pathlib import Path

from platformdirs import user_data_dir

# 资源路径开关（显眼开关）
# - MTGA_RESOURCE_DIR=... 指定资源目录（最高优先级）
# - 未设置时按“包资源 -> 本地 modules/resources -> 运行时回退目录”自动探测
RESOURCE_DIR = os.environ.get("MTGA_RESOURCE_DIR", "").strip()
LOGS_DIR_NAME = "logs"
LEGACY_USER_DATA_DIR_NAME = ".mtga"


def safe_print(message: object) -> None:
    """Print helper tolerant of non-ASCII stdout."""
    try:
        print(message)
    except UnicodeEncodeError:
        fallback = str(message).encode("unicode_escape").decode("ascii", errors="replace")
        print(fallback)


def _tauri_runtime_provider() -> str:
    runtime = os.environ.get("MTGA_RUNTIME", "").strip().lower()
    if runtime == "tauri":
        return "tauri"
    return "dev"


_PACKAGING_RUNTIME_PROVIDER: dict[str, Callable[[], str]] = {
    "provider": _tauri_runtime_provider
}


def set_packaging_runtime_provider(provider: Callable[[], str]) -> None:
    """注入运行时判定逻辑。默认使用 tauri/dev 判定。"""
    _PACKAGING_RUNTIME_PROVIDER["provider"] = provider


def get_packaging_runtime() -> str:
    """检测运行时类型：tauri / dev。"""
    return _PACKAGING_RUNTIME_PROVIDER["provider"]()


def is_packaged() -> bool:
    """检测是否在打包环境中运行（tauri）。"""
    return get_packaging_runtime() != "dev"


def get_user_data_dir() -> str:
    """获取用户数据目录，用于持久化存储。"""
    app_name = "MTGA"
    roaming = os.name == "nt"
    platform_dir = user_data_dir(app_name, appauthor=False, roaming=roaming)

    os.makedirs(platform_dir, exist_ok=True)
    return platform_dir


def get_legacy_user_data_dir() -> str:
    """获取历史遗留用户数据目录路径。"""
    return os.path.join(os.path.expanduser("~"), LEGACY_USER_DATA_DIR_NAME)


def has_legacy_user_data_dir() -> bool:
    """检测是否存在仍可能包含旧数据的历史目录。"""
    if os.name == "nt":
        return False
    legacy_dir = get_legacy_user_data_dir()
    if not os.path.isdir(legacy_dir):
        return False
    try:
        return len(os.listdir(legacy_dir)) > 0
    except Exception:
        return True


def _get_packaged_resource_dir() -> str | None:
    try:
        base = resources.files("modules") / "resources"
        if base.is_dir():
            with resources.as_file(base) as path:
                return str(path)
    except Exception:
        return None
    return None


def _get_local_resource_dir() -> str | None:
    path = Path(__file__).resolve().parent.parent / "resources"
    if path.is_dir():
        return str(path)
    return None


def get_program_resource_dir() -> str:
    """获取程序资源目录（临时目录，包含配置模板等）"""
    runtime = get_packaging_runtime()
    override_dir = RESOURCE_DIR
    packaged_dir = _get_packaged_resource_dir()
    local_dir = _get_local_resource_dir()
    resource_dir = override_dir or packaged_dir or local_dir
    if resource_dir:
        return resource_dir

    if runtime == "dev":
        # 开发环境使用项目根目录
        return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    exe_dir = os.path.dirname(sys.executable)
    # tauri 打包环境统一使用可执行文件目录
    return exe_dir


def get_base_path() -> str:
    """获取程序基础路径（兼容旧接口）"""
    return get_program_resource_dir()


def get_resource_path(relative_path: str) -> str:
    """
    获取程序资源文件的绝对路径（配置模板等）

    参数:
        relative_path: 相对于程序资源目录的路径

    返回:
        绝对路径字符串
    """
    base_path = get_program_resource_dir()
    return os.path.join(base_path, relative_path)


def get_user_data_path(relative_path: str) -> str:
    """
    获取用户数据文件的绝对路径（配置、证书、备份等）

    参数:
        relative_path: 相对于用户数据目录的路径

    返回:
        绝对路径字符串
    """
    user_dir = get_user_data_dir()
    return os.path.join(user_dir, relative_path)


def get_logs_dir() -> str:
    """获取日志目录路径（用户数据目录/logs）。"""
    logs_dir = get_user_data_path(LOGS_DIR_NAME)
    os.makedirs(logs_dir, exist_ok=True)
    return logs_dir


def get_log_path(filename: str) -> str:
    """获取日志文件路径（用户数据目录/logs）。"""
    return os.path.join(get_logs_dir(), filename)


def get_ca_path() -> str:
    """获取 CA 目录路径（用户数据目录）"""
    return get_user_data_path("ca")


def get_ca_template_path() -> str:
    """获取 CA 配置模板目录路径（程序资源目录）"""
    return get_resource_path("ca")


def get_temp_dir() -> str:
    """获取临时文件目录"""
    return tempfile.gettempdir()


def ensure_directory_exists(path: str) -> None:
    """确保目录存在，如果不存在则创建"""
    os.makedirs(path, exist_ok=True)


def copy_template_files() -> list[str]:
    """将配置模板文件复制到用户数据目录"""
    template_ca_dir = get_ca_template_path()
    user_ca_dir = get_ca_path()

    # 确保用户CA目录存在
    ensure_directory_exists(user_ca_dir)

    # 需要复制的模板文件
    template_files = [
        "README.md",
        "api.openai.com.cnf",
        "api.openai.com.subj",
        "genca.sh",
        "gencrt.sh",
        "google.cnf",
        "google.subj",
        "openssl.cnf",
        "pixiv.cnf",
        "pixiv.subj",
        "v3_ca.cnf",
        "v3_req.cnf",
        "youtube.cnf",
        "youtube.subj",
    ]

    copied_files: list[str] = []
    for filename in template_files:
        src_path = os.path.join(template_ca_dir, filename)
        dst_path = os.path.join(user_ca_dir, filename)

        # 只在目标文件不存在时复制
        if os.path.exists(src_path) and not os.path.exists(dst_path):
            try:
                shutil.copy2(src_path, dst_path)
                copied_files.append(filename)
            except Exception:
                pass

    return copied_files


class ResourceManager:
    """资源管理器类，提供统一的资源访问接口"""

    def __init__(self) -> None:
        self.program_resource_dir = get_program_resource_dir()
        self.user_data_dir = get_user_data_dir()
        self.ca_path = get_ca_path()
        self.ca_template_path = get_ca_template_path()

        # 初始化时复制模板文件
        self._ensure_user_data_setup()

    def _ensure_user_data_setup(self) -> None:
        """确保用户数据目录设置正确"""
        # 复制配置模板文件到用户目录
        copied_files = copy_template_files()
        if copied_files:
            safe_print(f"已复制模板文件到用户目录: {', '.join(copied_files)}")

    @property
    def base_path(self) -> str:
        """基础路径（兼容旧接口）"""
        return self.program_resource_dir

    def get_cert_file(self, domain: str = "api.openai.com") -> str:
        """获取证书文件路径（用户数据目录）"""
        return os.path.join(self.ca_path, f"{domain}.crt")

    def get_key_file(self, domain: str = "api.openai.com") -> str:
        """获取私钥文件路径（用户数据目录）"""
        return os.path.join(self.ca_path, f"{domain}.key")

    def get_ca_cert_file(self) -> str:
        """获取 CA 证书文件路径（用户数据目录）"""
        return os.path.join(self.ca_path, "ca.crt")

    def get_ca_key_file(self) -> str:
        """获取 CA 私钥文件路径（用户数据目录）"""
        return os.path.join(self.ca_path, "ca.key")

    def get_ca_info_file(self) -> str:
        """获取 CA 元数据文件路径（用户数据目录）"""
        return os.path.join(self.ca_path, "ca_info.json")

    def get_config_file(self, filename: str) -> str:
        """获取配置文件路径（用户数据目录）"""
        return os.path.join(self.ca_path, filename)

    def get_icon_file(self, filename: str) -> str:
        """获取图标文件路径（程序资源目录）"""
        return os.path.join(self.program_resource_dir, "icons", filename)

    def get_user_config_file(self) -> str:
        """获取用户配置文件路径"""
        return get_user_data_path("mtga_config.yaml")

    def get_hosts_backup_file(self) -> str:
        """获取 hosts 备份文件路径"""
        return get_user_data_path("hosts.backup")

    def get_logs_dir(self) -> str:
        """获取日志目录路径"""
        return get_logs_dir()

    def get_log_file(self, filename: str) -> str:
        """获取日志文件路径"""
        return get_log_path(filename)

    def check_resources(self) -> list[str]:
        """检查必要资源是否存在"""
        missing_resources: list[str] = []

        # 添加调试信息
        debug_info: list[str] = []
        debug_info.append(f"当前工作目录: {os.getcwd()}")
        debug_info.append(f"程序资源目录: {self.program_resource_dir}")
        debug_info.append(f"用户数据目录: {self.user_data_dir}")
        debug_info.append(f"CA目录: {self.ca_path}")
        debug_info.append("证书生成后端: cryptography")
        debug_info.append(f"运行环境: {get_packaging_runtime()}")

        # 如果是打包环境，显示额外的调试信息
        if is_packaged():
            debug_info.append(f"可执行文件路径: {sys.executable}")
            main_module = sys.modules.get("__main__")
            if main_module is not None:
                main_file = getattr(main_module, "__file__", None)
                if isinstance(main_file, str):
                    debug_info.append(f"主模块文件路径: {main_file}")

        # 打印调试信息
        safe_print("=== 资源路径调试信息 ===")
        for info in debug_info:
            safe_print(info)
        safe_print("=" * 30)

        # 检查 CA 目录（用户数据目录）
        if not os.path.exists(self.ca_path):
            missing_resources.append(f"CA目录: {self.ca_path}")

        return missing_resources
