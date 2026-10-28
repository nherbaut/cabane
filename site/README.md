# Étude visuelle Hugo — cabane et cellier

Site statique local. Les photographies et le JSON sont copiés depuis les sources du dossier par le Makefile racine ; les originaux restent inchangés.

```sh
make site-serve
```

Ouvrir <http://localhost:1313/>. Pour construire les fichiers statiques :

```sh
make site-build
```

Hugo est nécessaire. Si la version installée ne fonctionne pas, `make site-hugo-install` télécharge un binaire Linux amd64 dans `site/.bin/`, puis `make site-serve` l'utilise automatiquement. Un autre binaire peut être indiqué avec `make site-serve HUGO=/chemin/vers/hugo`.

La vue principale réunit le cellier et la cabane. Les deux espaces sont tracés à la même échelle depuis `donnees/geometrie.json` : cabane de 260 × 90 cm (190 cm puis 70 cm supplémentaires d’accès), cellier de 180 × 115 cm. Les 70 cm correspondent à la base horizontale de l’accès triangulaire dans le prolongement du mur ouest du cellier. Ils ne désignent pas une ouverture sur la largeur de 90 cm. Le mur nord est **commun**, donc le milieu de T2, à 50 cm de ce mur, est directement à **y=130 cm** dans le repère du cellier. Le passage décidé T1–T2 mesure **45 cm libres** ; les mesures sont exploitables des deux côtés de la cloison. La flèche représente cette liaison sans fixer des bords de découpe.

La page propose une seule vue d’ensemble exportable, `plans/03_ensemble_cellier_cabane.svg`. Le plan du cellier et l’élévation cotée restent disponibles dans `plans/` pour les détails. `make site-build` régénère les plans puis les copie vers `site/static/plans/`. La simulation d’habillage soustrait seulement les panneaux latéraux ; l’objectif de 168 cm finis reste à vérifier avec l’assemblage supérieur.

## Publication sur GitHub Pages

Le dépôt est `nherbaut/cabane`, branche `master`. Le workflow `.github/workflows/pages.yml` régénère les plans et le site, puis publie uniquement `site/public/`. L’adresse attendue est <https://nherbaut.github.io/cabane/>.

À effectuer une fois dans [Settings → Pages](https://github.com/nherbaut/cabane/settings/pages) : sélectionner **GitHub Actions** comme source. Les prochains envois sur `master` publieront automatiquement le site ; le workflow peut aussi être relancé depuis l’onglet Actions.

Hugo reçoit l’adresse publique grâce à `HUGO_BASEURL`, afin que les images, scripts, schémas et liens internes incluent le préfixe `/cabane/`. La configuration locale reste utilisable avec `make site-serve`. Vérification locale du build public :

```sh
HUGO_BASEURL=https://nherbaut.github.io/cabane/ make site-build
```

Les fichiers générés et le binaire Hugo sont exclus du dépôt par `.gitignore`. Le workflow installe la même version de Hugo que le Makefile local et le moteur `rsvg-convert` pour les aperçus des plans.

Le guide d’habillage inclut un gabarit SVG/PDF A4 généré par `make plan`, pour l’essai compact à 168 cm finis. Le PDF doit être imprimé à 100 %, contrôle par une barre de 50 mm. Il vérifie l’encombrement proposé (12 + 20 + 20 mm), sans valider les fixations ou la charge.

La page `achats/` regroupe la liste prévisionnelle, les formats et les repères Leroy Merlin. Son PDF se régénère avec `make achats-pdf` (Pandoc et XeLaTeX), puis doit être versionné avec le Markdown. La publication Hugo copie ce PDF sans dépendre de TeX. Les achats de supports et de fixations restent conditionnels.

Le stock confirmé du chantier est conservé dans `donnees/stock.json` et présenté sur `achats/`. Les quantités désignent les achats, sans suivi de consommation. Les justificatifs privés dans les répertoires racine `achat/` et `achats/` sont exclus de Git et ne doivent jamais être copiés dans le site ou les archives publiques. `make site-build` contrôle les exclusions, les fichiers suivis et l’absence de copies des documents privés avant et après génération grâce à `scripts/verifier_confidentialite.py`. Ce contrôle bloque aussi une copie identique renommée lorsque le justificatif local est disponible ; il ne remplace pas la vérification éditoriale des données publiées.

## Bardage et découpes du 28 octobre 2026

La page `bardage/` est la référence actuelle pour l’OSB, les coupes brutes et
les vues isométriques. Les sources sont dans `fabrication/bardage/` et les
mesures dans `donnees/geometrie.json`. La profondeur mesurée est de 6 cm
± 2 mm. Les premiers gabarits à 168 cm restent historiques.

`make -C fabrication/bardage all` régénère localement les figures et PDF
(Matplotlib, NumPy, Pandoc et XeLaTeX). Les fichiers produits sont versionnés.
`make site-build` copie uniquement huit PDF/PNG explicitement désignés par
`scripts/copier_documents_bardage.py` ; la CI n’a pas à installer les outils
de dessin ou TeX. Aucun répertoire d’achat privé n’est parcouru par ce script.
