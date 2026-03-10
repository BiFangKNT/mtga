# 构建与发布

## 本地构建

```bash
pnpm tauri build
```

指定目标三元组：

```bash
pnpm tauri build --target x86_64-pc-windows-msvc
pnpm tauri build --target x86_64-apple-darwin
pnpm tauri build --target aarch64-apple-darwin
pnpm tauri build --target x86_64-unknown-linux-gnu
```

调试构建：

```bash
pnpm tauri build --debug
```

## 移动端（如启用）

```bash
pnpm tauri android init
pnpm tauri ios init
pnpm tauri android build
pnpm tauri ios build
```

## 发布前检查

1. 核对 `beforeBuildCommand` 与前端构建产物目录。
2. 运行关键业务流回归（命令调用、文件读写、网络请求）。
3. 审核 capability 是否仍为最小权限。
4. 补齐平台签名/公证流程（Windows/macOS/iOS/Android 按各平台规则执行）。

## 产物验收

1. 安装包可正常安装/卸载。
2. 首次启动无白屏、无权限异常。
3. 崩溃日志与错误上报机制可用。
