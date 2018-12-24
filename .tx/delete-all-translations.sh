#!/bin/bash

cd "`dirname \"$0\"`"


for chapter in `ls ../play/en`; do
  tx delete -r "12-characters-play.`echo \"$chapter\" |  sed 's/[^0-9a-zA-Z-]/-/g'`"
done
