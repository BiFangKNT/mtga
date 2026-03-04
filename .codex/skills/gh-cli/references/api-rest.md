# gh api REST

```bash
gh api repos/{owner}/{repo}/issues --jq '.[] | {number, title, state}'
gh api --paginate repos/{owner}/{repo}/pulls --jq '.[] | {number, title, state}'
gh api repos/{owner}/{repo}/issues -F title='Bug report' -F body='Details'
```

用途：调用 REST 接口，支持分页和字段筛选。
