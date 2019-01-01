#!/usr/bin/python3

import json
import sys
import os
import time
import locale
import datetime

# -----------------------------------------
# configuration
NUMBER_OF_CHAPTERS_PER_PART = 3

# -----------------------------------------
# variables
LANG = sys.argv[1]
BASE = os.path.join("build", LANG)
MAIN = os.path.join(BASE, "main.tex")
CHAPTERS_FOLDER = os.path.join(BASE, "play")
CHAPTERS = [os.path.join(CHAPTERS_FOLDER, chapter)
            for chapter in os.listdir(CHAPTERS_FOLDER)]
CHAPTERS.sort()

# -----------------------------------------
# loading translations
with open(MAIN, encoding="UTF-8") as file:
    main_text = file.read()
TRANSLATIONS_PATH = os.path.join("book", "structure", LANG + ".json")
if not os.path.exists(TRANSLATIONS_PATH):
    TRANSLATIONS_PATH = os.path.join("book", "structure","en.json")
translations = json.load(open(TRANSLATIONS_PATH, encoding="UTF-8"))

# -----------------------------------------
# version information
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

# -----------------------------------------
# set the translators if given.
TRANSLATORS = os.path.join(BASE, "translators.txt")
if os.path.exists(TRANSLATORS):
    with open(TRANSLATORS, encoding="UTF-8") as file:
        text = translations.get("TRANSLATORS", "").replace("<TRANSLATORS>", file.read())
        translations["TRANSLATORS"] = text
else:
    translations["TRANSLATORS"] = ""

# -----------------------------------------
# add the translated content
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


\chapterimage{IMAGE} % Chapter heading image

\chapter{CHAPTER}

TEXT
"""

PICTURE_LICENSE_INFORMARTION_TEXT = """

\subsection*{HEADING}

TEXT

"""

PARTS = ""
PICTURE_LICENSE_INFORMARTION = ""

def add_license(heading, license_file):
    global PICTURE_LICENSE_INFORMARTION
    with open(license_file, encoding="UTF-8") as file: # needs a license file for the picture
        try:
            license_information = file.read()
        except UnicodeDecodeError:
            print(license_file)
            raise
    PICTURE_LICENSE_INFORMARTION += (PICTURE_LICENSE_INFORMARTION_TEXT
        .replace("HEADING", heading)
        .replace("TEXT", license_information)
    )

add_license(
    translations.get("PICTURE-SOURCE-COVER", "Book Cover"),
    os.path.join(BASE, "Pictures", "background.pdf.license.txt"))

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
    image_file_name = os.path.splitext(os.path.basename(chapter_file))[0] + ".pdf"
    image_file = os.path.join(BASE, "Pictures", "art", image_file_name)
    license_file = image_file + ".license.txt"
    if os.path.exists(image_file):
        image = os.path.join("art", image_file_name)
        add_license(heading, license_file)
    else:
        image = "chapter_head_2.pdf"
    PARTS += (CHAPTER
        .replace("CHAPTER", heading)
        .replace("TEXT", text)
        .replace("IMAGE", image)
    )

translations["PARTS"] = PARTS
translations["PICTURES-TEXT"] = PICTURE_LICENSE_INFORMARTION

# -----------------------------------------
# translate the strings
items = list(translations.items())
items.sort(key=lambda item: -len(item[0]))
for key, value in items:
    if key:
        main_text = main_text.replace(key, value)

with open(MAIN, "w", encoding="UTF-8") as file:
    file.write(main_text)

