# UI 迁移总览（Nuxt + Tailwind + daisyUI）

本文件合并原有分析/计划/配置说明，用于指导从 Tkinter UI 迁移到 `mtga-tauri/app/`。

## 迁移目标与组件拆分

- 页面级布局：`AppShell`（标题 + 分栏）
- 主要组件：
  - `ConfigGroupPanel`、`GlobalConfigPanel`、`RuntimeOptionsPanel`
  - `MainTabs` + 各 Tab 组件
  - `LogPanel`、`FooterActions`
  - `UpdateDialog`、`ConfirmDialog`

## 页面骨架建议（目录结构）

```
app/
  app.vue
  components/
    AppShell.vue
    LogPanel.vue
    FooterActions.vue
    panels/
      ConfigGroupPanel.vue
      GlobalConfigPanel.vue
      RuntimeOptionsPanel.vue
    tabs/
      MainTabs.vue
      CertTab.vue
      HostsTab.vue
      ProxyTab.vue
      DataManagementTab.vue
      AboutTab.vue
    dialogs/
      UpdateDialog.vue
      ConfirmDialog.vue
```

## 迁移顺序建议

1. 布局 + 日志面板
2. 配置组 / 全局配置 / 运行时选项
3. Tabs 功能区
4. 更新弹窗与确认弹窗

## 当前进度摘要（便于恢复上下文）

- 已确定 UI 技术选型：Tailwind + daisyUI（基于 daisyUI 5 / Tailwind v4 的 CSS-first 配置方式）。
- 已搭建组件骨架：`AppShell`、`LogPanel`、`FooterActions`、`panels/*`、`tabs/*`、`dialogs/*`。
- 已在 `mtga-tauri/app/app.vue` 挂载骨架布局：左侧面板 + Tabs，右侧日志面板，底部按钮。
- 交互方式确认：前端通过 `pyInvoke` 调用 Python 后端命令（pytauri-wheel）。

## TODO（下一步执行清单）

- [x] 安装并启用 Tailwind + daisyUI（创建 `mtga-tauri/app/assets/css/tailwind.css`，在 `mtga-tauri/nuxt.config.ts` 引入）。
- [x] `MainTabs` 支持切换并挂载各 Tab 内容（证书/hosts/代理/数据/关于）。
- [x] `ConfigGroupPanel` 改为可交互：列表数据、选中状态、增删改弹窗。
- [x] `GlobalConfigPanel` 与 `RuntimeOptionsPanel` 接入真实数据与保存逻辑。
- [x] `LogPanel` 支持追加日志流（从后端或前端事件）。
- [x] `UpdateDialog`、确认弹窗完善交互与 HTML 内容渲染。
- [x] 用 `pyInvoke` 串起最小功能链路（例如 `greet` -> 日志输出）。

## 现有 UI 功能梳理

- **整体布局**：标题 + 左右分栏，左侧操作区，右侧日志滚动面板。
- **配置区**：配置组列表（含新增/修改/删除/上移/下移/测活/刷新）、全局配置（映射模型 ID / MTGA 鉴权 Key）。
- **运行时选项**：调试模式、关闭 SSL 严格模式、强制流模式。
- **功能标签页**：
  - 证书管理：生成 / 安装 / 清除（确认弹窗）
  - hosts 文件：修改 / 备份 / 还原 / 打开
  - 代理操作：启动 / 停止 / 检查网络环境
  - 用户数据管理（仅打包态）：打开目录 / 备份 / 还原 / 清除
  - 关于：版本信息 + 检查更新
- **更新弹窗**：展示 HTML release notes + 跳转发布页

## 交互方式（pytauri-wheel）

前端通过 `tauri-plugin-pytauri-api` 调用 Python 后端：

```ts
import { pyInvoke } from "tauri-plugin-pytauri-api";
const msg = await pyInvoke("greet", { name: "bifang" });
```

需要对接的能力包括：配置读写、证书/hosts/代理操作、用户数据管理、更新检查、运行环境标志。

## 前后端契约（pyInvoke 命令）

### 已实现

```
greet({ name: string }) -> string

load_config() -> {
  config_groups: ConfigGroup[]
  current_config_index: number
  mapped_model_id: string
  mtga_auth_key: string
}

save_config({
  config_groups: ConfigGroup[]
  current_config_index: number
  mapped_model_id?: string
  mtga_auth_key?: string
}) -> boolean

get_app_info() -> {
  display_name: string
  version: string
  github_repo: string
  ca_common_name: string
  api_key_visible_chars: number
}

is_packaged() -> boolean
```

### 待实现（优先按 UI 按钮接入）

```
generate_certificates()
install_ca_cert()
clear_ca_cert({ ca_common_name?: string })

hosts_modify({ mode: "add" | "backup" | "restore" | "remove" })
hosts_open()

proxy_start()
proxy_stop()
proxy_check_network()
proxy_start_all()

user_data_open_dir()
user_data_backup()
user_data_restore_latest()
user_data_clear()

check_updates()
```

## 状态字段定义（前端 store）

