# PDF Extractor Pro - Build Script
$ErrorActionPreference = "Stop"

Write-Host "--- Starting Build Process ---" -ForegroundColor Cyan

# 1. Clean up previous builds to save space and avoid errors
$folders = @("build", "dist")
foreach ($folder in $folders) {
    if (Test-Path $folder) {
        Write-Host "Cleaning $folder folder..." -ForegroundColor Yellow
        Remove-Item -Recurse -Force $folder
    }
}

# 2. Ensure dependencies are installed
Write-Host "Verifying dependencies from requirements.txt..." -ForegroundColor Gray
pip install -r requirements.txt --quiet

# 3. Execute PyInstaller
Write-Host "Compiling PDFExtractorPro.exe..." -ForegroundColor Green
# --noconsole: Hides the black terminal
# --onefile: Bundles everything into a single EXE
# --manifest: Enables Windows Long Path support
pyinstaller --noconsole `
            --onefile `
            --manifest "longpaths.manifest" `
            --name "PDFExtractor" `
            "src/pdf_extractor/gui.py"

Write-Host "--- Build Complete! ---" -ForegroundColor Cyan
Write-Host "Your executable is located in: $(Get-Location)\dist\PDFExtractorPro.exe" -ForegroundColor White