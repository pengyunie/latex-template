.PHONY: all
all: 
	latexmk -pdf main.tex -synctex=1 -file-line-error

.PHONY: auto
auto:
	latexmk -pdf -pvc main.tex -synctex=1 -interaction=nonstopmode -file-line-error

.PHONY: clean
clean: 
	latexmk -c
