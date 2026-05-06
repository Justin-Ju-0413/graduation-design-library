$env:Path += ';C:\Users\16084\AppData\Local\Programs\MiKTeX\miktex\bin\x64'
Set-Location 'C:\Users\16084\Documents\Graduation_Design_Library\thesis_latex'

Write-Host "=== XeLaTeX Pass 1 ==="
xelatex -interaction=nonstopmode -synctex=1 main.tex 2>&1 | Select-String "Error|Warning:|Output written|pages" | Select-Object -Last 10

Write-Host "`n=== Biber (bibliography) ==="
biber main 2>&1 | Select-Object -Last 5

Write-Host "`n=== XeLaTeX Pass 2 ==="
xelatex -interaction=nonstopmode main.tex 2>&1 | Select-String "Error|Warning:|Output written|pages" | Select-Object -Last 10

Write-Host "`n=== XeLaTeX Pass 3 (final) ==="
xelatex -interaction=nonstopmode main.tex 2>&1 | Select-String "Error|Warning:|Output written|pages" | Select-Object -Last 10

Write-Host "`n=== Done ==="
if (Test-Path main.pdf) {
    $size = (Get-Item main.pdf).Length / 1KB
    Write-Host "PDF created: main.pdf ($size KB)"
} else {
    Write-Host "ERROR: main.pdf not found. Check main.log for errors."
}
