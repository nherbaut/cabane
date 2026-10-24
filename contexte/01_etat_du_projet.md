# État actuel du projet

**Dernière synthèse : 24 octobre 2026.**

## Objectif et faits

Créer un passage entre la cabane sous l’escalier et le cellier, en préservant les rangements et les éléments liés à l’escalier. L’entrée actuelle de la cabane depuis la pièce de vie reste accessible. La porte sud du cellier sera supprimée : le cellier communiquera alors librement avec le reste du logement. Le module de chauffage reste accessible par sa face ouest.

La cabane a été **très chaude pendant les canicules**, mais son confort est redevenu acceptable depuis. Aucun extracteur n’est retenu à l’achat à ce stade ; l’efficacité de la circulation naturelle par les deux accès et les températures comparées seront observées lors d’une nouvelle période chaude.

## Géométrie du cellier

Le repère est fixé à l’angle intérieur sud-ouest du cellier au sol : `x` vers l’est, `y` vers le nord, `z` vers le haut, en **cm**. Le cellier mesure **115 × 180 × 250 cm**. Les emprises du chauffage, des rayonnages A/B, de la poutre et de l’escalier sont conservées dans [`donnees/geometrie.json`](../donnees/geometrie.json).

Le côté cabane de la cloison est visible sur les photos originales. Une plaque de plâtre est présente côté cellier ; aucun isolant n’a été observé dans les parties photographiées. Le rail métallique au sol traverse la future ouverture.

## Repères des trois M48

**T1, T2 et T3 sont les montants**, numérotés en s’éloignant du mur nord. Le passage acté est l’espace **T1–T2**, large de **45 cm libres avant habillage**. La précédente valeur de 47 cm est corrigée. L’espace **T2–T3** mesure **37,5 cm libres** et ne sera pas ouvert, afin de préserver les rangements. Le milieu de T2 est à **50 cm du mur nord de la cabane** ; le mur nord étant commun aux deux espaces, ce milieu est directement à **`y=130`** dans le repère du cellier. Les mesures de la cabane sont donc exploitables côté cellier.

T1 s’ouvre vers le sud et T2 vers le nord : leurs parties creuses font face au passage. T1 s’arrête à **169,5 cm** et serait vissé aux cloisons nord et cellier, sans rail supérieur. T2 atteint la sous-face de l’escalier et rejoint un rail fixé sous celui-ci selon l’utilisateur.

La pièce liée à l’escalier qui limite le haut de T1–T2 a sa sous-face à **174 cm** ; une marche au-dessus de T2 est à **187 cm**. La pièce à 174 cm restera intacte. L’utilisateur propose **168 cm finis**, du sol au dessous de l’habillage : objectif à vérifier, non cote de découpe validée. Les 6 cm disponibles doivent contenir planche supérieure, traverse et liaison ; avec 15 mm de panneau, le dessous de la traverse serait à 169,5 cm, au sommet de T1, ce qui exige de vérifier le tasseau prolongé et l’équerre.

**Cabane : 260 × 90 cm au total**, soit 190 cm depuis le mur nord jusqu’au début de l’accès puis **70 cm supplémentaires**, confirmé par l’utilisateur. L’accès triangulaire se situe sur le prolongement de la cloison ouest du cellier, et non sur la largeur de 90 cm. L’enveloppe du plan est x=-90..0, y=-80..180 ; l’accès latéral correspond à x=0, y=-80..-10, épaisseur de cloison non représentée. Sa hauteur reste inconnue.

## Hypothèses, mesures manquantes et propositions

Deux panneaux latéraux de 12 mm laisseraient théoriquement **42,6 cm** de passage ; à 15 mm chacun, **42 cm**. Ce calcul suppose qu’aucun support ni accessoire ne déborde dans l’ouverture. La largeur doit être essayée pour l’accès d’un adulte.

Les équerres au-dessus de la traverse sont l’option privilégiée pour dégager son dessous, **sous réserve** de disposer du bois, de la place et de fixations suffisantes, notamment côté T1. Les ailes nominales de 35 mm des M48/35 ne garantissent pas la place intérieure pour un tasseau : un essai avec une chute dans chaque profil précédera les achats définitifs. L’épaisseur de cloison et la hauteur utilisable de la traverse restent à mesurer.

**Points de sécurité :** ne pas couper ni percer la pièce liée à l’escalier ou un support potentiellement porteur sans avoir vérifié sa fonction. Vérifier la tenue du bord de plâtre conservé et la fonction de la cloison avant découpe. Les dégagements du chauffage nécessitent sa notice ; les options de ventilation et d’éclairage ne sont pas des validations de conformité.

## Candidat compact pour essai à blanc

Un essai dimensionnel est documenté : panneau de 12 mm, traverse de 20 mm de hauteur × 40 mm de profondeur et équerre Hettich 9240442 à branches de 20 mm. Niveaux : 168 cm finis, dessous de traverse 169,2 cm, dessus 171,2 cm, haut nominal de l’équerre 173,2 cm, marge 8 mm sous la pièce à 174 cm. Le gabarit A4 SVG/PDF est généré depuis les données. La capacité de la petite équerre, le choix des vis, les distances aux bords, le maintien dans les M48 et l’accès de vissage dans les 28 mm au-dessus de la traverse restent à vérifier. Ce candidat n’est pas un plan de découpe validé.
