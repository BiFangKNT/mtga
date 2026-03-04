# gh api graphql

```bash
gh api graphql -f query='query($owner:String!, $repo:String!){repository(owner:$owner,name:$repo){pullRequests(states:OPEN){totalCount}}}' -f owner='{owner}' -f repo='{repo}'
```

用途：通过 GraphQL 查询聚合数据。
