#!/usr/bin/env python3
"""Copier uniquement les documents publics désignés, sans parcourir les achats."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'fabrication/bardage'
DESTINATION = ROOT / 'site/content/bardage'
FILES = (
    'commande_decoupe.pdf',
    'decoupes_v1.pdf',
    'schema_decoupes.pdf', 'schema_decoupes.png',
    'debit_preparatoire.pdf',
    'isometrie_bardage_v1.pdf', 'isometrie_bardage_v1.png',
    'isometrie_cellier_v1.pdf', 'isometrie_cellier_v1.png',
    'detail_rail_raccord_v2.pdf', 'detail_rail_raccord_v2.png',
)
for name in FILES:
    if not (SOURCE / name).is_file():
        raise SystemExit(f'Document de bardage manquant : {name}')
DESTINATION.mkdir(parents=True, exist_ok=True)
for name in FILES:
    shutil.copyfile(SOURCE / name, DESTINATION / name)
print(f'Bardage : {len(FILES)} documents publics copiés par liste explicite.')
