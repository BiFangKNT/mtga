@echo off
setlocal enabledelayedexpansion

:: 设置标题
title MTGA GUI 启动器

:: 设置颜色
color 0A

:: 获取当前脚本所在目录
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

:: 检查是否是重启后的进程
if "%~1"=="/RESTARTED" goto PYTHON_INSTALLED

:: 检查Python是否已安装
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Python未安装，开始自动安装Python 3.13...
    
    :: 检查安装包是否存在
    set "PYTHON_INSTALLER=%SCRIPT_DIR%\python-3.13.3-amd64.exe"
    if not exist "!PYTHON_INSTALLER!" (
        echo 错误: Python安装包不存在: !PYTHON_INSTALLER!
        echo 请下载Python 3.13安装包到程序目录。
        pause
        exit /b 1
    )
    
    :: 静默安装Python
    echo 正在静默安装Python 3.13，请稍候...
    "!PYTHON_INSTALLER!" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    if %ERRORLEVEL% neq 0 (
        echo Python安装失败，错误代码: %ERRORLEVEL%
        pause
        exit /b 1
    )
    
    echo Python 3.13已安装成功，正在重启批处理文件以加载新的环境变量...
    
    :: 创建一个临时重启脚本
    set "RESTART_SCRIPT=%TEMP%\restart_mtga.bat"
    echo @echo off > "!RESTART_SCRIPT!"
    echo timeout /t 1 >> "!RESTART_SCRIPT!"
    echo start "" "%~f0" /RESTARTED >> "!RESTART_SCRIPT!"
    echo exit >> "!RESTART_SCRIPT!"
    
    :: 启动重启脚本并退出当前脚本
    start "" "!RESTART_SCRIPT!"
    exit /b 0
)

:PYTHON_INSTALLED
:: 检查Python版本
for /f "tokens=2" %%a in ('python -c "import sys; print(sys.version.split()[0])"') do set "PYTHON_VERSION=%%a"
echo 检测到Python版本: !PYTHON_VERSION!

:: 设置Python虚拟环境路径
set "VENV_DIR=%SCRIPT_DIR%\.venv"
set "VENV_PYTHON=%VENV_DIR%\Scripts\python.exe"
set "VENV_ACTIVATE=%VENV_DIR%\Scripts\activate.bat"

:: 设置OpenSSL路径
set "OPENSSL_DIR=%SCRIPT_DIR%\openssl"

:: 检查虚拟环境是否存在
if not exist "%VENV_PYTHON%" (
    echo 虚拟环境不存在，开始创建...
    
    :: 检查uv是否已安装
    where uv >nul 2>nul
    if %ERRORLEVEL% neq 0 (
        echo 正在安装uv...
        pip install uv
        if %ERRORLEVEL% neq 0 (
            echo 安装uv失败，请手动安装：pip install uv
            pause
            exit /b 1
        )
    )
    
    :: 创建虚拟环境
    echo 正在创建虚拟环境...
    uv venv
    if %ERRORLEVEL% neq 0 (
        echo 创建虚拟环境失败
        pause
        exit /b 1
    )
    
    :: 激活虚拟环境
    echo 正在激活虚拟环境...
    call "%VENV_ACTIVATE%"
    
    :: 安装依赖
    echo 正在安装依赖...
    uv pip install -r "%SCRIPT_DIR%\requirements.txt"
    if %ERRORLEVEL% neq 0 (
        echo 安装依赖失败
        pause
        exit /b 1
    )
    
    echo 虚拟环境和依赖安装完成！
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