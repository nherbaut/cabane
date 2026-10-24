# Plans actuels du projet

La vue principale est **`03_ensemble_cellier_cabane.svg`** : cellier et cabane sur un même schéma, avec leur mur nord commun, le milieu de T2 à 50 cm du mur (`y=130 cm`) et la liaison T1–T2 de 45 cm libres. Les deux espaces sont à la même échelle : cabane **260 × 90 cm**, cellier **180 × 115 cm**. Les 70 cm de l’accès triangulaire s’ajoutent aux 190 cm. L’accès existant est représenté sur le prolongement de la cloison, x=0 et y=-80..-10.

Les détails restent disponibles :

- `01_cellier_plan_cote.svg` : emprises cotées du cellier et repère confirmé de T2.
- `02_passage_T1_T2_elevation_cotee.svg` : élévation du passage, 45 cm libres, sommet de T1 à 169,5 cm et pièce liée à l’escalier à 174 cm. Objectif de 168 cm finis, montage à vérifier dans les 6 cm sous la pièce à 174 cm.

```sh
make plan
```

Le script lit `donnees/geometrie.json`, génère les SVG avec la bibliothèque standard Python, puis le Makefile crée les aperçus PNG avec `rsvg-convert`. Le site présente la vue d’ensemble commune ; les versions antérieures restent dans `historique/`. La flèche de liaison ne constitue pas un tracé de découpe.
