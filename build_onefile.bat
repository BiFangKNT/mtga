@echo off
chcp 65001

REM ========== 版本配置 ==========
set "VERSION=1.2.0"
REM ================================

echo 正在使用 Nuitka 构建单文件版本...
echo 这可能需要较长时间（约40分钟），请耐心等待...
echo.

REM 检查虚拟环境是否存在
if not exist ".venv\Scripts\python.exe" (
    echo 错误：虚拟环境不存在，请先运行 uv sync --group win-build 安装依赖
    if defined GITHUB_ACTIONS (
        exit /b 1
    ) else (
        pause
        exit /b 1
    )
)

REM 检查是否存在可用的 Visual Studio MSVC 工具链
if not "%~1"=="" (
    set "VC_BUILD_DIR=%~1"
)

if defined VC_BUILD_DIR (
    if exist "%VC_BUILD_DIR%" (
        echo 使用外部提供的 MSVC 工具链目录：%VC_BUILD_DIR%
    ) else (
        echo 错误：传入的 MSVC 目录不存在：%VC_BUILD_DIR%
        if defined GITHUB_ACTIONS (
            exit /b 1
        ) else (
            pause
            exit /b 1
        )
    )
) else (
    set "PREFERRED_VS_DIR=C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build"
    if exist "%PREFERRED_VS_DIR%" (
        set "VC_BUILD_DIR=%PREFERRED_VS_DIR%"
    ) else (
        for %%I in (
            "C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Auxiliary\Build"
            "C:\Program Files\Microsoft Visual Studio\2022\Professional\VC\Auxiliary\Build"
            "C:\Program Files\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build"
            "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build"
            "C:\Program Files (x86)\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build"
            "C:\Program Files (x86)\Microsoft Visual Studio\2022\Enterprise\VC\Auxiliary\Build"
            "C:\Program Files (x86)\Microsoft Visual Studio\2022\Professional\VC\Auxiliary\Build"
            "C:\Program Files (x86)\Microsoft Visual Studio\2019\Enterprise\VC\Auxiliary\Build"
            "C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\VC\Auxiliary\Build"
            "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build"
            "C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\VC\Auxiliary\Build"
        ) do (
            if not defined VC_BUILD_DIR (
                if exist %%~I (
                    set "VC_BUILD_DIR=%%~I"
                )
            )
        )
    )

    if defined VC_BUILD_DIR (
        echo 找到 Visual Studio 工具链目录：%VC_BUILD_DIR%
    ) else (
        echo 错误：未找到可用的 Visual Studio 工具链，请先安装 Visual Studio（含 MSVC）
        if defined GITHUB_ACTIONS (
            exit /b 1
        ) else (
            pause
            exit /b 1
        )
    )
)

REM 写入内嵌版本号供打包读取
if defined MTGA_VERSION (
    set "APP_VERSION=%MTGA_VERSION%"
) else (
    set "APP_VERSION=%VERSION%"
)
if not "%APP_VERSION:~0,1%"=="v" (
    set "APP_VERSION=v%APP_VERSION%"
)
> "modules\runtime\_build_version.py" (
    echo BUILT_APP_VERSION = "%APP_VERSION%"
)
echo 已写入版本号到 modules\runtime\_build_version.py: %APP_VERSION%

REM 创建输出目录
if not exist "dist-onefile" mkdir dist-onefile

echo 正在构建单文件版本 (mtga_gui.py)...

