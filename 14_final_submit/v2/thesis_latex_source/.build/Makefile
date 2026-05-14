all: pdf
pdf:
	xelatex main
	biber main
	xelatex main
	xelatex main
clean:
	rm -f *.aux *.bbl *.bcf *.blg *.log *.out *.run.xml *.toc *.lof *.lot main.pdf chapters/*.aux
