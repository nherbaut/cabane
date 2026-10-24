(() => {
  const svg = document.getElementById('room-plan');
  const status = document.getElementById('plan-status');
  const ns = 'http://www.w3.org/2000/svg';
  const ox = 205, oy = 625, scale = 2.9;
  const X = x => ox + x * scale;
  const Y = y => oy - y * scale;
  const add = (tag, attrs, parent = svg) => {
    const el = document.createElementNS(ns, tag);
    Object.entries(attrs).forEach(([key, val]) => el.setAttribute(key, val));
    parent.appendChild(el);
    return el;
  };
  const rect = (box, attrs, parent) => add('rect', {x:X(box.x[0]), y:Y(box.y[1]), width:(box.x[1]-box.x[0])*scale, height:(box.y[1]-box.y[0])*scale, ...attrs}, parent);
  const line = (x1,y1,x2,y2,attrs,parent) => add('line',{x1:X(x1),y1:Y(y1),x2:X(x2),y2:Y(y2),...attrs},parent);
  const label = (x,y,value,attrs,parent) => {const t=add('text',{x:X(x),y:Y(y),...attrs},parent);t.textContent=value;return t};
  const box = e => e.footprint;
  fetch(document.body.dataset.geometryUrl)
    .then(r => {if(!r.ok) throw Error('Données géométriques introuvables'); return r.json()})
    .then(data => {
      const f = data.facts_from_user;
      const room=f.cellier.inside_box;
      rect(room,{fill:'#fffdf9',stroke:'#213b32','stroke-width':3});
      const heights=add('g',{'data-height-layer':'true'});
      rect(box(f.stairs_over_cellier),{fill:'#e4e9e9',opacity:.7},heights);
      rect(box(f.east_beam),{fill:'#b6c9cb',opacity:.65},heights);
      rect(box(f.shelf_A),{fill:'#e7bf80',stroke:'#9b7844','stroke-width':1.5});
      rect(box(f.shelf_B),{fill:'#88b59a',stroke:'#488164','stroke-width':1.5});
      rect(box(f.heating_MTA),{fill:'#ce8c82',stroke:'#a4625a','stroke-width':1.5});
      rect(room,{fill:'none',stroke:'#213b32','stroke-width':3});
      const historic=data.historical_assumptions_not_current_dimensions.west_opening_old_80cm.y;
      line(0,historic[0],0,historic[1],{stroke:'#d6834b','stroke-width':8,'stroke-dasharray':'11 7'});
      // Position conditionnelle : les murs nord de la cabane et du cellier
      // doivent partager la même référence. Les 50 cm sont une donnée utilisateur.
      const distance=f.stud_2_measurement.distance_from_north_wall;
      const north=room.y[1];
      const studY=north-distance;
      line(-35,studY,-35,north,{stroke:'#236f58','stroke-width':1.5});
      for (const y of [studY,north]) line(-39,y,-31,y,{stroke:'#236f58','stroke-width':1.5});
      const measured=label(-39,(north+studY)/2,`${distance} cm · mur → milieu`,{'text-anchor':'middle','font-size':13,'font-weight':700,fill:'#236f58'});
      measured.setAttribute('transform',`rotate(-90 ${X(-39)} ${Y((north+studY)/2)})`);
      add('circle',{cx:X(0),cy:Y(studY),r:5,fill:'#fffdf9',stroke:'#236f58','stroke-width':2});
      label(5,studY+8,`2e M48 · milieu à y = ${studY}*`,{'font-size':12,'font-weight':700,fill:'#236f58'});
      label(5,studY+2,'* Si les murs nord sont alignés',{'font-size':10,fill:'#236f58'});
      label(5,studY-6,`T1 : ${f.height_at_T1_north_end.floor_to_ceiling_height} / ${f.height_at_T1_T2_boundary.floor_to_ceiling_height} cm aux deux bords`,{'font-size':12,'font-weight':700,fill:'#236f58'},heights);
      label(5,studY-13,`Largeur libre T1 : ${f.new_west_passage.actual_clear_width} cm`,{'font-size':12,'font-weight':700,fill:'#236f58'});
      label(5,43,'A',{'font-size':22,'font-weight':800,fill:'#253d30'});
      label(90,132,'B',{'font-size':22,'font-weight':800,fill:'#253d30'});
      label(96,22,'MTA',{'font-size':13,'font-weight':800,fill:'#562e2c'});
      label(25,103,'ESCALIER',{'font-size':12,'font-weight':800,fill:'#607177'},heights);
      label(28,97,'au-dessus',{'font-size':11,fill:'#607177'},heights);
      label(91,77,'POUTRE',{'font-size':10,'font-weight':800,fill:'#425d61'},heights);
      line(0,190,115,190,{stroke:'#455c50','stroke-width':1.5});
      line(0,186,0,194,{stroke:'#455c50','stroke-width':1.5});
      line(115,186,115,194,{stroke:'#455c50','stroke-width':1.5});
      label(57.5,194,'115 cm',{'text-anchor':'middle','font-size':16,'font-weight':800,fill:'#213b32'});
      line(-10,0,-10,180,{stroke:'#455c50','stroke-width':1.5});
      line(-14,0,-6,0,{stroke:'#455c50','stroke-width':1.5});
      line(-14,180,-6,180,{stroke:'#455c50','stroke-width':1.5});
      const dim=label(-14,90,'180 cm',{'text-anchor':'middle','font-size':16,'font-weight':800,fill:'#213b32'});
      dim.setAttribute('transform',`rotate(-90 ${X(-14)} ${Y(90)})`);
      label(0,-12,'(0,0)',{'font-size':12,fill:'#455c50'});
      label(55,-12,'x → est',{'font-size':13,'font-weight':700,fill:'#236f58'});
      label(-65,195,'↑ y nord',{'font-size':13,'font-weight':700,fill:'#236f58'});
      label(-65,118,'ANCIENNE ZONE',{'font-size':11,'font-weight':800,fill:'#a65d2e'});
      label(-65,111,'y = 90…170',{'font-size':12,fill:'#a65d2e'});
      label(-65,104,`T1 : ${f.new_west_passage.actual_clear_width} cm mesurés`,{'font-size':12,fill:'#a65d2e'});
      label(5,201,'Nord',{'font-size':12,fill:'#455c50'});
      label(5,-24,'Sud · ancienne porte supprimée',{'font-size':12,fill:'#455c50'});
      const toggle=document.getElementById('show-heights');
      toggle.addEventListener('change',()=>{heights.style.display=toggle.checked?'':'none'});
      initializeFinish(f);
      status.textContent='Plan chargé à partir des données du projet.';
    })
    .catch(err => {status.textContent=err.message; svg.setAttribute('aria-label',err.message)});

  function initializeFinish(facts) {
    const rawWidth=facts.new_west_passage.actual_clear_width;
    const availableHeight=Math.min(facts.height_at_T1_north_end.floor_to_ceiling_height, facts.height_at_T1_T2_boundary.floor_to_ceiling_height);
    const slider=document.getElementById('finish');
    const output=document.getElementById('finish-value');
    const net=document.getElementById('net-width');
    const bar=document.getElementById('width-bar');
    const formula=document.getElementById('width-formula');
    const elevation=document.getElementById('passage-elevation');
    const fmt=n=>n.toLocaleString('fr-FR',{maximumFractionDigits:2});
    const s=1.8, left=215, floor=365, right=left+rawWidth*s, top=floor-availableHeight*s;
    const shape=(tag,attrs)=>add(tag,attrs,elevation);
    const note=(x,y,text,attrs={})=>{
      const node=shape('text',{x,y,fill:'#236f58','font-size':14,...attrs});
      node.textContent=text;
      return node;
    };
    // Enveloppe relevée et habillages latéraux seulement : aucun haut
    // de passage fini n'est fixé avant la définition de l'encadrement.
    shape('rect',{x:left,y:top,width:rawWidth*s,height:availableHeight*s,fill:'#fffdf7'});
    const leftFinish=shape('rect',{x:left,y:top,width:0,height:availableHeight*s,fill:'#b68b53'});
    const rightFinish=shape('rect',{x:right,y:top,width:0,height:availableHeight*s,fill:'#b68b53'});
    for (const x of [left,right]) shape('line',{x1:x,y1:top,x2:x,y2:floor,stroke:'#506459','stroke-width':2});
    shape('line',{x1:left,y1:top,x2:right,y2:top,stroke:'#506459','stroke-dasharray':'5 4'});
    shape('line',{x1:left-12,y1:floor,x2:right+12,y2:floor,stroke:'#506459'});
    shape('line',{x1:left,y1:30,x2:right,y2:30,stroke:'#236f58'});
    for (const x of [left,right]) shape('line',{x1:x,y1:25,x2:x,y2:35,stroke:'#236f58'});
    note((left+right)/2,20,`${fmt(rawWidth)} cm entre montants`,{'text-anchor':'middle'});
    shape('line',{x1:left-25,y1:top,x2:left-25,y2:floor,stroke:'#236f58'});
    for (const y of [top,floor]) shape('line',{x1:left-30,y1:y,x2:left-20,y2:y,stroke:'#236f58'});
    const midY=(top+floor)/2;
    note(left-35,midY,`${fmt(availableHeight)} cm sous plafond`,{'text-anchor':'middle',transform:`rotate(-90 ${left-35} ${midY})`});
    note(right+22,top+15,'Haut du passage');
    note(right+22,top+34,'à définir');
    note(right+22,top+140,'Bois latéral',{'font-size':13,fill:'#805b2e'});
    const widthDimension=shape('line',{x1:left,y1:388,x2:right,y2:388,stroke:'#236f58'});
    const widthCaption=note((left+right)/2,411,'',{'text-anchor':'middle','font-weight':700});
    const update=()=>{
      const mm=Number(slider.value), thickness=mm/10, width=rawWidth-2*thickness;
      output.textContent=`${mm} mm`;
      net.textContent=`${fmt(width)} cm`;
      bar.style.width=`${width/rawWidth*100}%`;
      formula.textContent=`${fmt(rawWidth)} − 2 × ${fmt(thickness)} = ${fmt(width)} cm · habillage latéral seul`;
      leftFinish.setAttribute('width',thickness*s);
      rightFinish.setAttribute('x',right-thickness*s);
      rightFinish.setAttribute('width',thickness*s);
      widthDimension.setAttribute('x1',left+thickness*s);
      widthDimension.setAttribute('x2',right-thickness*s);
      widthCaption.textContent=`Largeur restante : ${fmt(width)} cm`;
    };
    slider.addEventListener('input',update);
    slider.disabled=false;
    update();
  }
})();
