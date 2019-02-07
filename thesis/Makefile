all: clean draft
.PHONY: all

draft:
	echo '\setboolean{release}{false}' > condition.tex
	latexmk -pdf thesis.tex
	latexmk -c
	make clean
release:
	echo '\setboolean{release}{true}' > condition.tex
	latexmk -pdf thesis.tex
	latexmk -c
	make clean

clean:
	rm -rf condition.tex *.aux *.dvi *.log *.out *.toc *.fdb_latexmk *.fls *.bbl *.blg
.PHONY: clean