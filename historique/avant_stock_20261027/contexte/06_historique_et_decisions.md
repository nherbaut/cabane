# Historique consolidé des échanges

Les éléments ci-dessous reproduisent les intentions successives sans transformer les recommandations de l'assistant en décisions confirmées de l'utilisateur.

## Phase 1 — Cellier et passage sous escalier

L'utilisateur définit le cellier : **115 × 180 × 250 cm**, avec poutre est `(x=90..115, z libre 230)`, zone nord-ouest sous escalier `(x=0..80, y=80..180, hauteur simplifiée 188)`, MTA sud-est `(x=95..115, y=0..50, hauteur 230)`. Il prévoit deux rayonnages : A ouest-sud `(25 × 80 × 240)`, B est-nord `(30 × 90 × 220)`.

L'ancienne porte battante sud de 80 cm (pivot à `x=6`) doit être supprimée ; un des scénarios prévoit une ouverture sud de `x=6` à `x=86`, avec rideaux et zéro débattement au sol. Le vantail auparavant ouvert à 90° mobilisait environ 0,50 m². La première idée de passage ouest était **80 cm** entre `y=90` et `170`.

## Phase 2 — Chaleur, ventilation et éclairage

- L'utilisateur constate une forte chaleur dans l'espace sous escalier.
- La photo de la pièce de vie révèle une **autre entrée déjà existante** sous l'escalier.
- Plusieurs stratégies d'aération sont envisagées ; le principe discuté en dernier est une **extraction haute** depuis la cabane, avec entrée d'air par l'ouverture existante.
- L'utilisateur impose un **rejet de l'air uniquement vers le cellier**, qui doit ensuite communiquer avec le reste du logement. Le débit 20–30 m³/h est une estimation évoquée, pas une obligation.
- Pour l'éclairage, discussion de ruban LED COB **24 V**, profilé aluminium/diffuseur, lumière indirecte et alimentation au cellier ; pilotage à la hauteur des enfants.
- Pour l'appropriation : signalétique de cabane, décoration modifiable, coussins, rangement bas, contrôle de la lumière, rideau souple ne bloquant pas la ventilation.

## Phase 3 — Découverte de la cloison

L'utilisateur photographie depuis la cabane l'arrière d'une cloison : une seule plaque de plâtre côté cellier, montants métalliques visibles, absence d'isolant constatée. Il hésite entre retirer tout le panneau, le scier ou procéder autrement.

Réponse technique antérieure : privilégier une **découpe locale**, conserver le placo restant, encadrer la baie par des renforts, cacher les bords avec du bois, en expliquant les termes de bricolage. La proposition initiale de 80 cm aurait nécessité de modifier certains montants. Une ouverture plus petite **entre montants existants** limite l'intervention.

L'utilisateur transmet des panoramas de l'ossature, une photo du mètre au sol et une photo de hauteur. Il suggère la travée située **entre le montant proche du mur nord et celui du milieu** ; une largeur d'environ 53 cm est évoquée. La hauteur annoncée précédemment était 188 cm ; le cliché de mesure verticale semble montrer environ 175 cm au point photographié.

## Phase 4 — Guide Markdown/ZIP/PDF

Un dossier de chantier a été produit en septembre 2026, comprenant `chantier.md`, `Makefile` Pandoc/XeLaTeX, schémas, photos, couverture simulée et PDF. Sa dernière édition explicite : **cellier étroit 115 cm** et ouverture **entre deux montants existants près du mur nord**. Cet état historique figure sous `historique/guide_2026_09/`.

Le précédent PDF **n'a pas été régénéré** lors de la mise à jour de l'emplacement. Les visualisations antérieures étaient parfois trop larges ou erronées quant à la place exacte de l'ouverture.

## Phase 5 — Nouvelle hésitation travée 1 / travée 2

L'utilisateur présente de nouveau les dimensions et demande un plan coté et une vue 3D simplifiée, puis compare :

