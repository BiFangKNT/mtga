# MTGA 项目构建指南

## 🎯 项目状态总结

✅ **系统托盘支持：**
- `useTray.ts` - 修复了图标显示（`defaultWindowIcon`）和 TypeScript 类型错误。
- `lib.rs` - 移除了后端对窗口关闭事件的拦截，解决逻辑冲突。
- `Cargo.toml` - 启用了 `tray-icon` 特性支持。
- **验证通过**：托盘图标正常显示，左键显隐窗口，右键菜单退出，关闭按钮最小化到托盘。

✅ **开机自启动功能已完全修复：**
- `useAutoStart.ts` - 已修复异步函数类型错误，并增强了状态检查逻辑。
- Tauri autostart插件 - 已正确配置和集成。
- SettingsPanel.vue - 已正确使用自启动功能，并在开发环境下提供友好的错误提示。
- 权限配置 - 已在`default.toml`中添加`autostart:default`。

✅ **前端构建正常：**
- TypeScript类型检查通过。
- Vue/Nuxt构建成功。
- 已配置 Nuxt 监听所有网络接口 (`--host`) 以解决开发环境连接问题。

✅ **项目结构完整：**
- 前端：Vue 3 + Nuxt 3 + TypeScript
- 后端：Python 3.13 + Tauri Rust
- 构建系统：pnpm + uv + cargo

## 🛠️ 环境要求

### 必需工具
1. **Node.js 24+** - 前端构建（Node 22 也可运行，但会有警告，建议使用 `engines` 字段配置）。
2. **pnpm** - 包管理器 (`npm install -g pnpm`)。
3. **Python 3.13+** - 后端依赖（推荐使用 Conda 管理）。
4. **Rust工具链** - Tauri构建 (`rustup`安装)。
5. **Visual Studio C++ Build Tools** - (Windows) 需要安装 "Desktop development with C++" 工作负载，包含 MSVC 和 Windows SDK。

## 🚀 快速构建步骤

### 一键构建安装包 (推荐)

我们提供了一个稳健的 PowerShell 脚本，自动处理 Python 依赖安装和打包过程。

```powershell
# 在项目根目录下运行
powershell -ExecutionPolicy Bypass -File scripts/build-now.ps1
```

该脚本会：
1. 自动调用 `scripts/setup_pyembed.py` 将 Python 环境（含依赖）安装到 `src-tauri/pyembed`。
2. 设置必要的环境变量 (`PYO3_PYTHON`)。
3. 执行 `pnpm tauri:bundle:win` 生成安装包。

### 开发模式运行

```bash
# 同时启动前端和后端
pnpm dev:all
```

注意：
- 开发模式下，“开机自启动”功能无法生效（受限于系统权限），这是正常现象。
- 首次运行时，请确保 `.env` 文件已正确配置（脚本会自动生成默认配置）。

## ⚙️ 常见问题与配置

### 1. GitHub API 403 错误 (检查更新失败)
这是因为 GitHub 对匿名 API 请求有限流（60次/小时）。
**解决方法：**
1. 去 GitHub 生成一个 Personal Access Token (Classic)。
2. 在 `.env` 文件中配置：
   ```properties
   GITHUB_TOKEN=ghp_your_token_here
   ```
3. 重启应用。

### 2. "无法连接后端" 错误
这通常是因为 Python 依赖未正确打包。
**解决方法：**
务必使用 `scripts/build-now.ps1` 进行构建，它会自动处理依赖安装。

### 3. 开发环境无法访问 localhost
**解决方法：**
我们已配置 Nuxt 监听 `0.0.0.0`。尝试访问 `http://127.0.0.1:3000` 或本机局域网 IP。

## 📁 构建输出

构建成功后，可以在以下位置找到输出文件：

- **安装包**: `src-tauri\target\release\bundle\nsis\MTGA_x.x.x_x64-setup.exe`
- **可执行文件**: `src-tauri\target\release\mtga-tauri.exe`

## ✅ 功能状态检查清单

- [x] TypeScript编译无错误
- [x] 前端构建成功
- [x] 开机自启动功能修复完成
- [x] Tauri插件配置正确
- [x] 权限设置完整
- [x] Python环境自动打包脚本 (`setup_pyembed.py`)
- [x] 稳健的构建脚本 (`build-now.ps1`)
- [x] GitHub Token 支持

**现在项目已准备好进行发布！**
