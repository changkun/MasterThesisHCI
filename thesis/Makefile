all: clean
	latexmk -silent -pdf thesis.tex
	latexmk -c
.PHONY: all

clean:
	rm -rf *.aux *.dvi *.log *.out *.toc *.fdb_latexmk *.fls *.bbl *.blg
.PHONY: clean