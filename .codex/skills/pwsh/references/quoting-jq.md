# `--jq` 与引号规则

## 核心规则

- 在 PowerShell 中，`|` 是管道运算符。
- 向 `--jq` 传递包含 `|` 的 jq 表达式时，必须用单引号包裹整个表达式。

## 推荐写法

```powershell
gh pr list --json number,title --jq '.[] | {number, title}'
```

```powershell
$jq = '.[] | {number, title}'
gh pr list --json number,title --jq $jq
```

## 常见错误

```powershell
# 错误：| 被 PowerShell 当成管道而非 jq 表达式内容
gh pr list --json number,title --jq .[] | {number, title}
```

## 单引号内再包含单引号

- 用两个单引号 `''` 表示一个字面量单引号。

```powershell
$jq = '.[] | select(.title == ''fix: parser'')'
gh pr list --json title --jq $jq
```

## 需要变量时

- 先在 PowerShell 中构造字符串变量，再把变量传给 `--jq`。
- 避免在命令行中混用多层引号和插值。

```powershell
$field = 'title'
$jq = '.[] | .' + $field
gh pr list --json title --jq $jq
```
