from pathlib import Path
import json
# Génération SVG autonome : aucune dépendance Python externe.
from xml.etree import ElementTree as ET

SVG_NS='http://www.w3.org/2000/svg'
ET.register_namespace('', SVG_NS)

def _attrs(styles):
    return {key.replace('_','-'): str(value) for key,value in styles.items()}

class Drawing:
    def __init__(self, path, size, viewBox):
        self.path=path
        self.root=ET.Element(f'{{{SVG_NS}}}svg', {'width':size[0], 'height':size[1], 'viewBox':viewBox})
    def rect(self, insert, size, **styles):
        return ET.Element(f'{{{SVG_NS}}}rect', {'x':str(insert[0]), 'y':str(insert[1]), 'width':str(size[0]), 'height':str(size[1]), **_attrs(styles)})
    def line(self, start, end, **styles):
        return ET.Element(f'{{{SVG_NS}}}line', {'x1':str(start[0]), 'y1':str(start[1]), 'x2':str(end[0]), 'y2':str(end[1]), **_attrs(styles)})
    def text(self, value, insert, **styles):
        el=ET.Element(f'{{{SVG_NS}}}text', {'x':str(insert[0]), 'y':str(insert[1]), **_attrs(styles)})
        el.text=value
        return el
    def add(self, node):
        self.root.append(node)
    def save(self):
        ET.ElementTree(self.root).write(self.path, encoding='utf-8', xml_declaration=True)

root=Path(__file__).resolve().parents[1]
file=root/'plans/01_cellier_plan_cote.svg'
data=json.loads((root/'donnees/geometrie.json').read_text())
facts=data['facts_from_user']
passage=facts['new_west_passage']
room=facts['cellier']['inside_box']
room_width=room['x'][1]-room['x'][0]
room_depth=room['y'][1]-room['y'][0]
north_clear=passage['actual_clear_width']
south_clear=passage['second_gap_clear_width']
dwg=Drawing(str(file), size=('1100px','970px'), viewBox='0 0 1100 970')
BG='#fffefd'; dark='#20334b'; blue='#206d9a'; light='#ebf5fc'; gray='#83939d'; orange='#d78b30'; green='#3a896f'; red='#a24747'
dwg.add(dwg.rect(insert=(0,0),size=(1100,970),fill=BG))
dwg.add(dwg.text('Cellier — plan actuel coté',insert=(45,52),font_size=32,font_family='DejaVu Sans',font_weight='bold',fill=dark))
dwg.add(dwg.text(f'Vue de dessus  |  cotes en cm  |  géométrie intérieure {room_width} × {room_depth}',insert=(45,86),font_size=17,font_family='DejaVu Sans',fill=dark))
scale=3.1; ox=240; oy=755
P=lambda x,y:(ox+x*scale, oy-y*scale)
def rect(x0,x1,y0,y1,**styles):
    px,py=P(x0,y1)
    r=dwg.rect(insert=(px,py),size=((x1-x0)*scale,(y1-y0)*scale),**styles); dwg.add(r); return r
def rect_box(box,**styles):
    return rect(box['x'][0],box['x'][1],box['y'][0],box['y'][1],**styles)
def txt(x,y,t,sz=14,**styles):
    dwg.add(dwg.text(t,insert=P(x,y),font_family='DejaVu Sans',font_size=sz,**styles))
def line(a,b,**styles):
    dwg.add(dwg.line(start=P(*a),end=P(*b),**styles))
