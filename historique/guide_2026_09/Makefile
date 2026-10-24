PANDOC ?= pandoc
PDF_ENGINE ?= xelatex
SOURCE := chantier.md
PDF := chantier.pdf

.PHONY: all pdf clean

all: pdf

pdf: $(PDF)

$(PDF): $(SOURCE) $(wildcard images/*.png) $(wildcard images/photos/*) $(wildcard images/schemas/*)
	$(PANDOC) $(SOURCE) \
		--from=markdown+raw_tex \
		--standalone \
		--pdf-engine=$(PDF_ENGINE) \
		--resource-path=. \
		-o $(PDF)

clean:
	rm -f $(PDF)
