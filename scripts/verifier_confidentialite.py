#!/usr/bin/env python3
"""Empêcher l'ajout ou la copie des justificatifs privés dans la publication."""
import argparse
import hashlib
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PRIVATE_ROOTS = (ROOT / 'achat', ROOT / 'achats')


def digest(path):
    return hashlib.sha256(path.read_bytes()).digest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--public-dir', type=Path)
    args = parser.parse_args()
    tracked = subprocess.check_output(
        ['git', 'ls-files', '-z'], cwd=ROOT
    ).decode().split('\0')
    if any(name and Path(name).parts[0] in ('achat', 'achats') for name in tracked):
        sys.exit('Confidentialité : un document du répertoire privé est suivi par Git.')
    ignore_rules = (ROOT / '.gitignore').read_text().splitlines()
    if not all(rule in ignore_rules for rule in ('/achat/', '/achats/')):
        sys.exit('Confidentialité : les exclusions des justificatifs privés sont absentes.')
    documents = [path for folder in PRIVATE_ROOTS if folder.exists()
                 for path in folder.rglob('*') if path.is_file()]
    names = {path.name for path in documents}
    hashes = {digest(path) for path in documents}
    candidates = [ROOT / name for name in tracked if name and (ROOT / name).is_file()]
    folders = [ROOT / 'site/content', ROOT / 'site/static']
    if args.public_dir:
        folders.append(args.public_dir)
    for folder in folders:
        if folder.exists():
            candidates.extend(path for path in folder.rglob('*') if path.is_file())
    for path in candidates:
        if path.name in names or (hashes and digest(path) in hashes):
            sys.exit('Confidentialité : copie d’un document privé détectée ; publication interrompue.')
    print('Confidentialité : justificatifs privés exclus des sources suivies et de la publication.')


if __name__ == '__main__':
    main()
