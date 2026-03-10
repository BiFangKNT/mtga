# 项目初始化与前端接入

## 初始化项目

优先使用脚手架创建：

```bash
npm create tauri-app@latest
# 或
pnpm create tauri-app
# 或
yarn create tauri-app
```

进入项目后先安装依赖，再启动开发：

```bash
cd tauri-app
pnpm install
pnpm tauri dev
```

如果使用 Cargo 入口：

```bash
cargo install create-tauri-app --locked
cargo create-tauri-app
cd <project-dir>
cargo install tauri-cli --version "^2.0.0" --locked
cargo tauri dev
```

## 对接已有前端项目

在 `src-tauri/tauri.conf.json` 中至少确认：

```json
{
  "build": {
    "beforeDevCommand": "pnpm dev",
    "beforeBuildCommand": "pnpm build",
    "devUrl": "http://localhost:5173",
    "frontendDist": "../dist"
  }
}
```

执行前检查：

1. `beforeDevCommand` 能独立启动前端。
2. `beforeBuildCommand` 能独立产出构建目录。
3. `frontendDist` 与前端构建输出目录一致。

## 最小验收

1. 运行 `pnpm tauri dev`。
2. 确认桌面窗口成功打开且前端资源加载正常。
3. 修改前端页面并确认热更新行为符合预期。
