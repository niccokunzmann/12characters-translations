# pdf

This folder contains the programs to build a book version of the 12 characters.

## Installation

1. [Install docker](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-16-04)

## Create PDFs

To build all PDFs, run

```
./build.sh
```

To build a specific PDF e.g. for English `en`, run

```
./build.sh en
```

The results will be present in the `books` folder.

This uses the languages in the [play] folder.
If you wonder why there is only English, pull the translations
as describes in the [play] folder.

[play]: ../play
