MAINS := main
TEXS := $(wildcard *.tex)
TABLES := $(wildcard tables/*.tex)
FIGS := $(wildcard figs/*.tex)
PLOTS := $(wildcard figs/*.eps)
BIBS := $(wildcard *.bib)

LATEX = pdflatex
BIBTEX = bibtex

.PHONY: all
all: $(MAINS:=.pdf)

.PHONY: display
display: $(MAINS:=.pdf)
	evince $(MAINS:=.pdf)

$(MAINS:=.pdf) : %.pdf : ${TEXS} ${TABLES} ${BIBS} ${FIGS} ${PLOTS}
	-rm -f $*.aux
	-rm -f $*.bbl
	-$(LATEX) $*
	-$(BIBTEX) $*
	-$(LATEX) $*
	-$(LATEX) $*
	-$(LATEX) $*
	@echo '****************************************************************'
# vvvvvv For `latex` ONLY. Comment out for `pdflatex`
#	@dvips -j0 -t letter -o $(NAME).ps $(NAME).dvi
#	@ps2pdf -dPDFSETTINGS=/prepress $(NAME).ps $(NAME).pdf
# ^^^^^^^^^^^^^^^^^^^^^^^^
	@echo '******** Did you spell-check the paper? ********'

.PHONY: clean
clean:
	ls $(MAINS:=.*) | grep -v ".tex" | xargs rm -f
	rm -f *.bak *~
#	find -name "*.eps" | xargs rm -f