# Base room
rect_box(room,fill='#f8f8f5',stroke='none')
rect_box(facts['stairs_over_cellier']['footprint'],fill='#f0f1f4',stroke='none')
rect_box(facts['east_beam']['footprint'],fill='#d6e0e8',opacity=0.6,stroke='none')
# foot prints, order gives equipment first-plane
rect_box(facts['shelf_A']['footprint'],fill='#ead7aa',stroke='#937741',stroke_width=2)
rect_box(facts['shelf_B']['footprint'],fill='#bcdac6',stroke='#3a896f',stroke_width=2)
rect_box(facts['heating_MTA']['footprint'],fill='#e9a4a4',stroke='#a24747',stroke_width=2)
# room border
rect_box(room,fill='none',stroke=dark,stroke_width=5)
# Repère confirmé : le mur nord est commun ; milieu T2 à y=130 cm.
# Point de référence métrique T2 ; le symbole ne dessine pas les bords de coupe.
t2_ref=facts['stud_2_measurement']['center_y']
dwg.add(ET.Element(f'{{{SVG_NS}}}circle',{'cx':str(P(0,t2_ref)[0]),'cy':str(P(0,t2_ref)[1]),'r':'5','fill':green}))
# object labels
for x,y,s in [(5,68,'A'),(5,60,'réserves'),(5,53,'25 × 80'),(88,141,'B'),(87,136,'30 × 90'),(95,20,'MTA')]:
    txt(x,y,s,14 if s in ('A','B','MTA') else 11,fill=dark,font_weight='bold' if s in ('A','B','MTA') else 'normal')
txt(15,115,'Escalier au-dessus',sz=15,fill=dark)
txt(15,109,'x=0..80 ; y=80..180',sz=12,fill=dark)
txt(15,103,'Hauteur variable : voir élévation',sz=12,fill=dark)
# Cotes confirmées, affichées hors du mur sans inventer les coordonnées des faces.
px,py=P(-3,135)
dwg.add(dwg.text('PASSAGE T1–T2 ACTÉ',insert=(20,py-37),font_family='DejaVu Sans',font_size=14,fill=green,font_weight='bold'))
dwg.add(dwg.text(f'{north_clear} cm libres avant habillage',insert=(20,py-14),font_family='DejaVu Sans',font_size=13,fill=green))
dwg.add(dwg.text('T2 : milieu à y = 130 cm',insert=(20,py+9),font_family='DejaVu Sans',font_size=12,fill=dark))
# height annotation below beam
txt(90.5,76,'Poutre',sz=13,fill=dark)
txt(90.5,72,'h=230',sz=12,fill=dark)
# south entrance label
px,py=P(8,-10)
dwg.add(dwg.text('Porte sud à supprimer ; ouverture exacte à relever',insert=(115,py+10),font_family='DejaVu Sans',font_size=14,fill=green))
# dimensions
line((0,188),(room_width,188),stroke=dark,stroke_width=1.7)
line((0,184),(0,192),stroke=dark,stroke_width=1.7)
line((room_width,184),(room_width,192),stroke=dark,stroke_width=1.7)
px,py=P(room_width/2,191)
dwg.add(dwg.text(f'{room_width} cm',insert=(px,py-8),text_anchor='middle',font_size=18,font_family='DejaVu Sans',fill=dark))
line((-12,0),(-12,room_depth),stroke=dark,stroke_width=1.7)
line((-16,0),(-8,0),stroke=dark,stroke_width=1.7)
line((-16,room_depth),(-8,room_depth),stroke=dark,stroke_width=1.7)
px,py=P(-17,room_depth/2)
dwg.add(dwg.text(f'{room_depth} cm',insert=(px,py+80),text_anchor='middle',font_size=18,font_family='DejaVu Sans',fill=dark,transform=f'rotate(-90 {px},{py+80})'))
# Axis arrows
txt(42,-19,'x vers est →',sz=13,fill=blue)
px,py=P(-45,178)
dwg.add(dwg.text('↑ y vers nord',insert=(px,py),font_size=13,font_family='DejaVu Sans',fill=blue))
txt(1,-6,'(0,0)',sz=15,fill=dark)
# Legend panel
px=670

def boxtext(y,title,detail,color=None):
    if color: dwg.add(dwg.rect(insert=(px,y-15),size=(18,18),fill=color,stroke='#777',stroke_width=0.6))
    dwg.add(dwg.text(title,insert=(px+30 if color else px,y),font_family='DejaVu Sans',font_size=16,font_weight='bold',fill=dark))
    for i,ln in enumerate(detail):
        dwg.add(dwg.text(ln,insert=(px+30 if color else px,y+23+i*20),font_family='DejaVu Sans',font_size=13,fill=dark))
