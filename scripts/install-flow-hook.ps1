param(
  [string]$HookName   = "post-flow-release-finish",
  [string]$MainBranch = "tauri",
  [string]$DevBranch  = "dev",
  [string]$Remote     = "origin"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Write-TextFileUtf8NoBomLf([string]$Path, [string]$Content) {
  $lf = $Content -replace "`r`n", "`n"
  $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
  [System.IO.File]::WriteAllText($Path, $lf, $utf8NoBom)
}

# repo root / git dir
$repoRoot = (& git rev-parse --show-toplevel) 2>$null
if (-not $repoRoot) { throw "Not a git repository (git rev-parse failed)." }

$gitDir = (& git rev-parse --git-dir) 2>$null
if (-not $gitDir) { throw "Cannot resolve .git dir (git rev-parse --git-dir failed)." }

# Normalize gitDir to absolute
if (-not [System.IO.Path]::IsPathRooted($gitDir)) {
  $gitDir = Join-Path $repoRoot $gitDir
}

$hooksDir = Join-Path $gitDir "hooks"
New-Item -ItemType Directory -Force -Path $hooksDir | Out-Null

$hookCmd = Join-Path $hooksDir ($HookName + ".cmd")
$hookSh  = Join-Path $hooksDir ($HookName + ".sh")
$logPath = Join-Path $gitDir "flow-hook.log"

# 1) bash script (real logic)
$sh = @'
#!/usr/bin/env bash
set -euo pipefail

remote="${GITFLOW_ORIGIN:-$Remote}"
main_branch="$MainBranch"
dev_branch="$DevBranch"

gitdir="$(git rev-parse --git-dir)"
log="$gitdir/flow-hook.log"

{
  echo "----"
  echo "$HookName @ \$(date)"
  echo "remote=\$remote"
  echo "branch=\$(git rev-parse --abbrev-ref HEAD)"
  echo "GITFLOW_VERSION=\${GITFLOW_VERSION-}"
} >>"\$log" 2>&1

# push branches
git push "\$remote" "\$main_branch" "\$dev_branch" >>"\$log" 2>&1

# push tag (if HEAD is tagged)
tag="$(git describe --tags --exact-match 2>/dev/null || true)"
if [[ -n "\$tag" ]]; then
  git push "\$remote" "refs/tags/\$tag" >>"\$log" 2>&1
else
  echo "no tag on HEAD, skip tag push" >>"\$log" 2>&1
fi
'@

Write-TextFileUtf8NoBomLf -Path $hookSh -Content $sh

# 2) cmd wrapper (executable entry on Windows)
#    - find bash.exe from PATH
#    - call the .sh next to it
$cmd = @"
@echo off
setlocal enabledelayedexpansion

REM Find bash.exe on PATH
for %%B in (bash.exe) do set "BASH=%%~$PATH:B"

if not defined BASH (
  echo [git-flow hook] bash.exe not found in PATH. 1>&2
  echo Install Git for Windows (Git Bash) or add bash.exe to PATH. 1>&2
  exit /b 1
)

REM Call the .sh script in the same directory
"%BASH%" "%~dp0$HookName.sh"
exit /b %ERRORLEVEL%
"@

Write-TextFileUtf8NoBomLf -Path $hookCmd -Content $cmd

"✅ 已写入 flow hook:
- $hookCmd
- $hookSh
📄 日志会写到: $logPath"
