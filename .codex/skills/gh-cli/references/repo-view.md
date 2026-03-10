# gh repo view

```bash
gh repo view --json nameWithOwner,defaultBranchRef -q '{repo: .nameWithOwner, defaultBranch: .defaultBranchRef.name}'
gh repo view --json id,nameWithOwner,isPrivate,url
```

用途：确认仓库上下文、默认分支和仓库属性。
