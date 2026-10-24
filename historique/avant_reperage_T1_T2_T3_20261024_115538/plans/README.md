# Plan coté du cellier

- `01_cellier_plan_cote.svg` est un **plan vectoriel** dimensionné à partir des emprises utilisateur.
- `01_cellier_plan_cote.png` est son aperçu en image ; mêmes données.
- `generer_plan.py` est le script Python qui génère le SVG ; dépendance `svgwrite`.

Reconstruction sur Linux :

```sh
python3 -m pip install svgwrite
make plan
```

La ligne orange sur le mur ouest indique uniquement l'**ancienne zone de recherche** `y=90..170` de 80 cm. Elle n'est **pas** la baie définitive de 53 cm. Les deux travées candidates n'étant pas mesurées en coordonnées `y`, elles ne sont pas dessinées.
