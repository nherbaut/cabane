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
- T1, T2 et T3 désignent les **montants M48** du nord vers le sud, non les espaces. Ne pas déduire leurs coordonnées des infographies générées ; les faces des montants dans le repère du cellier restent à relever.
- La préférence ancienne de l’assistant pour l’espace T2–T3 est dépassée : l’utilisateur le met de côté à ce stade pour préserver les rangements du cellier. Étudier en priorité le passage **T1–T2**, large de 45 cm libres ; T2–T3 mesure 37,5 cm. Le milieu de T2 est à 50 cm du mur nord de la cabane ; ce n’est pas une largeur libre. Le choix définitif reste ouvert.
- Le chauffage doit rester accessible par sa face ouest ; les dégagements définitifs nécessitent la notice de l'appareil.
- T1 s’arrête à 169,5 cm ; la pièce liée à l’escalier au niveau du passage T1–T2 a sa sous-face à 174 cm et restera intacte. Les 187 cm concernent la sous-face d’une marche au-dessus de T2. Aucune modification de la structure de l’escalier, du poteau ni d’un support potentiellement porteur ne doit être prescrite sans vérification de sa fonction.
- Les recommandations sur ventilation, électrique et sécurité enfant restent des **options à vérifier** avec les conditions techniques réelles, pas une validation de conformité.
- Pour un texte de chantier destiné à un débutant, définir **en note de bas de page** chaque terme technique nouveau (BA13, montant, rail, traverse, jambage, chant, tasseau, etc.).
- L'utilisateur travaille sur Linux et souhaite conserver le Markdown et un Makefile de génération PDF via Pandoc ; conserver ces formats lors des révisions.
- Les plans numériques doivent être **cotés et reconstruits à partir de données** (SVG/Python/CAD), non dessinés par génération d'image si l'exactitude dimensionnelle est nécessaire.
- Ne pas écraser les originaux ; versionner les mises à jour et garder les anciennes variantes dans `historique/`.

## Entrées dans le projet

- `contexte/08_travaux_pour_codex.md` décrit des tâches possibles, non commandées d'avance.
- `plans/01_cellier_plan_cote.svg` présente le plan du cellier à l'échelle ; l'ouverture n'y est qu'une **zone de recherche**.
- Le script de conversion PDF existant est `historique/guide_2026_09/Makefile`.
