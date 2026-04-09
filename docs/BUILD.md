# 本地打包指南

以下是完整的本地打包步骤（假设您在 Windows 电脑上操作）：

## 1. 准备基础环境
确保您的电脑上已安装以下依赖：

- **Node.js** (版本 >= 24) 和 **pnpm** 包管理器。
- **Rust** (Stable 版本)。
- **Visual Studio C++ Build Tools** (仅 Windows 需要，包含在 Visual Studio 中，安装时勾选 "C++ 桌面开发" 工作负载)。
- **uv**：高性能的 Python 包管理器（可通过 `pip install uv` 安装）。

## 2. 安装项目依赖
在项目根目录下，安装前端和后端的依赖：

```bash
# 1. 安装前端依赖
pnpm install

# 2. 安装 Python 依赖
cd python-src
uv sync
cd ..
```

## 3. 下载并植入独立的 Python 运行时 (最关键的一步)
由于 MTGA 不需要用户电脑上安装 Python，它会将一个精简版的 Python 打包进 `.exe` 中。

1. 在项目根目录进入 `src-tauri`，创建一个名为 `pyembed` 的文件夹。
2. 前往 `astral-sh/python-build-standalone` 的 Release 页面 。
3. 下载适用于 Windows 的 Python 3.13 剥离版压缩包，文件名类似：`cpython-3.13.x+xxxxxxxx-x86_64-pc-windows-msvc-install_only_stripped.tar.gz`。
4. 将其解压到刚才创建的 `src-tauri/pyembed` 目录下。
5. 验证路径：确保存在文件 `src-tauri/pyembed/python/python.exe`。

## 4. 将后端代码安装到独立环境中
在项目根目录运行以下命令，这会使用 uv 将您的 `python-src` 源码安装到刚才下载的独立 Python 引擎中：

```bash
pnpm pytauri:install:win
```

## 5. 一键瘦身与打包
最后，在项目根目录运行打包命令：

```bash
pnpm tauri:bundle:win
```

这行命令在后台会做两件事：
- **瘦身 (`pyembed:prune`)**：自动运行内置的 Node.js 脚本，把独立 Python 环境里用不到的组件（比如 pip、测试用例、tkinter 等）全部删掉，大幅减小最终 `.exe` 的体积。
- **编译 (`tauri build`)**：将 Nuxt 前端编译成静态文件，将 Rust 壳和瘦身后的 Python 引擎一起打包。

## 6. 获取安装包
等待 Rust 编译完成后，您可以在以下目录找到最终的 Windows NSIS 安装程序（`.exe`）： 
`src-tauri/target/release/bundle/nsis/`

直接双击这个 `.exe` 即可像普通软件一样安装使用了。
