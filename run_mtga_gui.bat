@echo off
setlocal enabledelayedexpansion

:: 设置标题
title MTGA GUI 启动器

:: 设置颜色
color 0A

:: 获取当前脚本所在目录
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

:: 设置Python虚拟环境路径
set "VENV_DIR=%SCRIPT_DIR%\.venv"
set "VENV_PYTHON=%VENV_DIR%\Scripts\python.exe"

:: 设置OpenSSL路径
set "OPENSSL_DIR=%SCRIPT_DIR%\openssl"

:: 检查虚拟环境是否存在
if not exist "%VENV_PYTHON%" (
    echo 错误: Python虚拟环境不存在: %VENV_PYTHON%
    echo 请确保已正确安装虚拟环境。
    pause
    exit /b 1
)

:: 检查OpenSSL是否存在
if not exist "%OPENSSL_DIR%\openssl.exe" (
    echo 错误: OpenSSL不存在: %OPENSSL_DIR%\openssl.exe
    echo 请确保OpenSSL已正确安装。
    pause
    exit /b 1
)

:: 检查主程序是否存在
if not exist "%SCRIPT_DIR%\mtga_gui.py" (
    echo 错误: 主程序不存在: %SCRIPT_DIR%\mtga_gui.py
    echo 请确保程序文件完整。
    pause
    exit /b 1
)

:: 设置环境变量
set "PATH=%OPENSSL_DIR%;%PATH%"
set "PYTHONPATH=%SCRIPT_DIR%;%PYTHONPATH%"

echo ====================================
echo MTGA GUI 启动器
echo ====================================
echo 正在启动程序，请稍候...

:: 使用虚拟环境中的Python启动程序
"%VENV_PYTHON%" "%SCRIPT_DIR%\mtga_gui.py"

:: 如果程序异常退出，暂停显示错误信息
if %ERRORLEVEL% neq 0 (
    echo.
    echo 程序异常退出，错误代码: %ERRORLEVEL%
    pause
)

endlocal 