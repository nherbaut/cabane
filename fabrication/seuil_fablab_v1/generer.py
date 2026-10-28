#!/usr/bin/env python3
"""Échantillon de seuil, source en cm, STL en mm. Aucun fichier privé lu."""
import json
import math
import struct
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from shapely.geometry import Point, Polygon as ShapePolygon, box
from shapely.geometry.polygon import orient
from shapely.ops import triangulate

ROOT = Path(__file__).resolve().parent
C = json.loads((ROOT / 'parametres.json').read_text())
P, F = C['proposal'], C['facts']
W = P['sample_width_east_west'] * 10
L = P['sample_length_north_south'] * 10
H = P['top_height'] * 10
E = P['edge_height'] * 10
CW = P['rail_channel_width'] * 10
A, B = (W - CW) / 2, (W + CW) / 2
G = P['rail_channel_ceiling_above_tile'] * 10
D = P['screw_pocket_ceiling_above_tile'] * 10
R = P['screw_pocket_diameter'] * 5
CX = (W - F['rail_outer_width'] * 10) / 2 + F['screw_from_cabin_rail_edge'] * 10
CY = L / 2
assert 0 < E < H and 0 < G < D < H
assert A < CX - R and CX + R < B and R < CY < L - R


def roof(x):
    if x < A:
        return E + (H - E) * x / A
    if x > B:
        return E + (H - E) * (W - x) / (W - B)
    return H


def key(p):
    return tuple(round(float(x), 7) for x in p)


