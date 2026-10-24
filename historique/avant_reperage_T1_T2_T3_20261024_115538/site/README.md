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

Le plan est tracé dans le navigateur à partir de `donnees/geometrie.json`. Le milieu du deuxième montant est mesuré à 50 cm du mur nord de la cabane. Le plan le représente à y=130 sous condition d’alignement des murs nord du cellier et de la cabane ; la position exacte des faces dans le repère reste à établir. La largeur libre de T1 est mesurée à 47 cm et sa hauteur sous plafond à 174 cm aux deux extrémités. La simulation et la vue de face utilisent ces données ; seul l’habillage latéral est simulé, le haut de l’encadrement restant à définir.
