#!/bin/bash

mkdir source
python3 format.py main.tex
mv formatted.tex source/main.tex
cp bib.bib ACM-Reference-Format.bst acmart.cls source/
cp -r figs source/
cp -r tables source/

zip -r source source
rm -rf source/
