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
lining_depth=depth+t
rail_data=state['floor_rail']; rail_h=p['rail_render_assumptions']['flange_height']
rail_s=p['rail_render_assumptions']['sheet_thickness']
rail_x0=-rail_data['cabin_flange_offset_from_stud_face']['nominal']
rail_x1=rail_x0+rail_data['outer_width_east_west']
gap=passage['T1_T2_clear_bottom']; second=passage['T2_T3_clear_bottom']
stud=passage['stud_face_width_reported']; floor=p['floor_gap']
under=passage['crosspiece_lower_face']; opening_top=under-t
top=passage['cabin_cladding_top_zones']['over_T1_T2']-p['top_gap_under_stair']
side_top=passage['cabin_cladding_top_zones']['between_T2_T3']
joint=.3  # Proposition graphique de joint, pas une cote de coupe actée.
y_left=-t; y_right=-gap+t; y_far=-(gap+stud+second+stud)
palette={'A':'#86b7d3','B':'#8cbc99','C':'#e7b276',
         'R1':'#ad96cd','R2':'#db9295','R3':'#e3c75f',
         'L':'#8c969f','LW':'#8c969f','V':'#48515a','P':'#9fb6c1'}
plaster_display=p['isometric_view']['plaster_display']
plaster_alpha=plaster_display['opacity']
plaster_t=plaster_display['thickness_assumption_cm']
plaster_crop=plaster_display['display_crop_height_cm']

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
front+=box('A',-t,0,y_far,-gap,floor,side_top)
front+=box('B',-t,0,0,stud,floor,under)
# Une encoche basse dans C permet ici de garder A rectangulaire. C'est
# seulement un exemple de raccord : largeur haute et contour restent à relever.
header=[(-gap+joint,under),(stud,under),(stud,top),
        (-gap-stud,top),(-gap-stud,side_top+joint),
        (-gap+joint,side_top+joint)]
front+=extrusion('C',header,-t,0)
returns=[]
returns+=box('R1',-t,depth,-t,0,floor,under)
returns+=box('R2',-t,depth,-gap,-gap+t,floor,under)
returns+=box('R3',-t,depth,y_right,y_left,opening_top,under)
assert np.isclose(lining_depth,7.5)
assert rail_x0 < -t and rail_x1 < depth

# Surface finie côté cellier : la profondeur mesurée situe cette face à x=6.
# Épaisseur supposée pour la visualisation, non mesurée. La face finie reste
# à x=6 : montrer l'épaisseur ne change pas la profondeur des retours.
# Le placo continue au-dessus de A. Le dessin est tronqué à 188 cm : ce bord
# n'est ni le contour sous les marches, encore inconnu, ni une ligne de coupe.
wall_outline=[(y_far,0),(-gap,0),(-gap,under),(0,under),(0,0),
              (stud,0),(stud,plaster_crop),(y_far,plaster_crop)]
wall=extrusion('P',wall_outline,depth-plaster_t,depth)

def make_rail(y0,y1):
    faces=box('L',rail_x0,rail_x1,y0,y1,0,rail_s)
    # Le fond reste continu. Les ailes ne sont dessinées que hors passage.
    for a,b in [(y0,min(y1,-gap)),(max(y0,0),y1)]:
        if a>=b:continue
        faces+=box('LW',rail_x0,rail_x0+rail_s,a,b,rail_s,rail_h)
        faces+=box('L',rail_x1-rail_s,rail_x1,a,b,rail_s,rail_h)
    return faces

rail=make_rail(y_far,stud)
screw=rail_data['screw_in_T1_T2_gap']
sx=rail_x0+screw['distance_from_cabin_rail_edge']; sy=-screw['distance_from_T1_passage_edge']
radius=max(screw['head_diameter_range'])/2
angles=np.linspace(0,2*np.pi,25)[:-1]
low=np.array([(sx+radius*np.cos(a),sy+radius*np.sin(a),rail_s) for a in angles])
high=low.copy();high[:,2]=screw['head_height_above_tile']
rail += [('V',low[::-1]),('V',high)]
for i in range(len(low)):
    j=(i+1)%len(low);rail.append(('V',np.array([low[i],low[j],high[j],high[i]])))