dwg.add(dwg.text('Emprises et limites',insert=(px,170),font_size=23,font_family='DejaVu Sans',font_weight='bold',fill=dark))
boxtext(211,'A — réserves alimentaires',['x=0..25, y=0..80, hauteur 240'],'#ead7aa')
boxtext(300,'B — petit matériel',['x=85..115, y=90..180, hauteur 220'],'#bcdac6')
boxtext(389,'Module de chauffage urbain',['x=95..115, y=0..50, hauteur 230','Accès à préserver côté ouest'],'#e9a4a4')
boxtext(499,'Poutre est',['x=90..115, y=0..180, dessous à z=230'],'#d6e0e8')
boxtext(588,'Escalier en partie haute',['x=0..80, y=80..180, hauteur variable'],'#f0f1f4')
boxtext(687,'Passage choisi : T1–T2',[f'{north_clear} cm libres avant habillage.',f'T2–T3 : {south_clear} cm, sans passage.'],None)
dwg.add(dwg.text('Mur nord commun : mesures directement',insert=(px,763),font_size=13,font_family='DejaVu Sans',fill=green))
dwg.add(dwg.text('exploitables côté cabane et côté cellier.',insert=(px,785),font_size=13,font_family='DejaVu Sans',fill=green))
# footer
dwg.add(dwg.line(start=(40,897),end=(1060,897),stroke='#c6cdd1'))
dwg.add(dwg.text('Source : donnees/geometrie.json • mur nord commun et milieu T2 à y=130 cm',insert=(45,924),font_size=14,font_family='DejaVu Sans',fill=dark))
dwg.save()
print(file)

# Élévation métrique du passage décidé. Les traits verticaux marquent les
# faces internes des montants ; la hauteur de découpe reste inconnue.
elevation_file=root/'plans/02_passage_T1_T2_elevation_cotee.svg'
elev=Drawing(str(elevation_file),size=('1100px','1000px'),viewBox='0 0 1100 1000')
elev.add(elev.rect(insert=(0,0),size=(1100,1000),fill=BG))
def etext(x,y,value,size=16,**style):
    style.setdefault('fill',dark)
    elev.add(elev.text(value,insert=(x,y),font_family='DejaVu Sans',font_size=size,**style))
def eline(x1,y1,x2,y2,**style):
    elev.add(elev.line(start=(x1,y1),end=(x2,y2),**style))
