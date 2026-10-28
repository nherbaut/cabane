#!/usr/bin/env python3
"""Projection isométrique orthographique, données en cm. Aucun rendu IA."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Patch
from matplotlib import colors

HERE=Path(__file__).resolve().parent
data=json.loads((HERE.parents[1]/'donnees/geometrie.json').read_text())
state=data['site_progress_2026_10_28']
p=state['cladding_proposal']; passage=state['passage']
t=p['osb_thickness']; depth=passage['lining_depth']['nominal']
gap=passage['T1_T2_clear_bottom']; second=passage['T2_T3_clear_bottom']
stud=passage['stud_face_width_reported']; floor=p['floor_gap']
under=passage['crosspiece_lower_face']; opening_top=under-t
top=passage['cabin_cladding_top_zones']['over_T1_T2']-p['top_gap_under_stair']
side_top=passage['cabin_cladding_top_zones']['between_T2_T3']
joint=.3  # Proposition graphique de joint, pas une cote de coupe actée.
y_left=-t; y_right=-gap+t; y_far=-(gap+stud+second+stud)
palette={'A':'#86b7d3','B':'#8cbc99','C':'#e7b276',
         'R1':'#ad96cd','R2':'#db9295','R3':'#e3c75f'}

# Repère local translaté : x est, y nord, z haut ; origine au pied de la
# face de T1 donnant dans le passage. Aucune coordonnée globale n'est déduite.
# Caméra depuis l'ouest (cabane), légèrement au sud et en hauteur.
# Les projections des trois axes ont le même facteur d'échelle : vraie iso.
U=np.array([1,-1,0])/np.sqrt(2)
V=np.array([1,1,2])/np.sqrt(6)
EYE=np.array([-1,-1,1])/np.sqrt(3)
assert np.allclose([np.linalg.norm([U[i],V[i]]) for i in range(3)],np.sqrt(2/3))

def project(points):
    q=np.array(points,dtype=float)
    return np.stack([q@U,q@V],axis=-1)

def extrusion(name, polygon_yz, x0, x1):
    pts=np.array(polygon_yz,float)
    assert len(pts)>=4 and x0<x1
    a=np.column_stack([np.full(len(pts),x0),pts])
    b=np.column_stack([np.full(len(pts),x1),pts])
    surfaces=[a,b[::-1]]
    for i in range(len(pts)):
        j=(i+1)%len(pts);surfaces.append(np.array([a[i],a[j],b[j],b[i]]))
    return [(name,surface) for surface in surfaces]

def box(name,x0,x1,y0,y1,z0,z1):
    assert y0<y1 and z0<z1
    return extrusion(name,[(y0,z0),(y1,z0),(y1,z1),(y0,z1)],x0,x1)

front=[]
front+=box('A',-t,0,y_far,y_right,floor,side_top)
front+=box('B',-t,0,y_left,stud,floor,opening_top-joint)
# Une encoche basse dans C permet ici de garder A rectangulaire. C'est
# seulement un exemple de raccord : largeur haute et contour restent à relever.
header=[(y_right+joint,opening_top),(stud,opening_top),(stud,top),
        (-gap-stud,top),(-gap-stud,side_top+joint),
        (y_right+joint,side_top+joint)]
front+=extrusion('C',header,-t,0)
returns=[]
returns+=box('R1',0,depth,-t,0,floor,opening_top)
returns+=box('R2',0,depth,-gap,-gap+t,floor,opening_top)
returns+=box('R3',0,depth,y_right,y_left,opening_top,under)

def draw(ax,faces):
    ground=np.array([[-12,y_far-6,0],[depth+9,y_far-6,0],
                     [depth+9,stud+8,0],[-12,stud+8,0]])
    ax.add_patch(Polygon(project(ground),facecolor='#f0eeea',edgecolor='#c7c6c3',lw=.6))
    for name,face in sorted(faces,key=lambda part:np.mean(part[1],axis=0)@EYE):
        n=np.cross(face[1]-face[0],face[2]-face[0]);n/=np.linalg.norm(n)
        # Eclairage déterministe pour distinguer les faces, sans texture métrique.
        shade=.70+.30*abs(n@np.array([-.35,-.45,.82]))
        rgb=np.array(colors.to_rgb(palette[name]))*shade
        ax.add_patch(Polygon(project(face),facecolor=rgb,edgecolor='#3e4b53',lw=.65,joinstyle='round'))
    ax.set_aspect('equal');ax.axis('off')

def label(ax,point,text,offset,align='left'):
    xy=project([point])[0]
    ax.annotate(text,xy=xy,xytext=xy+np.array(offset),ha=align,va='center',fontsize=11,
                bbox={'boxstyle':'round,pad=.35','fc':'white','ec':'#c4cbd0','alpha':.96},
                arrowprops={'arrowstyle':'-','color':'#41535e','lw':1})

def dimension(ax,a,b,text,offset,text_offset=(0,0),rotation=0):
    xy=project([a,b]);o=np.array(offset)
    for q in xy: ax.plot([q[0],q[0]+o[0]],[q[1],q[1]+o[1]],color='#667680',lw=.65)
    ax.annotate('',xy=xy[0]+o,xytext=xy[1]+o,arrowprops={'arrowstyle':'<->','lw':1,'color':'#41535e'})
    q=xy.mean(axis=0)+o+np.array(text_offset)
    ax.text(*q,text,ha='center',va='center',rotation=rotation,fontsize=10,
            bbox={'facecolor':'white','edgecolor':'none','pad':2})

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'svg.fonttype':'none'})
fig,(ax,bx)=plt.subplots(1,2,figsize=(16,12))
fig.subplots_adjust(left=.04,right=.97,top=.85,bottom=.24,wspace=.18)
fig.suptitle('Bardage et habillage du passage — vue depuis la cabane',fontsize=21,fontweight='bold',y=.965)
fig.text(.5,.922,'Projection isométrique • Cotes en cm • OSB de 1,5 cm proposé',ha='center',fontsize=13)
ax.set_title('Vue assemblée : bardage A / B / C',fontsize=15,pad=15)
bx.set_title('Intérieur du passage : façade masquée',fontsize=15,pad=15)
draw(ax,returns+front)
draw(bx,returns)

# Repères directement sur les faces, puis légendes déportées.
for name,point in [('A',(-t,(y_far+y_right)/2,90)),('B',(-t,1,85)),
                   ('C',(-t,-22,179))]:
    x,y=project([point])[0];ax.text(x,y,name,ha='center',va='center',fontsize=18,fontweight='bold')
label(ax,(-t,-44.5,174),'Raccord A / C\nexemple à ajuster',(32,33))
ax.text(*project([(-t,-20,72)])[0],'Vers\nle cellier',ha='center',va='center',fontsize=12,color='#596773')
dimension(ax,(-t,stud,0),(-t,stud,188),'188\nlimite haute',(-13,0),(-7,0))
dimension(ax,(-t,y_far,0),(-t,y_far,side_top),'170',(12,0),(7,0))

label(bx,(depth/2,-t/2,103),'R1 — côté T1',(-24,11),'right')
label(bx,(depth/2,-gap+t/2,87),'R2 — côté T2',(22,6))
label(bx,(depth/2,-22,under),'R3 — sous la traverse',(13,16))
dimension(bx,(0,y_right,0),(0,y_left,0),'42 théoriques¹',(0,-9),(0,-6))
dimension(bx,(0,-22,under),(depth,-22,under),'6 ± 0,2',(0,7),(0,5))
dimension(bx,(depth,-gap,0),(depth,-gap,opening_top),'165,3²',(16,0),(7,0))

# Fenêtres communes : les deux dessins gardent le même facteur d'échelle.
corners=project([[-t,stud,0],[-t,y_far,0],[0,stud,188],[0,y_far,188]])
ax.set_xlim(corners[:,0].min()-30,corners[:,0].max()+45)
ax.set_ylim(-58,181)
bx.set_xlim(-32,85);bx.set_ylim(-58,181)

legend=[Patch(facecolor=palette[k],edgecolor='#41535e',label=v) for k,v in
        [('A','A : entre T2 et T3'),('B','B : côté T1'),('C','C : au-dessus du passage'),
         ('R1','R1 : côté intérieur T1'),('R2','R2 : côté intérieur T2'),('R3','R3 : dessus intérieur')]]
fig.legend(handles=legend,loc='lower center',bbox_to_anchor=(.5,.175),ncol=3,frameon=False,fontsize=11)
notes=[
 'MESURES : profondeur 6 cm ± 2 mm, avant ajout de la façade ; limite haute 188 cm sur T1–T2 et 170 cm sur T2–T3.',
 'PROPOSITIONS : panneaux de 1,5 cm ; jeu au sol de 1 cm ; 3 mm sous l’escalier ; raccord à décrochement dans C.',
 '¹ Largeur théorique : 45 − 1,5 − 1,5 = 42 cm, avant calage.  ² Sous-face proposée : 166,8 − 1,5 = 165,3 cm du carrelage.',
 'À MESURER : largeur haute à 188 cm, jeux et contours de raccord. T2 est représenté corrigé par l’habillage, sans déplacer le métal.',
 'Schéma de compréhension, pas un gabarit de coupe. Escalier, fixations et seuil non représentés ; aucun élément structurel à modifier.'
]
for i,text in enumerate(notes):fig.text(.045,.145-i*.026,text,fontsize=10,ha='left')
for ext in ('png','svg','pdf'):
    fig.savefig(HERE/f'isometrie_bardage_v1.{ext}',dpi=160)
print('Vue isométrique générée : profondeur mesurée 6 ± 0,2 cm ; épaisseur proposée 1,5 cm.')
plt.close(fig)

# Autre caméra : depuis le cellier, face est de la cloison. Le mur peint est
# une surface schématique sans épaisseur supposée. Les couvre-joints sont
# une proposition de finition, pas un détail de fixation validé.
U=np.array([1,1,0])/np.sqrt(2)
V=np.array([-1,1,2])/np.sqrt(6)
EYE=np.array([1,-1,1])/np.sqrt(3)
palette.update(P='#e3dfd6',J='#d6be92')
wall=[('P',np.array([(depth,y_far,0),(depth,-gap,0),(depth,-gap,170),(depth,y_far,170)])),
      ('P',np.array([(depth,0,0),(depth,stud,0),(depth,stud,188),(depth,0,188)])),
      ('P',np.array([(depth,-gap,under),(depth,0,under),(depth,0,188),(depth,-gap,188)]))]
trim=[]
# Largeur 3 cm et épaisseur 0,6 cm purement illustratives.
trim+=box('J',depth,depth+.6,-t,t,floor,opening_top)
trim+=box('J',depth,depth+.6,-gap-t,-gap+t,floor,opening_top)
trim+=box('J',depth,depth+.6,y_right-2*t,y_left+2*t,opening_top,opening_top+3)
fig,ax=plt.subplots(figsize=(10,12))
fig.subplots_adjust(top=.84,bottom=.21,left=.09,right=.92)
fig.suptitle('Finition côté cellier — proposition',fontsize=21,fontweight='bold',y=.965)
fig.text(.5,.923,'Mur peint montré partiellement • Panneaux intérieurs • Couvre-joints proposés',ha='center',fontsize=12)
draw(ax,returns+wall+trim)
label(ax,(depth+.6,-t/2,93),'Couvre-joint latéral\ncôté T1',(27,14))
label(ax,(depth+.6,-gap,62),'Couvre-joint latéral\ncôté T2',(-25,-4),'right')
label(ax,(depth+.6,-22,167),'Couvre-joint supérieur',(-12,25),'right')
label(ax,(depth,-72,126),'Plâtre peint',(-30,10),'right')
label(ax,(depth/2,-22,under),'R3 : panneau intérieur\nsous la traverse',(24,13))
ax.set_xlim(-100,65);ax.set_ylim(-56,180)
fig.legend(handles=[Patch(facecolor=palette['P'],edgecolor='#41535e',label='Plâtre côté cellier'),
                    Patch(facecolor=palette['J'],edgecolor='#41535e',label='Couvre-joints proposés'),
                    Patch(facecolor=palette['R1'],edgecolor='#41535e',label='Panneaux intérieurs')],
           loc='lower center',bbox_to_anchor=(.5,.14),frameon=False,ncol=1,fontsize=11)
for i,text in enumerate([
    'Les retours de 6 cm arrivent au niveau de la surface du plâtre côté cellier.',
    'Les baguettes recouvrent leur raccord avec le plâtre, sur les trois côtés du passage.',
    'Largeur 3 cm et épaisseur 0,6 cm des baguettes : hypothèses pour le dessin uniquement.',
    'Baguettes à ajuster ; le contour partiel du mur ne prescrit aucune coupe du plâtre.'
]):fig.text(.07,.12-.027*i,text,fontsize=10)
for ext in ('png','svg','pdf'):fig.savefig(HERE/f'isometrie_cellier_v1.{ext}',dpi=160)
plt.close(fig)
print('Vue côté cellier générée avec couvre-joints illustratifs.')

# Normaliser les espaces générés par Matplotlib dans les chemins SVG.
for name in ['isometrie_bardage_v1.svg', 'isometrie_cellier_v1.svg']:
    svg_path = HERE / name
    svg_path.write_text("\n".join(line.rstrip() for line in svg_path.read_text().splitlines()) + "\n")
