# Plan coté du cellier

`01_cellier_plan_cote.svg` est généré par `generer_plan.py` à partir des emprises du cellier et des largeurs du passage enregistrées dans `donnees/geometrie.json`. Le PNG est un aperçu du SVG. Le script utilise uniquement la bibliothèque standard Python ; `rsvg-convert` sert à régénérer le PNG.

```sh
make plan
rsvg-convert plans/01_cellier_plan_cote.svg -o plans/01_cellier_plan_cote.png
```

La ligne orange sur le mur ouest représente uniquement l’ancienne zone de recherche `y=90..170` de **80 cm**. Le passage prioritaire **T1–T2 mesure 45 cm libres** ; T2–T3 mesure **37,5 cm**. Les faces des montants n’étant pas localisées en coordonnées `y`, ces largeurs sont cotées dans les légendes mais aucun trou définitif n’est dessiné.