- travée 1 « entre le mur et le 2e M48 » ;
- travée 2 « entre les M48 2 et 3 ».

L'assistant a répondu **préférence pour la travée 2**, à condition d'éviter le rayonnage A (`y<80`) et d'obtenir effectivement plus de hauteur sous la pente. La position réelle des montants **n'est pas cotée** ; les repères « travée 1 » et « travée 2 » sont contradictoires entre certains croquis générés.

## Phase 6 — Handoff Codex (23 octobre 2026)

L'utilisateur demande un **ZIP contenant tout le contexte** pour continuer lui-même avec Codex. Ce dossier rassemble les sources réelles, le précédent guide et des documents structurés distinguant les dimensions validées des hypothèses.

## Disposition supérieure retenue pour étude (24 octobre 2026)

L’utilisateur demande de placer les équerres au-dessus de la traverse pour simplifier l’habillage, puis d’en tenir compte dans les hypothèses et les achats. Cette disposition devient la solution privilégiée, sous réserve de vérifier les supports, les charges et l’accès de vissage. Les dimensions des bois et les références des fixations ne sont pas arrêtées. La variante précédente avec équerres dessous et cales est conservée dans `historique/avant_equerres_superieures_20261024_092907/` ; les cales correspondantes sortent des achats prévisionnels.

## Correction des repères et des cotes (24 octobre 2026)

L’utilisateur confirme que T1, T2 et T3 nomment les **montants**, du nord au sud. L’espace T1–T2 mesure 45 cm libres, corrigeant les 47 cm antérieurs ; T2–T3 mesure 37,5 cm. T1 s’arrête à 169,5 cm, la pièce liée à l’escalier est à 174 cm au niveau de T1–T2 et restera intacte, tandis que 187 cm est la sous-face d’une marche au-dessus de T2. T1 s’ouvre vers le sud et T2 vers le nord : les deux C font face au passage. La porte sud du cellier sera supprimée ; la chaleur excessive n’était présente que pendant les canicules et aucun extracteur n’est retenu à l’achat à ce stade. Les versions antérieures des données, textes et dessins sont conservées dans `historique/avant_reperage_T1_T2_T3_20261024_115538/`.

## Passage T1–T2 acté et plans actuels (24 octobre 2026)

L’utilisateur acte le passage entre les montants T1 et T2 et demande de supprimer l’ancienne zone de 80 cm des plans et du site. Les plans courants montrent les emprises connues et une élévation cotée de T1–T2. Les faces exactes des montants dans le repère du cellier restent à relever, donc aucune découpe fictive n’est dessinée sur la vue de dessus. La variante précédente est archivée dans `historique/avant_plans_actuels_passage_acte_20261024_120629/`.

## Mur nord commun confirmé et vue commune (24 octobre 2026)

L’utilisateur confirme que le mur nord est commun aux deux espaces et que les montants longent leur cloison commune. Les mesures de la cabane sont directement exploitables dans le cellier ; le milieu de T2 est à y=130 cm. La demande précédente de refaire un relevé côté cellier était superflue pour la vue d’ensemble. La page principale réunit désormais cabane et cellier, avec une emprise de cabane explicitement schématique.

## Dimensions de la cabane (24 octobre 2026)

L’utilisateur mesure 190 cm du mur nord commun jusqu’à l’ouverture vers la pièce de vie, 90 cm de largeur et 70 cm pour cette ouverture. L’enveloppe rectangulaire est tracée à la même échelle que le cellier, soit x=-90..0 et y=-10..180 dans le repère partagé, épaisseur de cloison non représentée. Le placement latéral des 70 cm sur la largeur de 90 cm reste à préciser ; aucun centrage n’est supposé.

## Correction des 70 cm de l’accès triangulaire (24 octobre 2026)