def draw(ax,faces,transparent_plaster=False):
    ground=np.array([[-12,y_far-6,0],[depth+9,y_far-6,0],
                     [depth+9,stud+8,0],[-12,stud+8,0]])
    ax.add_patch(Polygon(project(ground),facecolor='#f0eeea',edgecolor='#c7c6c3',lw=.6))
    for name,face in sorted(faces,key=lambda part:np.mean(part[1],axis=0)@EYE):
        n=np.cross(face[1]-face[0],face[2]-face[0]);n/=np.linalg.norm(n)
        # Eclairage déterministe pour distinguer les faces, sans texture métrique.
        shade=.70+.30*abs(n@np.array([-.35,-.45,.82]))
        rgb=np.array(colors.to_rgb(palette[name]))*shade
        is_ghost = name=='P' and transparent_plaster
        ax.add_patch(Polygon(project(face),facecolor=rgb,
            alpha=plaster_alpha if is_ghost else 1,
            edgecolor='#526d7b' if is_ghost else '#3e4b53',
            linestyle='--' if is_ghost else '-',
            lw=1.05 if is_ghost else .65,joinstyle='round'))
    # Le rebord ouest est devant le pied des panneaux depuis la cabane.
    # Son dessin final évite une occultation incorrecte par les grandes faces.
    if EYE[0]<0:
        for name,face in faces:
            if name=='LW':ax.add_patch(Polygon(project(face),facecolor=palette['LW'],edgecolor='#3e4b53',lw=.65))
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
bx.set_title('Façade masquée : retours et plâtre conservé',fontsize=14,pad=15)
draw(ax,rail+wall+returns+front,transparent_plaster=True)
draw(bx,rail+wall+returns,transparent_plaster=True)

# Repères directement sur les faces, puis légendes déportées.
for name,point in [('A',(-t,(y_far+y_right)/2,90)),('B',(-t,1,85)),
                   ('C',(-t,-22,179))]:
    x,y=project([point])[0];ax.text(x,y,name,ha='center',va='center',fontsize=18,fontweight='bold')
label(ax,(-t,-44.5,174),'Raccord A / C\nexemple à ajuster',(32,33))
label(ax,(depth,-73,181),'Plâtre conservé\nau-dessus de A\ncontour non relevé',(21,11))
ax.text(*project([(-t,-20,72)])[0],'Vers\nle cellier',ha='center',va='center',fontsize=12,color='#596773')
dimension(ax,(-t,stud,0),(-t,stud,188),'188\nlimite haute',(-13,0),(-7,0))
dimension(ax,(-t,y_far,0),(-t,y_far,side_top),'170 visés',(12,0),(7,0))

label(bx,(depth/2,-t/2,103),'R1 — côté T1',(-24,11),'right')
label(bx,(depth/2,-gap+t/2,87),'R2 — côté T2',(22,6))
label(bx,(depth/2,-22,under),'R3 — sous la traverse',(13,16))
label(bx,(depth,-72,120),'Plâtre conservé\ncôté cellier',(-28,30))
dimension(bx,(0,y_right,0),(0,y_left,0),'42 théoriques¹',(0,-9),(0,-6))
dimension(bx,(-t,-22,under),(depth,-22,under),'7,5 nominaux',(0,7),(0,5))
dimension(bx,(depth,-gap,0),(depth,-gap,opening_top),'165,3²',(16,0),(7,0))

# Fenêtres communes : les deux dessins gardent le même facteur d'échelle.
corners=project([[-t,stud,0],[-t,y_far,0],[0,stud,188],[0,y_far,188]])
ax.set_xlim(corners[:,0].min()-30,corners[:,0].max()+45)
ax.set_ylim(-58,181)
bx.set_xlim(-32,85);bx.set_ylim(-58,181)

legend=[Patch(facecolor=palette[k],edgecolor='#41535e',label=v) for k,v in
        [('A','A : entre T2 et T3'),('B','B : côté T1'),('C','C : au-dessus du passage'),
         ('R1','R1 : côté intérieur T1'),('R2','R2 : côté intérieur T2'),('R3','R3 : dessus intérieur')]]
legend.append(Patch(facecolor=palette['P'],edgecolor='#526d7b',alpha=plaster_alpha,
                    linestyle='--',label='Plâtre conservé (transparent)'))
fig.legend(handles=legend,loc='lower center',bbox_to_anchor=(.5,.175),ncol=4,frameon=False,fontsize=10)
notes=[
 'MESURES : cloison 6 cm ± 2 mm ; rail large de 7 cm, rebord côté cabane à 2 cm ± 2 mm devant les M48.',
 'HYPOTHÈSE : retours jusqu’à la face visible du bardage, soit 6 + 1,5 = 7,5 cm ; R3 entre les retours verticaux.',
 '¹ Largeur théorique : 45 − 1,5 − 1,5 = 42 cm, avant calage.  ² Sous-face proposée : 166,8 − 1,5 = 165,3 cm du carrelage.',
 'À MESURER : largeur haute, profil sous les marches sur A, jeux et raccords. T2 est corrigé par l’habillage, sans déplacer le métal.',
 'RAIL : fond et vis conservés ; ailes retirées dans le passage (proposition). Ailes hautes de 3 cm et tôle 0,6 mm : non mesurées.',
 'PLÂTRE : translucide, épaisseur supposée 1,25 cm ; dessin tronqué à 188 cm. Contour réel sous les marches à relever, sans nouvelle coupe.'
]
for i,text in enumerate(notes):fig.text(.045,.145-i*.026,text,fontsize=10,ha='left')
for ext in ('png','svg','pdf'):
    fig.savefig(HERE/f'isometrie_bardage_v1.{ext}',dpi=160)