```
config_groups: ConfigGroup[]
current_config_index: number
mapped_model_id: string
mtga_auth_key: string
runtime_options: {
  debugMode: boolean
  disableSslStrict: boolean
  forceStream: boolean
  streamMode: "true" | "false"
}
logs: string[]
app_info: {
  display_name: string
  version: string
  github_repo: string
  ca_common_name: string
  api_key_visible_chars: number
}
show_data_tab: boolean
```

## ConfigGroup 结构

```
type ConfigGroup = {
  name?: string
  api_url: string
  model_id: string
  api_key: string
  middle_route?: string
  target_model_id?: string
  mapped_model_id?: string
}
```

## 旧 Tkinter 功能 → 新 UI 按钮映射

```
ConfigGroupPanel:
  测活 -> test_chat_completion
  刷新 -> load_config
  新增/修改/删除/上移/下移 -> save_config

GlobalConfigPanel:
  保存全局配置 -> save_config

RuntimeOptionsPanel:
  调试/SSL/流模式 -> 仅前端状态，启动代理时传给后端

CertTab:
  生成CA和服务器证书 -> generate_certificates
  安装CA证书 -> install_ca_cert
  清除系统CA证书 -> clear_ca_cert

HostsTab:
  修改hosts文件 -> hosts_modify(add)
  备份hosts -> hosts_modify(backup)
  还原hosts -> hosts_modify(restore)
  打开hosts文件 -> hosts_open

ProxyTab:
  启动代理服务器 -> proxy_start
  停止代理服务器 -> proxy_stop
  检查网络环境 -> proxy_check_network

FooterActions:
  一键启动全部服务 -> proxy_start_all

DataManagementTab（仅打包态）:
  打开目录 -> user_data_open_dir
  备份数据 -> user_data_backup
  还原数据 -> user_data_restore_latest
  清除数据 -> user_data_clear

AboutTab:
  检查更新 -> check_updates
```

## Tailwind + daisyUI 最小集成（按 daisyUI 5 / Tailwind v4）

依赖（示例 pnpm）：

```bash
pnpm add -D tailwindcss daisyui
```

`mtga-tauri/app/assets/css/tailwind.css`：

```css
@import "tailwindcss";
@plugin "daisyui";

/* 主题（可选）：先用 light 作为默认主题 */
@plugin "daisyui" {
  themes: light --default;
}
```

`mtga-tauri/nuxt.config.ts` 引入样式：

```ts
export default defineNuxtConfig({
  css: ["./app/assets/css/tailwind.css"],
});
```

常用组件类：

- Tabs：`tabs` / `tab`
- Dialog：`modal` / `modal-box`
- Tooltip：`tooltip`
- 表格：`table`
- 表单：`input` / `select` / `checkbox`
- 按钮：`btn` + `btn-primary/secondary`

## 迁移期开发环境下的开发方法

### 后端工程化

在 `mtga-tauri/python-src` 下：

```bash
uv venv
uv pip install -e .
```

### 启动前端

在 `mtga-tauri/app` 下：

```bash
pnpm dev
```

### 启动后端

在 `mtga-tauri/python-src` 下：

```pwsh
$env:DEV_SERVER="http://localhost:3000"; $env:MTGA_SRC_TAURI_DIR="..\\src-tauri"; uv run python -m mtga_app
```

## 打包：嵌入 Python（Tauri bundle）

### 1) 准备嵌入解释器

- 目录 `mtga-tauri/src-tauri/pyembed/...` 需要先准备。
- 使用 `python-build-standalone` 解压到 `mtga-tauri/src-tauri/pyembed/`：
  - Windows：`mtga-tauri/src-tauri/pyembed/python/python.exe`
  - macOS：`mtga-tauri/src-tauri/pyembed/python/bin/python3`

### 2) 安装后端到嵌入解释器

在 `mtga-tauri/src-tauri`：

Windows：

```pwsh
$env:PYTAURI_STANDALONE="1"
uv pip install --exact --python ".\pyembed\python\python.exe" --reinstall-package mtga-app "..\python-src"
```

macOS：

```zsh
export PYTAURI_STANDALONE="1"
uv pip install --exact --python "./pyembed/python/bin/python3" --reinstall-package mtga-app "../python-src"
```

### 3) 放置 .env（可选）

默认无需提供必填环境变量；如需覆盖自动探测到的资源目录，可放置 `.env` 并确保嵌入解释器可读取：

- Windows：`mtga-tauri/src-tauri/pyembed/python/Lib/.env`
- macOS：`mtga-tauri/src-tauri/pyembed/python/lib/python3.13/.env`（按实际版本调整）

当前仅保留可选项：

- `MTGA_RESOURCE_DIR`：覆盖默认资源目录探测

也可以在启动器中设置 `MTGA_ENV_FILE` 指向 `.env` 绝对路径。

### 4) 配置 tauri-cli（仅打包用）

新建 `mtga-tauri/src-tauri/tauri.bundle.json`：

```json
{
  "bundle": {
    "active": true,
    "targets": "all",
    "resources": {
      "pyembed/python": "./"
    }
  }
}
```