REM 使用 uv 运行 Nuitka 构建单文件版本
uv run --python .venv\Scripts\python.exe nuitka ^
    --onefile ^
    --msvc=latest ^
    --show-progress ^
    --show-memory ^
    --output-dir=dist-onefile ^
    --assume-yes-for-downloads ^
    --include-data-files=ca/README.md=ca/README.md ^
    --include-data-files=ca/api.openai.com.cnf=ca/api.openai.com.cnf ^
    --include-data-files=ca/api.openai.com.subj=ca/api.openai.com.subj ^
    --include-data-files=ca/genca.sh=ca/genca.sh ^
    --include-data-files=ca/gencrt.sh=ca/gencrt.sh ^
    --include-data-files=ca/google.cnf=ca/google.cnf ^
    --include-data-files=ca/google.subj=ca/google.subj ^
    --include-data-files=ca/openssl.cnf=ca/openssl.cnf ^
    --include-data-files=ca/pixiv.cnf=ca/pixiv.cnf ^
    --include-data-files=ca/pixiv.subj=ca/pixiv.subj ^
    --include-data-files=ca/v3_ca.cnf=ca/v3_ca.cnf ^
    --include-data-files=ca/v3_req.cnf=ca/v3_req.cnf ^
    --include-data-files=ca/youtube.cnf=ca/youtube.cnf ^
    --include-data-files=ca/youtube.subj=ca/youtube.subj ^
    --include-data-files=modules/runtime/_build_version.py=modules/runtime/_build_version.py ^
    --include-package-data=tkinterweb_tkhtml:* ^
    --include-data-files=openssl/openssl.exe=openssl/openssl.exe ^
    --include-data-files=openssl/libcrypto-3-x64.dll=openssl/libcrypto-3-x64.dll ^
    --include-data-files=openssl/libssl-3-x64.dll=openssl/libssl-3-x64.dll ^
    --include-data-files=icons/f0bb32_bg-black.ico=icons/f0bb32_bg-black.ico ^
    --windows-icon-from-ico=icons/f0bb32_bg-black.ico ^
    --enable-plugin=tk-inter ^
    --windows-console-mode=attach ^
    --include-package=modules ^
    --windows-uac-admin ^
    --output-filename=MTGA_GUI-v%VERSION%-x64.exe ^
    mtga_gui.py

echo.
if not %ERRORLEVEL%==0 goto BUILD_ONEFILE_FAIL

set "EXPECTED_EXE=dist-onefile\MTGA_GUI-v%VERSION%-x64.exe"
set "EXPECTED_EXE_NAME=MTGA_GUI-v%VERSION%-x64.exe"
set "WAIT_ATTEMPTS=0"
set "FOUND_EXE_PATH="
set "FOUND_EXE_NAME="

:WAIT_EXPECTED_ONEFILE
if exist "%EXPECTED_EXE%" goto REPORT_ONEFILE_SUCCESS
if %WAIT_ATTEMPTS% GEQ 15 goto SEARCH_ONEFILE_ALTERNATIVE
set /a WAIT_ATTEMPTS+=1
timeout /t 2 /nobreak >nul
goto WAIT_EXPECTED_ONEFILE

:SEARCH_ONEFILE_ALTERNATIVE
set "FOUND_EXE_PATH="
set "FOUND_EXE_NAME="
for %%F in (dist-onefile\*.exe) do (
    set "FOUND_EXE_PATH=%%~fF"
    set "FOUND_EXE_NAME=%%~nxF"
)
if defined FOUND_EXE_PATH (
    if /I "%FOUND_EXE_NAME%"=="%EXPECTED_EXE_NAME%" (
        if exist "%FOUND_EXE_PATH%" goto REPORT_ONEFILE_SUCCESS
    )
    echo ⚠️ 检测到输出文件 %FOUND_EXE_PATH%，重命名为 %EXPECTED_EXE_NAME%
    move /Y "%FOUND_EXE_PATH%" "%EXPECTED_EXE%" >nul 2>&1
    if exist "%EXPECTED_EXE%" goto REPORT_ONEFILE_RENAMED
    echo ❌ 重命名失败，请检查 dist-onefile 目录
    goto FAIL_ONEFILE
) else (
    goto FAIL_ONEFILE
)

:REPORT_ONEFILE_SUCCESS
echo ✅ 单文件版本构建完成！
echo 可执行文件位于：%EXPECTED_EXE%
goto PRINT_ONEFILE_FEATURES

:REPORT_ONEFILE_RENAMED
echo ✅ 单文件版本构建完成（已重命名）！
echo 可执行文件位于：%EXPECTED_EXE%
goto PRINT_ONEFILE_FEATURES

:FAIL_ONEFILE
echo ❌ 未能找到任何 .exe 文件，请检查 dist-onefile 目录
if defined GITHUB_ACTIONS (
    exit /b 1
) else (
    pause
    exit /b 1
)

:PRINT_ONEFILE_FEATURES
echo.
echo 单文件版本特点:
echo • ✅ 仅一个 .exe 文件，便于分发
echo • ✅ 启动时自动解压到临时目录
echo • ✅ 包含所有依赖，无需额外文件
echo • ✅ 自动请求管理员权限
echo • ⚠️  首次运行较慢（需要解压）
echo.
goto END_ONEFILE

:BUILD_ONEFILE_FAIL
echo ❌ 构建失败，返回码: %ERRORLEVEL%
if defined GITHUB_ACTIONS (
    exit /b %ERRORLEVEL%
) else (
    pause
    exit /b %ERRORLEVEL%
)

:END_ONEFILE

if defined GITHUB_ACTIONS (
    goto :EOF
)

pause
