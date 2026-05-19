# Сборка презентации Beamer; PDF: ../output/presentation.pdf
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$out = Join-Path $root 'output'
New-Item -ItemType Directory -Force -Path $out | Out-Null
$job = 'presentation'
$tex = 'main.tex'
$passes = 2
for ($i = 0; $i -lt $passes; $i++) {
    & pdflatex `
        -interaction=nonstopmode `
        -halt-on-error `
        -file-line-error `
        "-output-directory=$out" `
        "-jobname=$job" `
        $tex
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
Write-Host "OK: $(Join-Path $out "$job.pdf")"