> 不要把 `bundle.resources` 写进 `tauri.conf.json`，而是用 `--config` 传入。

同时建议在 `mtga-tauri/src-tauri/.taurignore` 中加入：

```
/pyembed/
```

避免 `tauri dev` 每次复制庞大的解释器目录。

`mtga-tauri/src-tauri/Cargo.toml` 增加：

```toml
[profile.bundle-dev]
inherits = "dev"

[profile.bundle-release]
inherits = "release"
```

### 5) Build & Bundle（环境变量 + 最终打包命令）

**回到 `mtga-tauri` 根目录下。**
设置编译期 Python：

```pwsh
$env:PYO3_PYTHON = (Resolve-Path -LiteralPath ".\src-tauri\pyembed\python\python.exe").Path
```

macOS 还需：

```zsh
export PYO3_PYTHON=$(realpath ./src-tauri/pyembed/python/bin/python3)
export RUSTFLAGS=" \
  -C link-arg=-Wl,-rpath,@executable_path/../Resources/lib \
  -L $(realpath ./src-tauri/pyembed/python/lib)"
install_name_tool -id '@rpath/libpython3.13.dylib' \
  ./src-tauri/pyembed/python/lib/libpython3.13.dylib
```

最终打包：

```bash
pnpm -- tauri build --config="src-tauri/tauri.bundle.json" -- --profile bundle-release
```

### Windows 安装器/应用图标配置

1. **NSIS 安装包（setup.exe）图标**
   在 `mtga-tauri/src-tauri/tauri.conf.json`：

```json
"bundle": {
  "windows": {
    "nsis": {
      "installerIcon": "icons/icon.ico"
    }
  }
}
```

2. **应用图标（程序窗口/任务栏/快捷方式）**
   在同一文件的 `bundle.icon` 中配置 `.ico`（Windows）：

```json
"bundle": {
  "icon": [
    "icons/icon.ico"
  ]
}
```

3. **MSI 安装界面图片（WiX banner/dialog BMP）**
   在 `mtga-tauri/src-tauri/tauri.conf.json`：

```json
"bundle": {
  "windows": {
    "wix": {
      "bannerPath": "icons/wix-banner.bmp",
      "dialogImagePath": "icons/wix-dialog.bmp"
    }
  }
}
```

### MSI 图片生成（PowerShell 快速生成）

使用现有 logo 生成 WiX 需要的两张 BMP：

```pwsh
Add-Type -AssemblyName System.Drawing
$logoPath = (Resolve-Path -LiteralPath ".\src-tauri\icons\128x128@2x.png").Path
$logo = [System.Drawing.Image]::FromFile($logoPath)

$iconsDir = (Resolve-Path -LiteralPath ".\src-tauri\icons").Path

# banner 493x58
$banner = New-Object System.Drawing.Bitmap 493,58
$g1 = [System.Drawing.Graphics]::FromImage($banner)
$g1.Clear([System.Drawing.Color]::White)
$g1.DrawImage($logo, 10, 4, 50, 50)
$banner.Save((Join-Path $iconsDir "wix-banner.bmp"), [System.Drawing.Imaging.ImageFormat]::Bmp)

# dialog 493x312
$dialog = New-Object System.Drawing.Bitmap 493,312
$g2 = [System.Drawing.Graphics]::FromImage($dialog)
$g2.Clear([System.Drawing.Color]::White)
$g2.DrawImage($logo, 20, 20, 80, 80)
$dialog.Save((Join-Path $iconsDir "wix-dialog.bmp"), [System.Drawing.Imaging.ImageFormat]::Bmp)
```

## Tauri 后端模块/资源对齐（关键约定）

- 采用“复制方案”：`mtga-tauri/python-src/modules` 作为 Tauri 侧核心逻辑来源，仓库根 `modules` 仅供旧 GUI 使用。
- `mtga-tauri/.env` 为可选配置入口（支持 `MTGA_ENV_FILE` 覆盖路径）；默认无需配置，当前仅保留 `MTGA_RESOURCE_DIR` 作为资源目录覆盖项。
- `mtga-tauri/python-src/mtga_app/__init__.py` 会最早加载 `mtga-tauri/.env`，当前固定从 `python-src/modules` 导入 `modules` 包。
- 开发期从 `python-src` 启动时需要设置 `MTGA_SRC_TAURI_DIR` 指向 `src-tauri`（用于定位 `tauri.conf.json`）。
- 资源目录约定：`mtga-tauri/python-src/modules/resources/{ca,openssl}`；`ResourceManager` 优先用包资源，
  其次本地 `mtga-tauri/python-src/modules/resources`，必要时可用 `MTGA_RESOURCE_DIR` 覆盖。
- 软件图标由 Tauri 处理（`mtga-tauri/src-tauri/icons` + `mtga-tauri/tauri.conf.json`），不进入 Python 资源。
- `mtga-tauri/python-src/pyproject.toml` 已声明 `modules` 包资源（`resources/ca`、`resources/openssl`）。
