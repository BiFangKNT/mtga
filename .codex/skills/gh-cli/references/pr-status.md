# gh pr status

```bash
gh pr status --json currentBranch,createdByCurrentUser,needsReview --jq '{currentBranch, needsReview}'
```

用途：查看与当前用户相关的 PR 状态汇总。
