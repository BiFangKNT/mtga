---
name: tauri
description: 构建、调试与发布 Tauri v2 应用的工程化工作流。覆盖项目初始化（create-tauri-app）、前端与 Rust 命令通信（`#[tauri::command]` + `invoke`）、状态管理、Capabilities 权限建模、插件接入、跨平台构建与问题排查。当用户需求涉及“创建 Tauri 项目”“把 Web 前端接到 Rust 后端”“最小权限配置（fs/http/shell）”“接入 Tauri 官方插件”“执行 tauri dev/build”“排查 Tauri 构建或运行错误”时使用此 skill。
---

# Tauri

## Overview

以“先跑通主流程，再收紧权限，再扩展插件”为原则执行 Tauri v2 任务。优先给出可执行命令、最小能力权限和可验证的验收步骤。

## Workflow

1. 确认目标：识别是新建项目、接入功能、配置权限、打包发布还是排障。
2. 建立基线：优先创建最小可运行项目并执行 `tauri dev`。
3. 打通通信：先实现一个最小 `#[tauri::command]` + `invoke` 闭环，再增加状态和异步逻辑。
4. 收紧权限：按窗口/功能拆分 capability，只授予任务必需权限。
5. 增量接入插件：先安装，再注册，再最小权限验证。
6. 构建发布：按目标平台执行 `tauri build`，再处理签名、公证、安装包分发。

## Decision Tree

1. 需求是“从零创建或改造前端集成”：读取 `references/quickstart.md`。
2. 需求是“Rust 命令、参数、异步、状态注入”：读取 `references/command-state.md`。
3. 需求是“权限模型、capabilities、fs/http/shell 约束”：读取 `references/security-capabilities.md`。
4. 需求是“官方插件接入流程与权限联动”：读取 `references/plugins.md`。
5. 需求是“多平台构建、目标三元组、发布前检查”：读取 `references/build-release.md`。
6. 需求是“dev/build 失败或运行异常”：读取 `references/troubleshooting.md`。

## Execution Rules

1. 优先使用项目已有包管理器（`npm`/`pnpm`/`yarn`/`bun`/`cargo`），避免混用。
2. 在首次改动 Rust 命令后，立即执行一次前端 `invoke` 冒烟测试。
3. 对 `fs`、`http`、`shell` 权限执行最小化配置，禁止“全开权限”作为默认方案。
4. 在 capability 中显式绑定 `windows`，避免权限泄漏到不相关窗口/WebView。
5. 在构建前检查 `beforeDevCommand`、`beforeBuildCommand`、`frontendDist` 与前端实际产物路径是否一致。
6. 输出时同时给出：执行命令、改动文件、验证方式、回滚点。

## Output Template

1. `Goal`: 本次 Tauri 任务目标。
2. `Changes`: 计划或已修改的文件与配置点。
3. `Commands`: 按顺序可执行命令（先验证，后变更）。
4. `Verification`: 最小验收步骤（dev 运行、命令调用、权限验证、build 结果）。
5. `Risk`: 安全与发布风险（权限范围、平台差异、签名/公证缺口）。

## References

仅按需读取，不要一次性加载全部文档：

- 项目初始化与前端接入：`references/quickstart.md`
- Rust 命令与状态管理：`references/command-state.md`
- 权限模型与 capability：`references/security-capabilities.md`
- 插件接入：`references/plugins.md`
- 构建发布：`references/build-release.md`
- 故障排查：`references/troubleshooting.md`