print('Vue isométrique générée : profondeur mesurée 6 ± 0,2 cm ; épaisseur proposée 1,5 cm.')
plt.close(fig)

# Autre caméra : depuis le cellier, face est de la cloison. Le mur peint est
# un volume translucide d'épaisseur supposée. Les couvre-joints sont
# une proposition de finition, pas un détail de fixation validé.
U=np.array([1,1,0])/np.sqrt(2)
V=np.array([-1,1,2])/np.sqrt(6)
EYE=np.array([1,-1,1])/np.sqrt(3)
palette.update(J='#d6be92')
trim=[]
# Largeur 3 cm et épaisseur 0,6 cm purement illustratives.
trim+=box('J',depth,depth+.6,-t,t,floor,opening_top)
trim+=box('J',depth,depth+.6,-gap-t,-gap+t,floor,opening_top)
trim+=box('J',depth,depth+.6,y_right-2*t,y_left+2*t,opening_top,opening_top+3)
fig,ax=plt.subplots(figsize=(10,12))
fig.subplots_adjust(top=.84,bottom=.21,left=.09,right=.92)
fig.suptitle('Finition côté cellier — proposition',fontsize=21,fontweight='bold',y=.965)
fig.text(.5,.923,'Mur peint montré partiellement • Panneaux intérieurs • Couvre-joints proposés',ha='center',fontsize=12)
draw(ax,rail+returns+wall+trim,transparent_plaster=True)
label(ax,(depth+.6,-t/2,93),'Couvre-joint latéral\ncôté T1',(27,14))
label(ax,(depth+.6,-gap,62),'Couvre-joint latéral\ncôté T2',(-25,-4),'right')
label(ax,(depth+.6,-22,167),'Couvre-joint supérieur',(-12,25),'right')
label(ax,(depth,-72,126),'Plâtre peint',(-30,10),'right')
label(ax,(depth/2,-22,under),'R3 : panneau intérieur\nsous la traverse',(24,13))
ax.set_xlim(-100,65);ax.set_ylim(-56,180)
fig.legend(handles=[Patch(facecolor=palette['P'],edgecolor='#526d7b',alpha=plaster_alpha,
                         linestyle='--',label='Plâtre conservé transparent'),
                    Patch(facecolor=palette['J'],edgecolor='#41535e',label='Couvre-joints proposés'),
                    Patch(facecolor=palette['R1'],edgecolor='#41535e',label='Panneaux intérieurs')],
           loc='lower center',bbox_to_anchor=(.5,.14),frameon=False,ncol=1,fontsize=11)
for i,text in enumerate([
    'Les retours de 7,5 cm relient la face visible du bardage à la surface du plâtre côté cellier.',
    'Les baguettes recouvrent leur raccord avec le plâtre, sur les trois côtés du passage.',
    'Largeur 3 cm et épaisseur 0,6 cm des baguettes : hypothèses pour le dessin uniquement.',
    'Plâtre : épaisseur supposée 1,25 cm ; bord haut schématique à 188 cm, sans nouvelle coupe.'
]):fig.text(.07,.12-.027*i,text,fontsize=10)
for ext in ('png','svg','pdf'):fig.savefig(HERE/f'isometrie_cellier_v1.{ext}',dpi=160)
plt.close(fig)
print('Vue côté cellier générée avec couvre-joints illustratifs.')

# Détail du pied de T1 et plan du raccord B/R1 : les longueurs sont calculées
# depuis les mesures, et non lues sur une photographie ou une image générée.
U=np.array([1,-1,0])/np.sqrt(2);V=np.array([1,1,2])/np.sqrt(6);EYE=np.array([-1,-1,1])/np.sqrt(3)
fig,(ax,bx)=plt.subplots(1,2,figsize=(16,10))
fig.subplots_adjust(left=.06,right=.96,top=.82,bottom=.24,wspace=.28)
fig.suptitle('Rail au sol et raccord B / R1 — hypothèse à 7,5 cm',fontsize=21,fontweight='bold',y=.965)
fig.text(.5,.917,'Vue depuis la cabane • Mesures en cm • Schéma de compréhension',ha='center',fontsize=13)
zoom=make_rail(-10,stud)+[(name,face) for name,face in rail if name=='V']
zoom+=box('B',-t,0,0,stud,floor,15)
zoom+=box('R1',-t,depth,-t,0,floor,15)
zoom += box('P',depth-plaster_t,depth,0,stud,0,15)
draw(ax,zoom,transparent_plaster=True);ax.set_title('Pied de T1 : B, R1 et plâtre translucide',fontsize=14)
ax.set_xlim(-12,18);ax.set_ylim(-13,18)
label(ax,(-t,1.5,10),'B',(-4,3),'right')
label(ax,(3,-t,10),'R1',(5,3))
label(ax,(rail_x0,2,2),'Rebord conservé',(-5,-2),'right')
label(ax,(sx,sy,.3),'Vis conservée',(5,-3))
dimension(ax,(rail_x0,stud,3),(0,stud,3),'2 ± 0,2',(0,3),(0,1.4))

