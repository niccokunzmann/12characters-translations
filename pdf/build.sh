#!/bin/bash
#
# Run this to build the project.
#

set -e

cd "`dirname \"$0\"`"

rm -rf build

for lang in "../play"/*; do
  if ! [ -d "$lang" ]; then
    echo "Skip $lang as it is not a language."
    continue
  fi
  code="`basename \"$lang\"`"
  echo "Prepare language $code for the book."
  for file in "$lang"/*; do
    # Replace the latex specific characters.
    # see https://tex.stackexchange.com/a/34586/125049
    #  &  %  $  #  _  {  }  ~               ^                \
    # \& \% \$ \# \_ \{ \} \textasciitilde \textasciicircum \textbackslash
    base="./build/`basename \"$lang\"`/"
    play_dir="$base/play"
    mkdir -p "$play_dir"
    output="$play_dir/`basename \"$file\"`"
    echo "    Saving `basename \"$file\"`"
    cp "$file" "$output"
    for substitution in \
      '\\/\\textbackslash' \
      '&/\\&' \
      '%/\\%' \
      '\$/\\$' \
      '#/\\#' \
      '_/\\_' \
      '{/\\{' \
      '}/\\}' \
      '~/$\\textasciitilde$' \
      '\^/$\\textasciicircum$' \
      "’/'"
#      '\[/\\[' \
#      '\]/\\]' \
#      '°/$\degree$'
    do
      sed -i "s/$substitution/g" "$output"
    done 
  done
  translators="../statistics/translators/$code.txt"
  if [ -f "$translators" ]; then
      cp "$translators" "$base/translators.txt"
  fi
done

mkdir -p "books"

for lang in "build"/*; do
  cp -r latex/* "$lang"/
  code="`basename \"$lang\"`"
  if [ -n "$1" ] && [ "$code" != "$1" ]; then
    echo "Skipping language $code because it is not $1."
    continue
  fi
  ./translate_book.py "$code"
  if docker run --rm -v "`pwd`/$lang":/latex niccokunzmann/ci-latex "/latex/build.sh"; then
    cp "$lang/main.pdf" "books/12-characters-$code.pdf"
  fi
done

