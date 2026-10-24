# Cabane sous escalier et cellier — dossier de transfert vers Codex

**État du dossier : 23 octobre 2026.** Langue de travail : français. Unités : centimètres.

Ce dossier rassemble le contexte d'un projet domestique : création d'un passage entre une future cabane d'enfants sous un escalier et un cellier étroit, aménagement des rangements du cellier, ventilation de l'espace chaud et éclairage LED.

## Démarrage conseillé dans Codex

1. Ouvrir ce dossier comme répertoire de travail, puis lire [`AGENTS.md`](AGENTS.md).
2. Lire [`contexte/01_etat_du_projet.md`](contexte/01_etat_du_projet.md) : état des décisions, faits observés et hypothèses.
3. Consulter [`donnees/geometrie.json`](donnees/geometrie.json) pour les cotes **connues**, la différence entre *données* et *hypothèses*, et les incohérences à lever.
4. Examiner les **cinq photographies originales** dans [`photos/originales/`](photos/originales/). Elles priment sur les visualisations générées pour la reconnaissance de l'existant.
5. Utiliser le [plan SVG paramétrique de référence](plans/01_cellier_plan_cote.svg), en tenant compte du fait que la position exacte de la nouvelle baie n'est PAS connue.
6. Consulter le guide antérieur dans [`historique/guide_2026_09/chantier.md`](historique/guide_2026_09/chantier.md) ; son PDF est un état **historique**, potentiellement obsolète.

## Arborescence

```text
.
├── AGENTS.md                         Instructions à Codex
├── README.md                         Ce fichier
├── contexte/
│   ├── 01_etat_du_projet.md          Synthèse actualisée
│   ├── 02_choix_de_la_travee.md      Options 1/2 et conditions du choix
│   ├── 03_travaux_et_securite.md     Principes constructifs et vérifications
│   ├── 04_ventilation_eclairage.md  Options étudiées, non dimensionnées définitivement
│   ├── 05_amenagement_cellier.md    Deux rayonnages et dégagements
│   ├── 06_historique_et_decisions.md Historique des échanges et des évolutions
│   ├── 07_index_des_images.md       Provenance et fiabilité des visuels
│   └── 08_travaux_pour_codex.md      Pistes de tâches et critères d'acceptation
├── donnees/
│   └── geometrie.json               Données numériques et incertitudes
├── plans/
│   └── 01_cellier_plan_cote.svg      Plan réellement coté (hors position de baie)
├── photos/
│   ├── originales/                   5 photographies de l'utilisateur (non retouchées)
│   └── annotees/                    Annotations de l'ancien guide
├── illustrations_ia_non_metriques/ Image de couverture indicative
└── historique/
    ├── guide_2026_09/               Markdown + Makefile + images + ancien PDF
    └── infographies_ia/            Variantes graphiques NON fiables pour mesurer
```

## Points à ne pas confondre

- **Cellier** : rectangle intérieur mesuré **115 cm (ouest-est) × 180 cm (sud-nord)**. L'escalier réduit la hauteur dans sa zone nord-ouest.
- **Cabane** : espace de jeu de l'autre côté de la cloison ouest du cellier, sous l'escalier ; sa géométrie en plan n'a **pas été relevée séparément**.
- **Largeur de passage ≈ 53 cm** : taille supposée d'une travée entre profils métalliques. Mesure nette de passage à refaire.
- **Intervalle initial `y=90..170`** : ancien repérage d'une zone du mur ouest sur **80 cm de longueur** ; ce n'est pas une cote compatible en l'état avec une baie de 53 cm. **Il faut relever la position exacte de la travée retenue**.
- **Travée 2** : dernier choix conseillé, **conditionnel**. La numérotation 1/2 visible dans les images IA est ambiguë : vérifier la désignation physique des montants et la position réelle de chaque travée.
- **Hauteur sous escalier** : 188 cm était une **hypothèse simplifiée de géométrie**, tandis que la photo du mètre présente un repère voisin de **175 cm au point photographié**. Il manque le relevé de hauteur à chaque bord de la baie.
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

