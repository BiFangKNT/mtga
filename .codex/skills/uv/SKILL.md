---
name: uv
description: 在 Windows/macOS/Linux 上使用 `uv` 执行 Python 运行、依赖同步、锁文件管理、Python 版本管理与工具命令（`uv run`、`uv sync`、`uv lock`、`uv python`、`uv tool`）。当任务涉及“用 uv 运行脚本/命令”“临时依赖（`--with`）”“锁文件一致性（`--locked`/`--frozen`）”“跨平台 shell（bash/zsh/PowerShell）下排查 uv 执行问题”时使用此 skill。
---

# Uv

## Overview

以可复现、可审计的方式使用 `uv`。优先给出最小可执行命令，先读状态后做写入，明确是否会修改 `uv.lock`、`.venv`、`.python-version`。

## Workflow

1. 确认上下文：当前目录是否为 `pyproject.toml` 项目、是否允许改动锁文件和环境。
2. 先选操作面：运行命令（`run`）、同步环境（`sync`）、更新锁（`lock`）、Python 版本（`python`）、工具（`tool`）。
3. 先执行只读探测：版本、help、检查状态（如 `uv --version`、`uv lock --check`、`uv sync --check`）。
4. 再执行变更命令：明确写入范围（`uv.lock`、`.venv`、`.python-version`、工具目录）。
5. 输出关键结果与下一步。

## Operation Decision

1. 只执行一次命令且不想持久安装工具：用 `uv tool run`（或 `uvx`）。
2. 在项目环境中执行代码/命令：用 `uv run`。
3. 需要补齐或重建项目环境：用 `uv sync`。
4. 需要检查或更新锁文件：用 `uv lock`（只检查用 `uv lock --check`）。
5. 需要固定解释器版本：用 `uv python install` + `uv python pin`。

## Command Rules

- `uv` 选项必须放在被执行命令之前；必要时用 `--` 分隔（例如 `uv run --python 3.12 -- python`）。
- 需要临时依赖时用 `uv run --with <pkg>` 或 `uv tool run --with <pkg>`。
- 不希望自动发现项目时用 `--no-project`。
- `uv run`/`uv sync` 默认会处理 lock/sync；需要禁止写锁文件时优先 `--locked`，需要跳过锁文件更新检查时用 `--frozen`。
- 执行 Python 脚本工具（如校验脚本）缺依赖时，优先 `uv run --with pyyaml <script>`。
- 在 Windows 下出现 Python 默认编码导致的 `UnicodeDecodeError` 时，可先设置 `$env:PYTHONUTF8='1'` 后再运行 `uv run ...`。

## Failure Handling

- 命令不存在或子命令写错：先运行对应 `--help`，再重试最小命令。
- `No module named ...`：改为 `uv run --with <missing-package> ...`。
- `--locked` 失败（锁文件过期）：先 `uv lock` 或 `uv sync` 更新，再重试。
- 目录不是项目却执行了项目命令：改用 `--no-project` 或切换到正确项目目录。
- PowerShell 环境变量导致参数展开异常：优先使用单引号和显式变量赋值。

## Safety Checklist

执行会写入的命令前，先确认：

- 当前仓库/目录是否正确。
- 是否允许修改 `uv.lock` 与 `.venv`。
- 是否允许写入 `.python-version`。
- 是否为一次性命令（应使用 `uv tool run`）还是持久安装（`uv tool install`）。

## Output Format

统一按以下结构输出：

1. `Plan`: 本次要完成的 uv 任务。
2. `Commands`: 实际执行命令（先只读，后变更）。
3. `Result`: 关键结果（是否改动锁文件/环境、关键版本、状态检查结果）。
4. `Next`: 失败时的最短可执行下一步。

## Reference

按需读取参考文档：

- 命令索引：`references/commands.md`
- 运行与临时依赖：`references/run.md`
- 锁与同步：`references/sync-lock.md`
- Python 版本管理：`references/python.md`
- 工具命令：`references/tool.md`
- 常见故障：`references/troubleshooting.md`
