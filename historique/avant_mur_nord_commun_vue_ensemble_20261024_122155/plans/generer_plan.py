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
# La baie T1–T2 est décidée, mais ses faces ne sont pas encore localisées
# en y dans le repère du cellier : aucune découpe n’est tracée.
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
dwg.add(dwg.text('position des faces à relever',insert=(20,py+9),font_family='DejaVu Sans',font_size=12,fill=dark))
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
dwg.add(dwg.text('Faces à localiser en y : le trou n’est pas',insert=(px,763),font_size=13,font_family='DejaVu Sans',fill=red))
dwg.add(dwg.text('dessiné sur la vue de dessus.',insert=(px,785),font_size=13,font_family='DejaVu Sans',fill=red))
# footer
dwg.add(dwg.line(start=(40,897),end=(1060,897),stroke='#c6cdd1'))
dwg.add(dwg.text('Source : donnees/geometrie.json • implantation des faces du passage à mesurer sur place',insert=(45,924),font_size=14,font_family='DejaVu Sans',fill=dark))
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
