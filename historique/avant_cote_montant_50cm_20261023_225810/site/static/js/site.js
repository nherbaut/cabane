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
      label(5,43,'A',{'font-size':22,'font-weight':800,fill:'#253d30'});
      label(90,132,'B',{'font-size':22,'font-weight':800,fill:'#253d30'});
      label(96,22,'MTA',{'font-size':13,'font-weight':800,fill:'#562e2c'});
      label(25,126,'ESCALIER',{'font-size':12,'font-weight':800,fill:'#607177'},heights);
      label(28,120,'au-dessus',{'font-size':11,fill:'#607177'},heights);
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
      label(-52,172,'↑ y nord',{'font-size':13,'font-weight':700,fill:'#236f58'});
      label(-65,139,'ANCIENNE ZONE',{'font-size':11,'font-weight':800,fill:'#a65d2e'});
      label(-65,132,'y = 90…170',{'font-size':12,fill:'#a65d2e'});
      label(-65,125,'80 cm ≠ baie 53 cm',{'font-size':12,fill:'#a65d2e'});
      label(5,201,'Nord',{'font-size':12,fill:'#455c50'});
      label(5,-24,'Sud · ancienne porte supprimée',{'font-size':12,fill:'#455c50'});
      const toggle=document.getElementById('show-heights');
      toggle.addEventListener('change',()=>{heights.style.display=toggle.checked?'':'none'});
      status.textContent='Plan chargé à partir des données du projet.';
    })
    .catch(err => {status.textContent=err.message; svg.setAttribute('aria-label',err.message)});

  const slider=document.getElementById('finish');
  const output=document.getElementById('finish-value');
  const net=document.getElementById('net-width');
  const bar=document.getElementById('width-bar');
  const update=()=>{const mm=Number(slider.value); const width=53-2*mm/10; output.textContent=`${mm} mm`;net.textContent=`${width.toFixed(1).replace('.',',')} cm`;bar.style.width=`${width/53*100}%`};
  slider.addEventListener('input',update);update();
})();
