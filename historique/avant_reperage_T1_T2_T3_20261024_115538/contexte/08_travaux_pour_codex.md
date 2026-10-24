# Suggestions pour la reprise avec Codex

Ce document n'est pas une commande de travaux automatiques. Il facilite une reprise du projet étape par étape.

## Tâche A — Géométrie des travées

Créer un tableau de mesures physiques pour les trois premiers montants depuis le mur de référence choisi ; fixer une convention **sans ambiguïté** (par exemple M0 = montant mural nord, M1 et M2 en allant vers le sud). Relever leurs coordonnées `y` sur le mur ouest du cellier, la largeur réellement libre entre faces internes et les deux hauteurs sous pente pour chaque travée. Ne pas inférer ces distances depuis les panoramas.

**Critère d'acceptation :** chaque baie candidate est associée à ses deux montants nommés, ses `y_min/y_max` mesurés et ses hauteurs aux deux bords ; aucune contradiction entre largeur et coordonnées.

## Tâche B — Comparaison travée 1 / travée 2

Calculer largeur finie pour plusieurs habillages de 12 ou 15 mm, hauteur libre et conflits avec A, B, le chauffage et le chemin d'accès. Documenter les avantages et limites. Conserver l'option « travée 2 si `y_min >= 80` et plus haute » comme recommandation provisoire.

**Critère d'acceptation :** plan coté fidèle, comparaison chiffrée, toutes incertitudes explicites.

## Tâche C — Plan du cellier

Partir du `donnees/geometrie.json` pour réaliser un plan à l'échelle et une 3D simplifiée, par exemple avec Python/Matplotlib, SVG ou FreeCAD. Le dessin doit reproduire les éléments rectangulaires sans les déplacer arbitrairement. Représenter poutre et escalier comme contraintes en hauteur, et vérifier l'accès à la face ouest du MTA.

**Critère d'acceptation :** plan intérieur de 115 × 180 cm, coordonnées conformes, baie non figée tant qu'elle n'est pas mesurée.

## Tâche D — Mise à jour du guide de chantier

Réécrire `historique/guide_2026_09/chantier.md` sous une **nouvelle version**, sans perdre les sources. Définir chaque terme de bricolage nouveau en note de bas de page (demande explicite de l'utilisateur). Incorporer les photographies d'origine et des annotations manuelles lisibles. Ne générer le PDF que lorsque l'utilisateur le demande ; le pipeline historique repose sur Pandoc et XeLaTeX.

**Critère d'acceptation :** source Markdown autonome, images locales, Makefile correct, mesures incohérentes retirées ou déclarées provisoires.

## Tâche E — Étude de ventilation et LED

Élaborer un schéma des volumes (pièce de vie, cabane, cellier), tracer le chemin d'air et la source de chaleur possible, puis estimer les débits seulement après mesure de température et de volume. Respecter la contrainte de rejet vers le cellier. Préparer un câblage de ruban LED 24 V avec alimentation accessible dans le cellier, sans composants secteur exposés aux enfants.

**Critère d'acceptation :** schéma du flux d'air, distinction débit théorique/mesuré, localisation et raccordement électrique à faire vérifier selon configuration réelle.

## Tâche F — Habillage bois simplifié

Préparer une fiche de découpe de trois pièces de contreplaqué et d'éventuels tasseaux, uniquement après prise de cotes réelles. Illustrer joints, position des vis, traitement des bords et rail au seuil.

**Critère d'acceptation :** les cotes et pièces ne sont pas inventées ; toutes les arêtes accessibles sont protégées ; aucun élément structurel n'est supprimé sans validation.
