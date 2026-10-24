# Ventilation, chaleur et rubans LED — état des échanges

## 1. Observation initiale

L'utilisateur est entré sous l'escalier et a constaté qu'il y fait **très chaud**. Les températures, les sources de chaleur et le renouvellement d'air n'ont pas été mesurés.

Le volume comporte **déjà une ouverture basse ou latérale visible côté pièce de vie** (photographie originale 01). L'ouverture vers le cellier serait un **second passage**, non l'entrée unique.

## 2. Hypothèse de ventilation discutée

Schéma de principe envisagé :

```text
Pièce de vie
    ↓ apport d'air par l'ouverture existante
Cabane sous escalier
    ↑ accumulation d'air chaud sous l'escalier
    → petit extracteur placé en partie haute
Cellier (rejet de l'air extrait)
    → sortie par l'ouverture sud avec rideaux, vers le reste du logement
```

La contrainte explicite est qu'**une extraction éventuelle ne pourrait rejeter que vers le cellier**. L'assistant avait évoqué un extracteur silencieux réglable de l'ordre de **20–30 m³/h**, placé haut, avec une arrivée d'air basse passive. Ce chiffre est une **piste de dimensionnement**, pas un débit démontré suffisant ou conforme pour l'occupation.

**Points à étudier avant de valider :**

- Températures simultanées au sol et en haut de la cabane, dans le cellier et dans la pièce de vie ; vérifier si le MTA est une source majeure.
- Possibilité réelle de boucler la circulation d'air depuis le cellier vers la pièce de vie (rideaux, obstacles, pressions liées à la VMC et aux ouvertures).
- Une extraction vers un cellier chaud **transporte** la chaleur sans nécessairement l'évacuer du logement.
- Débit mesuré (ou mesurable), bruit, maintien d'une faible vitesse près des enfants, emplacement accessible pour entretien.
- Protection mécanique (doigts, jouets, grilles) et comportement en cas d'incendie.
- Ne pas se raccorder à une VMC collective sans étude ou autorisation adaptée.
- Le retour d'air par le cellier peut transporter chaleur/odeurs/poussières et doit être apprécié en fonction du stockage et du matériel technique.

## 3. Solution LED proposée

Ruban LED 24 V continu, de préférence **COB**[^cob] pour obtenir une lumière uniforme, dans un **profilé aluminium**[^profile] avec diffuseur opale. Valeurs proposées au cours de l'échange, non commandées :

- Température de couleur 2700 à 3000 K ; rendu des couleurs CRI ≥ 90.
- Puissance indicative 8–10 W/m, par exemple 2–3 mètres si compatible avec l'espace réel.
- Variateur accessible aux enfants pour adapter le niveau de lumière ; possibilité de trois usages « veilleuse / lecture / cabane ».
- Source lumineuse indirecte, tournée vers une paroi pour éviter l'éblouissement.
- Alimentation secteur 230 V → 24 V logée dans le **cellier**, accessible et ventilée, éloignée du MTA et des températures excessives.
- Puissance de l'alimentation à choisir après mesure de la longueur/puissance du ruban, avec marge d'environ 20–30 %.
- Câbles basse tension protégés, fixés et dimensionnés selon courant, longueur et chute de tension ; aucune installation 230 V exposée dans la cabane.

## 4. Ambiance de la cabane et appropriation par les enfants

Éléments évoqués : rideau léger non bloquant la ventilation, enseigne « cabane », dessins et panneau d'affichage, tapis facilement nettoyable, coussins déplaçables, petite bibliothèque, rangements bas, couleur choisie par les enfants, interrupteur à leur hauteur. Ne pas créer de points d'accroche dangereux ni bloquer les deux ouvertures ; tenir compte de la chaleur déjà présente et éviter l'accumulation de textiles volumineux.

## 5. État de validation

| Sujet | État |
|---|---|
| Point d'extraction en hauteur | Principe proposé ; implantation non fixée |
| Rejet vers le cellier | Seule destination annoncée possible, faisabilité aéraulique à confirmer |
| Ventilateur 20–30 m³/h | Hypothèse, non dimensionnée par calcul ni mesure |
| Température dans les volumes | Données manquantes |
| Ruban LED 24 V | Orientation retenue à titre de conception |
| Longueur et cheminement du ruban | À mesurer |
| Localisation alimentation 24 V | Cellier, emplacement exact inconnu |

[^cob]: **COB** (*chip on board*) : technologie où de nombreuses LED rapprochées fournissent un effet de ligne lumineuse continue.
[^profile]: **Profilé aluminium** : support allongé qui maintient et aide à dissiper la chaleur d'un ruban LED.