L’utilisateur précise que les 70 cm correspondent à la distance dans le prolongement du mur ouest du cellier, délimitant l’espace triangulaire entre le sol, l’escalier et ce mur, derrière la plante sur la photo 01. L’interprétation précédente d’une ouverture transversale de 70 cm, à centrer sur les 90 cm, est abandonnée. Il reste à préciser si les 70 cm prolongent la cote nord–accès de 190 cm ou y sont compris. La longueur totale n’est pas déduite sans cette précision.

## Longueur totale confirmée et objectif de hauteur (24 octobre 2026)

L’utilisateur confirme que les 70 cm s’ajoutent aux 190 cm : **260 cm de longueur totale**, sur 90 cm de largeur. L’accès triangulaire existant se situe le long du prolongement du mur ouest du cellier, de y=-10 à y=-80. Il propose un passage fini de **168 cm** entre T1 et T2. Cette hauteur devient un objectif à vérifier : réserve totale de 6 cm sous la pièce de l’escalier, panneau inclus ; avec 15 mm, le dessous de la traverse serait à 169,5 cm, au sommet du métal de T1. L’assemblage au-dessus reste à dimensionner et la hauteur de coupe n’est pas arrêtée.

## Recherche de liaison compacte et gabarit (24 octobre 2026)

À la demande de l’utilisateur, recherche de références et préparation d’un essai concret. La fiche fabricant Hettich 9240442 décrit une équerre de chaise 16 × 20 × 20 × 2 mm, sans fixations fournies ni charge admissible pour notre cloison. Avec un panneau de 12 mm et une traverse de 20 mm de hauteur × 40 mm de profondeur, l’encombrement nominal est de 52 mm pour 60 mm disponibles. Un gabarit A4 à taille réelle et une liste de pièces d’essai sont ajoutés. Le dimensionnement mécanique, les vis et l’accessibilité de l’outil ne sont pas validés ; les 168 cm restent une cible avant essai sur place et vérification du support.

## Liste d’achats prévisionnelle et magasin (24 octobre 2026)

L’utilisateur demande une liste globale même s’il n’achète pas tout demain, puis précise qu’il va chez Leroy Merlin. Une page et un PDF regroupent les formats bruts : deux supports de 2 m, une traverse brute de 60 cm, trois bandes de panneau de 12 mm, deux équerres envisagées, finitions et consommables. La section des supports et les fixations restent à déterminer ; un échantillon d’équerre suffit pour commencer. Le tasseau Leroy Merlin 70841883 correspond au format 20 × 40 mm de l’essai, sans validation mécanique ni confirmation de stock local. Les originaux modifiés sont archivés dans `historique/avant_liste_achats_20261024_185014/`.

## Avancement et achats actualisés (27 octobre 2026)

TA1 et TA2, en pin de 32 mm est–ouest × 19 mm nord–sud, sont insérés et vissés dans T1 et T2. Les vis du plâtre côté T1 ont été légèrement dévissées puis resserrées pour permettre l’insertion. Les longueurs de présentation sont conservées. Les équerres achetées sont les Hettich 9209109, et non 9240442 ; quatre sont discutées, une au-dessus et une au-dessous à chaque extrémité, sans validation de résistance. L’utilisateur confirme que leurs branches horizontales dépassent des M48.

L’utilisateur accepte une hauteur réduite. Une traverse en sapin de 34 × 44 mm (44 verticalement) est proposée, non encore déclarée achetée. L’habillage proposé devient un contreplaqué ordinaire de 15 mm à la découpe. Les cotes de coupe, les vis, le maintien du plâtre et l’habillage sous les équerres restent à arrêter. Le gabarit compact 168 cm décrit le premier essai et ne doit pas dicter les achats actuels.

La scie à métaux DEXTER 95595161 est disponible ; la scie japonaise 95595174 et la scie à guichet EDMA 68141311 sont proposées, sans confirmation d’achat. Deux serre-joints et une protection de table sont ajoutés à la liste. Le retrait du rail seulement dans le passage est choisi ; il repose sur du carrelage sur dalle béton. Ses attaches et le maintien des pieds ne sont pas identifiés : la cisaille est conditionnelle et aucune coupe n’est prescrite.
