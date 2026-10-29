#!/usr/bin/env python3
"""Préparation magasin + scie manuelle, calculée en cm depuis la géométrie."""
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
proposal = json.loads((ROOT / 'donnees/geometrie.json').read_text())[
    'site_progress_2026_10_28']['cladding_proposal']
v = proposal['leroy_merlin_home_variant']
store = {p['id']: p for p in v['store_pieces']}
blanks = {p['id']: p for p in proposal['rough_blanks'] + proposal['lining_reserves']}
W, H = v['sheet']['width'], v['sheet']['height']
k = v['store_kerf_for_drawing']
L = store['P']['length']
top_h = H - L - k
bottom_waste = W - store['A']['width'] - store['P']['width'] - 2*k
top_right_width = W - store['C']['width'] - k
split_width = (top_right_width-k)/2

# Six coupes droites successives : trois morceaux utiles et quatre chutes.
pieces = [
    ('A', 0, 0, store['A']['width'], L),
    ('P', store['A']['width']+k, 0, store['P']['width'], L),
    ('S1', store['A']['width']+store['P']['width']+2*k, 0, bottom_waste, L),
    ('C', 0, L+k, store['C']['width'], store['C']['length']),
    ('S2', 0, L+store['C']['length']+2*k,
     store['C']['width'], top_h-store['C']['length']-k),
    ('S3', store['C']['width']+k, L+k, split_width, top_h),
    ('S4', store['C']['width']+split_width+2*k, L+k, split_width, top_h),
]

def accepts(a, b):
    small, large = sorted((a, b))
    return (small >= 20 and large >= 20) or (small >= 10 and large >= 60)

for name, x, y, w, h in pieces:
    assert min(w, h) > 0 and x >= 0 and y >= 0
    assert x+w <= W+1e-8 and y+h <= H+1e-8
    assert accepts(w, h), f'Format hors limites Leroy Merlin : {name}'
    assert max(w, h) <= v['transport']['largest_piece_length']+1e-8
    assert min(w, h) <= v['transport']['largest_piece_width']+1e-8
for i, (_, x, y, w, h) in enumerate(pieces):
    for _, u, t, a, b in pieces[i+1:]:
        assert x+w <= u+1e-8 or u+a <= x+1e-8 or y+h <= t+1e-8 or t+b <= y+1e-8
assert len(pieces) == v['store_remainders_transport']['all_piece_count']
assert len(pieces)*v['thickness'] == v['store_remainders_transport']['stack_thickness_nominal']
for key in ('A', 'C'):
    assert store[key]['length'] == blanks[key]['height']
    assert store[key]['width'] == blanks[key]['width']

# À domicile : on retrace depuis le bord restant après chaque coupe.
kh = v['parent_P']['manual_kerf_for_drawing']
offset = 0
strips = []
for key in ('R1', 'R2', 'B'):
    w = blanks[key]['width']
    assert blanks[key]['height'] == L
    strips.append((key, offset, 0, w, L))
    offset += w+kh
remainder = store['P']['width']-offset
assert remainder > blanks['R3']['height']+kh
assert L >= blanks['R3']['width']
strips.append(('R3', offset, 0, blanks['R3']['height'], blanks['R3']['width']))
assert 3*L+blanks['R3']['width'] == v['parent_P']['manual_total_rip_length']

def fr(value):
    return f'{value:g}'.replace('.', ',')

plt.rcParams.update({'svg.fonttype': 'none', 'font.size': 10})
fig, axes = plt.subplots(1, 2, figsize=(11.69, 8.27))
fig.subplots_adjust(left=.04, right=.98, bottom=.15, top=.84, wspace=.17)
fig.suptitle('Variante : Leroy Merlin puis scie manuelle à la maison', fontsize=17, y=.97)
fig.text(.5, .92, 'Panneau de 15 mm · cotes en cm · matériau et transport à confirmer', ha='center', fontsize=11)
colors = {'A':'#9fc6ca', 'C':'#9fc6ca', 'P':'#f0cc8e',
          'R1':'#e7c89a', 'R2':'#b5d2bf', 'B':'#9fc6ca', 'R3':'#d8bedb'}
ax = axes[0]
for name, x, y, w, h in pieces:
    ax.add_patch(Rectangle((x, y), w, h, fc=colors.get(name, '#eeeeea'), ec='#34464c', lw=1))
    label = f'{name}\n{fr(h)} × {fr(w)}'
    ax.text(x+w/2, y+h/2, label, ha='center', va='center', fontsize=9)
