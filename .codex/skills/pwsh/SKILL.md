---
name: pwsh
description: 在 Windows PowerShell 5.1 与 PowerShell 7 中编写和执行稳定命令，重点处理引号、管道符、原生命令参数传递与跨版本兼容。遇到 `--jq`/过滤表达式被 PowerShell 误解析、同一命令在 pwsh5 与 pwsh7 行为不一致、或需要为 pwsh7.3+ 增加参数传递适配时使用此 skill。
---

# Pwsh

## Overview

以“先兼容、后增强”为原则生成 PowerShell 命令。默认先满足 pwsh5 可运行，再按需启用 pwsh7 专属能力。

## Workflow

1. 确认目标解释器：先读取 `$PSVersionTable.PSVersion`，判断是 5.1 还是 7.x。
2. 选兼容级别：默认按 pwsh5 语法生成；仅在确认 7.x 时使用 7 专属语法。
3. 组装参数：优先用变量或数组传参，避免在命令行内堆叠转义。
4. 处理原生命令：当参数被误解析时，先改写引号；必要时使用 `--%` 或 pwsh7 参数传递设置。
5. 输出结果：明确命令、兼容前提、以及可能影响行为的版本差异。

## Baseline Rules

- 将 pwsh5 视为最低兼容基线。
- 在 PowerShell 中向 `--jq` 或类似参数传入含 `|` 的表达式时，必须使用单引号字符串。
- 需要变量拼接时，先构造变量再传参，不在命令行直接拼复杂引号。
- 文件读写显式指定编码，避免依赖不同版本默认值。

## pwsh7 Adaptation

- 仅在确认 `PowerShell 7.3+` 时考虑 `$PSNativeCommandArgumentPassing` 影响。
- 旧脚本因参数传递行为变化失败时，按需临时切换 `Legacy`，任务完成后恢复原值。
- 使用 pwsh7 专属语法（如 `??`、`||`、`&&`、`ForEach-Object -Parallel`）前先做版本判断。

## Failure Handling

1. 出现 `|` 被吃掉：检查表达式是否被单引号包裹。
2. 原生命令参数异常：先改为变量传参，再评估 `--%` 或 `$PSNativeCommandArgumentPassing`。
3. 跨版本结果不同：回显版本号与关键变量值后，再给出兼容改写命令。

## Output Format

1. `Plan`: 要解决的 PowerShell 兼容问题。
2. `Commands`: 可直接执行的命令（必要时分 5.1 与 7.x 两套）。
3. `Result`: 关键输出与版本信息。
4. `Compat`: 是否依赖 pwsh7 特性，及回退方案。

## Reference

按需加载，不要一次性读取全部细节：

- 通用兼容基线：`references/pwsh5-baseline.md`
- `--jq` 与引号规则：`references/quoting-jq.md`
- pwsh7 增量适配：`references/pwsh7-adaptation.md`
