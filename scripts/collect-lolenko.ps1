[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

$targetDir = Join-Path $projectRoot "лоленко"
if (-not (Test-Path -LiteralPath $targetDir)) {
    New-Item -ItemType Directory -Path $targetDir | Out-Null
}

$sourceDocx = Join-Path $projectRoot "Пояснительная записка_Лоленко.docx"
$targetDocx = Join-Path $targetDir "Пояснительная записка_Лоленко.docx"
if (Test-Path -LiteralPath $sourceDocx) {
    Move-Item -LiteralPath $sourceDocx -Destination $targetDocx -Force
}

$legacyDir = Join-Path $projectRoot "sections\lolenko"
if (Test-Path -LiteralPath $legacyDir) {
    Get-ChildItem -LiteralPath $legacyDir -Force | ForEach-Object {
        Move-Item -LiteralPath $_.FullName -Destination (Join-Path $targetDir $_.Name) -Force
    }

    if (-not (Get-ChildItem -LiteralPath $legacyDir -Force | Select-Object -First 1)) {
        Remove-Item -LiteralPath $legacyDir -Force
    }
}

if (-not (Test-Path -LiteralPath $targetDocx)) {
    throw "Source file not found: $targetDocx"
}

if (-not (Get-Command pandoc -ErrorAction SilentlyContinue)) {
    throw "pandoc not found in PATH."
}

$markdownPath = Join-Path $targetDir "Пояснительная записка_Лоленко.md"
$mediaDir = Join-Path $targetDir "media"

& pandoc `
    --from=docx `
    --to=gfm `
    --wrap=none `
    --extract-media="$mediaDir" `
    --output="$markdownPath" `
    "$targetDocx"

Write-Host "Done:"
Write-Host " - Folder: $targetDir"
Write-Host " - Markdown: $markdownPath"

