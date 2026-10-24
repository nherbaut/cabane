# Étude visuelle Hugo — cabane et cellier

Site statique local. Les photographies et le JSON sont copiés depuis les sources du dossier par le Makefile racine ; les originaux restent inchangés.

```sh
make site-serve
```

Ouvrir <http://localhost:1313/>. Pour construire les fichiers statiques :

```sh
make site-build
```

Hugo est nécessaire. Si la version installée ne fonctionne pas, `make site-hugo-install` télécharge un binaire Linux amd64 dans `site/.bin/`, puis `make site-serve` l'utilise automatiquement. Un autre binaire peut être indiqué avec `make site-serve HUGO=/chemin/vers/hugo`.

La vue principale réunit le cellier et la cabane. Les deux espaces sont tracés à la même échelle depuis `donnees/geometrie.json` : cabane de 190 × 90 cm, cellier de 180 × 115 cm. L’accès à la pièce de vie mesure 70 cm ; son décalage latéral reste à préciser. Le mur nord est **commun**, donc le milieu de T2, à 50 cm de ce mur, est directement à **y=130 cm** dans le repère du cellier. Le passage décidé T1–T2 mesure **45 cm libres** ; les mesures sont exploitables des deux côtés de la cloison. La flèche représente cette liaison sans fixer des bords de découpe.

La page propose une seule vue d’ensemble exportable, `plans/03_ensemble_cellier_cabane.svg`. Le plan du cellier et l’élévation cotée restent disponibles dans `plans/` pour les détails. `make site-build` régénère les plans puis les copie vers `site/static/plans/`. La simulation d’habillage soustrait seulement les panneaux latéraux ; la hauteur finie reste à définir.
