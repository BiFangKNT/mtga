# gh pr checks

```bash
gh pr checks 123 --required
gh pr checks 123 --json name,state,workflow,link --jq '.[] | {name, state, workflow}'
```

用途：查看 PR CI 检查状态，定位阻塞项。
