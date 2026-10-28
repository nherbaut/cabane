#!/usr/bin/env python3
"""Plan de préparation matière en cm, pas un plan de pose."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

here = Path(__file__).resolve().parent
data = json.loads((here.parents[1]/'donnees/geometrie.json').read_text())
p = data['site_progress_2026_10_28']['cladding_proposal']
sheet = p['provisional_panel_purchase']
w, h = sheet['width'], sheet['height']
kerf = .4
blanks={v['id']:v for v in p['rough_blanks']+p['lining_reserves']}
positions={}; next_x=0
for name in ['A','B','R1','R2']:
    positions[name]=(next_x,0)
    next_x+=blanks[name]['width']+kerf
positions.update(C=(0,170+kerf),R3=(55+kerf,170+kerf))
pieces=[]
for name,(x,y) in positions.items():
    q=blanks[name]; a,b=q['width'],q['height']
    label=name if a<=6 else (f'{name}\nEnveloppe {b:g} × {a:g} cm' if name in ('A','B','C') else f'{name} : {b:g} × {a:g}')
    pieces.append((label,x,y,a,b,'#9fc6ca' if name in ('A','B','C') else '#f1d099'))
for _,x,y,a,b,_ in pieces:
    assert 0 <= x and 0 <= y and x+a <= w and y+b <= h
for i,(_,x,y,a,b,_) in enumerate(pieces):
    for _,u,v,c,d,_ in pieces[i+1:]:
        assert x+a <= u or u+c <= x or y+b <= v or v+d <= y

plt.rcParams.update({'svg.fonttype':'none','font.size':10})
fig,ax=plt.subplots(figsize=(8.27,11.69),layout='constrained')
ax.add_patch(Rectangle((0,0),w,h,facecolor='#f7f3eb',edgecolor='black'))
for label,x,y,a,b,color in pieces:
    ax.add_patch(Rectangle((x,y),a,b,facecolor=color,edgecolor='#35454a'))
    ax.text(x+a/2,y+b/2,label,ha='center',va='center',rotation=90 if a<=12 else 0)
ax.text(62.5,220,'CHUTES À CONSERVER\n\nR1/R2 : 170 × 6 cm\nR3 : 50 × 6 cm\nLongueurs à raccourcir.',ha='center',va='center')
ax.annotate('',xy=(0,-7),xytext=(w,-7),arrowprops={'arrowstyle':'<->'})
ax.text(w/2,-13,f'{w:g} cm',ha='center')
ax.annotate('',xy=(-7,0),xytext=(-7,h),arrowprops={'arrowstyle':'<->'})
ax.text(-12,h/2,f'{h:g} cm',ha='center',va='center',rotation=90)
ax.set_title('OSB proposé : 15 mm — dimensions en cm\nA/B/C : enveloppes ; R1/R2/R3 : bandes de 6 cm',pad=15)
ax.set_xlim(-20,w+5); ax.set_ylim(-22,h+5); ax.set_aspect('equal'); ax.axis('off')
fig.text(.5,.013,'A/B/C : relever les largeurs finales avant coupe en magasin. Trait de scie supposé : 4 mm.',ha='center',fontsize=9)
for ext in ('pdf','svg','png'):
    fig.savefig(here/f'debit_preparatoire.{ext}',dpi=150)
print('Placement vérifié dans un panneau de 250 × 125 cm ; aucune superposition.')

# Normaliser les espaces générés par Matplotlib dans les chemins SVG.
for name in ['debit_preparatoire.svg']:
    svg_path = here / name
    svg_path.write_text("\n".join(line.rstrip() for line in svg_path.read_text().splitlines()) + "\n")
