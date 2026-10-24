# Aménagement du cellier pour une famille

## Coordonnées

Intérieur rectangulaire de **115 cm (est–ouest)** × **180 cm (sud–nord)**, hauteur **250 cm**. Origine `(x,y)=(0,0)` à l'angle intérieur sud-ouest ; `x` vers l'est, `y` vers le nord.

| Équipement | Emprise en cm | Hauteur cm | Fonction / contrainte |
|---|---|---:|---|
| A | `x=0..25`, `y=0..80` | 240 | Réserves alimentaires, mur ouest |
| B | `x=85..115`, `y=90..180` | 220 | Petit matériel, mur est |
| MTA | `x=95..115`, `y=0..50` | 230 | Chauffage urbain, face ouest accessible |
| Poutre | `x=90..115`, `y=0..180` | sous-face à 230 | Limite hauteur des objets dessous |
| Escalier au-dessus du cellier | `x=0..80`, `y=80..180` | libre simplifié à 188 | Affecte hauteur disponible à proximité de la baie |
| Ouverture sud | précédemment `x=6..86`, `y=0` | hauteur non fournie | Ancienne porte battante supprimée, hypothèse de rideaux |
| Ouverture vers cabane | `x=0`, `y=?` | inconnue | Travée physique à définir ; largeur ≈53 cm, non 80 |

## Dégagements résultants

- Entre le rayonnage A (jusqu'à `x=25`) et la face ouest du module de chauffage (`x=95`), il existe **70 cm** à `y=0..50` en supposant ces emprises exhaustives.
- Devant le rayonnage B, l'allée nord va de `x=0` à `x=85`, soit **85 cm** tant qu'aucun autre objet n'est présent.
- Sur `y=0..80`, le rayonnage A occupe `x=0..25` ; devant l'ancienne ouverture sud `x=6..86`, l'alignement praticable sans changement latéral est de **61 cm** (`x=25..86`).
- Entre A et B, les implantations en `y` sont disjointes (`A` s'arrête à 80, `B` débute à 90), laissant une bande de 10 cm entre leurs extrémités.
- A (hauteur 240) ne peut pas se trouver sous la poutre est de sous-face 230, mais sa position ouest hors emprise convient au modèle. B (hauteur 220) est sous la poutre à 230 avec marge verticale théorique de **10 cm**.
- La partie nord doit être laissée libre près de l'ouverture choisie pour permettre le passage depuis la cabane.

## Contraintes de stockage

Réserves alimentaires sèches : étagères stables, surfaces nettoyables, contenants protégés des nuisibles et de la chaleur. Éloigner les denrées sensibles de la source chaude, du MTA et des parois excessivement chaudes. Petit matériel : réserver les niveaux hauts aux objets peu fréquemment employés, éviter tout objet lourd en hauteur et fixer les rayonnages contre le renversement. Conserver l'accès technique au module de chauffage selon sa notice.

## Changements envisagés mais non décidés

Au début des échanges, il a été suggéré de diminuer la profondeur du rayonnage A ou de le remplacer par un stockage haut pour gagner une circulation d'environ 80 cm au sud. L'utilisateur a ensuite fourni une implantation explicite **A=25 cm** et **B=30 cm** sans annoncer la suppression de A. Le dessin actuel doit donc conserver ces deux rayonnages **comme implantation proposée**, tout en signalant les circulations étroites et la possibilité de variantes.

## Éléments à ajouter au futur plan

Tracer à l'échelle exacte les emprises A, B, MTA, poutre et zone d'escalier, les hauteurs libres par zone et l'ouverture sud. Pour la nouvelle baie, dessiner uniquement une **zone de positionnement encore à mesurer** ; ne pas prendre `y=90..170` comme une baie définitive de 53 cm. L'espace de la cabane au-delà du mur ouest n'est pas coté.
