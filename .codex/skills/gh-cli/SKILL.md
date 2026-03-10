---
name: gh-cli
description: 使用 GitHub CLI (`gh`) 执行非交互式 GitHub 协作与自动化任务（PR、Issue、Actions、Release、API 查询/修改）。当用户要求“用 gh 命令完成任务”、需要结构化 JSON 输出（`--json`/`--jq`）、批量处理 PR/Issue（如“批量 review 多个 PR”）、按策略合并（如“检查通过后自动 squash 合并”）时使用此 skill。
---

# gh-cli

## Overview

以可复现、可审计的方式调用 `gh`。默认输出结构化数据，优先使用非交互命令，避免依赖浏览器或 TUI。

## Workflow

1. 确认认证与仓库上下文。
2. 如果命令参数不确定，先运行 `gh <subcommand> --help` 或 `gh help <topic>`。
3. 先生成“只读探测命令”，再生成“变更命令”。
4. 变更命令明确影响范围（仓库、PR/Issue 编号、merge 策略、是否删除分支）。
5. 执行后返回关键输出与下一步建议。

## Operation Decision

1. 用户只问“现状/列表/状态”：只执行只读命令（`list`/`view`/`status`/`api GET`）。
2. 用户要求“评论/审查/合并/触发工作流”：先只读确认对象存在与状态，再执行变更命令。
3. 用户同时要“查询+修改”：拆成两段，先回显查询结果，再给修改命令并执行。
4. 用户目标不完整（缺编号、缺仓库、缺 merge 方法）：先补齐参数，不直接变更。
5. 用户要求“整体审查结论”（`approve`/`request-changes`/`comment`）：使用 `gh pr review`。
6. 用户要求“按文件/按行评论”：使用 `gh api repos/{owner}/{repo}/pulls/{num}/reviews` 或 `gh api repos/{owner}/{repo}/pulls/{num}/comments`，不要把 `gh pr review` 当作行内评论接口。

## Command Rules

- 默认使用非交互模式；不要依赖手动输入。
- 优先输出 JSON：使用 `--json` + `--jq/-q` 精简结果。
- 需要批量查询时，优先 `gh api --paginate`。
- 需要复杂参数时，优先 `gh api -f/-F` 或 `--input` 传文件。
- `gh pr diff` 不支持按文件路径直接过滤；按文件获取 patch 使用 `gh api repos/{owner}/{repo}/pulls/{num}/files --paginate` 再筛选。
- 提交行内评论前，必须先查询 `headRefOid`，并保证请求里的 `commit_id` 与其一致；否则常见 `422`。
- 构造复杂 JSON 时，优先内存对象后通过标准输入喂给 `gh api --input -`，避免在工作区落地临时文件。

## Failure Handling

- 认证失败：先执行 `gh auth status`，返回失败原因并给出最小修复命令。
- 权限不足（repo/org/token scope）：明确缺失权限，不尝试重复写操作。
- 资源不存在（PR/Issue 编号错误）：先回显查询命令与空结果，再请求更正目标。
- 分支保护或检查未通过导致无法 merge：返回阻塞项（review/check/protection），并给出可执行下一步。
- 二次执行冲突（已 merge、已关闭、已评论）：识别幂等场景并停止重复变更。

## Safety Checklist

执行任何写操作前，先确认：

- 目标仓库（`owner/repo`）。
- 目标对象（PR/Issue 编号或 workflow 名称）。
- 操作类型（comment/review/merge/run 等）。
- 关键策略（merge 方法、是否 `--delete-branch`、是否 `--auto`）。
- 若为行内评论：`headRefOid` 与 `commit_id` 一致。
- 预期结果（状态变化、评论内容、触发记录）。

缺任一关键项时，先补信息，再执行。

## Output Format

统一按以下结构输出：

1. `Plan`: 本次要做的动作（1-2 行）。
2. `Commands`: 实际执行的命令（先只读，后变更）。
3. `Result`: 关键字段（如 `number`、`state`、`url`、`reviewDecision`）。
4. `Next`: 若失败或受阻，给最短可执行下一步。

## Reference

按需读取参考文档，避免一次加载全部命令：

- 入口索引：`references/commands.md`
- 认证：`references/auth.md`
- 仓库上下文：`references/repo.md`
- PR：`references/pr.md`
- Issue：`references/issue.md`
- Workflow：`references/workflow.md`
- Run：`references/run.md`
- API：`references/api.md`
- 细粒度子命令：`references/commands.md` 列出的 `*-*.md` 文件（如 `pr-diff.md`、`run-watch.md`）
