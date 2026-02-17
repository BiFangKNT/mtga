# Final Build Script (Fixed Python Environment)
$ErrorActionPreference = "Stop"

Write-Host "=== MTGA Build Process ===" -ForegroundColor Cyan

# 1. Add Cargo to PATH (for safety)
$cargoBin = "$env:USERPROFILE\.cargo\bin"
$env:PATH = "$env:PATH;$cargoBin"

# 2. Setup Python Environment Correctly
Write-Host "Running Python setup script..." -ForegroundColor Yellow
Push-Location python-src
uv run python ../scripts/setup_pyembed.py
Pop-Location

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Python environment setup failed!" -ForegroundColor Red
    exit 1
}

# 3. Set Environment Variables
$pyPath = "$pwd\src-tauri\pyembed\python\python.exe"
$env:PYO3_PYTHON = $pyPath
Write-Host "Set PYO3_PYTHON: $pyPath"

# 4. Run Build
Write-Host "Starting build..." -ForegroundColor Green
pnpm tauri:bundle:win

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n🎉 Build Success!" -ForegroundColor Green
    Get-ChildItem -Path "src-tauri\target\release\bundle\nsis\*.exe" -Recurse | ForEach-Object { 
        Write-Host "Installer: $($_.FullName)" -ForegroundColor Cyan 
    }
}
