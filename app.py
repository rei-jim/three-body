import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Trisolaris — Three-Body Problem",
    page_icon="☀️",
    layout="wide",
)

st.markdown("""
<style>
  /* Dark full-page background */
  .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: #0a0a12 !important;
  }
  /* Hide Streamlit chrome */
  header[data-testid="stHeader"],
  [data-testid="stToolbar"],
  footer { display: none !important; }
  /* Remove default padding */
  .block-container {
    padding: 1.4rem 1.6rem 0 1.6rem !important;
    max-width: 100% !important;
  }
  /* Title row */
  .title-row {
    display: flex;
    align-items: baseline;
    gap: 14px;
    margin-bottom: 2px;
  }
  .app-title {
    font-family: 'SF Mono', 'Fira Mono', 'Cascadia Code', monospace;
    font-size: 22px;
    font-weight: 600;
    color: #e8e8f0;
    letter-spacing: 0.04em;
  }
  .app-sub {
    font-family: 'SF Mono', 'Fira Mono', monospace;
    font-size: 11px;
    color: #44445a;
    letter-spacing: 0.06em;
    text-transform: uppercase;
  }
</style>
<div class="title-row">
  <span class="app-title">Trisolaris</span>
  <span class="app-sub">Alpha Centauri · gravitational n-body simulation</span>
</div>
""", unsafe_allow_html=True)