ax.set_title(f'1. En magasin : panneau {fr(H)} × {fr(W)}\nA, C et P utiles ; S1–S4 = chutes', pad=16)
ax.set_xlim(-4, W+4); ax.set_ylim(H+5, -5)
ax.set_aspect('equal'); ax.axis('off')
ax = axes[1]
pw = store['P']['width']
ax.add_patch(Rectangle((0,0), pw,L,fc='#eeeeea',ec='#34464c'))
for name, x, y, w, h in strips:
    ax.add_patch(Rectangle((x,y),w,h,fc=colors[name],ec='#34464c'))
    ax.text(x+w/2,y+h/2,f'{name} : {fr(h)} × {fr(w)}',ha='center',va='center',rotation=90,fontsize=10)
ax.plot([offset,pw],[blanks['R3']['width']]*2,'--',color='#34464c')
ax.text(offset+remainder/2,120,'Reste\nà conserver',rotation=90,ha='center',va='center',fontsize=9)
for i,(_,x,_,w,_) in enumerate(strips[:3],1):
    ax.text(x+w/2,-7,str(i),ha='center',weight='bold')
ax.annotate('',xy=(0,-15),xytext=(pw,-15),arrowprops={'arrowstyle':'<->'})
ax.text(pw/2,-19,f'{fr(pw)} cm',ha='center')
ax.set_title(f'2. Chez vous : planche P {fr(L)} × {fr(pw)}\nTrois coupes de {fr(L)} cm, puis R3 sur 50 cm',pad=16)
ax.set_xlim(-8, pw+8); ax.set_ylim(L+5,-24)
ax.set_aspect('equal'); ax.axis('off')
fig.text(.5,.105,'Transport à vérifier : gabarit conseillé 171 × 54 cm, coffre fermé. Aucun raccord ajouté aux pièces longues.',ha='center',fontsize=10)
fig.text(.5,.065,'Magasin : trait illustré 4 mm, tolérance annoncée ±3 mm. Maison : tracer chaque bande après la coupe précédente.',ha='center',fontsize=9)
fig.text(.5,.03,'A et C : contrôler les largeurs au retrait. Les longueurs et le petit contour de C restent à ajuster après présentation.',ha='center',fontsize=9)
for ext in ('png','svg','pdf'):
    fig.savefig(HERE/f'schema_leroy_maison.{ext}',dpi=160)
svg=HERE/'schema_leroy_maison.svg'
svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')

rows='\n'.join(f'| **{key}** | 1 | **{fr(p["length"])} × {fr(p["width"])} cm** | '
               + {'A':'Façade T2–T3','C':'Haut du passage','P':'Planche à recouper pour B et R1–R3'}[key]+' |'
               for key,p in store.items())
