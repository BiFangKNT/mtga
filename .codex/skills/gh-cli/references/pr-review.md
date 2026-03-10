# gh pr review

```bash
gh pr review 123 --comment --body "请补充回归测试说明。"
gh pr review 123 --approve --body "LGTM"
gh pr review 123 --request-changes --body "请修复空指针分支。"
```

用途：提交 PR 整体审查结论（评论/批准/请求修改）。

边界：`gh pr review` 不是行内评论接口。需要“按文件/按行评论”时，使用 `gh api`：

1. 先获取当前头提交 SHA（`headRefOid`）：

```bash
gh pr view 123 --json headRefOid --jq '.headRefOid'
```

2. 再调用行内评论 API，并保证 `commit_id=headRefOid`（否则常见 `422`）：

```bash
gh api repos/{owner}/{repo}/pulls/123/comments --method POST --input -
gh api repos/{owner}/{repo}/pulls/123/reviews --method POST --input -
```

PowerShell 不落盘示例（单条行内评论）：

```powershell
$owner = "octo-org"
$repo = "octo-repo"
$pr = 123
$head = gh pr view $pr --repo "$owner/$repo" --json headRefOid --jq '.headRefOid'

$payload = @{
  body = "建议抽出公共函数，减少重复逻辑。"
  commit_id = $head
  path = "src/app.ts"
  line = 42
  side = "RIGHT"
} | ConvertTo-Json -Depth 8

$payload | gh api "repos/$owner/$repo/pulls/$pr/comments" --method POST --input -
```
