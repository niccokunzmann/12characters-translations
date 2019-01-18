#/bin/bash

input="$1"
output="$2"

if [ -z "$input" ] || [ -z "$output" ]; then
  echo "Need two arguments: input and output."
  exit 1
fi

cp "$input" "$output"
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
  "’/'" \
  '₂/$_2$'
#      '\[/\\[' \
#      '\]/\\]' \
#      '°/$\degree$'
do
  cat "$output" | sed "s/$substitution/g" > "$output.tmp"
  rm -f "$output"
  mv "$output.tmp" "$output"
done

