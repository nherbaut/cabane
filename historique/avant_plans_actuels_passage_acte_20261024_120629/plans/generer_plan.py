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
dwg.add(dwg.text('Cellier — plan coté de référence',insert=(45,52),font_size=32,font_family='DejaVu Sans',font_weight='bold',fill=dark))
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
# entrance south old: only old hypothesis draw gap dashed
line((6,0),(86,0),stroke=green,stroke_width=7,stroke_dasharray='10 6')
# west wall historical search region y90..170
historical_y=data['historical_assumptions_not_current_dimensions']['west_opening_old_80cm']['y']
line((0,historical_y[0]),(0,historical_y[1]),stroke=orange,stroke_width=9,stroke_dasharray='10 7')
# object labels
for x,y,s in [(5,68,'A'),(5,60,'réserves'),(5,53,'25 × 80'),(88,141,'B'),(87,136,'30 × 90'),(95,20,'MTA')]:
    txt(x,y,s,14 if s in ('A','B','MTA') else 11,fill=dark,font_weight='bold' if s in ('A','B','MTA') else 'normal')
txt(15,115,'Escalier au-dessus',sz=15,fill=dark)
txt(15,109,'x=0..80 ; y=80..180',sz=12,fill=dark)
txt(15,103,'Hauteur simplifiée : 188',sz=12,fill=dark)
# labels outside western north opening historical
px,py=P(-3,135)
dwg.add(dwg.text('ancienne zone envisagée',insert=(33,py-42),font_family='DejaVu Sans',font_size=12,fill='#945f22'))
dwg.add(dwg.text('y = 90..170 (80 cm)',insert=(33,py-21),font_family='DejaVu Sans',font_size=13,fill='#945f22'))
dwg.add(dwg.text(f'T1–T2 : {north_clear} cm libres',insert=(33,py+3),font_family='DejaVu Sans',font_size=13,fill=red,font_weight='bold'))
dwg.add(dwg.text('faces non localisées ici',insert=(33,py+25),font_family='DejaVu Sans',font_size=12,fill=red))
# height annotation below beam
txt(90.5,76,'Poutre',sz=13,fill=dark)
txt(90.5,72,'h=230',sz=12,fill=dark)
# south entrance label
px,py=P(8,-10)
dwg.add(dwg.text('Porte sud à supprimer ; largeur de baie à vérifier',insert=(115,py+10),font_family='DejaVu Sans',font_size=14,fill=green))
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
boxtext(588,'Escalier en partie haute',['x=0..80, y=80..180, modèle z libre 188'],'#f0f1f4')
boxtext(687,'Passage vers cabane',[f'T1–T2 : {north_clear} cm libres.',f'T2–T3 : {south_clear} cm libres.'],None)
dwg.add(dwg.text('Faces exactes non placées dans le repère.',insert=(px,755),font_size=13,font_family='DejaVu Sans',fill=red))
dwg.add(dwg.text('La ligne orange (80 cm) est une ANCIENNE',insert=(px,780),font_size=13,font_family='DejaVu Sans',fill=red))
dwg.add(dwg.text('hypothèse : ce N’EST PAS le trou à découper.',insert=(px,802),font_size=13,font_family='DejaVu Sans',fill=red))
# footer
dwg.add(dwg.line(start=(40,897),end=(1060,897),stroke='#c6cdd1'))
dwg.add(dwg.text('Référence : géométrie.json • les largeurs de baie sont cotées, leurs faces restent à localiser',insert=(45,924),font_size=14,font_family='DejaVu Sans',fill=dark))
dwg.save()
print(file)
