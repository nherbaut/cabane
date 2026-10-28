#!/usr/bin/env python3
"""Projection isométrique orthographique, données en cm. Aucun rendu IA."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Patch, PathPatch
from matplotlib.path import Path as PlotPath
from matplotlib import colors
from shapely.geometry import Polygon as ShapePolygon
from shapely.geometry.polygon import orient

HERE=Path(__file__).resolve().parent
data=json.loads((HERE.parents[1]/'donnees/geometrie.json').read_text())
state=data['site_progress_2026_10_28']
p=state['cladding_proposal']; passage=state['passage']
t=p['osb_thickness']; measured_depth=passage['lining_depth']['nominal']
rail_data=state['floor_rail']; rail_h=p['rail_render_assumptions']['flange_height']
rail_s=p['rail_render_assumptions']['sheet_thickness']
rail_x0=-rail_data['cabin_flange_offset_from_stud_face']['nominal']
rail_x1=rail_x0+rail_data['outer_width_east_west']
# Appui de la façade sur la face intérieure du rebord ouest. Le BA13 est
# extérieur au rail : on garde ses 12,5 mm confirmés, sans intersection.
# Les cotes arrondies laissent 2,5 mm d'écart avec la profondeur mesurée.
plaster_t=passage['plasterboard_thickness_cm']
plaster_inner=rail_x1
depth=plaster_inner+plaster_t
front_x0=rail_x0+rail_s
front_x1=front_x0+t
shim=-front_x1
lining_depth=depth-front_x0
gap=passage['T1_T2_clear_bottom']; second=passage['T2_T3_clear_bottom']
stud=passage['stud_face_width_reported']; floor=p['floor_gap']
under=passage['crosspiece_lower_face']; opening_top=under-t
top=passage['cabin_cladding_top_zones']['over_T1_T2']-p['top_gap_under_stair']
side_top=passage['cabin_cladding_top_zones']['between_T2_T3']
joint=.3  # Proposition graphique de joint, pas une cote de coupe actée.
y_left=-t; y_right=-gap+t; y_far=-(gap+stud+second+stud)
palette={'A':'#86b7d3','B':'#8cbc99','C':'#e7b276',
         'R1':'#ad96cd','R2':'#db9295','R3':'#e3c75f',
         'L':'#8c969f','LW':'#8c969f','V':'#48515a','P':'#9fb6c1',
         'S':'#b2b9c0','W':'#d7ad72','W3':'#efd5ad','K':'#c8b998'}
plaster_display=p['isometric_view']['plaster_display']
plaster_alpha=plaster_display['opacity']
plaster_crop=plaster_display['display_crop_height_cm']
frame_data=p['frame_render_assumptions']

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
front+=box('A',front_x0,front_x1,y_far,-gap,floor,side_top)
front+=box('B',front_x0,front_x1,0,stud,floor,under)
# Une encoche basse dans C permet ici de garder A rectangulaire. C'est
# seulement un exemple de raccord : largeur haute et contour restent à relever.
header=[(-gap+joint,under),(stud,under),(stud,top),
        (-gap-stud,top),(-gap-stud,side_top+joint),
        (-gap+joint,side_top+joint)]
front+=extrusion('C',header,front_x0,front_x1)
returns=[]
returns+=box('R1',front_x0,depth,-t,0,floor,under)
returns+=box('R2',front_x0,depth,-gap,-gap+t,floor,under)
returns+=box('R3',front_x0,depth,y_right,y_left,opening_top,under)
assert np.isclose(lining_depth,8.19)
assert np.isclose(front_x0,rail_x0+rail_s) and front_x1<0
assert np.isclose(plaster_inner,rail_x1) and plaster_inner>=4.8
assert np.isclose(depth-measured_depth,.25)

# BA13 après le rail, de x=5 à x=6,25. La profondeur mesurée de 6 cm reste
# conservée comme fait ; l'écart de fermeture est explicite dans les légendes.
# Le placo continue au-dessus de A. Le dessin est tronqué à 188 cm : ce bord
# n'est ni le contour sous les marches, encore inconnu, ni une ligne de coupe.
wall_outline=[(y_far,0),(-gap,0),(-gap,under),(0,under),(0,0),
              (stud,0),(stud,plaster_crop),(y_far,plaster_crop)]
wall=extrusion('P',wall_outline,plaster_inner,depth)

# Ossature : T1 et T2 sont des C ouverts l'un vers l'autre. T3 est montré
# par son enveloppe, son orientation réelle n'ayant pas été relevée.
steel=frame_data['stud_sheet_cm']; stud_depth=frame_data['stud_depth_cm']
def make_stud(y0,y1,z1,opening):
    faces=box('S',0,steel,y0,y1,rail_s,z1)
    faces+=box('S',stud_depth-steel,stud_depth,y0,y1,rail_s,z1)
    a,b=(y1-steel,y1) if opening=='sud' else (y0,y0+steel)
    faces+=box('S',steel,stud_depth-steel,a,b,rail_s,z1)
    return faces

frame=make_stud(0,stud,frame_data['T1_top_cm'],'sud')
frame+=make_stud(-gap-stud,-gap,frame_data['T2_top_cm'],'nord')
# Deux ailes seulement pour T3 : ne pas inventer le côté fermé du profil.
frame+=box('S',0,steel,y_far,y_far+stud,rail_s,frame_data['T3_display_top_cm'])
frame+=box('S',stud_depth-steel,stud_depth,y_far,y_far+stud,rail_s,frame_data['T3_display_top_cm'])
wx=frame_data['timber_x_start_cm']
ww=frame_data['timber_section_cm']['east_west']
wy=frame_data['timber_section_cm']['north_south']
ta1_y=stud-steel-wy;ta2_y=-gap-stud+steel;ta3_y=y_far+steel
for name,y,z in [('W',ta1_y,frame_data['wood_display_heights_cm']['TA1']),
                 ('W',ta2_y,frame_data['wood_display_heights_cm']['TA2']),
                 ('W3',ta3_y,frame_data['wood_display_heights_cm']['TA3'])]:
    frame+=box(name,wx,wx+ww,y,y+wy,rail_s,z)
    # Cales aux appuis de la façade : mise en place à vérifier sur le chantier.
    for z0 in (15,80,150):
        frame+=box('K',front_x1,0,y,y+wy,z0,z0+5)
frame+=box('W',wx,wx+frame_data['beam_depth_cm'],ta2_y+wy,ta1_y,
           under,passage['crosspiece_upper_face'])
# Cales devant la traverse pour que C reste dans le même plan que A/B.
for y in (-35,-15):frame+=box('K',front_x1,wx,y,y+4,under,passage['crosspiece_upper_face'])

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

def draw(ax,faces,transparent_plaster=False,transparent_steel=False):
    ground=np.array([[-12,y_far-6,0],[depth+9,y_far-6,0],
                     [depth+9,stud+8,0],[-12,stud+8,0]])
    ax.add_patch(Polygon(project(ground),facecolor='#f0eeea',edgecolor='#c7c6c3',lw=.6))
    # Calculer les parties visibles : trier les grands panneaux par leur seul
    # centre ferait apparaître des cales à travers l'OSB opaque. Chaque face
    # est masquée uniquement par les portions de matière situées devant elle.
    projected=[]
    for name,face in faces:
        uv=project(face);shape=ShapePolygon(uv)
        if shape.area<1e-8:continue
        shape=shape.buffer(0)
        plane=np.linalg.lstsq(np.column_stack([uv,np.ones(len(uv))]),face@EYE,rcond=None)[0]
        projected.append((name,face,shape,plane))
    def front_halfplane(poly,coeff):
        a,b,c=coeff
        if abs(a)+abs(b)<1e-9:return poly if c>1e-7 else ShapePolygon()
        x0,y0,x1,y1=poly.bounds
        pts=[(x0-1,y0-1),(x1+1,y0-1),(x1+1,y1+1),(x0-1,y1+1)]
        out=[]
        for i,q in enumerate(pts):
            r=pts[(i+1)%len(pts)]
            v=a*q[0]+b*q[1]+c-1e-7;w=a*r[0]+b*r[1]+c-1e-7
            if v>=0:out.append(q)
            if (v>=0)!=(w>=0):
                f=v/(v-w);out.append((q[0]+f*(r[0]-q[0]),q[1]+f*(r[1]-q[1])))
        return poly.intersection(ShapePolygon(out)) if len(out)>=3 else ShapePolygon()
    def polygons(shape):
        if shape.is_empty:return []
        if shape.geom_type=='Polygon':return [shape]
        return [p for g in getattr(shape,'geoms',[]) for p in polygons(g)]
    for name,face,shape,plane in sorted(projected,key=lambda part:np.mean(part[1],axis=0)@EYE):
        visible=shape
        for other,_,occluder,other_plane in projected:
            if (other=='P' and transparent_plaster) or (other=='S' and transparent_steel) or other=='W3':continue
            if not visible.intersects(occluder):continue
            hidden=front_halfplane(occluder,other_plane-plane)
            if not hidden.is_empty:visible=visible.difference(hidden)
            if visible.is_empty:break
        n=np.cross(face[1]-face[0],face[2]-face[0]);n/=np.linalg.norm(n)
        # Eclairage déterministe pour distinguer les faces, sans texture métrique.
        shade=.70+.30*abs(n@np.array([-.35,-.45,.82]))
        rgb=np.array(colors.to_rgb(palette[name]))*shade
        is_ghost = name=='P' and transparent_plaster
        steel_ghost=name=='S' and transparent_steel
        proposed=name=='W3'
        for part in polygons(visible):
            part=orient(part,sign=1)
            paths=[]
            for ring in [part.exterior,*part.interiors]:
                q=np.array(ring.coords)
                codes=[PlotPath.MOVETO]+[PlotPath.LINETO]*(len(q)-2)+[PlotPath.CLOSEPOLY]
                paths.append(PlotPath(q,codes))
            ax.add_patch(PathPatch(PlotPath.make_compound_path(*paths),facecolor=rgb,
                alpha=plaster_alpha if is_ghost else (.22 if steel_ghost else (.45 if proposed else 1)),edgecolor='none'))
        # Tracer les seuls contours d'origine encore visibles ; les arêtes de
        # découpage d'occultation ne sont pas des joints réels.
        contour=shape.boundary.intersection(visible.buffer(1e-7))
        lines=[contour] if contour.geom_type=='LineString' else list(getattr(contour,'geoms',[]))
        for line in lines:
            if line.geom_type!='LineString':continue
            q=np.array(line.coords)
            ax.plot(q[:,0],q[:,1],color='#526d7b' if is_ghost else '#3e4b53',
                    alpha=plaster_alpha if is_ghost else (.6 if steel_ghost else 1),
                    ls='--' if is_ghost or proposed or steel_ghost else '-',lw=1.05 if is_ghost else .65)
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
fig,(ax,bx,cx)=plt.subplots(1,3,figsize=(24,13))
fig.subplots_adjust(left=.04,right=.97,top=.85,bottom=.24,wspace=.18)
fig.suptitle('Bardage et habillage du passage — vue depuis la cabane',fontsize=21,fontweight='bold',y=.965)
fig.text(.5,.922,'Projection isométrique • Cotes en cm • OSB de 1,5 cm proposé',ha='center',fontsize=13)
ax.set_title('Vue assemblée : bardage A / B / C',fontsize=15,pad=15)
bx.set_title('Façade masquée : retours et plâtre conservé',fontsize=14,pad=15)
cx.set_title('OSB masqué : M48 transparents et tasseaux',fontsize=14,pad=15)
draw(ax,rail+frame+wall+returns+front,transparent_plaster=True)
draw(bx,rail+frame+wall+returns,transparent_plaster=True)
draw(cx,rail+frame+wall,transparent_plaster=True,transparent_steel=True)

# Repères directement sur les faces, puis légendes déportées.
for name,point in [('A',(front_x0,(y_far+y_right)/2,90)),('B',(front_x0,1,85)),
                   ('C',(front_x0,-22,179))]:
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
dimension(bx,(front_x0,-22,under),(depth,-22,under),'≈ 8,2 à vérifier',(0,7),(0,5))
dimension(bx,(depth,-gap,0),(depth,-gap,opening_top),'165,3²',(16,0),(7,0))

# Fenêtres communes : les deux dessins gardent le même facteur d'échelle.
corners=project([[-t,stud,0],[-t,y_far,0],[0,stud,188],[0,y_far,188]])
ax.set_xlim(corners[:,0].min()-30,corners[:,0].max()+45)
ax.set_ylim(-58,181)
bx.set_xlim(-32,85);bx.set_ylim(-58,181)
cx.set_xlim(-32,100);cx.set_ylim(-58,181)
label(cx,(wx,ta1_y+wy/2,105),'TA1 dans T1',(-20,14),'right')
label(cx,(wx,ta2_y+wy/2,100),'TA2 dans T2',(21,10))
label(cx,(wx,ta3_y+wy/2,53),'TA3 à poser',(24,-3))
label(cx,(wx,-22,169),'Traverse en place',(-15,24),'right')
label(cx,(front_x1,-15,169),'Calage proposé',(18,24))

legend=[Patch(facecolor=palette[k],edgecolor='#41535e',label=v) for k,v in
        [('A','A : entre T2 et T3'),('B','B : côté T1'),('C','C : au-dessus du passage'),
         ('R1','R1 : côté intérieur T1'),('R2','R2 : côté intérieur T2'),('R3','R3 : dessus intérieur')]]
legend.append(Patch(facecolor=palette['P'],edgecolor='#526d7b',alpha=plaster_alpha,
                    linestyle='--',label='Plâtre conservé (transparent)'))
legend.extend(Patch(facecolor=palette[k],edgecolor='#41535e',label=v) for k,v in
              [('S','M48'),('W','TA1 / TA2 et traverse'),('W3','TA3 proposé'),('K','Cales proposées')])
fig.legend(handles=legend,loc='lower center',bbox_to_anchor=(.5,.175),ncol=4,frameon=False,fontsize=10)
notes=[
 'MESURES : cloison 6 cm ± 2 mm ; rail large de 7 cm, rebord côté cabane à 2 cm ± 2 mm devant les M48.',
 'POSE PROPOSÉE : façade contre le rebord intérieur ; calage ≈ 5 mm aux appuis ; retours ≈ 8,2 cm à relever avant coupe.',
 '¹ Largeur théorique : 45 − 1,5 − 1,5 = 42 cm, avant calage.  ² Sous-face proposée : 166,8 − 1,5 = 165,3 cm du carrelage.',
 'À MESURER : largeur haute, profil sous les marches sur A, jeux et raccords. T2 est corrigé par l’habillage, sans déplacer le métal.',
 'RAIL : fond et vis conservés ; ailes retirées dans le passage (proposition). Ailes hautes de 3 cm et tôle 0,6 mm : non mesurées.',
 'BA13 CONFIRMÉ : 12,5 mm après le rail. Face finie déduite 6,25 cm contre 6 cm mesurés : écart 2,5 mm à contrôler.',
 'OSSATURE : sections bois 32 × 19 mm ; hauteurs et positions fines des tasseaux schématiques. TA3 à poser. Contour sous les marches non relevé.'
]
for i,text in enumerate(notes):fig.text(.045,.14-i*.021,text,fontsize=10,ha='left')
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
draw(ax,rail+frame+returns+wall+trim,transparent_plaster=True)
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
    'Retours ≈ 8,2 cm : façade contre le rebord intérieur, plâtre après le rail ; cote finale à relever.',
    'Les baguettes recouvrent leur raccord avec le plâtre, sur les trois côtés du passage.',
    'Largeur 3 cm et épaisseur 0,6 cm des baguettes : hypothèses pour le dessin uniquement.',
    'BA13 12,5 mm confirmé ; face finie déduite 6,25 cm contre 6 cm mesurés. Haut schématique.'
]):fig.text(.07,.12-.027*i,text,fontsize=10)
for ext in ('png','svg','pdf'):fig.savefig(HERE/f'isometrie_cellier_v1.{ext}',dpi=160)
plt.close(fig)
print('Vue côté cellier générée avec couvre-joints illustratifs.')

# Détail du pied de T1 et plan du raccord B/R1 : les longueurs sont calculées
# depuis les mesures, et non lues sur une photographie ou une image générée.
U=np.array([1,-1,0])/np.sqrt(2);V=np.array([1,1,2])/np.sqrt(6);EYE=np.array([-1,-1,1])/np.sqrt(3)
fig,(ax,bx)=plt.subplots(1,2,figsize=(16,10))
fig.subplots_adjust(left=.06,right=.96,top=.82,bottom=.24,wspace=.28)
fig.suptitle('Rail au sol et raccord B / R1 — façade contre le rebord intérieur',fontsize=20,fontweight='bold',y=.965)
fig.text(.5,.917,'Vue depuis la cabane • Mesures en cm • Schéma de compréhension',ha='center',fontsize=13)
zoom=make_rail(-10,stud)+[(name,face) for name,face in rail if name=='V']
zoom+=box('B',front_x0,front_x1,0,stud,floor,15)
zoom+=box('R1',front_x0,depth,-t,0,floor,15)
zoom+=make_stud(0,stud,15,'sud')
zoom+=box('W',wx,wx+ww,ta1_y,ta1_y+wy,rail_s,15)
zoom+=box('K',front_x1,0,ta1_y,ta1_y+wy,8,12)
zoom += box('P',plaster_inner,depth,0,stud,0,15)
draw(ax,zoom,transparent_plaster=True);ax.set_title('Pied de T1 : B, R1 et plâtre translucide',fontsize=14)
ax.set_xlim(-12,18);ax.set_ylim(-13,18)
label(ax,(-t,1.5,10),'B',(-4,3),'right')
label(ax,(3,-t,10),'R1',(5,3))
label(ax,(rail_x0,2,2),'Rebord conservé',(-5,-2),'right')
label(ax,(sx,sy,.3),'Vis conservée',(5,-3))
dimension(ax,(rail_x0,stud,3),(0,stud,3),'2 ± 0,2',(0,3),(0,1.4))

bx.set_title('Plan du raccord : les retours couvrent le bord de la façade',fontsize=13)
bx.add_patch(Polygon([(front_x0,0),(front_x1,0),(front_x1,stud),(front_x0,stud)],facecolor=palette['B'],edgecolor='#41535e'))
bx.add_patch(Polygon([(front_x0,-t),(depth,-t),(depth,0),(front_x0,0)],facecolor=palette['R1'],edgecolor='#41535e'))
bx.add_patch(Polygon([(plaster_inner,0),(depth,0),(depth,stud),(plaster_inner,stud)],
                    facecolor=palette['P'],edgecolor='#526d7b',alpha=plaster_alpha,linestyle='--'))
for x0,x1,y0,y1,k in [(0,steel,0,stud,'S'),(stud_depth-steel,stud_depth,0,stud,'S'),
                     (steel,stud_depth-steel,stud-steel,stud,'S'),
                     (wx,wx+ww,ta1_y,ta1_y+wy,'W'),(front_x1,0,ta1_y,ta1_y+wy,'K')]:
    bx.add_patch(Polygon([(x0,y0),(x1,y0),(x1,y1),(x0,y1)],facecolor=palette[k],edgecolor='#41535e',lw=.7))
bx.plot([0,0],[-3,4],ls=':',color='#41535e',lw=1)
bx.plot([depth,depth],[-3,4],ls=':',color='#41535e',lw=1)
bx.plot([rail_x0,rail_x0],[-2.3,3.8],ls='--',color='#8c969f',lw=1.6)
bx.plot([rail_x1,rail_x1],[-2.3,3.8],ls='--',color='#8c969f',lw=1.6)
bx.text((front_x0+front_x1)/2,1.7,'B',ha='center',fontsize=16,fontweight='bold')
bx.text(wx+ww/2,ta1_y+wy/2,'TA1',ha='center',va='center',fontsize=11)
bx.text(2.4,-.75,'R1',ha='center',fontsize=16,fontweight='bold')
for a,b,y,labeltext in [(front_x0,front_x1,4.3,'1,5'),(0,depth,4.3,'6,25 déduits*'),(front_x0,depth,-2.8,'≈ 8,2 à relever')]:
    bx.annotate('',xy=(a,y),xytext=(b,y),arrowprops={'arrowstyle':'<->','lw':1})
    bx.text((a+b)/2,y+.18,labeltext,ha='center',va='bottom',fontsize=11)
bx.annotate('Face M48',xy=(0,3.7),xytext=(1.6,3.5),fontsize=10,arrowprops={'arrowstyle':'-'})
bx.annotate('Face finie du plâtre\ncôté cellier',xy=(depth,1),xytext=(7.1,1.5),ha='left',fontsize=10,arrowprops={'arrowstyle':'-'})
bx.annotate('BA13 après le rail',xy=(plaster_inner,2.8),xytext=(7.1,3.5),ha='left',fontsize=10,arrowprops={'arrowstyle':'-'})
bx.annotate('Cale ≈ 5 mm',xy=(front_x1/2,2.5),xytext=(-5,5.8),fontsize=10,arrowprops={'arrowstyle':'-'})
bx.annotate('Rebord du rail\n(projeté au sol)',xy=(rail_x0,1),xytext=(-5,1),ha='left',fontsize=10,arrowprops={'arrowstyle':'-'})
bx.text(1.8,-4.4,'← CABANE                         CELLIER →',ha='center',fontsize=11)
bx.set_xlim(-5.2,11);bx.set_ylim(-5,6.7);bx.set_aspect('equal');bx.axis('off')
for i,text in enumerate([
    'FAITS : profondeur M48 → plâtre 6 ± 0,2 cm ; rebord rail → M48 2 ± 0,2 cm ; rail large de 7 cm.',
    'HYPOTHÈSE : OSB 1,5 cm contre le rebord intérieur ; cales ≈ 5 mm derrière. Fixation aux tasseaux, pas au rebord.',
    '* BA13 confirmé 1,25 cm après le rail : 7 − 2 + 1,25 = 6,25 cm, contre 6 cm mesurés. Écart de 2,5 mm à contrôler.',
    'À RELEVER : rebord intérieur → face finie du BA13 pour les retours (≈ 8,2 cm dessinés). Ailes 3 cm et tôle 0,6 mm supposées.',
    'Le rebord reste visible devant le pied de B/A : finition basse à définir. Ailes retirées uniquement dans le passage : proposition.',
    'Ce dessin ne valide ni les coupes finales ni les fixations. Aucun retrait de métal sous les montants n’est prescrit.'
]):fig.text(.045,.184-.027*i,text,fontsize=10)
for ext in ('png','svg','pdf'):fig.savefig(HERE/f'detail_rail_raccord_v2.{ext}',dpi=160)
plt.close(fig)

# Normaliser les espaces générés par Matplotlib dans les chemins SVG.
for name in ['isometrie_bardage_v1.svg', 'isometrie_cellier_v1.svg','detail_rail_raccord_v2.svg']:
    svg_path = HERE / name
    svg_path.write_text("\n".join(line.rstrip() for line in svg_path.read_text().splitlines()) + "\n")
