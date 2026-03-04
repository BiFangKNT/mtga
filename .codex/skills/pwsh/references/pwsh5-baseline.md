# pwsh5 通用兼容基线

## 目标

- 将 Windows PowerShell 5.1 作为最低兼容基线。
- 让同一命令在 5.1 和 7.x 下都能稳定执行。

## 语法与能力边界

- 优先使用 5.1 可用语法，避免默认使用 7.x 新语法。
- 仅在确认版本后再使用 7.x 特性（例如 `??`、`||`、`&&`、`ForEach-Object -Parallel`）。

## 参数与引号

- 对包含空格、`|`、`&`、`(`、`)` 等特殊字符的参数，始终显式加引号。
- 对字面量字符串优先用单引号，避免意外变量展开。
- 原生命令复杂参数优先用变量或参数数组构造，降低转义复杂度。

## 原生命令保底方案

- 参数总被 PowerShell 误解析时，使用 `--%` 终止后续解析。
- `--%` 后内容尽量保持原生命令期望格式，不再混入 PowerShell 表达式。

```powershell
cmd /c --% echo "a|b"
```

## 编码基线

- 在 Windows PowerShell 5.1 中，默认编码行为不一致。
- 文件读写命令显式指定 `-Encoding`，避免依赖默认值。

```powershell
Get-Content .\data.txt -Encoding utf8
Set-Content .\out.txt -Encoding utf8 -Value $text
```
