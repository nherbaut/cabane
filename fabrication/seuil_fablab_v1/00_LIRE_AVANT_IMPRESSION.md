---
title: "Seuil cabane / cellier — échantillon v1"
date: "28 octobre 2026"
lang: fr-FR
---

**À imprimer : `01_ESSAI_seuil_SUR_TRANCHE_mm.stl`, une seule pièce,
à l’échelle 100 %. Il s’agit d’un échantillon d’ajustement, pas du seuil final.**

## À l’attention du fablab

La pièce en position de pose mesure **120 × 40 × 8 mm** : 120 mm entre
cabane et cellier, 40 mm dans la longueur du passage, hauteur maximale 8 mm.
Le fichier STL[^stl] est déjà tourné pour une impression **sur sa tranche**[^tranche] :
sa boîte extérieure dans le logiciel doit mesurer **120 × 8 × 40 mm**.
Les nombres du fichier sont en **millimètres**, même si les données du projet
et le schéma coté sont en centimètres. Ne pas importer le STL en centimètres.

Le plateau, l’imprimante et le matériau ne sont pas encore connus.
Le **PETG**[^petg] est proposé pour étudier la future pièce ; un essai en PLA
peut servir au contrôle des dimensions uniquement. Le fablab choisit son profil
d’impression, les supports[^supports] éventuels dans le logement de vis et
l’adhérence au plateau. L’orientation sur la tranche évite un grand pont
horizontal de 72 mm au-dessus du logement du rail, mais doit être examinée
dans l’aperçu du logiciel de préparation. Le pied étroit peut demander une
bordure d’adhérence[^bordure].

**Aucun G-code[^gcode] n’est fourni**, car il dépend de l’imprimante.
Les réglages d’impression et la résistance à une charge de pied ne sont pas validés.

## Faits mesurés

| Donnée | Valeur confirmée |
|:--|:--|
| Sols cabane et cellier | Même carrelage, même niveau |
| Rail[^rail] posé sur le carrelage | 70 mm de large extérieurement |
| Sommet de la tête de vis au-dessus du carrelage | 3 mm, comparé à une cale |
| Diamètre extérieur de la tête | Entre 13 et 15 mm ; pièce dessous plus petite |
| Distance de la vis au bord de T1 donnant dans le passage | 53 mm |
| Distance annoncée côté cabane / côté cellier | 33 / 37 mm, voir hypothèse d’unité |
| Fixation à conserver | Vis et fond du rail continus jusqu’à T1 |

T1 et T2 sont les montants[^montant] métalliques bordant le passage.
Le passage brut mesure 450 mm en bas ; cela **ne fixe pas encore la longueur
du seuil fini**, qui dépend de l’habillage et de ses jeux.

## Propositions intégrées au modèle

| Élément | Cote du modèle, à essayer |
|:--|:--|
| Enveloppe de la pièce | 120 × 40 × 8 mm |
| Deux pentes | 24 mm de largeur chacune ; bord extérieur à 0,8 mm |
| Dégagement sous le rail | 72 mm de large ; plafond à 1 mm du carrelage |
| Logement local de la vis | Diamètre 18 mm ; plafond à 4 mm du carrelage |
| Matière au-dessus du logement de vis | 4 mm |
| Centre du logement depuis le bord extérieur côté cabane | 58 mm |
| Centre du logement depuis le bord extérieur côté cellier | 62 mm |
| Centre du logement dans la longueur de l’échantillon | 20 mm de chaque bout |

Les 4 mm sont la hauteur du plafond du logement **depuis le carrelage**,
pas une profondeur à ajouter au dégagement de 1 mm sous le rail.
Le cylindre est approché par 96 facettes. Le volume géométrique de plastique
est d’environ 27,85 cm³ ; ce n’est pas une estimation du temps ou du coût d’impression.

## Hypothèses et mesures manquantes

- **Le dégagement de 1 mm pour le fond du rail est une hypothèse.**
  L’épaisseur réelle de la tôle et les éventuels résidus de coupe restent à relever.
- L’utilisateur a écrit « 3,7 mm / 3,3 mm » pour la position latérale.
  Le modèle interprète **3,7 cm / 3,3 cm**, cohérents avec les 7 cm du rail.
  Vérifier cette position à la présentation.
- Les appuis extérieurs supposent un carrelage localement plan.
  Aucune épaisseur de colle n’est incluse ; la fixation finale reste à choisir.
