param(
  [string]$AgentType = "claude"
)

$repoRoot = Get-Location
$target = Join-Path $repoRoot ".claude\AGENT_CONTEXT.md"
$timestamp = Get-Date -Format "yyyy-MM-dd"
$content = @(
  "AgentType: $AgentType"
  "Updated: $timestamp"
  "Note: 本次规划未新增运行时依赖，仅更新规划与配置说明。"
)

$dir = Split-Path $target -Parent
if (!(Test-Path $dir)) {
  New-Item -ItemType Directory -Path $dir | Out-Null
}

Set-Content -Path $target -Value $content -Encoding UTF8
