PYTHON ?= python3
.PHONY: all modele pdf
all: modele pdf
modele:
	MPLCONFIGDIR=/tmp/cabane-matplotlib $(PYTHON) generer.py
pdf:
	pandoc 00_LIRE_AVANT_IMPRESSION.md --standalone --pdf-engine=xelatex -V geometry:margin=1.8cm -V fontsize=10pt -V papersize=a4 -o 00_LIRE_AVANT_IMPRESSION.pdf
