#!/usr/bin/env python3
"""Schéma coté des bruts OSB : vue éclatée et placement dans une feuille."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

here = Path(__file__).resolve().parent
data = json.loads((here.parents[1]/'donnees/geometrie.json').read_text())
p = data['site_progress_2026_10_28']['cladding_proposal']
pieces = {v['id']:v for v in p['rough_blanks']+p['lining_reserves']}
width = p['provisional_panel_purchase']['width']
height = p['provisional_panel_purchase']['height']
kerf = .4
colors = {'A':'#a2cbdc','B':'#a7cbb0','C':'#f2c38c',
          'R1':'#d9dce1','R2':'#d9dce1','R3':'#d9dce1'}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.fonttype':'none'})
def fr(value):return f'{value:g}'.replace('.',',')
fig = plt.figure(figsize=(15,10), facecolor='white')
fig.suptitle('Bardage : découpes de préparation à commander',fontsize=22,fontweight='bold',y=.97)
fig.text(.5,.919,'OSB de 15 mm proposé • Cotes en cm : hauteur × largeur',ha='center',fontsize=13)
fig.text(.5,.885,'Zones visées : 188 cm au-dessus de T1–T2 ; 170 cm entre T2 et T3.',ha='center',fontsize=12)
gs = fig.add_gridspec(1,2,left=.06,right=.97,bottom=.22,top=.81,wspace=.2)
left,right = fig.add_subplot(gs[0]),fig.add_subplot(gs[1])

def panel(ax, name, x, y, reserve=False):
    a,b=pieces[name]['width'],pieces[name]['height']
    ax.add_patch(Rectangle((x,y),a,b,facecolor=colors[name],edgecolor='#34454d',lw=1.3))
    label=name if a<15 else f'{name}\n{fr(b)} × {fr(a)}'
    ax.text(x+a/2,y+b/2,label,ha='center',va='center',fontsize=11 if not reserve else 9,
            rotation=90 if name in ['R1','R2'] else 0,fontweight='bold' if not reserve else 'normal')

def dim(ax,x1,y1,x2,y2,text,vertical=False):
    ax.annotate('',xy=(x1,y1),xytext=(x2,y2),arrowprops={'arrowstyle':'<->','lw':1.1})
    if vertical:
        ax.text(x1-3,(y1+y2)/2,text,ha='right',va='center',rotation=90)
    else:
        ax.text((x1+x2)/2,y1-5,text,ha='center',va='top')

left.set_title('1. Identifier les trois morceaux',fontsize=15,pad=18,fontweight='bold')
# Vue éclatée : dimensions des pièces exactes ; positions d'affichage sans
# correspondance avec les coordonnées de pose ou les limites réelles du passage.
panel(left,'B',0,0)
panel(left,'A',60,0)
panel(left,'C',0,183)
left.text(pieces['C']['width']/2,217,'C : au-dessus du passage',ha='center',fontsize=11)
left.text(33,80,'Passage\n\nEspacement\nschématique',ha='center',va='center',fontsize=11,color='#52616b')
left.text(84,-13,'A : entre T2 et T3',ha='center',fontsize=10)
left.annotate('B : côté T1',xy=(pieces['B']['width']/2,24),xytext=(18,10),fontsize=10,
              arrowprops={'arrowstyle':'-','color':'#52616b'})
dim(left,-8,0,-8,170,'170')
dim(left,0,176,pieces['C']['width'],176,fr(pieces['C']['width']))
left.set_xlim(-22,115);left.set_ylim(-27,232)
left.set_aspect('equal');left.axis('off')

right.set_title('2. Découper dans le panneau',fontsize=15,pad=18,fontweight='bold')
right.add_patch(Rectangle((0,0),width,height,facecolor='#f8f5ef',edgecolor='#34454d',lw=1.4))
positions={}; x=0
for name in ['A','B','R1','R2']:
    positions[name]=(x,0)
    x += pieces[name]['width']+kerf
positions['C']=(0,170+kerf)
positions['R3']=(pieces['C']['width']+kerf,170+kerf)
for name,(x,y) in positions.items():
    a,b=pieces[name]['width'],pieces[name]['height']
    assert x>=0 and y>=0 and x+a<=width and y+b<=height
    panel(right,name,x,y,reserve=name.startswith('R'))
for i,(n,(x,y)) in enumerate(positions.items()):
    a,b=pieces[n]['width'],pieces[n]['height']
    for m,(u,v) in list(positions.items())[i+1:]:
        c,d=pieces[m]['width'],pieces[m]['height']
        assert x+a<=u or u+c<=x or y+b<=v or v+d<=y
right.text(62.5,224,'CHUTES\nÀ CONSERVER',ha='center',va='center',fontsize=12,color='#52616b')
dim(right,0,-7,width,-7,f'{width:g}')
dim(right,-7,0,-7,height,f'{height:g}')
right.set_xlim(-23,width+5);right.set_ylim(-25,height+5)
right.set_aspect('equal');right.axis('off')

fig.text(.06,.158,'    '.join(f"{name} — {fr(pieces[name]['height'])} × {fr(pieces[name]['width'])} cm" for name in ('A','B','C')),fontsize=12,fontweight='bold')
fig.text(.06,.121,f"R1/R2 : 170 × {fr(pieces['R1']['width'])} cm ; R3 : 50 × {fr(pieces['R3']['height'])} cm. Profondeur nominale retenue après relevés T1/T2.",fontsize=11)
fig.text(.06,.080,'Longueurs à raccourcir après présentation ; petit décrochement de C à reporter et découper chez soi.',fontsize=11)
fig.text(.06,.050,'Atelier adapté aux bandes de 3,2 et 8,25 cm ; tolérance visée ±1 mm à confirmer. Trait de scie supposé : 4 mm.',fontsize=11)
for ext in ('png','svg','pdf'):
    fig.savefig(here/f'schema_decoupes.{ext}',dpi=160)
print('Schéma coté généré depuis les données ; réserves placées sans recouvrement.')

# Normaliser les espaces générés par Matplotlib dans les chemins SVG.
for name in ['schema_decoupes.svg']:
    svg_path = here / name
    svg_path.write_text("\n".join(line.rstrip() for line in svg_path.read_text().splitlines()) + "\n")
