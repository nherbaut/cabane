# Plans actuels du projet

La vue principale est **`03_ensemble_cellier_cabane.svg`** : cellier et cabane sur un même schéma, avec leur mur nord commun, le milieu de T2 à 50 cm du mur (`y=130 cm`) et la liaison T1–T2 de 45 cm libres. Le cellier est à l’échelle ; les limites de la cabane sont schématiques, non mesurées.

Les détails restent disponibles :

- `01_cellier_plan_cote.svg` : emprises cotées du cellier et repère confirmé de T2.
- `02_passage_T1_T2_elevation_cotee.svg` : élévation du passage, 45 cm libres, sommet de T1 à 169,5 cm et pièce liée à l’escalier à 174 cm. Hauteur de traverse à définir.

```sh
make plan
```

Le script lit `donnees/geometrie.json`, génère les SVG avec la bibliothèque standard Python, puis le Makefile crée les aperçus PNG avec `rsvg-convert`. Le site présente la vue d’ensemble commune ; les versions antérieures restent dans `historique/`. La flèche de liaison ne constitue pas un tracé de découpe.
