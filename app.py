import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Trisolaris — Three-Body Problem Simulation",
    page_icon="☀️",
    layout="wide",
)

st.title("Trisolaris")
st.caption(
    "A gravitational simulation of the Alpha Centauri triple-star system and its planet. "
    "Three suns in chaotic mutual orbit produce unpredictable Stable and Calamity Eras for the civilisation below."
)

SIMULATION_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Trisolaris</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: #0e0e16; color: #e0e0e0; font-family: monospace; padding: 12px; }
  canvas { display: block; width: 100%; border-radius: 10px; background: #020208; }
  #eraBox {
    margin-top: 10px; padding: 10px 14px;
    border-radius: 8px; background: #1a1a2e;
    border-left: 4px solid #FFC107;
    display: flex; justify-content: space-between; align-items: baseline;
    flex-wrap: wrap; gap: 8px;
  }
  #eraLabel { font-size: 13px; font-weight: 500; color: #FFC107; }
  #eraSub   { font-size: 12px; color: #888; }
  .controls {
    display: flex; gap: 8px; flex-wrap: wrap;
    align-items: center; margin-top: 10px;
  }
  .label { font-size: 12px; color: #888; }
  button {
    font-size: 12px; padding: 4px 9px; cursor: pointer;
    background: #1a1a2e; color: #ccc;
    border: 0.5px solid #444; border-radius: 6px;
    font-family: monospace;
  }
  button:hover { background: #2a2a3e; }
  button.act {
    background: #1e3a5f; color: #60a5fa;
    border-color: #3b82f6;
  }
  .hint { font-size: 11px; color: #555; margin-top: 6px; }
</style>
</head>
<body>

<canvas id="c" height="520"></canvas>

<div id="eraBox">
  <span id="eraLabel">CHAOTIC ERA — fate uncertain</span>
  <span id="eraSub">planet drifting</span>
</div>

<div class="controls">
  <span class="label">Speed</span>
  <button class="spd" data-v="1">1×</button>
  <button class="spd" data-v="2">2×</button>
  <button class="spd act" data-v="4">4×</button>
  <button class="spd" data-v="8">8×</button>
  <button class="spd" data-v="16">16×</button>
  <button class="spd" data-v="32">32×</button>
  <span class="label" style="margin-left:6px;">Trails</span>
  <button class="trl act" data-v="1">normal</button>
  <button class="trl" data-v="2.5">long</button>
  <button class="trl" data-v="0.3">short</button>
  <button id="rstBtn" style="margin-left:6px;">Reset</button>
  <button id="pauBtn">Pause</button>
</div>
<p class="hint">Trail color: red/orange = scorching · green-blue = habitable · deep blue = frozen void. Click a sun to nudge it.</p>

<script>
const canvas = document.getElementById('c');
const ctx    = canvas.getContext('2d');
const SH = 520;
const G=1e5, SOFT=10, DT=0.016, SPF=20;
const mA=1.1, mB=0.907, mProx=0.1221, mPl=1e-6;
const M_TOTAL = mA+mB+mProx;

let speedMul=4, paused=false, trailScale=1;
let bodies=[], bgStars=[];
let eraState='chaotic', stableCount=0, burnCount=0, frozenCount=0;
let particleT=0;

const STAR_DEF=[
  {name:'α Cen A', color:'#FFE47A', glow:'#FFFBE0', r:11, m:mA},
  {name:'α Cen B', color:'#FF9B40', glow:'#FFE0B0', r: 8, m:mB},
  {name:'Proxima', color:'#FF3B1A', glow:'#FF9977', r: 5, m:mProx},
];

function hr(h){return`${parseInt(h.slice(1,3),16)},${parseInt(h.slice(3,5),16)},${parseInt(h.slice(5,7),16)}`;}

function makeBgStars(){
  bgStars=[];
  for(let i=0;i<110;i++)
    bgStars.push({x:Math.random()*canvas.width, y:Math.random()*SH,
                  r:Math.random()*1.1+0.2, a:Math.random()*0.3+0.07});
}

function initBodies(){
  const W=canvas.width, cx=W/2, cy=SH/2, R0=80;
  const angs=[-Math.PI/2, Math.PI/6+0.12, 5*Math.PI/6-0.08];

  let st=STAR_DEF.map((s,i)=>({
    ...s, x:R0*Math.cos(angs[i]), y:R0*Math.sin(angs[i]),
    vx:0, vy:0, trail:[], maxTrail:320
  }));

  let cmx=0, cmy=0, M=0;
  st.forEach(s=>{cmx+=s.m*s.x; cmy+=s.m*s.y; M+=s.m;});
  st.forEach(s=>{s.x-=cmx/M; s.y-=cmy/M;});

  st.forEach(s=>{
    const r=Math.hypot(s.x,s.y)||1, th=Math.atan2(s.y,s.x);
    const v=0.36*Math.sqrt(G*M_TOTAL/r);
    s.vx=Math.sin(th)*v; s.vy=-Math.cos(th)*v;
  });

  const A=st[0], rPl=42, vOrb=Math.sqrt(G*mA/rPl);
  const planet={
    name:'Planet', color:'#4DD0E1', glow:'#B3EBF5', r:3.5, m:mPl,
    x:A.x, y:A.y-rPl, vx:A.vx-vOrb, vy:A.vy,
    trail:[], maxTrail:2200
  };

  bodies=[...st, planet];
  let px=0, py=0, TM=0;
  bodies.forEach(b=>{px+=b.m*b.vx; py+=b.m*b.vy; TM+=b.m;});
  bodies.forEach(b=>{b.vx-=px/TM; b.vy-=py/TM;});
  bodies.forEach(b=>{b.x+=cx; b.y+=cy; b.rgb=hr(b.color);});

  eraState='chaotic'; stableCount=0; burnCount=0; frozenCount=0;
}

function sysCoM(){
  let sx=0, sy=0, M=0;
  bodies.forEach(b=>{sx+=b.m*b.x; sy+=b.m*b.y; M+=b.m;});
  return {x:sx/M, y:sy/M};
}

function step(dt){
  const n=bodies.length, ax=new Float64Array(n), ay=new Float64Array(n);
  for(let i=0;i<n;i++) for(let j=0;j<n;j++){
    if(i===j) continue;
    const dx=bodies[j].x-bodies[i].x, dy=bodies[j].y-bodies[i].y;
    const d2=dx*dx+dy*dy+SOFT*SOFT, d=Math.sqrt(d2), f=G*bodies[j].m/(d2*d);
    ax[i]+=f*dx; ay[i]+=f*dy;
  }
  const com=sysCoM();
  for(let i=0;i<3;i++){
    const b=bodies[i], dx=b.x-com.x, dy=b.y-com.y, d=Math.hypot(dx,dy)||1;
    if(d>310){
      const vr=(b.vx*dx+b.vy*dy)/d;
      if(vr>0){ const dp=Math.min(0.7,(d-310)/80); b.vx-=dp*vr*(dx/d); b.vy-=dp*vr*(dy/d); }
    }
  }
  for(let i=0;i<n;i++){
    bodies[i].vx+=ax[i]*dt; bodies[i].vy+=ay[i]*dt;
    const pt={x:bodies[i].x, y:bodies[i].y};
    if(i===3) pt.t=pState().temp;
    bodies[i].trail.push(pt);
    const lim=Math.round(bodies[i].maxTrail*trailScale);
    if(bodies[i].trail.length>lim) bodies[i].trail.shift();
    bodies[i].x+=bodies[i].vx*dt; bodies[i].y+=bodies[i].vy*dt;
  }
}

function pState(){
  const pl=bodies[3]; let minD=Infinity;
  for(let i=0;i<3;i++) minD=Math.min(minD,Math.hypot(pl.x-bodies[i].x, pl.y-bodies[i].y));
  if(minD<38) return{cat:'burning', minD, temp:1};
  if(minD<108){ const t=0.45+0.55*(108-minD)/70; return{cat:'habitable', minD, temp:t}; }
  if(minD<200){ const t=0.28*(200-minD)/92;       return{cat:'cold',     minD, temp:t}; }
  return{cat:'frozen', minD, temp:0};
}

function tempRGB(t){
  let r,g,b;
  if(t<0.35){const f=t/0.35; r=Math.round(10+25*f); g=Math.round(20+100*f); b=Math.round(210-40*f);}
  else if(t<0.65){const f=(t-0.35)/0.3; r=Math.round(35+160*f); g=Math.round(120+100*f); b=Math.round(170-110*f);}
  else if(t<0.85){const f=(t-0.65)/0.2; r=Math.round(195+50*f); g=Math.round(220-80*f);  b=Math.round(60-30*f);}
  else{const f=(t-0.85)/0.15; r=Math.round(245+10*f); g=Math.round(140-100*f); b=Math.round(30-20*f);}
  return[r,g,b];
}

function pulse(speed,offset){ return 0.5+0.5*Math.sin(particleT*speed+offset); }

function drawBurningOverlay(W){
  const intensity=0.55+0.2*pulse(2.1,0);
  ctx.fillStyle=`rgba(220,60,0,${(0.10*intensity).toFixed(3)})`;
  ctx.fillRect(0,0,W,SH);
  const t=Math.round(14*intensity);
  for(let i=0;i<t;i++){
    const a=(0.07*(1-i/t)*intensity).toFixed(3);
    ctx.fillStyle=`rgba(255,120,0,${a})`;
    ctx.fillRect(0,i,W,1); ctx.fillRect(0,SH-1-i,W,1);
    ctx.fillRect(i,0,1,SH); ctx.fillRect(W-1-i,0,1,SH);
  }
  ctx.font='500 14px monospace';
  ctx.fillStyle=`rgba(255,160,60,${(0.55+0.25*pulse(1.8,1)).toFixed(3)})`;
  ctx.fillText('SCORCHING — surface temperature lethal',12,22);
  ctx.font='11px monospace';
  ctx.fillStyle=`rgba(255,130,50,${(0.4+0.15*pulse(2.3,2)).toFixed(3)})`;
  ctx.fillText('civilizations entering dehydrated folded state',12,40);
}

function drawFrozenOverlay(W){
  const intensity=0.55+0.2*pulse(1.3,0);
  ctx.fillStyle=`rgba(0,30,120,${(0.12*intensity).toFixed(3)})`;
  ctx.fillRect(0,0,W,SH);
  const t=Math.round(14*intensity);
  for(let i=0;i<t;i++){
    const a=(0.07*(1-i/t)*intensity).toFixed(3);
    ctx.fillStyle=`rgba(40,80,220,${a})`;
    ctx.fillRect(0,i,W,1); ctx.fillRect(0,SH-1-i,W,1);
    ctx.fillRect(i,0,1,SH); ctx.fillRect(W-1-i,0,1,SH);
  }
  ctx.strokeStyle=`rgba(140,180,255,${(0.18*intensity).toFixed(3)})`;
  ctx.lineWidth=1;
  for(let x=20;x<W;x+=40){
    const h=4+3*Math.sin(x*0.3+particleT*0.4);
    ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,h);ctx.stroke();
    ctx.beginPath();ctx.moveTo(x,SH);ctx.lineTo(x,SH-h);ctx.stroke();
  }
  for(let y=20;y<SH;y+=40){
    const h=4+3*Math.sin(y*0.3+particleT*0.4);
    ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(h,y);ctx.stroke();
    ctx.beginPath();ctx.moveTo(W,y);ctx.lineTo(W-h,y);ctx.stroke();
  }
  ctx.font='500 14px monospace';
  ctx.fillStyle=`rgba(100,160,255,${(0.55+0.25*pulse(1.4,1)).toFixed(3)})`;
  ctx.fillText('FROZEN — surface temperature lethal',12,22);
  ctx.font='11px monospace';
  ctx.fillStyle=`rgba(80,140,255,${(0.4+0.15*pulse(1.9,2)).toFixed(3)})`;
  ctx.fillText('civilizations entering hibernation state',12,40);
}

function drawStableOverlay(){
  ctx.font='500 14px monospace';
  ctx.fillStyle='rgba(100,210,110,0.55)';
  ctx.fillText('STABLE ERA — civilization developing',12,22);
}

function drawPlanetEffects(plx,ply,pl,cat,temp){
  const[pr,pg,pbl]=tempRGB(temp);
  if(cat==='burning'){
    const scale=1+0.4*pulse(3,0);
    for(const[rr,aa] of [[pl.r*7*scale,0.04],[pl.r*5*scale,0.08],[pl.r*3,0.15],[pl.r*1.8,0.25]]){
      ctx.beginPath();ctx.arc(plx,ply,rr,0,Math.PI*2);
      ctx.fillStyle=`rgba(255,80,0,${aa})`;ctx.fill();
    }
    ctx.strokeStyle=`rgba(255,140,30,${(0.15+0.1*pulse(4,1)).toFixed(3)})`;
    ctx.lineWidth=1;
    for(let i=0;i<8;i++){
      const a=(i/8)*Math.PI*2+particleT*0.5;
      const r1=pl.r*2, r2=pl.r*(4+2*Math.sin(particleT*3+i));
      ctx.beginPath();ctx.moveTo(plx+Math.cos(a)*r1,ply+Math.sin(a)*r1);
      ctx.lineTo(plx+Math.cos(a)*r2,ply+Math.sin(a)*r2);ctx.stroke();
    }
  } else if(cat==='frozen'){
    for(const[rr,aa] of [[pl.r*5,0.05],[pl.r*3.5,0.10],[pl.r*2.2,0.15]]){
      ctx.beginPath();ctx.arc(plx,ply,rr,0,Math.PI*2);
      ctx.strokeStyle=`rgba(120,170,255,${aa})`;ctx.lineWidth=1.5;ctx.stroke();
    }
    ctx.strokeStyle=`rgba(160,200,255,${(0.2+0.1*pulse(1.2,0)).toFixed(3)})`;
    ctx.lineWidth=1;
    for(let i=0;i<6;i++){
      const a=(i/6)*Math.PI*2;
      ctx.beginPath();ctx.moveTo(plx,ply);
      ctx.lineTo(plx+Math.cos(a)*pl.r*4,ply+Math.sin(a)*pl.r*4);ctx.stroke();
    }
  } else if(cat==='habitable'||eraState==='stable'){
    ctx.beginPath();ctx.arc(plx,ply,pl.r*2.8,0,Math.PI*2);
    ctx.fillStyle='rgba(30,160,70,0.1)';ctx.fill();
    ctx.beginPath();ctx.arc(plx,ply,pl.r*2.8,0,Math.PI*2);
    ctx.strokeStyle='rgba(60,180,90,0.2)';ctx.lineWidth=1;ctx.stroke();
  }
  ctx.beginPath();ctx.arc(plx,ply,pl.r,0,Math.PI*2);
  ctx.fillStyle=`rgb(${pr},${pg},${pbl})`;ctx.fill();
}

function updateEraUI(cat,minD){
  const box=document.getElementById('eraBox');
  const label=document.getElementById('eraLabel');
  const sub=document.getElementById('eraSub');
  if(cat==='habitable'){stableCount++;burnCount=Math.max(0,burnCount-4);frozenCount=Math.max(0,frozenCount-4);}
  else if(cat==='burning'){burnCount++;stableCount=Math.max(0,stableCount-8);}
  else if(cat==='frozen'){frozenCount++;stableCount=Math.max(0,stableCount-8);}
  else{stableCount=Math.max(0,stableCount-4);}
  if(burnCount>40) eraState='burning';
  else if(frozenCount>40) eraState='frozen';
  else if(stableCount>100) eraState='stable';
  else eraState='chaotic';
  const cfg={
    stable: {bc:'#66BB6A',lt:'STABLE ERA — civilization developing',lc:'#66BB6A',
              st:`nearest sun: ${minD.toFixed(0)} · conditions nominal`},
    burning:{bc:'#FF5722',lt:'CALAMITY: SCORCHING — dehydrate and fold',lc:'#FF5722',
              st:`${minD.toFixed(0)} from sun · civilizations folding into dehydrated state`},
    frozen: {bc:'#42A5F5',lt:'CALAMITY: ICE AGE — civilizations hibernate',lc:'#42A5F5',
              st:`${minD.toFixed(0)} from nearest sun · surface temperature lethal`},
    chaotic:{bc:'#FFC107',lt:'CHAOTIC ERA — fate uncertain',lc:'#FFC107',
              st:`nearest sun: ${minD.toFixed(0)} · unpredictable`},
  };
  const c=cfg[eraState]||cfg.chaotic;
  box.style.borderColor=c.bc; label.textContent=c.lt; label.style.color=c.lc; sub.textContent=c.st;
}

function draw(){
  const W=canvas.width;
  particleT+=0.05*speedMul;
  ctx.fillStyle='#020208'; ctx.fillRect(0,0,W,SH);
  for(const s of bgStars){
    ctx.beginPath();ctx.arc(s.x,s.y,s.r,0,Math.PI*2);
    ctx.fillStyle=`rgba(255,255,255,${s.a})`;ctx.fill();
  }
  const com=sysCoM(), ox=W/2-com.x, oy=SH/2-com.y;
  const toS=(x,y)=>[x+ox, y+oy];

  for(let i=0;i<3;i++){
    const b=bodies[i], t=b.trail;
    for(let k=1;k<t.length;k++){
      const frac=k/t.length;
      ctx.strokeStyle=`rgba(${b.rgb},${(frac*0.5).toFixed(3)})`;ctx.lineWidth=1.2;
      const[x1,y1]=toS(t[k-1].x,t[k-1].y),[x2,y2]=toS(t[k].x,t[k].y);
      ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(x2,y2);ctx.stroke();
    }
  }

  const pt=bodies[3].trail;
  for(let k=1;k<pt.length;k++){
    const frac=k/pt.length, temp=pt[k].t??0.3, [r,g,bl]=tempRGB(temp);
    ctx.strokeStyle=`rgba(${r},${g},${bl},${(frac*0.9).toFixed(3)})`;ctx.lineWidth=1.5;
    const[x1,y1]=toS(pt[k-1].x,pt[k-1].y),[x2,y2]=toS(pt[k].x,pt[k].y);
    ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(x2,y2);ctx.stroke();
  }

  for(let i=0;i<3;i++){
    const b=bodies[i],[bx,by]=toS(b.x,b.y);
    for(const[rr,aa] of [[b.r*7,0.03],[b.r*3.5,0.1],[b.r*1.8,0.22]]){
      ctx.beginPath();ctx.arc(bx,by,rr,0,Math.PI*2);
      ctx.fillStyle=`rgba(${b.rgb},${aa})`;ctx.fill();
    }
    ctx.beginPath();ctx.arc(bx,by,b.r,0,Math.PI*2);ctx.fillStyle=b.color;ctx.fill();
    ctx.beginPath();ctx.arc(bx-b.r*.2,by-b.r*.2,b.r*.35,0,Math.PI*2);ctx.fillStyle=b.glow;ctx.fill();
    ctx.font='10px monospace';ctx.fillStyle='rgba(255,255,255,0.5)';
    ctx.fillText(b.name,bx+b.r+4,by+3);
  }

  const pl=bodies[3],[plx,ply]=toS(pl.x,pl.y);
  const{cat,temp,minD}=pState();
  drawPlanetEffects(plx,ply,pl,cat,temp);
  ctx.font='9px monospace';ctx.fillStyle='rgba(255,255,255,0.35)';
  ctx.fillText('planet',plx+pl.r+3,ply+3);

  if(eraState==='burning') drawBurningOverlay(W);
  else if(eraState==='frozen') drawFrozenOverlay(W);
  else if(eraState==='stable') drawStableOverlay();

  updateEraUI(cat,minD);
}

function loop(){
  if(!paused){ const dt=DT*speedMul/SPF; for(let s=0;s<SPF;s++) step(dt); }
  draw(); requestAnimationFrame(loop);
}

document.querySelectorAll('.spd').forEach(b=>b.addEventListener('click',()=>{
  speedMul=parseFloat(b.dataset.v);
  document.querySelectorAll('.spd').forEach(x=>x.classList.remove('act')); b.classList.add('act');
}));
document.querySelectorAll('.trl').forEach(b=>b.addEventListener('click',()=>{
  trailScale=parseFloat(b.dataset.v);
  document.querySelectorAll('.trl').forEach(x=>x.classList.remove('act')); b.classList.add('act');
}));
document.getElementById('rstBtn').addEventListener('click', initBodies);
document.getElementById('pauBtn').addEventListener('click',()=>{
  paused=!paused; document.getElementById('pauBtn').textContent=paused?'Resume':'Pause';
});

canvas.addEventListener('click',e=>{
  const rect=canvas.getBoundingClientRect();
  const mx=(e.clientX-rect.left)*(canvas.width/rect.width);
  const my=(e.clientY-rect.top)*(canvas.height/rect.height);
  const com=sysCoM(), ox=canvas.width/2-com.x, oy=SH/2-com.y;
  let best=0, bestD=Infinity;
  for(let i=0;i<3;i++){
    const d=Math.hypot(bodies[i].x+ox-mx, bodies[i].y+oy-my);
    if(d<bestD){ bestD=d; best=i; }
  }
  const b=bodies[best], dx=mx-(b.x+ox), dy=my-(b.y+oy), d=Math.hypot(dx,dy)||1;
  b.vx+=(dx/d)*6; b.vy+=(dy/d)*6;
});

function resize(){
  canvas.width=canvas.offsetWidth; canvas.height=SH;
  makeBgStars(); initBodies();
}
window.addEventListener('resize', resize);
resize();
requestAnimationFrame(loop);
</script>
</body>
</html>
"""

components.html(SIMULATION_HTML, height=780, scrolling=False)
