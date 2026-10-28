.PHONY: all dessin pdf
all: dessin pdf
dessin:
	MPLCONFIGDIR=/tmp/cabane-matplotlib python3 generer_debit.py
pdf:
	pandoc decoupes_v1.md --standalone --pdf-engine=xelatex -V geometry:margin=1.8cm -V fontsize=10pt -V papersize=a4 -o decoupes_v1.pdf
