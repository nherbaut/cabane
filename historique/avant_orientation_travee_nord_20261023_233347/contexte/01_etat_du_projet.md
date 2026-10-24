# État actuel du projet

**Dernière synthèse : 23 octobre 2026.**

## Objectifs

Créer une **cabane de jeu pour enfants** dans un espace sous escalier, reliée au **cellier** par une ouverture découpée dans une cloison en plaque de plâtre. Prévoir un éclairage LED à basse tension, une ventilation adaptée à la chaleur observée, et maintenir des rangements pour les aliments secs et le petit matériel domestique.

## Ce qui est observé

- L'escalier en bois est accessible depuis la pièce de vie par une ouverture existante sous les marches (photo `01_...jpg`).
- Depuis la cabane, l'arrière de la cloison vers le cellier montre les profils métalliques de l'ossature et une seule plaque de plâtre, apparente côté cellier. Aucune couche isolante n'est visible dans les travées photographiées.
- Au sol, un rail métallique continu traverse la future ouverture.
- Plusieurs montants verticaux métalliques sont visibles, présumés de type M48 (à confirmer par mesure).
- L'espace sous l'escalier est **déjà très chaud**, constat rapporté par l'utilisateur.
- La photo de mesure verticale (`photos/originales/05_...png`) montre un repère voisin de 175 cm au contact de la surface représentée. Le modèle initial employait 188 cm de hauteur simplifiée : mesures à réconcilier.

## Configuration du cellier selon l'utilisateur

| Élément | Emplacement `(x, y, z)` et dimensions en cm |
|---|---|
| Cellier | `x=0..115`, `y=0..180`, hauteur générale `z=0..250` |
| Poutre le long du mur est | `x=90..115`, `y=0..180`, dessous à `z=230` |
| Volume sous escalier projeté dans le cellier | `x=0..80`, `y=80..180`, hauteur libre simplifiée `188` |
| Module de chauffage urbain (MTA) | `x=95..115`, `y=0..50`, hauteur `230` |
| Rayonnage A (réserves) | `x=0..25`, `y=0..80`, hauteur `240` |
| Rayonnage B (matériel) | `x=85..115`, `y=90..180`, hauteur `220` |
| Ancienne ouverture au sud | Ancien vantail de 80 cm supprimé ; une version précédente prévoyait l'ouverture sud `x=6..86` sans porte, avec rideaux |
| Nouvelle baie vers la cabane | Dans le mur ouest `x=0`; **travée à sélectionner**, largeur brute annoncée ≈53 cm |

Le modèle « espace sous escalier appartenant au cellier » décrit l'encombrement vertical **du côté cellier**. La cabane elle-même est **de l'autre côté du mur ouest** : son plan complet n'a pas été mesuré.

## Situation de l'ouverture

Le projet est passé d'une ouverture initiale de 80 cm (`x=0, y=90..170`) à un passage plus petit entre deux montants métalliques existants (environ 53 cm avant finition). Plus récemment, l'utilisateur hésite entre **la travée 1**, décrite comme entre un mur et le deuxième M48, et **la travée 2**, entre les deuxième et troisième M48. La dernière réponse de l'assistant privilégie la **travée 2**, à condition qu'elle se trouve dans la zone nord du cellier au-delà de `y=80` et que le passage y soit plus haut.

Cette recommandation ne prouve ni la numérotation des montants, ni leurs coordonnées. Les schémas IA ont employé des numérotations parfois contradictoires. Voir `02_choix_de_la_travee.md`.

## Compromis importants

- Entrée de cabane de 53 cm **brut** : le bois de finition peut réduire la largeur nette de 2 × 12–15 mm ; vérifier que la largeur finale accepte un adulte pour l'entretien et l'évacuation.
- Pente de l'escalier : hauteur utile différente selon la travée. Ne pas choisir à partir de la hauteur maximale annoncée.
- Le rayonnage B laisse 85 cm au sol depuis le mur ouest (`x=0..85`) dans la partie nord. Il n'empiète pas sur la baie si celle-ci est bien placée au nord.
- Le rayonnage A et le MTA réduisent la circulation dans la partie sud. La solution initiale A peut créer un passage de 61 cm dans l'alignement de l'ouverture sud et 70 cm au niveau du MTA.
- La chaleur dans la cabane ne sera pas dissipée par simple brassage si le cellier et l'air de reprise sont eux-mêmes chauds.

## Nature des livrables passés

Un guide Markdown illustré, des schémas, une image de résultat simulé, un Makefile Pandoc et un PDF de septembre 2026 existent dans `historique/guide_2026_09`. Les variantes d'illustration IA sont dans `historique/infographies_ia`. Elles sont conservées pour continuité, sans valeur dimensionnelle.
