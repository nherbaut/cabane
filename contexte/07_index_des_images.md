# Index des images et statut de fiabilité

## Photographies fournies par l'utilisateur (source primaire)

| Fichier | Ce qui est visible | Utilisation |
|---|---|---|
| `photos/originales/01_vue_escalier_depuis_piece_de_vie.jpg` | Escalier en bois, accès déjà existant sous la partie basse depuis la pièce de vie, entrée du cellier voisine | Comprendre les accès et la circulation d'air |
| `photos/originales/02_panorama_cloison_bas.png` | Mur côté cabane, montants métalliques, rail au sol, une plaque côté cellier | Voir les emplacements relatifs ; photo panoramique déformée |
| `photos/originales/03_panorama_cloison_haut.png` | Partie haute sous pente, montants et rail sous escalier | Repérer contraintes de hauteur, sans mesurer directement sur pixels |
| `photos/originales/04_mesure_largeur_rail.png` | Mètre ruban au pied d'un montant, rail au sol | Indice de position ; mesurer physiquement la largeur entre faces internes |
| `photos/originales/05_mesure_hauteur.png` | Mètre vertical dans l’espace entre les montants T1 et T2 | **174 cm** jusqu’à la pièce liée à l’escalier ; pas une hauteur finie de passage |
| `photos/originales/06_portant_escalier_T1.jpg` | Pièce liée à l’escalier et son voisinage, cliché transmis le 24 octobre 2026 | Comprendre la limite haute du passage T1–T2 ; la fonction mécanique exacte ne se déduit pas de la photo |

Ces **six fichiers sont des copies non modifiées** des photos présentes dans le fil.

## Images annotées de la documentation antérieure

- `photos/annotees/01_ouverture_precedemment_retenue.png` : ancienne annotation de la travée envisagée ; **ne vaut pas identification actuelle des travées 1/2**.
- `photos/annotees/02_plan_115x180_precedent.png` : plan de l'ancienne hypothèse ; la nouvelle ouverture dessinée peut être incohérente avec le passage final de 53 cm.
- `historique/guide_2026_09/images/schemas/*` : trois anciens croquis de chantier et un plan 115 × 180.

## Images générées par IA (source non dimensionnelle)

- `illustrations_ia_non_metriques/couverture_precedente.png` : simulation esthétique du passage bois depuis la cabane ; dimensions et mobilier **fictifs**.
- `historique/infographies_ia/01_infographie_cellier_3d_hypothese.png` : vue 3D et plan générés, comportant des erreurs possibles sur ouverture/hauteur/échelle.
- `historique/infographies_ia/02_comparaison_travees_1_2.png` : comparaison graphique *non fiable* pour numéroter les montants ; examiner seulement comme idée de présentation.
- `historique/infographies_ia/03_...png` à `08_...png` : variations conceptuelles précédentes ; certaines visualisent un cellier trop large.

Toutes ces images sont conservées pour référence historique. **Ne jamais extraire de cotes de ces illustrations.**

## Plans actuels construits à partir des cotes

- [`plans/01_cellier_plan_cote.svg`](../plans/01_cellier_plan_cote.svg) : plan du cellier et de ses emprises connues. Le passage T1–T2 est acté, large de 45 cm libres ; le milieu de T2 est repéré à y=130 cm, le mur nord commun étant confirmé.
- [`plans/02_passage_T1_T2_elevation_cotee.svg`](../plans/02_passage_T1_T2_elevation_cotee.svg) : élévation du passage depuis la cabane, avec 45 cm libres, T1 à 169,5 cm et la limite locale de la pièce liée à l’escalier à 174 cm. La hauteur de coupe et les fixations restent à définir.

Les deux SVG sont générés par `plans/generer_plan.py` depuis les cotes de `donnees/geometrie.json`, avec des aperçus PNG et des copies accessibles depuis le site Hugo. Les anciennes versions sont conservées dans `historique/`.

La vue principale actuelle est `plans/03_ensemble_cellier_cabane.svg` : un seul schéma réunit les deux espaces. Cabane de 190 × 90 cm et cellier sont à la même échelle ; les 70 cm sont la base de l’accès triangulaire dans le prolongement du mur ouest du cellier, et non une ouverture sur la largeur de 90 cm.
