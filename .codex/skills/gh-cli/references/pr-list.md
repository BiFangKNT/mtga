# gh pr list

```bash
gh pr list --state open --limit 30 --json number,title,author,reviewDecision,statusCheckRollup --jq '.[] | {number, title, author: .author.login, reviewDecision}'
```

用途：拉取 PR 列表并输出结构化摘要。
