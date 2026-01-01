# Windows集成

<cite>
**本文档引用的文件**
- [system.py](file://modules/platform/system.py#L7-L34)
- [privileges.py](file://modules/platform/privileges.py#L13-L112)
- [build_onefile.bat](file://build_onefile.bat#L1-L212)
- [Windows_Onefile_Build.md](file://docs/Windows_Onefile_Build.md#L1-L172)
- [mtga_gui.py](file://mtga_gui.py#L85-L86)
- [privilege_service.py](file://modules/services/privilege_service.py#L3-L5)
- [__init__.py](file://modules/platform/__init__.py#L3-L23)
- [file_operability.py](file://modules/hosts/file_operability.py#L144-L189)
</cite>

## 目录
1. [平台检测机制](#平台检测机制)
2. [管理员权限管理](#管理员权限管理)
3. [单文件构建流程](#单文件构建流程)
4. [资源包含策略](#资源包含策略)
5. [故障排除指南](#故障排除指南)

## 平台检测机制

项目通过 `modules/platform/system.py` 文件中的 `is_windows()` 函数实现Windows平台检测。该函数基于Python标准库的 `os.name` 属性进行判断，当 `os.name` 等于 "nt" 时返回 `True`，表示当前运行环境为Windows系统。这种检测方法是Python跨平台开发中的标准实践，能够准确区分Windows与POSIX系统（如Linux和macOS）。

`is_windows()` 函数作为基础平台检测工具，被其他模块广泛引用，为条件性代码执行提供依据。例如，权限管理、文件路径处理和系统调用等功能模块会根据此函数的返回值来决定执行路径。

**Section sources**
- [system.py](file://modules/platform/system.py#L7-L9)

## 管理员权限管理

项目的Windows UAC（用户账户控制）权限管理由 `modules/platform/privileges.py` 文件实现。该模块提供了完整的权限检测和提升机制，核心功能包括：

- `is_windows_admin()`：检查当前用户是否为管理员账户
- `is_windows_elevated()`：检查当前进程是否具有提升的权限
- `run_as_admin()`：请求管理员权限并重新启动应用

权限管理流程在应用启动时被调用，通过 `privilege_service.py` 模块提供的 `check_is_admin()` 和 `run_as_admin()` 接口实现。当应用需要修改系统文件（如hosts文件）或监听特权端口时，会自动触发UAC权限提升对话框，确保操作的合法性。

在 `mtga_gui.py` 主程序中，通过导入 `privilege_service` 模块来集成权限管理功能。`file_operability.py` 模块在检查文件可操作性时，会调用 `is_windows_admin()` 函数来评估当前权限状态，为后续的文件操作决策提供依据。

**Section sources**
- [privileges.py](file://modules/platform/privileges.py#L13-L112)
- [mtga_gui.py](file://mtga_gui.py#L85-L86)
- [privilege_service.py](file://modules/services/privilege_service.py#L3-L5)
- [__init__.py](file://modules/platform/__init__.py#L3-L23)
- [file_operability.py](file://modules/hosts/file_operability.py#L144-L189)

## 单文件构建流程

`build_onefile.bat` 构建脚本使用Nuitka将整个Python应用打包为单一的Windows可执行文件（.exe）。构建流程包含以下关键步骤：

1. **环境检查**：脚本首先验证虚拟环境 `.venv` 是否存在，并检查Visual Studio MSVC编译工具链的安装情况。它会自动搜索多个可能的安装路径，包括Community、Professional和Enterprise版本。

2. **版本信息写入**：构建脚本将版本号写入 `modules/runtime/_build_version.py` 文件，供应用在运行时读取。

3. **Nuitka编译**：使用 `uv run` 命令调用Nuitka执行编译，核心参数包括：
   - `--onefile`：将所有依赖打包为单个.exe文件
   - `--msvc=latest`：使用最新的MSVC编译器工具链
   - `--windows-uac-admin`：确保应用启动时自动请求管理员权限
   - `--windows-console-mode=attach`：设置控制台模式，允许在需要时显示控制台窗口

4. **输出验证**：构建完成后，脚本会验证输出文件是否存在，并进行必要的重命名操作。

**Section sources**
- [build_onefile.bat](file://build_onefile.bat#L1-L212)

## 资源包含策略

构建脚本通过 `--include-data-files` 和 `--include-package-data` 参数精确控制打包内容，确保应用在解压运行时拥有所有必需的资源：

- **SSL证书文件**：包含 `ca/` 目录下的所有证书配置文件（.cnf, .subj）和生成脚本
- **OpenSSL二进制文件**：包含 `openssl/` 目录下的 `openssl.exe` 及其依赖的DLL文件（`libcrypto-3-x64.dll`, `libssl-3-x64.dll`）
- **图标资源**：通过 `--windows-icon-from-ico` 参数将 `icons/f0bb32_bg-black.ico` 嵌入到可执行文件中
- **Python模块**：使用 `--include-package=modules` 包含整个 `modules/` 目录
- **运行时数据**：包含 `_build_version.py` 文件以提供版本信息

此外，`--enable-plugin=tk-inter` 参数确保了Tkinter GUI框架的正确打包，使应用界面能够正常显示。

**Section sources**
- [build_onefile.bat](file://build_onefile.bat#L102-L122)

## 故障排除指南

### MSVC工具链缺失

**问题**：构建脚本无法找到Visual Studio编译工具链
```
错误：未找到可用的 Visual Studio 工具链，请先安装 Visual Studio（含 MSVC）
```

**解决方案**：
1. 安装Visual Studio 2022 Community版本
2. 在安装时确保选择"C++桌面开发"工作负载
3. 或者通过命令行安装：`vs_buildtools.exe --add Microsoft.VisualStudio.Workload.VCTools`

### 构建失败

**问题**：虚拟环境不存在或依赖未安装
```
错误：虚拟环境不存在，请先运行 uv sync --group win-build 安装依赖
```

**解决方案**：
1. 运行 `uv sync --group win-build` 安装构建依赖
2. 确保Python版本为3.13或更高
3. 检查网络连接，确保可以下载Nuitka等大型包

### 运行时问题

**问题**：单文件应用首次运行缓慢
**说明**：这是正常现象，因为应用需要将自身解压到临时目录。后续运行速度会显著提升。

**问题**：杀毒软件误报
**说明**：打包后的.exe文件可能被某些杀毒软件误判为恶意软件。建议提供SHA256校验和供用户验证文件完整性。

**Section sources**
- [build_onefile.bat](file://build_onefile.bat#L12-L72)
- [Windows_Onefile_Build.md](file://docs/Windows_Onefile_Build.md#L116-L136)