disk = Point(CX, CY).buffer(R, quad_segs=P['circle_segments'] // 4)
regions = [(box(0, 0, A, L), 0),
           (box(A, 0, B, L).difference(disk), G),
           (disk, D), (box(B, 0, W, L), 0)]
faces = []
edges = defaultdict(list)

for region, floor in regions:
    region = orient(region, sign=1)
    for tri in triangulate(region):
        if not region.covers(tri):
            continue
        xy = list(tri.exterior.coords)[:3]
        signed = sum(xy[i][0] * xy[(i+1) % 3][1] - xy[(i+1) % 3][0] * xy[i][1]
                     for i in range(3))
        if signed < 0:
            xy.reverse()
        faces.append([(x, y, roof(x)) for x, y in xy])
        faces.append([(x, y, floor) for x, y in reversed(xy)])
    for ring in [region.exterior, *region.interiors]:
        coords = list(ring.coords)
        for a, b in zip(coords, coords[1:]):
            edges[tuple(sorted((key(a), key(b))))].append((a, b, floor))

levels = defaultdict(set)
for adjacent in edges.values():
    for a, b, floor in adjacent:
        for pt in (a, b):
            levels[key(pt)].update([floor, roof(pt[0])])

for adjacent in edges.values():
    assert len(adjacent) in (1, 2)
    if len(adjacent) == 1:
        a, b, low = adjacent[0]
        high_a, high_b = roof(a[0]), roof(b[0])
    else:
        low_side, high_side = sorted(adjacent, key=lambda side: side[2])
        a, b, low = low_side
        high_a = high_b = high_side[2]
        if high_a == low:
            continue
    # Découper aussi les arêtes verticales aux niveaux des faces voisines :
    # aucune jonction en T, y compris aux deux sorties du canal.
    wall = [(0, low), (1, low)]
    wall += [(1, z) for z in sorted(levels[key(b)]) if low < z < high_b]
    wall += [(1, high_b), (0, high_a)]
    wall += [(0, z) for z in sorted(levels[key(a)], reverse=True) if low < z < high_a]
    poly = ShapePolygon(wall)
    for tri in triangulate(poly):
        if not poly.covers(tri):
            continue
        pts = list(orient(tri, sign=1).exterior.coords)[:3]
        faces.append([(a[0]+t*(b[0]-a[0]), a[1]+t*(b[1]-a[1]), z) for t,z in pts])

mesh = np.array(faces, dtype=float)


def check(mesh):
    counts, directed = Counter(), Counter()
    for tri in mesh:
        assert np.linalg.norm(np.cross(tri[1]-tri[0], tri[2]-tri[0])) > 1e-8
        for a, b in zip(tri, np.roll(tri, -1, axis=0)):
            a, b = key(a), key(b)
            counts[tuple(sorted((a, b)))] += 1
            directed[(a, b)] += 1
    assert set(counts.values()) == {2}, 'Maillage ouvert ou non-manifold'
    assert all(v == directed[(b, a)] for (a, b), v in directed.items()), 'Orientation incohérente'
    volume = np.einsum('ij,ij->i', mesh[:, 0], np.cross(mesh[:, 1], mesh[:, 2])).sum()/6
    analytic = L * (CW * H + (W-CW)*(E+H)/2) - CW*L*G - disk.area*(D-G)
    assert abs(volume-analytic) < 1e-6, (volume, analytic)
    return volume


volume = check(mesh)
# Rotation rigide : impression sur la face nord de 120 x 8 mm.
print_mesh = np.stack([mesh[:, :, 0], mesh[:, :, 2], L-mesh[:, :, 1]], axis=2)
check(print_mesh)
outfile = ROOT / '01_ESSAI_seuil_SUR_TRANCHE_mm.stl'
with outfile.open('wb') as out:
    out.write(b'ESSAI uniquement - unite mm - ne pas utiliser comme seuil'.ljust(80, b' '))
    out.write(struct.pack('<I', len(print_mesh)))
    for tri in print_mesh:
        n = np.cross(tri[1]-tri[0], tri[2]-tri[0]); n /= np.linalg.norm(n)
        out.write(struct.pack('<12fH', *n, *tri.flatten(), 0))

# Contrôle après quantification réelle en float32 du fichier STL.
with outfile.open('rb') as inp:
    inp.read(80); n = struct.unpack('<I', inp.read(4))[0]
    reread = np.array([struct.unpack('<12fH', inp.read(50))[3:12] for _ in range(n)]).reshape(-1, 3, 3)
    assert inp.read() == b''
# Les coordonnées identiques restent identiques après l'export float32.
saved_counts = Counter(tuple(sorted((key(a), key(b)))) for tri in reread
                       for a, b in zip(tri, np.roll(tri, -1, axis=0)))
assert set(saved_counts.values()) == {2}
assert np.allclose(np.ptp(reread.reshape(-1, 3), axis=0), [W, H, L])

report = {
 'statut':'Échantillon de présentation ; aucune validation de charge ou de conformité.',
 'unites_stl':'mm', 'dimensions_piece_en_position_pose_mm':[W,L,H],
 'dimensions_stl_oriente_impression_mm':[W,H,L],
 'maillage_ferme':True, 'aretes_partagees_par_exactement_deux_triangles':True,
 'orientations_coherentes':True, 'triangles':len(mesh),
 'volume_matiere_geometrique_cm3':round(volume/1000,3),
 'logement_vis_diametre_mm':2*R, 'plafond_logement_depuis_carrelage_mm':D,
 'epaisseur_mini_au_dessus_vis_mm':H-D,
 'centre_logement_depuis_bord_cabane_mm':CX,
 'centre_logement_depuis_bord_cellier_mm':W-CX,
 'degagement_rail_largeur_mm':CW,'degagement_rail_hauteur_hypothese_mm':G,
 'note':'Le contrôle du maillage ne démontre pas la résistance de la pièce imprimée.'
}
(ROOT/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')

scad = f'''// ÉCHANTILLON SEULEMENT — pas un seuil de circulation.
// Généré depuis parametres.json (cm). Ici les longueurs sont en mm.
// Repère local : x vers cellier/est, y vers T1/nord, z vers le haut.
largeur = {W}; longueur = {L}; hauteur = {H}; bord = {E};
canal = {CW}; jeu_rail = {G}; diametre_vis = {2*R}; plafond_vis = {D};
centre_vis_x = {CX}; centre_vis_y = {CY};
sur_tranche = true;
$fn = {P['circle_segments']};
module echantillon() {{
  difference() {{
    translate([0,longueur,0]) rotate([90,0,0])
      linear_extrude(height=longueur)
        polygon([[0,0],[largeur,0],[largeur,bord],
                 [(largeur+canal)/2,hauteur],[(largeur-canal)/2,hauteur],[0,bord]]);
    translate([(largeur-canal)/2,-1,-1]) cube([canal,longueur+2,jeu_rail+1]);
    translate([centre_vis_x,centre_vis_y,-1]) cylinder(h=plafond_vis+1,d=diametre_vis);
  }}
}}
if (sur_tranche) translate([0,0,longueur]) rotate([-90,0,0]) echantillon();
else echantillon();
'''
(ROOT/'modele_modifiable.scad').write_text(scad)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, Circle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

plt.rcParams.update({'font.size':10,'svg.fonttype':'none'})
fig=plt.figure(figsize=(10,10),layout='constrained')
gs=fig.add_gridspec(3,1,height_ratios=[1,1,1.5])
ax=fig.add_subplot(gs[0]); ax.set_title('Coupe au centre de la vis — cotes en cm (propositions)')
ax.add_patch(Polygon([(0,0),(A/10,0),(A/10,G/10),((CX-R)/10,G/10),
                      ((CX-R)/10,D/10),((CX+R)/10,D/10),((CX+R)/10,G/10),
                      (B/10,G/10),(B/10,0),(W/10,0),(W/10,E/10),
                      (B/10,H/10),(A/10,H/10),(0,E/10)],
                     facecolor='#6bb6c7',edgecolor='#163e52'))
ax.axhline(0,color='gray',linewidth=1)
ax.annotate('',xy=(0,-.22),xytext=(W/10,-.22),arrowprops={'arrowstyle':'<->'})
ax.text(W/20,-.40,f'{W/10:g} cm de large',ha='center',va='top')
ax.text(CX/10,.42,'logement Ø 1,8\nplafond z = 0,4',ha='center',fontsize=9)
ax.text(.1,.9,'CABANE / ouest',ha='left'); ax.text(W/10-.1,.9,'CELLIER / est',ha='right')
ax.text(.1,-.9,'Canal sous le rail : 7,2 cm de large × 0,1 cm de haut (hauteur à vérifier).')
ax.set_xlim(-.4,W/10+.4); ax.set_ylim(-1.1,1.2); ax.set_aspect('equal'); ax.axis('off')

ax=fig.add_subplot(gs[1]); ax.set_title('Plan des logements sous la pièce — regard depuis le dessus, par transparence')
ax.add_patch(Rectangle((0,0),W/10,L/10,facecolor='#eef4f5',edgecolor='#163e52'))
ax.add_patch(Rectangle((A/10,0),CW/10,L/10,facecolor='#c4e0e5',edgecolor='#163e52',linestyle='--'))
ax.add_patch(Circle((CX/10,CY/10),R/10,facecolor='#e7ac60',edgecolor='#163e52'))
ax.plot([CX/10],[CY/10],'+',color='black'); ax.text(CX/10,CY/10+1.1,'Ø 1,8 cm',ha='center')
ax.annotate('',xy=(0,-.25),xytext=(CX/10,-.25),arrowprops={'arrowstyle':'<->'})
ax.text(CX/20,-.65,f'centre à {CX/10:g} cm du bord CABANE',ha='center',fontsize=9)
ax.text(W/10+.2,L/20,'4 cm\nvers T1 ↑',va='center')
ax.set_xlim(-.4,W/10+1.4); ax.set_ylim(-.9,L/10+.35); ax.set_aspect('equal'); ax.axis('off')

ax=fig.add_subplot(gs[2],projection='3d')
normals = np.cross(mesh[:,1]-mesh[:,0],mesh[:,2]-mesh[:,0])
normals /= np.linalg.norm(normals,axis=1)[:,None]
shade = .60 + .35*np.maximum(0, normals@np.array([-.5,-.4,.75]))
colors = np.array([.40,.70,.76])[None,:]*shade[:,None]
collection=Poly3DCollection(mesh/10,facecolors=colors,edgecolors='none')
ax.add_collection3d(collection); ax.set_xlim(0,W/10); ax.set_ylim(0,L/10); ax.set_zlim(0,1.2)
ax.set_box_aspect((W,L,12)); ax.view_init(elev=24,azim=-58)
ax.set_axis_off()
ax.set_title('Échantillon de présentation — ne pas marcher dessus')
fig.suptitle('Seuil imprimable : essai v1, pas le seuil final',fontsize=16)
fig.savefig(ROOT/'schema_cote.svg'); fig.savefig(ROOT/'schema_cote.pdf');
fig.savefig(ROOT/'apercu.png',dpi=140); plt.close(fig)
print(json.dumps(report,ensure_ascii=False,indent=2))

# Normaliser les espaces générés par Matplotlib dans les chemins SVG.
for name in ['schema_cote.svg']:
    svg_path = ROOT / name
    svg_path.write_text("\n".join(line.rstrip() for line in svg_path.read_text().splitlines()) + "\n")
