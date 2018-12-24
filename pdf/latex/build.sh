#!/bin/bash

set -e

cd "`dirname \"$0\"`"

pdflatex main
makeindex main.idx -s StyleInd.ist
biber main
pdflatex main x 2