etext(40,52,'Passage T1–T2 — élévation cotée',30,font_weight='bold')
etext(40,84,'Vue depuis la cabane  |  cotes en cm  |  choix du passage acté',17,fill=blue)
etext(40,116,'Les traits cotés sont à l’échelle ; aucun niveau de découpe n’est fixé.',15,fill=gray)
px_per_cm=4
floor_y=900
x_t1=300
x_t2=x_t1+north_clear*px_per_cm
limit_cm=facts['partition']['stair_support_at_first_gap']['height_from_floor_to_lower_face']
t1_cm=facts['partition']['T1_stud_top_heights']['T1_north_stud']
t2_step_cm=facts['partition']['stair_tread_underside_over_T2']['height_from_floor']
limit_y=floor_y-limit_cm*px_per_cm
t1_y=floor_y-t1_cm*px_per_cm
t2_step_y=floor_y-t2_step_cm*px_per_cm
# Sol, faces internes et sous-face de la pièce liée à l’escalier.
eline(210,floor_y,580,floor_y,stroke=dark,stroke_width=3)
eline(x_t1,t1_y,x_t1,floor_y,stroke='#617986',stroke_width=7)
eline(x_t2,limit_y,x_t2,floor_y,stroke='#617986',stroke_width=7)
eline(260,limit_y,525,limit_y,stroke='#a24747',stroke_width=5)
eline(260,limit_y-4,525,limit_y-4,stroke='#a24747',stroke_width=1,stroke_dasharray='7 5')
# La bande claire figure uniquement l’enveloppe disponible sous la limite.
elev.add(elev.rect(insert=(x_t1+4,limit_y+3),size=(x_t2-x_t1-8,floor_y-limit_y-4),fill='#e7f1eb',opacity='0.55'))
eline(x_t1,t1_y,x_t1,floor_y,stroke='#617986',stroke_width=7)
eline(x_t2,limit_y,x_t2,floor_y,stroke='#617986',stroke_width=7)
eline(x_t2,t2_step_y,x_t2,limit_y,stroke='#617986',stroke_width=5,stroke_dasharray='8 6')
etext(x_t1-12,285,'T1 · nord',16,text_anchor='end',font_weight='bold')
etext(x_t2+14,285,'T2 · sud',16,font_weight='bold')
etext(600,limit_y+6,f'Pièce liée à l’escalier : sous-face à {limit_cm:g} cm',16,fill='#a24747',font_weight='bold')
etext(600,t1_y+39,f'Sommet de T1 : {t1_cm:g} cm',16,fill='#617986',font_weight='bold')
etext(600,t1_y+68,f'Écart vertical local : {limit_cm-t1_cm:g} cm',15,fill=gray)
etext(600,345,'T2 se prolonge sous la marche (pointillé).',16)
etext(600,375,f'Sous-face de cette marche : {t2_step_cm:g} cm.',16)
etext(600,440,'Hauteur de la traverse : à définir.',17,font_weight='bold')
etext(600,470,'Équerres au-dessus : place à vérifier côté T1.',15)
etext(600,500,'La pièce de l’escalier reste intacte.',15,fill='#a24747')
# Cotes de largeur et hauteur, prises sur les faces internes et le sol.
dim_y=942
eline(x_t1,dim_y,x_t2,dim_y,stroke=green,stroke_width=2)
for x in (x_t1,x_t2): eline(x,dim_y-7,x,dim_y+7,stroke=green,stroke_width=2)
etext((x_t1+x_t2)/2,dim_y-10,f'{north_clear:g} cm libres avant habillage',16,text_anchor='middle',fill=green,font_weight='bold')
dim_x=230
eline(dim_x,limit_y,dim_x,floor_y,stroke=green,stroke_width=2)
for y in (limit_y,floor_y): eline(dim_x-7,y,dim_x+7,y,stroke=green,stroke_width=2)
etext(dim_x-16,(limit_y+floor_y)/2,f'{limit_cm:g} cm · limite haute locale',16,text_anchor='middle',fill=green,transform=f'rotate(-90 {dim_x-16} {(limit_y+floor_y)/2})')
etext(600,565,'Passage fini : largeur et hauteur à confirmer',17,font_weight='bold')
etext(600,595,'après choix des bois et de leurs fixations.',15)
etext(600,665,'Aucune coupe ni fixation dans la pièce liée',15,fill='#a24747')
etext(600,690,'à l’escalier sans vérification de sa fonction.',15,fill='#a24747')
etext(40,980,'Source : donnees/geometrie.json • relevé coté, non plan de découpe ou de structure',14,fill=gray)
elev.save()
print(elevation_file)

# Vue commune métrique : cabane de 190 × 90 cm et cellier de 180 × 115 cm.
overview_file=root/'plans/03_ensemble_cellier_cabane.svg'
overview=Drawing(str(overview_file),size=('1400px','1040px'),viewBox='0 0 1400 1040')
overview.add(overview.rect(insert=(0,0),size=(1400,1040),fill=BG))
def ot(x,y,value,size=16,**style):
    style.setdefault('fill',dark)
    overview.add(overview.text(value,insert=(x,y),font_family='DejaVu Sans',font_size=size,**style))
def ol(x1,y1,x2,y2,**style):
    overview.add(overview.line(start=(x1,y1),end=(x2,y2),**style))
