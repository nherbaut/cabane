# Fichiers de fabrication — 28 octobre 2026

- **Fablab :** `FABLAB_seuil_ESSAI_v1.zip`. Décompresser et copier le dossier
  `seuil_fablab_v1` sur la clé USB. Ouvrir la fiche PDF avant d’imprimer le STL.
  Il contient seulement un **échantillon d’ajustement**, pas le seuil complet.
- **Bardage :** `bardage/decoupes_v1.pdf` explique les deux hauteurs
  (188 cm au-dessus de T1–T2, 170 cm entre T2 et T3) et sépare les découpes
  brutes proposées des cotes finales à mesurer. `bardage/debit_preparatoire.pdf`
  donne la disposition des réserves dans un panneau proposé de 250 × 125 cm.

## Régénération

```sh
make -C fabrication/seuil_fablab_v1 all
python3 fabrication/preparer_cle_fablab.py
make -C fabrication/bardage all
```

Les dépendances du générateur 3D sont dans
`seuil_fablab_v1/requirements.txt`. Les PDF de texte utilisent Pandoc et XeLaTeX.
Le plan de débit utilise les données du projet dans `donnees/geometrie.json`.
Le dossier fablab, lui, est autonome : ses paramètres sont inclus.

Les dimensions du projet et des schémas sont en **cm** ; le STL utilise les
**mm**, explicitement indiqués dans la notice. Les vérifications informatiques
du maillage ne valident pas la résistance d’une pièce imprimée.

L’archive USB est construite depuis une liste explicite de fichiers : aucun
ticket, document d’achat privé ou photo du logement n’y figure. Ces fichiers
de fabrication ne sont pas copiés dans le site web.
