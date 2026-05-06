@echo off
set PATH=%PATH%;C:\Users\16084\AppData\Local\Programs\MiKTeX\miktex\bin\x64
cd /d "C:\Users\16084\Documents\Graduation_Design_Library\thesis_latex"

echo ========================================
echo Step 1/4: xelatex (first pass)
echo ========================================
xelatex -interaction=nonstopmode main.tex
if %ERRORLEVEL% NEQ 0 (
    echo WARNING: xelatex first pass had errors, continuing...
)

echo.
echo ========================================
echo Step 2/4: biber (bibliography)
echo ========================================
biber main
if %ERRORLEVEL% NEQ 0 (
    echo WARNING: biber had errors, continuing...
)

echo.
echo ========================================
echo Step 3/4: xelatex (second pass)
echo ========================================
xelatex -interaction=nonstopmode main.tex

echo.
echo ========================================
echo Step 4/4: xelatex (third pass)
echo ========================================
xelatex -interaction=nonstopmode main.tex

echo.
echo ========================================
echo DONE! Check main.pdf
echo ========================================
dir main.pdf 2>nul
