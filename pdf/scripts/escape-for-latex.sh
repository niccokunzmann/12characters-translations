#/bin/bash

set -e

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
  # cross platform inplace sed replacement
  # see https://stackoverflow.com/a/22084103
  sed -i.bak "s/$substitution/g" "$output" && rm "$output.bak"
done