chutes=' ; '.join(f'{name} : {fr(h)} × {fr(w)}' for name,_,_,w,h in pieces if name.startswith('S'))
document=f'''---
title: "Découpes Leroy Merlin + scie à la maison"
date: "29 octobre 2026"
lang: fr-FR
---

## Hypothèse et matière

Variante demandée : faire les grandes découpes au magasin, puis les bandes
étroites avec votre scie japonaise. Épaisseur conservée : **1,5 cm**.
Le panneau n’est pas acheté : OSB/3[^osb] initialement proposé, ou
contreplaqué[^cp] tout peuplier A+ si une référence est trouvée.
**Le contreplaqué vu chez Leroy Merlin est classé A, pas A+**, selon votre
relevé ; aucun contreplaqué A+ de ce magasin n’est confirmé.
Le placement utilise ici un panneau de **{fr(H)} × {fr(W)} cm** ; un autre
format doit être recalculé avant commande.

## À commander au magasin — trois morceaux utiles

| Repère | Quantité | Longueur × largeur | Destination |
|:--|--:|:--|:--|
{rows}

Ces trois formats respectent les minimums publiés : **20 × 20 cm ou
60 × 10 cm**. Leroy Merlin annonce **±3 mm** : mesurer A et C au retrait,
car cette tolérance peut consommer les jeux proposés de 3 mm au mur/bois.
Une reprise peut rester nécessaire ; demander un contrôle avant départ.
Ne pas demander directement B à 3,2 cm ou les retours[^retour] à 8,25 cm.

**Pour transporter toutes les chutes[^chute] :** demander aussi de partager
en deux le bloc large restant au-dessus de A/P, comme sur le schéma.
Avec une perte de lame[^trait] de 0,4 cm, cela donne : **{chutes} cm**.
Leurs dimensions sont indicatives : l’opérateur adapte aux pertes réelles.
Tous ces restes dépassent également les minimums de coupe.
Le schéma correspond à **six coupes droites au total**, à confirmer par
l’opérateur ; aucun tarif total n’est déduit du nombre de coupes.

## Transport : mesure encore manquante

La voiture et ses dimensions utiles ne sont pas connues. Les morceaux
utiles s’inscrivent, empilés et orientés, dans **170 × 52,4 cm** ; il faut
**4,5 cm d’épaisseur** pour les trois. Avec les quatre chutes fractionnées,
compter **sept morceaux, soit 10,5 cm d’épaisseur de bois**, hors protection.
Tester un carton de **171 × 54 cm** : ouverture du coffre, chemin de chargement,
place disponible avec les sièges rabattus et coffre fermé. Cette marge ne
constitue pas une validation pour votre véhicule. Arrimer les morceaux.
Si les chutes ne sont pas souhaitées, demander si le magasin accepte de
les conserver ; ne pas supposer ce service acquis. Si 170 cm ne rentre pas,
**ne pas couper les grandes pièces en deux sans revoir les raccords et leurs appuis**.

\\newpage

## Chez vous : découper P, étape par étape

![À gauche, découpe du panneau en magasin ; à droite, bandes prises dans P.](schema_leroy_maison.png){{ width=100% }}

1. Sur P **170 × 30 cm**, tracer **R1 de 8,25 cm de large** depuis un bord
   droit. Scier sur les 170 cm, du côté du bois à écarter, sans retirer le trait utile.
2. Depuis le nouveau bord droit de la planche restante, retracer **R2 à 8,25 cm**,
   puis scier sur 170 cm. Ne pas cumuler les cotes sans tenir compte de la lame.
3. Depuis le bord restant, tracer **B à 3,2 cm**, puis scier sur 170 cm.
4. Dans ce qui reste, prélever un morceau de **50 cm de long**, puis le recouper
   à **8,25 cm de large** pour R3. La partie de 50 cm est une réserve : sa
   longueur finale sera mesurée entre les deux retours présentés.

Il reste donc **trois coupes longues de 170 cm et une de 50 cm**, soit environ
**5,6 m de sciage dans la longueur**, plus les coupes en travers et les
ajustements. Cette variante évite une machine à acheter, mais reste un travail
manuel conséquent. Les quatre pièces longues restent d’un seul tenant.

## Présentation, ajustements et sécurité

Raccourcir A/B/R1/R2 selon leur position réelle ; vérifier les marches sur
toute la largeur de A. Ajuster la hauteur et le petit contour en angle de C.
Le dessous de la traverse[^traverse] posée est à **166,8 cm** ; les hauteurs
170/24 cm sont des réserves, pas toutes des hauteurs finies.

Utiliser une table stable, les deux serre-joints[^serrejoint] et un trait
de crayon sur toute la longueur. Maintenir le morceau conservé, dégager le
trajet de la scie de la table et de toute pièce métallique, et repositionner
le panneau après arrêt de la coupe si nécessaire. Soutenir la bande en fin
de coupe sans refermer le passage de la lame. Faire un essai sur une chute
avant les bandes utiles et poncer les bords. Cette fiche ne valide pas la
stabilité d’une installation de sciage non observée.

Source : [service officiel Leroy Merlin](https://www.leroymerlin.fr/services/decoupe/decoupe-du-bois.html),
consulté le 29 octobre 2026. Les dimensions proviennent de `donnees/geometrie.json`.

[^osb]: **OSB** : panneau de grandes lamelles de bois collées.
[^cp]: **Contreplaqué** : panneau formé de fines feuilles de bois collées en couches croisées.
[^retour]: **Retour** : panneau couvrant l’épaisseur de la cloison à l’intérieur du passage.
[^chute]: **Chute** : morceau restant après découpe.
[^trait]: **Perte de lame** : largeur de bois retirée lors du sciage.
[^traverse]: **Traverse** : bois horizontal placé au-dessus du passage.
[^serrejoint]: **Serre-joint** : outil maintenant fermement le bois contre la table.
'''
(HERE/'variante_leroy_maison.md').write_text(document)
print(f'Variante vérifiée : {len(pieces)} morceaux sans chevauchement, tous compatibles avec les minimums du magasin.')
print(f'P : R1/R2/B continus + R3, largeur restante après les trois bandes : {fr(remainder)} cm (hypothèse de lame).')
