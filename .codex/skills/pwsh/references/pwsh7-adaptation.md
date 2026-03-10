# pwsh7 适配（增量）

## 版本门槛

- 仅在 `$PSVersionTable.PSVersion.Major -ge 7` 时启用本文件策略。
- 涉及参数传递差异时，再细分 `7.3+`。

```powershell
$isPwsh7 = $PSVersionTable.PSVersion.Major -ge 7
$isPwsh73Plus = $PSVersionTable.PSVersion -ge [version]'7.3'
```

## 7.3+ 原生命令参数变化

- pwsh 7.3 起，原生命令参数传递行为有破坏性变更。
- 通过 `$PSNativeCommandArgumentPassing` 控制行为。
- 常见值：`Legacy`、`Standard`、`Windows`。

```powershell
Get-Variable PSNativeCommandArgumentPassing -Scope Global
```

## 推荐适配流程

1. 先保持默认值执行。
2. 若旧脚本因参数引用失败，再临时切换到 `Legacy` 兼容模式。
3. 命令完成后恢复原值，避免影响后续命令。

```powershell
$old = $PSNativeCommandArgumentPassing
try {
  $PSNativeCommandArgumentPassing = 'Legacy'
  # 运行依赖旧参数行为的原生命令
}
finally {
  $PSNativeCommandArgumentPassing = $old
}
```

## 何时优先 `--%`

- 只需修单条命令且不想改全局变量时，优先 `--%`。
- 需要兼容一组旧脚本时，再考虑临时切换 `Legacy`。

## 7.x 增强特性使用原则

- 先给 5.1 兼容解法，再给 7.x 增强写法。
- 输出中明确“此写法需要 pwsh7+”。
