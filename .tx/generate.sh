#!/bin/bash

cd "`dirname \"$0\"`"

echo "[main]"
echo "host = https://www.transifex.com"
echo
echo "[12-characters-book.structure-json]"
echo "file_filter = pdf/book/structure/<lang>.json"
echo "minimum_perc = 0"
echo "source_file = pdf/book/structure/en.json"
echo "source_lang = en"
echo "type = KEYVALUEJSON"
echo


for chapter in `ls ../play/en`; do
  echo "[12-characters-play.`echo \"$chapter\" |  sed 's/[^0-9a-zA-Z-]/-/g'`]"
  echo "file_filter = play/<lang>/$chapter"
  echo "minimum_perc = 100"
  echo "source_file = play/en/$chapter"
  echo "source_lang = en"
  echo "type = TXT"
  echo
done
