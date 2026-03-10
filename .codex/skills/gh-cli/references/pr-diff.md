# gh pr diff

```bash
gh pr diff 123
gh pr diff 123 --name-only
gh pr diff 123 --patch --color=never
```

用途：查看 PR 变更内容、变更文件列表或完整 patch。

限制：`gh pr diff` 不能按文件路径直接过滤（例如 `gh pr diff 123 -- path/to/file` 不生效）。

按文件查看 patch（推荐用 API）：

```bash
gh api --paginate repos/{owner}/{repo}/pulls/123/files --jq '.[] | {filename, status, patch}'
gh api --paginate repos/{owner}/{repo}/pulls/123/files --jq '.[] | select(.filename=="src/app.ts") | .patch'
```

说明：按文件级别分析或 review 前置筛选时，统一走 `repos/{owner}/{repo}/pulls/{num}/files`。
