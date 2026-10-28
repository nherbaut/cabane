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
positions={'A':(0,0),'B':(48+kerf,0),'R1':(54+2*kerf,0),
           'R2':(66+3*kerf,0),'C':(0,170+kerf),'R3':(55+kerf,170+kerf)}
pieces=[]
for name,(x,y) in positions.items():
    q=blanks[name]; a,b=q['width'],q['height']
    label=f'{name}\nBRUT {b:g} × {a:g} cm' if name in ('A','B','C') else f'{name}\nRéserve {b:g} × {a:g}'
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
ax.text(62.5,220,'CHUTES À CONSERVER\n\nR1–R3 : réserves seulement,\nprofondeur réelle du passage à mesurer.',ha='center',va='center')
ax.annotate('',xy=(0,-7),xytext=(w,-7),arrowprops={'arrowstyle':'<->'})
ax.text(w/2,-13,f'{w:g} cm',ha='center')
ax.annotate('',xy=(-7,0),xytext=(-7,h),arrowprops={'arrowstyle':'<->'})
ax.text(-12,h/2,f'{h:g} cm',ha='center',va='center',rotation=90)
ax.set_title('Préparation OSB proposé : 15 mm\nDimensions en cm — coupes brutes, pas cotes finales',pad=15)
ax.set_xlim(-20,w+5); ax.set_ylim(-22,h+5); ax.set_aspect('equal'); ax.axis('off')
fig.text(.5,.013,'A : côté T2–T3 ; B : côté T1 ; C : au-dessus du passage. Trait de scie supposé : 4 mm.',ha='center',fontsize=9)
for ext in ('pdf','svg','png'):
    fig.savefig(here/f'debit_preparatoire.{ext}',dpi=150)
print('Placement vérifié dans un panneau de 250 × 125 cm ; aucune superposition.')
