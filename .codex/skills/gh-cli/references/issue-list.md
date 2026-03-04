# gh issue list

```bash
gh issue list --state open --limit 50 --json number,title,labels,assignees --jq '.[] | {number, title}'
```

用途：查询 issue 列表并输出关键字段。
