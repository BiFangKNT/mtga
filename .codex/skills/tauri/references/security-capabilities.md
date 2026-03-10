# 权限模型与 Capabilities

## Tauri v2 权限结构

按以下顺序建模：

1. 定义 permission：允许哪些命令族可用。
2. 定义 scope：限制参数范围（路径、URL、参数格式）。
3. 定义 capability：把权限与 scope 绑定到具体窗口/WebView。

## capability 最小模板

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "main-capability",
  "windows": ["main"],
  "permissions": [
    "core:path:default",
    "core:event:default",
    "core:window:default",
    "core:app:default"
  ]
}
```

## 文件系统权限示例

只放行业务必需目录：

```json
{
  "permissions": [
    "fs:default",
    {
      "identifier": "fs:allow-read-text-file",
      "allow": [{ "path": "$APPDATA/**" }]
    },
    {
      "identifier": "fs:allow-write-text-file",
      "allow": [{ "path": "$APPDATA/**" }]
    }
  ]
}
```

## 网络权限示例

显式白名单目标域名：

```json
{
  "permissions": [
    {
      "identifier": "http:default",
      "allow": [{ "url": "https://api.example.com/*" }]
    }
  ]
}
```

## Shell 插件权限示例

只允许受控命令，限制参数格式：

```json
{
  "permissions": [
    {
      "identifier": "shell:allow-execute",
      "allow": [
        {
          "name": "exec-sh",
          "cmd": "sh",
          "args": ["-c", { "validator": "\\S+" }],
          "sidecar": false
        }
      ]
    }
  ]
}
```

## 审核要点

1. capability 是否绑定了正确窗口。
2. 是否存在超范围路径（如全盘读写）。
3. 是否存在过宽网络白名单（如 `*`）。
4. shell 权限是否限制命令与参数。
