[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

$artifacts = @(
    "main.aux",
    "main.bbl",
    "main.bcf",
    "main.blg",
    "main.log",
    "main.out",
    "main.pdf",
    "main.run.xml",
    "main.synctex.gz",
    "main.toc",
    "texput.aux",
    "texput.log",
    "texput.pdf",
    "font_test.aux",
    "font_test.log",
    "font_test.pdf"
)

foreach ($artifact in $artifacts) {
    $artifactPath = Join-Path $projectRoot $artifact
    if (Test-Path $artifactPath) {
        Remove-Item $artifactPath -Force
        Write-Host "Removed $artifact"
    }
}