bx.set_title('Plan du raccord : les retours couvrent le bord de la façade',fontsize=13)
bx.add_patch(Polygon([(-t,0),(0,0),(0,stud),(-t,stud)],facecolor=palette['B'],edgecolor='#41535e'))
bx.add_patch(Polygon([(-t,-t),(depth,-t),(depth,0),(-t,0)],facecolor=palette['R1'],edgecolor='#41535e'))
bx.add_patch(Polygon([(depth-plaster_t,0),(depth,0),(depth,stud),(depth-plaster_t,stud)],
                    facecolor=palette['P'],edgecolor='#526d7b',alpha=plaster_alpha,linestyle='--'))
bx.plot([0,0],[-3,4],ls=':',color='#41535e',lw=1)
bx.plot([depth,depth],[-3,4],ls=':',color='#41535e',lw=1)
bx.plot([rail_x0,rail_x0],[-2.3,3.8],ls='--',color='#8c969f',lw=1.6)
bx.plot([rail_x1,rail_x1],[-2.3,3.8],ls='--',color='#8c969f',lw=1.6)
bx.text(-.75,1.7,'B',ha='center',fontsize=16,fontweight='bold')
bx.text(2.4,-.75,'R1',ha='center',fontsize=16,fontweight='bold')
for a,b,y,labeltext in [(-t,0,4.3,'1,5'),(0,depth,4.3,'6 mesurés'),(-t,depth,-2.8,'7,5 nominaux')]:
    bx.annotate('',xy=(a,y),xytext=(b,y),arrowprops={'arrowstyle':'<->','lw':1})
    bx.text((a+b)/2,y+.18,labeltext,ha='center',va='bottom',fontsize=11)
bx.annotate('Face M48',xy=(0,3.7),xytext=(1.6,3.5),fontsize=10,arrowprops={'arrowstyle':'-'})
bx.annotate('Face finie du plâtre\ncôté cellier',xy=(depth,1),xytext=(7.1,1.5),ha='left',fontsize=10,arrowprops={'arrowstyle':'-'})
bx.annotate('Rebord du rail\n(projeté au sol)',xy=(rail_x0,1),xytext=(-5,1),ha='left',fontsize=10,arrowprops={'arrowstyle':'-'})
bx.text(1.8,-4.4,'← CABANE                         CELLIER →',ha='center',fontsize=11)
bx.set_xlim(-5.2,11);bx.set_ylim(-5,5.7);bx.set_aspect('equal');bx.axis('off')
for i,text in enumerate([
    'FAITS : profondeur M48 → plâtre 6 ± 0,2 cm ; rebord rail → M48 2 ± 0,2 cm ; rail large de 7 cm.',
    'HYPOTHÈSE : OSB 1,5 cm ; retours jusqu’à la face visible du bardage : 6 + 1,5 = 7,5 cm nominaux.',
    'DANS LE RAIL : l’OSB laisse 0,5 cm de marge nominale, soit 3 à 7 mm avec la variation annoncée.',
    'NON MESURÉS : ailes hautes de 3 cm, tôle de 0,6 mm et plâtre de 1,25 cm représentés par hypothèse. Seuil non dessiné.',
    'Le rebord reste visible devant le pied de B/A : finition basse à définir. Ailes retirées uniquement dans le passage : proposition.',
    'Ce dessin ne valide ni les coupes finales ni les fixations. Aucun retrait de métal sous les montants n’est prescrit.'
]):fig.text(.045,.184-.027*i,text,fontsize=10)
for ext in ('png','svg','pdf'):fig.savefig(HERE/f'detail_rail_raccord_v2.{ext}',dpi=160)
plt.close(fig)

# Normaliser les espaces générés par Matplotlib dans les chemins SVG.
for name in ['isometrie_bardage_v1.svg', 'isometrie_cellier_v1.svg','detail_rail_raccord_v2.svg']:
    svg_path = HERE / name
    svg_path.write_text("\n".join(line.rstrip() for line in svg_path.read_text().splitlines()) + "\n")
