param(
    [string]$BaselineDir = "14_final_submit\v2"
)

$ErrorActionPreference = "Stop"

function Fail($Message) {
    Write-Error $Message
    exit 1
}

$root = git rev-parse --show-toplevel
if (-not $root) {
    Fail "Not inside a Git repository."
}

Set-Location $root

$requiredFiles = @(
    "$BaselineDir\README.md",
    "$BaselineDir\BASELINE_MANIFEST.txt",
    "$BaselineDir\thesis\FYP_Thesis_Final_v2_SUBMISSION_BASELINE.docx",
    "$BaselineDir\thesis\main_final_SUBMISSION_REFERENCE.pdf",
    "$BaselineDir\presentation\FYP_Final_Defense_English_Draft_REPORT_BASELINE.pptx",
    "$BaselineDir\presentation\Final_Defense_Bilingual_Script.docx",
    "$BaselineDir\presentation\Final_Defense_QA_Bilingual.docx",
    "$BaselineDir\thesis_latex_source\main.tex",
    "$BaselineDir\thesis_latex_source\references.bib"
)

Write-Host "Checking required final baseline files..."
foreach ($file in $requiredFiles) {
    if (-not (Test-Path -LiteralPath $file -PathType Leaf)) {
        Fail "Missing required file: $file"
    }
}

Write-Host "Checking Git tracking for baseline files..."
foreach ($file in $requiredFiles) {
    git ls-files --error-unmatch -- "$file" *> $null
    if ($LASTEXITCODE -ne 0) {
        Fail "Required file is not tracked by Git: $file"
    }
}

Write-Host "Checking thesis_latex_source archive..."
$sourceCount = (Get-ChildItem -LiteralPath "$BaselineDir\thesis_latex_source" -Recurse -File | Measure-Object).Count
if ($sourceCount -lt 50) {
    Fail "thesis_latex_source looks incomplete: only $sourceCount files."
}

Write-Host "Checking Git remote..."
$remote = git remote get-url origin 2>$null
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($remote)) {
    Fail "Git remote 'origin' is not configured."
}
Write-Host "origin: $remote"

Write-Host "Checking working tree status..."
$status = git status --short
if ($status) {
    Write-Host $status
    Fail "Working tree has uncommitted changes. Commit or intentionally leave them before pushing."
}

Write-Host "Checking current baseline tag..."
$tags = git tag --points-at HEAD
if ($tags -notmatch "fyp-final-v2-complete-archive-2026-05-14") {
    Write-Warning "HEAD is not tagged with fyp-final-v2-complete-archive-2026-05-14."
}

Write-Host "Upload check passed."
