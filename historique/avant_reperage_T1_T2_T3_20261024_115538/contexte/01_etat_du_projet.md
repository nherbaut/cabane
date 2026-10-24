# État actuel du projet

**Dernière synthèse : 24 octobre 2026.**

## Objectifs

Créer une **cabane de jeu pour enfants** dans un espace sous escalier, reliée au **cellier** par une ouverture découpée dans une cloison en plaque de plâtre. Prévoir un éclairage LED à basse tension, une ventilation adaptée à la chaleur observée, et maintenir des rangements pour les aliments secs et le petit matériel domestique.

## Ce qui est observé

- L'escalier en bois est accessible depuis la pièce de vie par une ouverture existante sous les marches (photo `01_...jpg`).
- Depuis la cabane, l'arrière de la cloison vers le cellier montre les profils métalliques de l'ossature et une seule plaque de plâtre, apparente côté cellier. Aucune couche isolante n'est visible dans les travées photographiées.
- Au sol, un rail métallique continu traverse la future ouverture.
- Plusieurs montants verticaux métalliques sont visibles, présumés de type M48 (à confirmer par mesure).
- L’utilisateur précise que les M48 s’arrêtent sous le haut du mur. La hauteur de leurs sommets et leurs fixations en tête restent à déterminer ; les 174 cm sous plafond ne sont pas leur hauteur.
- L'espace sous l'escalier est **déjà très chaud**, constat rapporté par l'utilisateur.
- L’utilisateur précise **174 cm sous plafond à la séparation T1/T2**, au niveau du deuxième montant, en référence à la photo 05. Cette mesure locale remplace la lecture approximative de 175 cm ; elle ne valide pas le modèle initial de hauteur uniforme à 188 cm.

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
| Nouvelle baie vers la cabane | Dans le mur ouest `x=0`; **travée nord étudiée en priorité**, milieu du 2e M48 à 50 cm du mur nord ; largeur libre 47 cm avant habillage |

Le modèle « espace sous escalier appartenant au cellier » décrit l'encombrement vertical **du côté cellier**. La cabane elle-même est **de l'autre côté du mur ouest** : son plan complet n'a pas été mesuré.

## Situation de l'ouverture

Le scénario initial de 80 cm et l'estimation ultérieure de 53 cm sont historiques. L'utilisateur précise que le milieu du deuxième M48 se trouve à **50 cm du mur nord de la cabane** ; il précise ensuite **47 cm entre les deux montants de T1**, avant habillage.

L'utilisateur met désormais de côté, à ce stade, l'ouverture entre les deuxième et troisième montants : il estime qu'elle laisserait trop peu d'espace pour les rangements. **L'étude se concentre sur la travée côté mur nord, jusqu'au deuxième M48**, sans choix définitif de l'ouverture. Le conflit de la travée 2 avec les rangements n'a pas été chiffré.

Si les murs nord de la cabane et du cellier sont alignés, le milieu du deuxième montant est à `y=130`. Ce raccordement reste une hypothèse. La hauteur sous plafond est confirmée à **174 cm aux deux bords de T1** : côté mur nord et côté séparation T1/T2. La largeur libre de T1 est mesurée à **47 cm avant habillage**. La hauteur finie du passage reste à définir avec son encadrement. Voir `02_choix_de_la_travee.md`.

## Compromis importants

- Largeur libre de la travée nord **47 cm avant habillage** : le bois de finition peut réduire la largeur nette de 2 × 12–15 mm ; vérifier que la largeur finale accepte un adulte pour l'entretien et l'évacuation.
- Pente de l'escalier : hauteur utile différente selon la travée. Ne pas choisir à partir de la hauteur maximale annoncée.
- Le rayonnage B laisse 85 cm au sol depuis le mur ouest (`x=0..85`) dans la partie nord. Il n'empiète pas sur la baie si celle-ci est bien placée au nord.
- Le rayonnage A et le MTA réduisent la circulation dans la partie sud. La solution initiale A peut créer un passage de 61 cm dans l'alignement de l'ouverture sud et 70 cm au niveau du MTA.
- La chaleur dans la cabane ne sera pas dissipée par simple brassage si le cellier et l'air de reprise sont eux-mêmes chauds.

## Nature des livrables passés

Un guide Markdown illustré, des schémas, une image de résultat simulé, un Makefile Pandoc et un PDF de septembre 2026 existent dans `historique/guide_2026_09`. Les variantes d'illustration IA sont dans `historique/infographies_ia`. Elles sont conservées pour continuité, sans valeur dimensionnelle.