- La hauteur de 8 mm et la largeur de 120 mm sont des **propositions d’essai**,
  pas des mesures de chantier ni des dimensions finales actées.
- La résistance à une charge de pied, les appuis définitifs et l’assemblage
  des futurs morceaux du seuil complet restent à concevoir et à vérifier.

## Présentation sur place et sécurité

1. Retirer les supports d’impression, éliminer les fils et adoucir les angles
   qui piquent. Vérifier les dimensions au réglet.
2. **Ne pas poser la pièce sur les ailes[^aile] encore relevées du rail.**
   Tant qu’elles sont présentes, l’essai réel n’est pas possible. Ne pas forcer,
   tordre le rail ou retirer la vis pour faire rentrer l’échantillon.
   Ce dossier ne définit pas la méthode de découpe du métal.
3. Une fois l’emplacement préparé, propre et les arêtes métalliques traitées,
   présenter la pièce sans colle. Le côté où le logement est à **58 mm** du bord
   extérieur va vers la **cabane** ; celui à 62 mm va vers le cellier.
4. Centrer le logement sur la vis. L’échantillon de 40 mm **ne commence pas
   au pied de T1** : centré sur la vis à 53 mm, il occupe la zone de 33 à 73 mm
   depuis le bord de T1 vers T2.
5. Vérifier que les appuis se posent sans bascule, que la pièce n’appuie pas
   sur la tête de vis et que le rail ne force pas dans son logement. Noter
   tout écart et corriger le modèle avant une nouvelle impression.

**Ne pas marcher sur l’échantillon, ne pas le coller et ne pas le laisser comme
un seuil provisoire accessible aux enfants.** Son examen dimensionnel ne valide
pas une capacité portante. Les bords fins et la surface finale devront aussi
être revus pour la pièce de circulation. Conserver intactes les fixations
de T1/T2 et la structure de l’escalier.

## Contenu et régénération

- `01_ESSAI_seuil_SUR_TRANCHE_mm.stl` : pièce d’essai, prête à importer.
- `schema_cote.pdf` et `apercu.png` : repères et vue de la pièce.
- `parametres.json` : faits, hypothèses et propositions, en **cm**.
- `generer.py` : générateur Python du STL, du schéma et des vérifications.
- `modele_modifiable.scad` : autre source modifiable dans OpenSCAD[^scad],
  générée à partir des mêmes paramètres. Elle n’a pas été compilée ici ;
  le STL livré est produit et vérifié par Python.
- `verification.json` : contrôle de fermeture, orientation et dimensions du
  maillage[^maillage]. Ce contrôle informatique n’est pas un essai de résistance.
- `Makefile` : `make all` régénère les fichiers et ce PDF via Pandoc/XeLaTeX.

Le repère général du projet garde son origine à l’angle intérieur sud-ouest du
cellier, x vers l’est, y vers le nord, z vers le haut, en cm. Pour cette pièce,
le repère de fabrication est **translaté** à son coin sud-ouest au niveau du sol,
avec les mêmes directions ; sa translation globale n’est pas déduite de photos.
La rotation du STL est seulement une orientation d’impression.

Source matériau : [guide PETG Prusa](https://help.prusa3d.com/article/petg_2059).
Les qualités générales du matériau ne constituent pas une validation de ce seuil.

[^stl]: **STL** : format décrivant la surface d’une pièce 3D, lisible par les logiciels d’impression.
[^tranche]: **Sur la tranche** : posé verticalement sur la petite face de 120 × 8 mm, et non à plat comme au sol.
[^petg]: **PETG** : plastique couramment employé pour des impressions techniques. Le PLA est un autre plastique courant.
[^supports]: **Supports d’impression** : structures temporaires qui soutiennent les parties en surplomb, retirées ensuite.
[^bordure]: **Bordure d’adhérence**, ou *brim* : quelques lignes de plastique autour du pied de la pièce pour la maintenir sur le plateau.
[^gcode]: **G-code** : instructions de déplacement et de chauffe spécifiques à une imprimante.
[^rail]: **Rail** : profil métallique en U, ici posé et vissé au sol.
[^montant]: **Montant** : profil métallique vertical de la cloison.
[^aile]: **Aile du rail** : un des deux bords relevés de son profil en U.
[^scad]: **OpenSCAD** : logiciel de dessin 3D à partir de paramètres et de commandes textuelles.
[^maillage]: **Maillage** : ensemble de triangles représentant la surface de la pièce.
