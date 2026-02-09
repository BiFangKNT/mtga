param(
  [switch]$Json
)

$repoRoot = Get-Location
$specsDir = Join-Path $repoRoot ".specify\specs"
if (!(Test-Path $specsDir)) {
  New-Item -ItemType Directory -Path $specsDir | Out-Null
}

$specFile = Get-ChildItem $specsDir -Recurse -Filter "spec.md" -ErrorAction SilentlyContinue |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First 1

if (-not $specFile) {
  Write-Error "spec.md not found under .specify\specs"
  exit 1
}

$featureDir = Split-Path $specFile.FullName -Parent
$implPlan = Join-Path $featureDir "plan.md"
$templatePath = Join-Path $repoRoot ".specify\templates\plan-template.md"
if (!(Test-Path $templatePath)) {
  Write-Error "plan-template.md not found"
  exit 1
}

Copy-Item $templatePath $implPlan -Force

$branch = ""
try {
  $branch = (git branch --show-current 2>$null)
} catch {
  $branch = ""
}

$payload = [ordered]@{
  FEATURE_SPEC = $specFile.FullName
  IMPL_PLAN = $implPlan
  SPECS_DIR = $specsDir
  BRANCH = $branch.Trim()
}

if ($Json) {
  $payload | ConvertTo-Json -Depth 5
} else {
  $payload
}
