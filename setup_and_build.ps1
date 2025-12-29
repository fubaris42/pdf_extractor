# setup_and_build.ps1
$ErrorActionPreference = "Stop"
Write-Host "--- Industry Standard Build Initialized ---" -ForegroundColor Cyan

# 1. Environment Isolation
if (-not (Test-Path ".venv")) {
    Write-Host "Creating Isolated Environment..." -ForegroundColor Yellow
    python -m venv .venv
}
$pip = ".venv\Scripts\pip.exe"
$pyinstaller = ".venv\Scripts\pyinstaller.exe"

# 2. Dependency Management
Write-Host "Syncing requirements..." -ForegroundColor Gray
& $pip install -r requirements.txt --upgrade

# 3. Clean Artifacts
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }

# 4. High-Performance Build (--onedir for instant launch)
Write-Host "Compiling High-Performance Binary..." -ForegroundColor Green
& $pyinstaller --noconsole `
    --onedir `
    --manifest "build_tools/longpaths.manifest" `
    --name "PDFExtractor" `
    --paths "src/pdf_extractor" `
    "src/pdf_extractor/gui.py"

# 5. Desktop Integration
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$([Environment]::GetFolderPath('Desktop'))\PDFExtractor.lnk")
$Shortcut.TargetPath = "$(Get-Location)\dist\PDFExtractor\PDFExtractor.exe"
$Shortcut.WorkingDirectory = "$(Get-Location)\dist\PDFExtractor"
$Shortcut.Save()

Write-Host "Build Complete! Desktop shortcut created." -ForegroundColor Cyan