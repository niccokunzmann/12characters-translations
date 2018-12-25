#!/bin/bash

set -e

cd "`dirname \"$0\"`"

lualatex main
makeindex main.idx -s StyleInd.ist
biber main
lualatex main x 2

