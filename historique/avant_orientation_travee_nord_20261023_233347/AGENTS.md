# Instructions Codex — projet cabane / cellier

## Objectif

Aider à concevoir, documenter et éventuellement produire des plans ou schémas reproductibles pour un passage sous escalier menant au cellier et un aménagement de rangement, sur la base des documents locaux.

## Sources et priorités

1. Les dimensions explicites formulées par l'utilisateur, consolidées dans `donnees/geometrie.json`.
2. Les photos originales du dossier `photos/originales`.
3. Les décisions et incertitudes identifiées dans `contexte/`.
4. Le guide historique `historique/guide_2026_09/chantier.md` (peut contenir des hypothèses aujourd'hui dépassées).
5. Les images générées par IA, purement illustratives et **non métriques**.

## Instructions à respecter

- Répondre et produire les documents en **français formel**.
- Conserver le repère : origine `(0,0,0)` à l'angle intérieur sud-ouest du cellier ; `x` vers l'est, `y` vers le nord, `z` vers le haut ; unité = **cm**.
- Séparer systématiquement **faits**, **hypothèses**, **mesures manquantes**, **propositions** et **points de sécurité**.
- Ne pas prétendre que la baie de 53 cm est située précisément de `y=90` à `y=170` : cet intervalle fait 80 cm.
- Ne pas fixer la travée 1/2 uniquement à partir des infographies générées ; identifier les vrais montants et leurs coordonnées réelles.
- La **travée 2 est préférée sous condition** (hauteur libre plus grande et absence de conflit avec rayonnage A), mais le choix **n'a pas été arrêté par l'utilisateur**.
- Le chauffage doit rester accessible par sa face ouest ; les dégagements définitifs nécessitent la notice de l'appareil.
- Aucune modification de la structure de l'escalier, du poteau ni d'un support potentiellement porteur ne doit être prescrite sans vérification de sa fonction.
- Les recommandations sur ventilation, électrique et sécurité enfant restent des **options à vérifier** avec les conditions techniques réelles, pas une validation de conformité.
- Pour un texte de chantier destiné à un débutant, définir **en note de bas de page** chaque terme technique nouveau (BA13, montant, rail, traverse, jambage, chant, tasseau, etc.).
- L'utilisateur travaille sur Linux et souhaite conserver le Markdown et un Makefile de génération PDF via Pandoc ; conserver ces formats lors des révisions.
- Les plans numériques doivent être **cotés et reconstruits à partir de données** (SVG/Python/CAD), non dessinés par génération d'image si l'exactitude dimensionnelle est nécessaire.
- Ne pas écraser les originaux ; versionner les mises à jour et garder les anciennes variantes dans `historique/`.

## Entrées dans le projet

- `contexte/08_travaux_pour_codex.md` décrit des tâches possibles, non commandées d'avance.
- `plans/01_cellier_plan_cote.svg` présente le plan du cellier à l'échelle ; l'ouverture n'y est qu'une **zone de recherche**.
- Le script de conversion PDF existant est `historique/guide_2026_09/Makefile`.
