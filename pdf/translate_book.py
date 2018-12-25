#!/usr/bin/python3

import json
import sys
import os

# configuration
NUMBER_OF_CHAPTERS_PER_PART = 3

# varaibles
LANG = sys.argv[1]
BASE = os.path.join("build", LANG)
MAIN = os.path.join(BASE, "main.tex")
CHAPTERS_FOLDER = os.path.join(BASE, "play")
CHAPTERS = [os.path.join(CHAPTERS_FOLDER, chapter)
            for chapter in os.listdir(CHAPTERS_FOLDER)]

with open(MAIN) as file:
    main_text = file.read()
translations = json.load(open(os.path.join("book", "structure", LANG + ".json")))
for key, value in translations.items():
    if key:
        main_text = main_text.replace(key, value)

PART = """
%----------------------------------------------------------------------------------------
%	PART
%----------------------------------------------------------------------------------------

\part{PART}

"""

CHAPTER = """
%----------------------------------------------------------------------------------------
%	CHAPTER
%----------------------------------------------------------------------------------------


\chapterimage{chapter_head_2.pdf} % Chapter heading image

\chapter{CHAPTER}

TEXT
"""

PARTS = ""

for i, chapter_file in enumerate(CHAPTERS):
    if i % NUMBER_OF_CHAPTERS_PER_PART == 0:
        key = "PART-{}".format(i//NUMBER_OF_CHAPTERS_PER_PART)
        part_heading = translations.get(key, key)
        PARTS += PART.replace("PART", part_heading)
    with open(chapter_file) as file:
        text = file.read()
    heading, text = text.split("\n", 1)
    PARTS += CHAPTER.replace("CHAPTER", heading).replace("TEXT", text)

main_text = main_text.replace("PARTS", PARTS)

with open(MAIN, "w") as file:
    file.write(main_text)

