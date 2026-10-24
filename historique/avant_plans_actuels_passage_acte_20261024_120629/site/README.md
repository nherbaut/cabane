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

Le plan est tracé dans le navigateur à partir de `donnees/geometrie.json`. T1, T2 et T3 nomment les trois montants du nord vers le sud. Le passage prioritaire T1–T2 mesure **45 cm libres** ; T2–T3 mesure **37,5 cm**. Le milieu de T2 est à 50 cm du mur nord de la cabane et n’est placé à `y=130` sur le plan que sous l’hypothèse d’alignement des murs nord. La vue de face indique la pièce de l’escalier à **174 cm** au niveau de T1–T2 et T1 à **169,5 cm** ; elle ne fixe pas la hauteur finie du passage. La simulation soustrait seulement l’épaisseur des deux planches latérales.
