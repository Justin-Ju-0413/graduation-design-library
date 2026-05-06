@echo off
echo === XeLaTeX (1) ===
xelatex -interaction=nonstopmode main.tex
echo === Biber ===
biber main
echo === XeLaTeX (2) ===
xelatex -interaction=nonstopmode main.tex
echo === XeLaTeX (3) ===
xelatex -interaction=nonstopmode main.tex
echo === Output: main.pdf ===
