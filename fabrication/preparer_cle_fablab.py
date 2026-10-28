#!/usr/bin/env python3
"""Archive USB par liste blanche explicite : aucune photo ni achat privé."""
import hashlib
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

base = Path(__file__).resolve().parent
source = base / 'seuil_fablab_v1'
files = [
    '00_LIRE_AVANT_IMPRESSION.pdf', '00_LIRE_AVANT_IMPRESSION.md',
    '01_ESSAI_seuil_SUR_TRANCHE_mm.stl', 'schema_cote.pdf',
    'schema_cote.svg', 'apercu.png', 'parametres.json',
    'modele_modifiable.scad', 'generer.py', 'verification.json',
    'requirements.txt', 'Makefile',
]
assert all((source/name).is_file() for name in files)
manifest = ''.join(f'{hashlib.sha256((source/name).read_bytes()).hexdigest()}  {name}\n'
                   for name in files)
(source/'SHA256SUMS.txt').write_text(manifest)
files.append('SHA256SUMS.txt')
destination = base/'FABLAB_seuil_ESSAI_v1.zip'
with ZipFile(destination, 'w', compression=ZIP_DEFLATED) as archive:
    for name in files:
        info = ZipInfo('seuil_fablab_v1/'+name, date_time=(2026,10,28,0,0,0))
        info.compress_type = ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        archive.writestr(info,(source/name).read_bytes())
with ZipFile(destination) as archive:
    assert archive.testzip() is None
    assert set(archive.namelist()) == {'seuil_fablab_v1/'+name for name in files}
    for line in manifest.splitlines():
        digest,name=line.split('  ',1)
        assert hashlib.sha256(archive.read('seuil_fablab_v1/'+name)).hexdigest()==digest
print(f'{destination.name} : {len(files)} fichiers vérifiés, {destination.stat().st_size} octets.')
