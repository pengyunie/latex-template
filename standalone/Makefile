.PHONY: all
all: main.pdf

main.pdf: main.tex
	latexmk -pdf main

.PHONY: clean
clean:
	latexmk -C