oscale=3.1;oox=640;ooy=790
OX=lambda x:oox+x*oscale
OY=lambda y:ooy-y*oscale
cabin_box=data['current_geometric_hypotheses']['cabin_plan_box']
cabin_facts=facts['cabin']
north_y=room['y'][1]
t2_y=facts['stud_2_measurement']['center_y']
def ob(box,**style):
    overview.add(overview.rect(insert=(OX(box['x'][0]),OY(box['y'][1])),size=((box['x'][1]-box['x'][0])*oscale,(box['y'][1]-box['y'][0])*oscale),**style))
ot(40,55,'Cellier + cabane — vue d’ensemble du projet',32,font_weight='bold')
ot(40,92,'Mur nord commun confirmé • passage décidé entre T1 et T2',19,fill=green)
ot(40,125,'Cellier et cabane à la même échelle • dimensions de la cabane : 190 × 90 cm.',16,fill=gray)
# Enveloppe rectangulaire de la cabane, selon longueur et largeur fournies.
ob(cabin_box,fill='#edf2eb',stroke='none')
ol(OX(cabin_box['x'][0]),OY(north_y),OX(cabin_box['x'][0]),OY(cabin_box['y'][0]),stroke=green,stroke_width=3)
ol(OX(0),OY(north_y),OX(0),OY(cabin_box['y'][0]),stroke=dark,stroke_width=3)
# Bord d’accès connu à y=-10 ; position latérale des 70 cm non inventée.
ol(OX(cabin_box['x'][0]),OY(cabin_box['y'][0]),OX(0),OY(cabin_box['y'][0]),stroke=green,stroke_width=2,stroke_dasharray='8 6')
ob(room,fill='#f8f8f5',stroke='none')
ob(facts['stairs_over_cellier']['footprint'],fill='#e9edef',stroke='none')
ob(facts['east_beam']['footprint'],fill='#d6e0e8',opacity='0.65')
for name,color,stroke in [('shelf_A','#ead7aa','#937741'),('shelf_B','#bcdac6','#3a896f'),('heating_MTA','#e9a4a4','#a24747')]:
    ob(facts[name]['footprint'],fill=color,stroke=stroke,stroke_width=2)
