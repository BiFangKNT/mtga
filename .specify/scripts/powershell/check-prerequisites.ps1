param(
  [switch]$Json,
  [switch]$RequireTasks,
  [switch]$IncludeTasks
)

$repoRoot = Get-Location
$specsDir = Join-Path $repoRoot ".specify\specs"
if (!(Test-Path $specsDir)) {
  Write-Error "specs dir not found"
  exit 1
}

$specFile = Get-ChildItem $specsDir -Recurse -Filter "spec.md" -ErrorAction SilentlyContinue |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First 1

if (-not $specFile) {
  Write-Error "spec.md not found under .specify\specs"
  exit 1
}

$featureDir = Split-Path $specFile.FullName -Parent
$available = @()
Get-ChildItem $featureDir -File -ErrorAction SilentlyContinue | ForEach-Object {
  $available += $_.Name
}

if ($IncludeTasks -and (Test-Path (Join-Path $featureDir "tasks.md"))) {
  if ($available -notcontains "tasks.md") {
    $available += "tasks.md"
  }
}

if ($RequireTasks -and -not (Test-Path (Join-Path $featureDir "tasks.md"))) {
  Write-Error "tasks.md not found under feature dir"
  exit 1
}

$payload = [ordered]@{
  FEATURE_DIR = $featureDir
  AVAILABLE_DOCS = $available
}

if ($Json) {
  $payload | ConvertTo-Json -Depth 5
} else {
  $payload
}
