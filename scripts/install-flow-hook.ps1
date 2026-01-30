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

# repo root
$repoRoot = (& git rev-parse --show-toplevel) 2>$null
if (-not $repoRoot) { throw "Not a git repository (git rev-parse failed)." }

# IMPORTANT: respect core.hooksPath
$hooksPath = (& git rev-parse --git-path hooks) 2>$null
if (-not $hooksPath) { throw "Cannot resolve hooks path (git rev-parse --git-path hooks failed)." }
$hooksPath = $hooksPath.Trim()

if (-not [System.IO.Path]::IsPathRooted($hooksPath)) {
  $hooksDir = Join-Path $repoRoot $hooksPath
} else {
  $hooksDir = $hooksPath
}

New-Item -ItemType Directory -Force -Path $hooksDir | Out-Null

$hookCmd = Join-Path $hooksDir ($HookName + ".cmd")
$hookSh  = Join-Path $hooksDir ($HookName + ".sh")

# --- bash logic ---
$shTemplate = @'
#!/usr/bin/env bash
set -euo pipefail

remote="${GITFLOW_ORIGIN:-__REMOTE__}"
main_branch="__MAIN__"
dev_branch="__DEV__"

gitdir="$(git rev-parse --git-dir)"
log="$gitdir/flow-hook.log"

{
  echo "----"
  echo "__HOOK__ @ $(date)"
  echo "remote=$remote"
  echo "branch=$(git rev-parse --abbrev-ref HEAD)"
  echo "GITFLOW_VERSION=${GITFLOW_VERSION-}"
} >>"$log" 2>&1

git push "$remote" "$main_branch" "$dev_branch" >>"$log" 2>&1

tag="$(git describe --tags --exact-match 2>/dev/null || true)"
if [[ -n "$tag" ]]; then
  git push "$remote" "refs/tags/$tag" >>"$log" 2>&1
else
  echo "no tag on HEAD, skip tag push" >>"$log" 2>&1
fi
'@

$sh = $shTemplate.
  Replace("__REMOTE__", $Remote).
  Replace("__MAIN__", $MainBranch).
  Replace("__DEV__", $DevBranch).
  Replace("__HOOK__", $HookName)

Write-TextFileUtf8NoBomLf -Path $hookSh -Content $sh

# --- windows cmd wrapper ---
$cmd = @"
@echo off
setlocal

REM Find bash.exe (Git for Windows)
for %%B in (bash.exe) do set "BASH=%%~$PATH:B"
if not defined BASH (
  echo [git-flow hook] bash.exe not found in PATH. 1>&2
  exit /b 1
)

"%BASH%" "%~dp0$HookName.sh"
exit /b %ERRORLEVEL%
"@

Write-TextFileUtf8NoBomLf -Path $hookCmd -Content $cmd

"OK:
- Hook CMD : $hookCmd
- Hook SH  : $hookSh
- hooksDir : $hooksDir
Log file will be written under: (git rev-parse --git-dir)\flow-hook.log
"
