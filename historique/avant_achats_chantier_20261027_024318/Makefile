PYTHON ?= python3

.PHONY: help plan guide-historique site-assets site-build site-serve site-hugo-install guide-bois-pdf achats-pdf
help:
	@printf '%s\n' 'make plan              : régénérer les plans SVG et PNG à partir des données' 'make guide-historique  : régénérer l ancien PDF, pandoc et xelatex nécessaires' 'make achats-pdf        : régénérer la liste imprimable, Pandoc et XeLaTeX nécessaires' 'make site-build        : générer le site Hugo dans site/public' 'make site-serve        : servir le site localement sur http://localhost:1313' 'make site-hugo-install : installer un binaire Hugo local si nécessaire'

plan:
	$(PYTHON) plans/generer_plan.py
	rsvg-convert plans/01_cellier_plan_cote.svg -o plans/01_cellier_plan_cote.png
	rsvg-convert plans/02_passage_T1_T2_elevation_cotee.svg -o plans/02_passage_T1_T2_elevation_cotee.png
	rsvg-convert plans/03_ensemble_cellier_cabane.svg -o plans/03_ensemble_cellier_cabane.png
	rsvg-convert --format=pdf site/content/habillage-bois/gabarit-168.svg -o site/content/habillage-bois/gabarit-168.pdf

guide-historique:
	$(MAKE) -C historique/guide_2026_09 pdf

# Pandoc utilise rsvg-convert pour l'illustration SVG ; XeLaTeX produit le PDF.
guide-bois-pdf:
	cd site/content/habillage-bois && pandoc index.md --standalone --pdf-engine=xelatex -V lang=fr-FR -V geometry:margin=2cm -o habillage-bois.pdf

# PDF conservé dans le dépôt pour publication sans dépendance TeX en CI.
achats-pdf:
	cd site/content/achats && pandoc index.md --standalone --pdf-engine=xelatex -M date="24 octobre 2026" -V lang=fr-FR -V geometry:margin=1.5cm -V fontsize=10pt -V papersize=a4 -o achats.pdf

HUGO ?= $(if $(wildcard site/.bin/hugo),site/.bin/hugo,hugo)

site-hugo-install:
	mkdir -p site/.bin
	curl -fsSL https://github.com/gohugoio/hugo/releases/download/v0.111.3/hugo_0.111.3_linux-amd64.deb -o site/.bin/hugo.deb
	dpkg-deb -x site/.bin/hugo.deb site/.bin/package
	cp site/.bin/package/usr/local/bin/hugo site/.bin/hugo
	chmod +x site/.bin/hugo
	rm -rf site/.bin/package site/.bin/hugo.deb

site-assets: plan
	mkdir -p site/static/data site/static/img site/static/plans
	cp donnees/geometrie.json site/static/data/geometrie.json
	cp photos/originales/01_vue_escalier_depuis_piece_de_vie.jpg site/static/img/01_vue_escalier.jpg
	cp photos/originales/02_panorama_cloison_bas.png site/static/img/02_cloison_bas.png
	cp photos/originales/03_panorama_cloison_haut.png site/static/img/03_cloison_haut.png
	cp photos/originales/04_mesure_largeur_rail.png site/static/img/04_mesure_largeur.png
	cp photos/originales/05_mesure_hauteur.png site/static/img/05_mesure_hauteur.png
	cp photos/originales/06_portant_escalier_T1.jpg site/static/img/06_portant_escalier_T1.jpg
	cp plans/01_cellier_plan_cote.svg site/static/plans/01_cellier_plan_cote.svg
	cp plans/02_passage_T1_T2_elevation_cotee.svg site/static/plans/02_passage_T1_T2_elevation_cotee.svg
	cp plans/03_ensemble_cellier_cabane.svg site/static/plans/03_ensemble_cellier_cabane.svg

site-build: site-assets
	$(HUGO) --source site --minify

site-serve: site-assets
	$(HUGO) server --source site --bind 127.0.0.1 --port 1313 --disableFastRender
