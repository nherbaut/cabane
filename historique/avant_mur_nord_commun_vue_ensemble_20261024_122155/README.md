# Cabane sous escalier et cellier — dossier de transfert vers Codex

**État du dossier : 24 octobre 2026.** Langue de travail : français. Unités : centimètres.

Ce dossier rassemble le contexte d'un projet domestique : création d'un passage entre une future cabane d'enfants sous un escalier et un cellier étroit, aménagement des rangements du cellier, ventilation de l'espace chaud et éclairage LED.

## Démarrage conseillé dans Codex

1. Ouvrir ce dossier comme répertoire de travail, puis lire [`AGENTS.md`](AGENTS.md).
2. Lire [`contexte/01_etat_du_projet.md`](contexte/01_etat_du_projet.md) : état des décisions, faits observés et hypothèses.
3. Consulter [`donnees/geometrie.json`](donnees/geometrie.json) pour les cotes **connues**, la différence entre *données* et *hypothèses*, et les incohérences à lever.
4. Examiner les **six photographies originales** dans [`photos/originales/`](photos/originales/). Elles priment sur les visualisations générées pour la reconnaissance de l'existant.
5. Utiliser le [plan actuel du cellier](plans/01_cellier_plan_cote.svg) et l’[élévation cotée du passage T1–T2](plans/02_passage_T1_T2_elevation_cotee.svg). Le passage est choisi ; seules les coordonnées de ses faces dans le plan du cellier restent à relever.
6. Consulter le guide antérieur dans [`historique/guide_2026_09/chantier.md`](historique/guide_2026_09/chantier.md) ; son PDF est un état **historique**, potentiellement obsolète.

## Arborescence

```text
.
├── AGENTS.md                         Instructions à Codex
├── README.md                         Ce fichier
├── contexte/
│   ├── 01_etat_du_projet.md          Synthèse actualisée
│   ├── 02_choix_de_la_travee.md      Passage T1–T2 acté et cotes confirmées
│   ├── 03_travaux_et_securite.md     Principes constructifs et vérifications
│   ├── 04_ventilation_eclairage.md  Options étudiées, non dimensionnées définitivement
│   ├── 05_amenagement_cellier.md    Deux rayonnages et dégagements
│   ├── 06_historique_et_decisions.md Historique des échanges et des évolutions
│   ├── 07_index_des_images.md       Provenance et fiabilité des visuels
│   └── 08_travaux_pour_codex.md      Pistes de tâches et critères d'acceptation
├── donnees/
│   └── geometrie.json               Données numériques et incertitudes
├── plans/
│   ├── 01_cellier_plan_cote.svg      Plan actuel du cellier
│   └── 02_passage_T1_T2_elevation_cotee.svg  Élévation cotée du passage
├── photos/
│   ├── originales/                   6 photographies de l'utilisateur (non retouchées)
│   └── annotees/                    Annotations de l'ancien guide
├── illustrations_ia_non_metriques/ Image de couverture indicative
└── historique/
    ├── guide_2026_09/               Markdown + Makefile + images + ancien PDF
    └── infographies_ia/            Variantes graphiques NON fiables pour mesurer
```

## Points à ne pas confondre

- **Cellier** : rectangle intérieur mesuré **115 cm (ouest-est) × 180 cm (sud-nord)**. L'escalier réduit la hauteur dans sa zone nord-ouest.
- **Cabane** : espace de jeu de l'autre côté de la cloison ouest du cellier, sous l'escalier ; sa géométrie en plan n'a **pas été relevée séparément**.
- **Repères actuels** : T1, T2 et T3 sont les montants M48 du nord vers le sud ; le passage décidé est entre T1 et T2, large de **45 cm libres** avant habillage. L’espace T2–T3 mesure **37,5 cm** et restera sans ouverture pour préserver les rangements. Les anciennes cotes 53 puis 47 cm pour le passage nord sont dépassées.
- **Position** : milieu de T2 à 50 cm du mur nord de la cabane ; raccordement exact au repère du cellier encore conditionnel. Le plan actuel ne place pas les faces du passage tant que leurs coordonnées `y` ne sont pas relevées.
- **Hauteurs distinctes** : T1 s’arrête à **169,5 cm** ; sous-face de la pièce liée à l’escalier à **174 cm** au niveau du passage T1–T2 ; sous-face d’une marche à **187 cm** au-dessus de T2. La pièce liée à l’escalier restera intacte ; la hauteur finie du passage reste à définir.
- **Orientations** : T1 s’ouvre vers le sud et T2 vers le nord ; les deux C sont ouverts vers le passage. La porte sud du cellier sera supprimée. La cabane était chaude pendant les canicules mais est redevenue confortable : pas d’extracteur à acheter pour l’instant.
- **Illustrations IA** : plusieurs vues représentent un cellier trop grand ou des géométries incohérentes. Utiliser les cotes écrites et les photos réelles pour tout choix d'implantation.

## Guides et PDF déjà produits

Le sous-dossier `historique/guide_2026_09/` est une copie complète du précédent guide. On peut y reconstruire son PDF avec :

```sh
cd historique/guide_2026_09
make
```

Prérequis : `pandoc` et `xelatex`. **Aucun PDF actualisé n'a été généré dans ce dossier de transfert.** Le PDF historique est conservé uniquement comme trace et exemple de mise en page.

## Critère de fiabilité

| Catégorie | Usage |
|---|---|
| « Donnée utilisateur » | Cote à reprendre telle quelle, sauf contradiction signalée |
| « Photographie originale » | Indice visuel de l'existant ; perspective/panorama non métriques |
| « Mesure à confirmer » | Interdit d'en faire une cote de fabrication définitive |
| « Hypothèse de l'assistant » | Proposition, susceptible d'être modifiée |
| « Image IA » | Illustration qualitative seulement, jamais source dimensionnelle |

