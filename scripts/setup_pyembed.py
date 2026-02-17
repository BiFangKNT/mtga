import os
import sys
import shutil
import subprocess
from pathlib import Path

# 配置路径
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PYEMBED_DIR = PROJECT_ROOT / "src-tauri" / "pyembed" / "python"
PYTHON_SRC_DIR = PROJECT_ROOT / "python-src"
PYTHON_EXE = sys.executable
PYTHON_PREFIX = Path(sys.prefix)
PYTHON_BASE_PREFIX = Path(sys.base_prefix)

def setup_pyembed():
    print(f"=== Setting up Python environment in {PYEMBED_DIR} ===")
    
    # 1. 清理旧环境
    if PYEMBED_DIR.exists():
        print("Cleaning old environment...")
        shutil.rmtree(PYEMBED_DIR)
    
    PYEMBED_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"Using Python from: {PYTHON_BASE_PREFIX}")
    
    # 2. 复制解释器和 DLL
    print("Copying python.exe and DLLs...")
    # Use base executable if in venv
    base_exe = PYTHON_BASE_PREFIX / "python.exe"
    if not base_exe.exists():
         # Fallback if base_exe not found (e.g. system python)
         base_exe = Path(sys.executable)
    
    shutil.copy2(base_exe, PYEMBED_DIR / "python.exe")
    
    # 复制根目录下的 DLL (python3.dll, python3x.dll, vcruntime140.dll 等)
    # Also copy from PYTHON_PREFIX/Library/bin if exists (common in Conda)
    dll_sources = [PYTHON_BASE_PREFIX, PYTHON_BASE_PREFIX / "Library" / "bin"]
    
    for source in dll_sources:
        if source.exists():
            print(f"Searching DLLs in {source}")
            for file in source.glob("*.dll"):
                # Avoid copying system dlls that might be huge or irrelevant if not careful, 
                # but for now copy all to be safe or specific ones like python*.dll, vcruntime*.dll, libcrypto*.dll, libssl*.dll
                if file.name.lower().startswith(("python", "vcruntime", "libcrypto", "libssl", "ffi", "sqlite", "tcl", "tk", "zlib")):
                     print(f"Copying {file.name}")
                     shutil.copy2(file, PYEMBED_DIR / file.name)
    
    # Also copy DLLs directory if it exists (standard python)
    src_dlls = PYTHON_BASE_PREFIX / "DLLs"
    if src_dlls.exists():
        print("Copying DLLs directory...")
        shutil.copytree(src_dlls, PYEMBED_DIR / "DLLs", dirs_exist_ok=True)
    
    # 2.5 Copy libs directory (for building Rust extensions)
    src_libs = PYTHON_BASE_PREFIX / "libs"
    if src_libs.exists():
        print("Copying libs directory...")
        shutil.copytree(src_libs, PYEMBED_DIR / "libs", dirs_exist_ok=True)
        
    # 3. 复制标准库 (Lib)
    print("Copying standard library...")
    src_lib = PYTHON_BASE_PREFIX / "Lib"
    dest_lib = PYEMBED_DIR / "Lib"
    
    # 复制 Lib 目录，排除 site-packages (我们会单独安装依赖)
    shutil.copytree(src_lib, dest_lib, ignore=shutil.ignore_patterns("site-packages", "__pycache__", "*.pyc"))
    
    # 确保 site-packages 目录存在
    site_packages = dest_lib / "site-packages"
    site_packages.mkdir(exist_ok=True)
    
    # 4. 安装依赖
    print("Installing dependencies...")
    # 使用 pip 安装 python-src 及其依赖到 site-packages
    try:
        # Check if uv is available
        uv_path = shutil.which("uv")
        if uv_path:
            print("Using uv for installation...")
            # uv pip install needs --python to resolve correctly for the target environment
            # or we assume current environment is compatible.
            # Using --python PYTHON_EXE ensures compatibility.
            cmd = [
                uv_path, "pip", "install",
                str(PYTHON_SRC_DIR),
                "--target", str(site_packages),
                "--no-cache-dir",
                "--upgrade",
                "--python", str(base_exe)
            ]
        else:
            print("Using pip for installation...")
            cmd = [
                PYTHON_EXE, "-m", "pip", "install", 
                str(PYTHON_SRC_DIR),
                "--target", str(site_packages),
                "--no-cache-dir",
                "--upgrade"
            ]
            
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError as e:
        print(f"Dependency installation failed: {e}")
        sys.exit(1)
    
    # 5. 复制 .env
    print("Copying .env...")
    env_file = PROJECT_ROOT / ".env"
    if not env_file.exists():
        with open(env_file, "w", encoding="utf-8") as f:
            f.write("MTGA_ENV=prod\n")
    
    shutil.copy2(env_file, dest_lib / ".env")
    
    print("=== Python environment setup complete! ===")

if __name__ == "__main__":
    setup_pyembed()
