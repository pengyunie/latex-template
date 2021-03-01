#!/bin/bash

set -x
set -e

make clean && make
rm -rf source.zip source
mkdir source
python3 format.py main.tex
mv formatted.tex source/main.tex

# ACM
cp main.bbl ACM-Reference-Format.bst acmart.cls source/
# IEEE
#cp main.bbl IEEEtran.bst IEEEtran.cls source/

cp -r figs source/
cp -r tables source/

zip -r source source
rm -rf source/
