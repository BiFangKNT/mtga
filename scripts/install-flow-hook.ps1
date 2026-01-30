# scripts\install-flow-hook.ps1
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

# hooks dir: prefer --git-path (supports worktree)
$hooksRel = (& git rev-parse --git-path hooks) 2>$null
if (-not $hooksRel) { throw "Cannot resolve hooks dir (git rev-parse --git-path hooks failed)." }

# make absolute hooks dir
$hooksDir = $hooksRel
if (-not [System.IO.Path]::IsPathRooted($hooksDir)) {
  $hooksDir = Join-Path $repoRoot $hooksDir
}
New-Item -ItemType Directory -Force -Path $hooksDir | Out-Null

$hookPath = Join-Path $hooksDir $HookName

# bash script template (no PowerShell expansion; we do placeholder replacement)
$template = @'
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
  echo "GITFLOW_BRANCH_TYPE=${GITFLOW_BRANCH_TYPE-}"
  echo "GITFLOW_BRANCH_NAME=${GITFLOW_BRANCH_NAME-}"
  echo "GITFLOW_FULL_BRANCH=${GITFLOW_FULL_BRANCH-}"
  echo "GITFLOW_BASE_BRANCH=${GITFLOW_BASE_BRANCH-}"
  echo "GITFLOW_ORIGIN=${GITFLOW_ORIGIN-}"
  echo "GITFLOW_VERSION=${GITFLOW_VERSION-}"
} >>"$log" 2>&1

# push branches
git push "$remote" "$main_branch" "$dev_branch" >>"$log" 2>&1

# push tag (if HEAD is tagged)
tag="$(git describe --tags --exact-match 2>/dev/null || true)"
if [[ -n "$tag" ]]; then
  git push "$remote" "refs/tags/$tag" >>"$log" 2>&1
else
  echo "no tag on HEAD, skip tag push" >>"$log" 2>&1
fi
'@

$script = $template.
  Replace("__REMOTE__", $Remote).
  Replace("__MAIN__",   $MainBranch).
  Replace("__DEV__",    $DevBranch).
  Replace("__HOOK__",   $HookName)

Write-TextFileUtf8NoBomLf -Path $hookPath -Content $script

# Try to chmod +x via Git Bash (bash.exe on PATH)
$bashCmd = Get-Command bash.exe -ErrorAction SilentlyContinue
if ($bashCmd) {
  # Use relative path inside repoRoot to avoid Windows path quoting issues.
  $hookRelPath = Join-Path $hooksRel $HookName
  $repoRootBash = ($repoRoot -replace '\\','/')
  $hookRelBash  = ($hookRelPath -replace '\\','/')

  & $bashCmd.Source -lc "cd '$repoRootBash' && chmod +x '$hookRelBash'"
  "✅ 已写入 hook 并 chmod +x：$hookPath"
} else {
  "✅ 已写入 hook：$hookPath"
  "⚠️ 未找到 bash.exe（Git Bash）。请打开 Git Bash 手动执行：chmod +x $hooksRel/$HookName"
}

"📄 日志会写到：$(Join-Path ((& git rev-parse --git-dir)) 'flow-hook.log')"
