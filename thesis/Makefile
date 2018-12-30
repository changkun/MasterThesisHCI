all: clean
	latexmk -pdf thesis.tex
	latexmk -c
	make clean
.PHONY: all

clean:
	rm -rf *.aux *.dvi *.log *.out *.toc *.fdb_latexmk *.fls *.bbl *.blg
.PHONY: clean