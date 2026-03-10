# gh workflow run

```bash
gh workflow run ci.yml -f ref=main
gh workflow run deploy.yml -f environment=staging
```

用途：手动触发 workflow 并传入参数。
