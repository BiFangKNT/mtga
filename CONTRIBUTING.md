# Contributing Guide

感谢你为 MTGA 项目做贡献。

本文档面向社区贡献者，说明从环境准备到提交 PR 的完整流程。

## 贡献前须知

- 所有功能/修复改动都通过 Pull Request 合入。
- PR 目标分支必须是 `dev`。
- 保持改动聚焦：一个 PR 只解决一个问题或一类需求。
- 不要提交生成产物或本地环境目录（如 `node_modules/`、`src-tauri/target/`、`dist/`、`.venv/`）。

## 开发环境准备

### 必要工具

- Node.js（见 `package.json` 中 `engines.node` 约束）
- pnpm
- uv（Python 依赖与运行）
- Rust toolchain（用于 `src-tauri/`）

### 初始化依赖

```bash
pnpm i
uv sync --project python-src
```

### Python 运行约束

- 需要运行 Python 时，一律使用 `uv run ...`。
- 不要直接使用 `python ...`。

## 推荐 Git 工作流（git-flow-next）

本项目推荐使用 [git-flow-next](https://github.com/gittower/git-flow-next) 规范化管理分支与发布流程。

### 安装 git-flow-next

- Linux/macOS：

```bash
brew install gittower/tap/git-flow-next
```

- Windows：
  1. 在 git-flow-next 的 Release 页面下载可执行文件。
  2. 放到你希望的目录。
  3. 将该目录加入 `PATH`。

### 初始化

在仓库根目录执行：

```bash
pnpm gitflow:setup
```

初始化后，其余操作基本遵循 git-flow-next 官方规范。

## 分支与提交规范

### 提交信息

提交信息使用 Conventional Commits，例如：

- `feat: add xxx`
- `fix: resolve xxx`
- `chore: update xxx`
- `feat(tauri): add xxx`

## 本地开发与自检

### 常用开发命令

```bash
# 启动前后端开发服务器（默认 `http://localhost:3000`）
pnpm dev:all

# 启动 Tauri 原生开发环境以验证原生行为，必须先安装 python 后端
pnpm pytauri:install:{平台：win/mac}
pnpm tauri:dev
```

### 按改动类型执行质量检查

- Python 改动：

```bash
pnpm py:check
```

- YAML 改动：

```bash
pnpm eslint . --fix
```

- Rust 改动：

```bash
pnpm rs:check
```

- JS/TS/Vue 改动：

```bash
pnpm app:check
```

## Pull Request 规范

提交 PR 时请确保：

1. 目标分支是 `dev`。
2. 描述清楚变更目的、影响范围、验证方式。
3. 涉及 UI 变更时附截图。
4. 涉及 `src-tauri/tauri.conf.json` 或 `src-tauri/capabilities/` 变更时说明权限影响。

## 维护者专属流程

- `release:push` 仅用于维护者最终发版。
- 社区开发者请忽略该命令，不需要执行。

## 常见问题

### 为什么 PR 被提示目标分支不正确？

仓库规则要求贡献 PR 的目标分支是 `dev`。请将 PR 的 base branch 修改为 `dev`。

### 本地通过但 CI 失败怎么办？

1. 先确认已按改动类型执行对应检查命令。
2. 再对照 CI 日志定位平台差异或环境差异。
3. 若是 Tauri/Rust 相关问题，优先查看 `src-tauri/` 相关配置和构建日志。