SIMULATION_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500&display=swap');

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    background: #0a0a12;
    color: #c8c8d8;
    font-family: 'JetBrains Mono', 'SF Mono', 'Fira Mono', monospace;
    padding: 0 0 10px 0;
  }

  canvas {
    display: block;
    width: 100%;
    border-radius: 12px;
    background: #020208;
    box-shadow: 0 0 0 1px rgba(255,255,255,0.04), 0 8px 40px rgba(0,0,0,0.7);
  }

  /* ── Era status bar ── */
  #eraBox {
    margin-top: 10px;
    padding: 10px 16px;
    border-radius: 10px;
    background: linear-gradient(135deg, #111120 0%, #0d0d1c 100%);
    border: 1px solid rgba(255,255,255,0.06);
    border-left: 3px solid #FFC107;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 8px;
    transition: border-color 0.6s ease;
  }
  #eraLeft  { display: flex; align-items: center; gap: 10px; }
  #eraDot   { width: 7px; height: 7px; border-radius: 50%; background: #FFC107;
               box-shadow: 0 0 8px #FFC107; flex-shrink: 0; transition: all 0.6s; }
  #eraLabel { font-size: 12px; font-weight: 500; color: #FFC107; letter-spacing: 0.05em;
               transition: color 0.6s; }
  #eraSub   { font-size: 11px; color: #3a3a52; letter-spacing: 0.03em; }

  /* ── Controls ── */
  .controls {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
    align-items: center;
    margin-top: 9px;
  }

  .ctrl-group {
    display: flex;
    align-items: center;
    gap: 4px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 8px;
    padding: 4px 6px;
  }

  .ctrl-label {
    font-size: 10px;
    color: #33334a;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 0 4px 0 2px;
    user-select: none;
  }

  button {
    font-size: 11px;
    font-family: inherit;
    padding: 3px 9px;
    cursor: pointer;
    background: transparent;
    color: #5a5a78;
    border: 1px solid transparent;
    border-radius: 6px;
    transition: all 0.15s;
    letter-spacing: 0.02em;
  }
  button:hover { background: rgba(255,255,255,0.06); color: #a0a0c0; }
  button.act {
    background: rgba(96, 165, 250, 0.12);
    color: #60a5fa;
    border-color: rgba(96, 165, 250, 0.3);
  }

  .btn-action {
    background: rgba(255,255,255,0.04);
    color: #6a6a88;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 6px;
    padding: 3px 11px;
  }
  .btn-action:hover { background: rgba(255,255,255,0.08); color: #9090b0; }

  .hint {
    font-size: 10px;
    color: #252538;
    margin-top: 8px;
    letter-spacing: 0.03em;
    line-height: 1.6;
  }
  .hint span { color: #35354e; }
</style>
</head>
<body>

<canvas id="c" height="530"></canvas>

<div id="eraBox">
  <div id="eraLeft">
    <div id="eraDot"></div>
    <span id="eraLabel">CHAOTIC ERA — fate uncertain</span>
  </div>
  <span id="eraSub">planet drifting · nearest sun: —</span>
</div>

<div class="controls">
  <div class="ctrl-group">
    <span class="ctrl-label">Speed</span>
    <button class="spd" data-v="1">1×</button>
    <button class="spd" data-v="2">2×</button>
    <button class="spd act" data-v="4">4×</button>
    <button class="spd" data-v="8">8×</button>
    <button class="spd" data-v="16">16×</button>
    <button class="spd" data-v="32">32×</button>
  </div>
  <div class="ctrl-group">
    <span class="ctrl-label">Trails</span>
    <button class="trl act" data-v="1">normal</button>
    <button class="trl" data-v="2.5">long</button>
    <button class="trl" data-v="0.3">short</button>
  </div>
  <button id="pauBtn" class="btn-action">Pause</button>
  <button id="rstBtn" class="btn-action">Reset</button>
</div>

<p class="hint">
  Trail color: <span>red/orange = scorching</span> · <span>green-blue = habitable</span> · <span>deep blue = frozen</span>
  &nbsp;·&nbsp; click a star to nudge it
</p>

<script>
const canvas = document.getElementById('c');
const ctx    = canvas.getContext('2d');
const SH = 530;
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
  for(let i=0;i<130;i++)
    bgStars.push({
      x:Math.random()*canvas.width, y:Math.random()*SH,
      r:Math.random()*1.2+0.15,
      a:Math.random()*0.25+0.05,
      twinkle:Math.random()*Math.PI*2
    });
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
  ctx.fillStyle=`rgba(200,50,0,${(0.08*intensity).toFixed(3)})`;
  ctx.fillRect(0,0,W,SH);
  const t=Math.round(16*intensity);
  for(let i=0;i<t;i++){
    const a=(0.055*(1-i/t)*intensity).toFixed(3);
    ctx.fillStyle=`rgba(255,100,0,${a})`;
    ctx.fillRect(0,i,W,1); ctx.fillRect(0,SH-1-i,W,1);
    ctx.fillRect(i,0,1,SH); ctx.fillRect(W-1-i,0,1,SH);
  }
  ctx.font='500 13px "JetBrains Mono",monospace';
  ctx.fillStyle=`rgba(255,150,50,${(0.6+0.2*pulse(1.8,1)).toFixed(3)})`;
  ctx.fillText('SCORCHING — surface temperature lethal',13,22);
  ctx.font='10px "JetBrains Mono",monospace';
  ctx.fillStyle=`rgba(255,120,40,${(0.38+0.12*pulse(2.3,2)).toFixed(3)})`;
  ctx.fillText('civilizations entering dehydrated folded state',13,39);
}

function drawFrozenOverlay(W){
  const intensity=0.55+0.2*pulse(1.3,0);
  ctx.fillStyle=`rgba(0,20,100,${(0.10*intensity).toFixed(3)})`;
  ctx.fillRect(0,0,W,SH);
  const t=Math.round(16*intensity);
  for(let i=0;i<t;i++){
    const a=(0.055*(1-i/t)*intensity).toFixed(3);
    ctx.fillStyle=`rgba(30,70,210,${a})`;
    ctx.fillRect(0,i,W,1); ctx.fillRect(0,SH-1-i,W,1);
    ctx.fillRect(i,0,1,SH); ctx.fillRect(W-1-i,0,1,SH);
  }
  ctx.strokeStyle=`rgba(120,170,255,${(0.14*intensity).toFixed(3)})`;
  ctx.lineWidth=1;
  for(let x=20;x<W;x+=40){
    const h=4+3*Math.sin(x*0.3+particleT*0.4);
    ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,h);ctx.stroke();
    ctx.beginPath();ctx.moveTo(x,SH);ctx.lineTo(x,SH-h);ctx.stroke();
  }
  ctx.font='500 13px "JetBrains Mono",monospace';
  ctx.fillStyle=`rgba(90,150,255,${(0.6+0.2*pulse(1.4,1)).toFixed(3)})`;
  ctx.fillText('FROZEN — surface temperature lethal',13,22);
  ctx.font='10px "JetBrains Mono",monospace';
  ctx.fillStyle=`rgba(70,130,255,${(0.38+0.12*pulse(1.9,2)).toFixed(3)})`;
  ctx.fillText('civilizations entering hibernation state',13,39);
}

function drawStableOverlay(){
  ctx.font='500 13px "JetBrains Mono",monospace';
  ctx.fillStyle='rgba(100,210,110,0.5)';
  ctx.fillText('STABLE ERA — civilization developing',13,22);
}

function drawPlanetEffects(plx,ply,pl,cat,temp){
  const[pr,pg,pbl]=tempRGB(temp);
  if(cat==='burning'){
    const scale=1+0.4*pulse(3,0);
    for(const[rr,aa] of [[pl.r*7*scale,0.035],[pl.r*5*scale,0.07],[pl.r*3,0.13],[pl.r*1.8,0.22]]){
      ctx.beginPath();ctx.arc(plx,ply,rr,0,Math.PI*2);
      ctx.fillStyle=`rgba(255,70,0,${aa})`;ctx.fill();
    }
    ctx.strokeStyle=`rgba(255,130,20,${(0.14+0.08*pulse(4,1)).toFixed(3)})`;
    ctx.lineWidth=1;
    for(let i=0;i<8;i++){
      const a=(i/8)*Math.PI*2+particleT*0.5;
      const r1=pl.r*2, r2=pl.r*(4+2*Math.sin(particleT*3+i));
      ctx.beginPath();ctx.moveTo(plx+Math.cos(a)*r1,ply+Math.sin(a)*r1);
      ctx.lineTo(plx+Math.cos(a)*r2,ply+Math.sin(a)*r2);ctx.stroke();
    }
  } else if(cat==='frozen'){
    for(const[rr,aa] of [[pl.r*5,0.04],[pl.r*3.5,0.09],[pl.r*2.2,0.14]]){
      ctx.beginPath();ctx.arc(plx,ply,rr,0,Math.PI*2);
      ctx.strokeStyle=`rgba(110,160,255,${aa})`;ctx.lineWidth=1.5;ctx.stroke();
    }
    ctx.strokeStyle=`rgba(150,190,255,${(0.18+0.08*pulse(1.2,0)).toFixed(3)})`;
    ctx.lineWidth=1;
    for(let i=0;i<6;i++){
      const a=(i/6)*Math.PI*2;
      ctx.beginPath();ctx.moveTo(plx,ply);
      ctx.lineTo(plx+Math.cos(a)*pl.r*4,ply+Math.sin(a)*pl.r*4);ctx.stroke();
    }
  } else if(cat==='habitable'||eraState==='stable'){
    ctx.beginPath();ctx.arc(plx,ply,pl.r*3,0,Math.PI*2);
    ctx.fillStyle='rgba(30,160,70,0.08)';ctx.fill();
    ctx.beginPath();ctx.arc(plx,ply,pl.r*3,0,Math.PI*2);
    ctx.strokeStyle='rgba(60,180,90,0.18)';ctx.lineWidth=1;ctx.stroke();
  }
  ctx.beginPath();ctx.arc(plx,ply,pl.r,0,Math.PI*2);
  ctx.fillStyle=`rgb(${pr},${pg},${pbl})`;ctx.fill();
  /* subtle specular */
  ctx.beginPath();ctx.arc(plx-pl.r*.25,ply-pl.r*.25,pl.r*.32,0,Math.PI*2);
  ctx.fillStyle=`rgba(255,255,255,0.18)`;ctx.fill();
}

const ERA_CFG={
  stable: {bc:'#66BB6A', dot:'#66BB6A', glow:'#66BB6A',
           lt:'STABLE ERA — civilization developing',
           st:(d)=>`nearest sun ${d} · conditions nominal`},
  burning:{bc:'#FF5722', dot:'#FF6040', glow:'#FF4400',
           lt:'CALAMITY: SCORCHING — dehydrate and fold',
           st:(d)=>`${d} from sun · civilizations folding into dehydrated state`},
  frozen: {bc:'#42A5F5', dot:'#60BFFF', glow:'#3090FF',
           lt:'CALAMITY: ICE AGE — civilizations hibernate',
           st:(d)=>`${d} from nearest sun · surface temperature lethal`},
  chaotic:{bc:'#FFC107', dot:'#FFD040', glow:'#FFA000',
           lt:'CHAOTIC ERA — fate uncertain',
           st:(d)=>`nearest sun ${d} · fate unpredictable`},
};

function updateEraUI(cat,minD){
  const box=document.getElementById('eraBox');
  const dot=document.getElementById('eraDot');
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

  const c=ERA_CFG[eraState]||ERA_CFG.chaotic;
  const d=minD.toFixed(0);
  box.style.borderColor=c.bc;
  dot.style.background=c.dot;
  dot.style.boxShadow=`0 0 8px ${c.glow}`;
  label.textContent=c.lt;
  label.style.color=c.bc;
  sub.textContent=c.st(d);
}

function draw(){
  const W=canvas.width;
  particleT+=0.05*speedMul;
  ctx.fillStyle='#020208'; ctx.fillRect(0,0,W,SH);

  /* twinkling background stars */
  for(const s of bgStars){
    const tw=s.a*(0.7+0.3*Math.sin(particleT*0.4+s.twinkle));
    ctx.beginPath();ctx.arc(s.x,s.y,s.r,0,Math.PI*2);
    ctx.fillStyle=`rgba(255,255,255,${tw.toFixed(3)})`;ctx.fill();
  }

  const com=sysCoM(), ox=W/2-com.x, oy=SH/2-com.y;
  const toS=(x,y)=>[x+ox, y+oy];

  /* star trails */
  for(let i=0;i<3;i++){
    const b=bodies[i], t=b.trail;
    for(let k=1;k<t.length;k++){
      const frac=k/t.length;
      ctx.strokeStyle=`rgba(${b.rgb},${(frac*0.45).toFixed(3)})`;ctx.lineWidth=1.1;
      const[x1,y1]=toS(t[k-1].x,t[k-1].y),[x2,y2]=toS(t[k].x,t[k].y);
      ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(x2,y2);ctx.stroke();
    }
  }

  /* planet trail */
  const pt=bodies[3].trail;
  for(let k=1;k<pt.length;k++){
    const frac=k/pt.length, temp=pt[k].t??0.3, [r,g,bl]=tempRGB(temp);
    ctx.strokeStyle=`rgba(${r},${g},${bl},${(frac*0.85).toFixed(3)})`;ctx.lineWidth=1.6;
    const[x1,y1]=toS(pt[k-1].x,pt[k-1].y),[x2,y2]=toS(pt[k].x,pt[k].y);
    ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(x2,y2);ctx.stroke();
  }

  /* stars */
  for(let i=0;i<3;i++){
    const b=bodies[i],[bx,by]=toS(b.x,b.y);
    /* outer glow layers */
    for(const[rr,aa] of [[b.r*9,0.018],[b.r*5,0.06],[b.r*2.5,0.16],[b.r*1.6,0.28]]){
      ctx.beginPath();ctx.arc(bx,by,rr,0,Math.PI*2);
      ctx.fillStyle=`rgba(${b.rgb},${aa})`;ctx.fill();
    }
    /* core */
    ctx.beginPath();ctx.arc(bx,by,b.r,0,Math.PI*2);ctx.fillStyle=b.color;ctx.fill();
    /* specular */
    ctx.beginPath();ctx.arc(bx-b.r*.22,by-b.r*.22,b.r*.32,0,Math.PI*2);ctx.fillStyle=b.glow;ctx.fill();
    /* label */
    ctx.font='10px "JetBrains Mono",monospace';
    ctx.fillStyle='rgba(255,255,255,0.38)';
    ctx.fillText(b.name,bx+b.r+5,by+3.5);
  }

  /* planet */
  const pl=bodies[3],[plx,ply]=toS(pl.x,pl.y);
  const{cat,temp,minD}=pState();
  drawPlanetEffects(plx,ply,pl,cat,temp);
  ctx.font='9px "JetBrains Mono",monospace';
  ctx.fillStyle='rgba(255,255,255,0.28)';
  ctx.fillText('planet',plx+pl.r+3,ply+3.5);

  if(eraState==='burning') drawBurningOverlay(W);
  else if(eraState==='frozen') drawFrozenOverlay(W);
  else if(eraState==='stable') drawStableOverlay();

  updateEraUI(cat,minD);
}

function loop(){
  if(!paused){ const dt=DT*speedMul/SPF; for(let s=0;s<SPF;s++) step(dt); }
  draw(); requestAnimationFrame(loop);
}

/* controls */
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
  paused=!paused;
  document.getElementById('pauBtn').textContent=paused?'Resume':'Pause';
});

/* nudge star on click */
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
  canvas.width=canvas.offsetWidth;
  canvas.height=SH;
  makeBgStars();
  initBodies();
}
window.addEventListener('resize', resize);
resize();
requestAnimationFrame(loop);
</script>
</body>
</html>
"""

components.html(SIMULATION_HTML, height=800, scrolling=False)
