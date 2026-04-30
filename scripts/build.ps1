[CmdletBinding()]
param(
    [switch]$SkipCleanup
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

$outputDir = Join-Path $projectRoot "output"
if (-not (Test-Path $outputDir)) {
    New-Item -Path $outputDir -ItemType Directory | Out-Null
}

$rootArtifacts = @(
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

if (-not $SkipCleanup) {
    foreach ($artifact in $rootArtifacts) {
        $artifactPath = Join-Path $projectRoot $artifact
        if (Test-Path $artifactPath) {
            Remove-Item $artifactPath -Force
        }
    }
}

if (-not (Get-Command xelatex -ErrorAction SilentlyContinue)) {
    throw "xelatex is not available in PATH."
}

if (-not (Get-Command biber -ErrorAction SilentlyContinue)) {
    throw "biber is not available in PATH."
}

$xelatexArgs = @(
    "-interaction=nonstopmode",
    "-halt-on-error",
    "-file-line-error",
    "-synctex=1",
    "-aux-directory=output",
    "-output-directory=output",
    "main.tex"
)

& xelatex @xelatexArgs
# & biber "--input-directory" "output" "--output-directory" "output" "main"
& xelatex @xelatexArgs
& xelatex @xelatexArgs


# Копируем готовый PDF из output в корень проекта
$sourcePdf = Join-Path $outputDir "main.pdf"
$targetPdf = Join-Path $projectRoot "main.pdf"
if (Test-Path $sourcePdf) {
    Copy-Item -Path $sourcePdf -Destination $targetPdf -Force
    Write-Host "PDF copied to: $targetPdf"
} else {
    Write-Warning "PDF not found in $outputDir"
}

Write-Host "Build succeeded. PDF: output/main.pdf"
