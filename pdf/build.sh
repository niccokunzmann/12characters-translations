#!/bin/bash
#
# Run this to build the project.
#

cd "`dirname \"$0\"`"

for lang in "../play"/*; do
  if ! [ -d "$lang" ]; then
    echo "Skip $lang as it is not a language."
    continue
  fi
  echo "Prepare language $lang for the book."
  for file in "$lang"/*; do
    # Replace the latex specific characters.
    # see https://tex.stackexchange.com/a/34586/125049
    #  &  %  $  #  _  {  }  ~               ^                \
    # \& \% \$ \# \_ \{ \} \textasciitilde \textasciicircum \textbackslash
    dir="./translations/play/`basename \"$lang\"`"
    mkdir -p "$dir"
    output="$dir/`basename \"$file\"`"
    echo "Saving $file to $output"
    cp "$file" "$output"
    for substitution in '\\/\textbackslash' '&/\&' '%/\%' '$/\$' '#/\#' '_/\_' '\{/\{' '\}/\}' '~/$\textasciitilde$' '^/$\textasciicircum$' '\[/\[' '\]/\]'; do
      sed -i "s/$substitution/g" "$output"
    done 
  done
done

