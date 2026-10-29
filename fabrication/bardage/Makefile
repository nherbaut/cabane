.PHONY: all dessin pdf variante-leroy
all: dessin pdf
dessin:
	MPLCONFIGDIR=/tmp/cabane-matplotlib python3 generer_debit.py
	MPLCONFIGDIR=/tmp/cabane-matplotlib python3 generer_schema.py
	MPLCONFIGDIR=/tmp/cabane-matplotlib python3 generer_isometrie.py
variante-leroy:
	MPLCONFIGDIR=/tmp/cabane-matplotlib python3 generer_variante_leroy.py
	pandoc variante_leroy_maison.md --standalone --pdf-engine=xelatex -V geometry:margin=1.5cm -V fontsize=10pt -V papersize=a4 -o variante_leroy_maison.pdf

pdf: variante-leroy
	pandoc decoupes_v1.md --standalone --pdf-engine=xelatex -V geometry:margin=1.8cm -V fontsize=10pt -V papersize=a4 -o decoupes_v1.pdf
	pandoc commande_decoupe.md --standalone --pdf-engine=xelatex -V geometry:margin=1.5cm -V fontsize=10pt -V papersize=a4 -o commande_decoupe.pdf
