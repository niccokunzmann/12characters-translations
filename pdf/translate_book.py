#!/usr/bin/python3

import json
import sys
import os
import time
import locale
import datetime

# configuration
NUMBER_OF_CHAPTERS_PER_PART = 3

# varaibles
LANG = sys.argv[1]
BASE = os.path.join("build", LANG)
MAIN = os.path.join(BASE, "main.tex")
CHAPTERS_FOLDER = os.path.join(BASE, "play")
CHAPTERS = [os.path.join(CHAPTERS_FOLDER, chapter)
            for chapter in os.listdir(CHAPTERS_FOLDER)]
CHAPTERS.sort()

with open(MAIN, encoding="UTF-8") as file:
    main_text = file.read()
TRANSLATIONS_PATH = os.path.join("book", "structure", LANG + ".json")
if not os.path.exists(TRANSLATIONS_PATH):
    TRANSLATIONS_PATH = os.path.join("book", "structure","en.json")
translations = json.load(open(TRANSLATIONS_PATH, encoding="UTF-8"))

# set the correct locale
# see https://docs.python.org/3/library/locale.html
locale.resetlocale()
try:
    locale.setlocale(locale.LC_ALL, LANG)
except locale.Error:
    pass
# set the version according to the locale used by the document
# see https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
translations["VERSION"] = datetime.datetime.now().strftime("%c")
# set the translators if given.
TRANSLATORS = os.path.join(BASE, "translators.txt")
if os.path.exists(TRANSLATORS):
    with open(TRANSLATORS) as file:
        text = translations.get("TRANSLATORS", "").replace("<TRANSLATORS>", file.read())
        translations["TRANSLATORS"] = text
else:
    translations["TRANSLATORS"] = ""

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
        key = "PART-{}".format(i // NUMBER_OF_CHAPTERS_PER_PART + 1)
        part_heading = translations.get(key, key)
        PARTS += PART.replace("PART", part_heading)
    with open(chapter_file, encoding="UTF-8") as file:
        try:
            text = file.read()
        except UnicodeDecodeError:
            print(chapter_file)
            raise
    heading, text = text.split("\n", 1)
    PARTS += CHAPTER.replace("CHAPTER", heading).replace("TEXT", text)

main_text = main_text.replace("PARTS", PARTS)

with open(MAIN, "w", encoding="UTF-8") as file:
    file.write(main_text)

