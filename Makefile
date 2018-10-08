NAME := main
TEXS := $(wildcard *.tex)
TABLES := $(wildcard tables/*.tex)
FIGS := $(wildcard figs/*.tex)
PLOTS := $(wildcard figs/*.eps)
BIBS := $(wildcard *.bib)

LATEX = latex
BIBTEX = bibtex

all: ${NAME}.pdf

${NAME}.pdf: ${TEXS} ${TABLES} ${BIBS} ${FIGS} ${PLOTS} bib.bib
	-rm -f ${NAME}.aux
	-rm -f ${NAME}.bbl
	-$(LATEX) $(NAME)
	-$(BIBTEX) $(NAME)
	-$(LATEX) $(NAME)
	-$(LATEX) $(NAME)
	@echo '****************************************************************'
# vvvvvv For `latex` ONLY. Comment out for `pdflatex`
	@dvips -j0 -t letter -o $(NAME).ps $(NAME).dvi
	@ps2pdf -dPDFSETTINGS=/prepress $(NAME).ps $(NAME).pdf
# ^^^^^^^^^^^^^^^^^^^^^^^^
	@echo '******** Did you spell-check the paper? ********'

clean:
	ls $(NAME)* | grep -v ".tex" | xargs rm -f
	rm -f *.bak *~
#	find -name "*.eps" | xargs rm -f