ob(room,fill='none',stroke=dark,stroke_width=4)
ol(OX(cabin_box['x'][0]),OY(north_y),OX(room_width),OY(north_y),stroke=dark,stroke_width=4)
ot(470,164,'MUR NORD COMMUN',17,font_weight='bold')
ot(390,435,'CABANE',28,font_weight='bold',fill=green)
ot(390,465,'Sous l’escalier',18,fill=green)
ot(390,500,f'{cabin_facts["length_north_south"]:g} × {cabin_facts["width_east_west"]:g} cm',20,font_weight='bold',fill=green)
ot(760,720,'CELLIER',25,font_weight='bold')
ot(OX(6),OY(43),'A',24,font_weight='bold')
ot(OX(88),OY(132),'B',24,font_weight='bold')
ot(OX(96),OY(22),'MTA',16,font_weight='bold')
ot(OX(15),OY(99),'Escalier au-dessus',15,fill=gray)
# Le passage est un symbole de liaison : il ne fixe pas le bord de coupe.
passage_symbol_y=OY((north_y+t2_y)/2)
ot(oox,passage_symbol_y+11,'↔',40,text_anchor='middle',fill=green,font_weight='bold')
ot(370,passage_symbol_y+24,'Passage T1–T2',19,font_weight='bold',fill=green)
ot(370,passage_symbol_y+50,f'{north_clear:g} cm libres avant habillage',16,fill=green)
ot(380,OY(north_y)+30,'T1 contre le mur nord',15,fill=green)
overview.add(ET.Element(f'{{{SVG_NS}}}circle',{'cx':str(oox),'cy':str(OY(t2_y)),'r':'6','fill':green}))
ol(oox,OY(t2_y),OX(12),OY(t2_y),stroke=green,stroke_width=2)
ot(OX(14),OY(t2_y)-8,f'T2 · milieu à y = {t2_y:g} cm',15,font_weight='bold',fill=green)
ot(OX(14),OY(t2_y)+15,'50 cm du mur nord commun',13,fill=green)
# Distance nord → milieu T2, directement reprise des mesures de la cabane.
ol(235,OY(north_y),235,OY(t2_y),stroke=green,stroke_width=2)
for yy in [OY(north_y),OY(t2_y)]:ol(228,yy,242,yy,stroke=green,stroke_width=2)
ot(217,(OY(north_y)+OY(t2_y))/2,'50 cm → milieu T2',15,text_anchor='middle',fill=green,transform=f'rotate(-90 217 {(OY(north_y)+OY(t2_y))/2})')
# Dimensions du cellier.
ol(OX(0),205,OX(room_width),205,stroke=dark,stroke_width=2)
for xx in [OX(0),OX(room_width)]:ol(xx,198,xx,212,stroke=dark,stroke_width=2)
ot(OX(room_width/2),194,f'{room_width:g} cm',16,text_anchor='middle',font_weight='bold')
ol(1030,OY(0),1030,OY(north_y),stroke=dark,stroke_width=2)
for yy in [OY(0),OY(north_y)]:ol(1023,yy,1037,yy,stroke=dark,stroke_width=2)
ot(1053,(OY(0)+OY(north_y))/2,f'{room_depth:g} cm',16,text_anchor='middle',transform=f'rotate(-90 1053 {(OY(0)+OY(north_y))/2})')
ot(OX(0),OY(0)+25,'(0,0) · origine du cellier',14)
ot(OX(cabin_box['x'][0]),855,f'Vers la pièce de vie : ouverture {cabin_facts["living_room_opening_width"]:g} cm',14,fill=green)
ot(OX(-90),878,'Position latérale à préciser',13,fill=gray)
# Longueur et largeur de la cabane : mêmes échelles que le cellier.
ol(315,OY(cabin_box['y'][0]),315,OY(north_y),stroke=green,stroke_width=2)
for yy in [OY(cabin_box['y'][0]),OY(north_y)]:ol(308,yy,322,yy,stroke=green,stroke_width=2)
ot(297,(OY(cabin_box['y'][0])+OY(north_y))/2,f'{cabin_facts["length_north_south"]:g} cm',16,text_anchor='middle',fill=green,transform=f'rotate(-90 297 {(OY(cabin_box["y"][0])+OY(north_y))/2})')
ol(OX(-90),205,OX(0),205,stroke=green,stroke_width=2)
for xx in [OX(-90),OX(0)]:ol(xx,198,xx,212,stroke=green,stroke_width=2)
ot(OX((cabin_box['x'][0]+cabin_box['x'][1])/2),194,f'{cabin_facts["width_east_west"]:g} cm',16,text_anchor='middle',font_weight='bold',fill=green)
ot(690,847,'Porte sud du cellier supprimée dans le projet',14,fill=green)
ot(1085,235,'Cotes de l’accès',20,font_weight='bold')
for yy,value in [(275,'T1–T2 : 45 cm libres'),(309,'T1 : sommet à 169,5 cm'),(343,'Pièce de l’escalier : 174 cm'),(377,'Marche au-dessus T2 : 187 cm'),(411,'T2–T3 : 37,5 cm, sans passage')]:ot(1085,yy,value,14)
ot(1085,470,'Hauteur finie à définir',16,font_weight='bold')
ot(1085,500,'Équerres au-dessus :',14)
ot(1085,524,'place à vérifier côté T1.',14)
ot(1085,585,'Pièce liée à l’escalier',15,font_weight='bold',fill=red)
ot(1085,610,'conservée intacte.',15,fill=red)
ot(280,930,'La flèche indique la liaison choisie ; les bords de découpe seront définis avec l’encadrement.',15,fill=gray)
ot(280,960,'Repère commun : x vers l’est, y vers le nord, z vers le haut ; cotes en cm.',14,fill=gray)
ot(280,990,'Source : donnees/geometrie.json • enveloppes rectangulaires, épaisseur de cloison non représentée.',14,fill=gray)
overview.save()
print(overview_file)
