# Plans actuels du cellier et du passage T1–T2

`generer_plan.py` lit `donnees/geometrie.json` et génère deux SVG cotés avec la bibliothèque standard Python :

- `01_cellier_plan_cote.svg` : plan du cellier, de ses rangements, du chauffage et des emprises en hauteur. Le passage **T1–T2 est décidé** et mesure **45 cm libres** ; ses faces ne sont pas dessinées sur le mur ouest parce que leurs coordonnées `y` manquent.
- `02_passage_T1_T2_elevation_cotee.svg` : élévation du passage, avec sa largeur libre de **45 cm**, le sommet de T1 à **169,5 cm** et la sous-face de la pièce liée à l’escalier à **174 cm**. La hauteur de découpe et la traverse restent à définir.

```sh
make plan
```

Les PNG de même nom sont des aperçus régénérés par `make plan` avec `rsvg-convert`. Les deux SVG sont copiés dans le site par `make site-build`. Les versions antérieures sont conservées dans `historique/`.
