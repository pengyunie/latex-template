MAIN := main
TARGETS := $(MAIN)

TARGETS_PATTERN := ($(shell echo $(TARGETS) | sed 's/ /|/g'))
DEPENDENCIES := $(shell find . -type f | grep -v -E "/$(TARGETS_PATTERN)\." | grep -v -E "\.gitignore|pdflatex2041000\.fls|\.DS_Store|\*~")


.PHONY: all
all: $(TARGETS:=.pdf)

$(TARGETS) : % : %.pdf

$(TARGETS:=.pdf) : %.pdf : %.tex $(DEPENDENCIES)
	latexmk -pdf $< -synctex=1 -file-line-error -interaction=nonstopmode -halt-on-error -logfilewarninglist

$(TARGETS:=-auto) : %-auto : %.tex $(DEPENDENCIES)
	latexmk -pdf $< -synctex=1 -file-line-error -interaction=nonstopmode -halt-on-error -logfilewarninglist -pvc

.PHONY: clean
clean:
	latexmk -C
