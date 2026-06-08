import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="TRISOLARIS.EXE",
    page_icon="☀️",
    layout="wide",
)

st.markdown("""
<style>
  .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: #008080 !important;
  }
  header[data-testid="stHeader"],
  [data-testid="stToolbar"],
  footer { display: none !important; }
  .block-container {
    padding: 8px 8px 0 8px !important;
    max-width: 100% !important;
  }
</style>
""", unsafe_allow_html=True)

SIMULATION_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  background: #008080;
  font-family: Arial, 'MS Sans Serif', sans-serif;
  font-size: 11px;
  padding: 4px 6px 6px 6px;
  color: #000;
}

/* ── Win95 window ── */
.w95 {
  background: #C0C0C0;
  box-shadow:
    inset -1px -1px 0 #000000,
    inset  1px  1px 0 #FFFFFF,
    inset -2px -2px 0 #808080,
    inset  2px  2px 0 #DFDFDF;
  padding: 2px;
}

/* Title bar */
.titlebar {
  background: linear-gradient(90deg, #000080 0%, #1084d0 100%);
  height: 20px;
  padding: 1px 2px 1px 4px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  user-select: none;
  margin-bottom: 2px;
}
.tb-title {
  color: #fff;
  font-weight: bold;
  font-size: 11px;
  display: flex;
  align-items: center;
  gap: 5px;
  white-space: nowrap;
}
.tb-title img, .tb-icon { font-size: 13px; }
.tb-btns { display: flex; gap: 2px; }
.tb-btn {
  width: 16px; height: 14px;
  background: #C0C0C0; color: #000;
  border: none; cursor: default; font-size: 9px;
  display: flex; align-items: center; justify-content: center;
  box-shadow:
    inset -1px -1px 0 #000, inset 1px 1px 0 #fff,
    inset -2px -2px 0 #808080, inset 2px 2px 0 #dfdfdf;
  font-weight: bold; padding-bottom: 1px;
}

/* ── CRT screen area ── */
.screen-wrap {
  position: relative;
  margin: 0 2px 2px 2px;
  background: #020208;
  overflow: hidden;
  box-shadow: inset 1px 1px 0 #808080, inset -1px -1px 0 #fff;
}
/* scanlines */
.screen-wrap::after {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; bottom: 0;
  background: repeating-linear-gradient(
    0deg,
    transparent 0px, transparent 2px,
    rgba(0,0,0,0.12) 2px, rgba(0,0,0,0.12) 4px
  );
  pointer-events: none;
  z-index: 2;
}
/* vignette */
.screen-wrap::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; bottom: 0;
  background: radial-gradient(ellipse at center, transparent 48%, rgba(0,0,0,0.52) 100%);
  pointer-events: none;
  z-index: 3;
}
canvas { display: block; width: 100%; }

/* ── Controls ── */
.ctrl-area {
  padding: 4px 4px 2px 4px;
  border-bottom: 1px solid #808080;
}
.ctrl-row {
  display: flex; flex-wrap: wrap;
  align-items: center; gap: 3px;
}
.ctrl-sep { width: 6px; }
.ctrl-lbl {
  font-size: 11px; color: #000;
  white-space: nowrap; padding-right: 2px;
}

button {
  font-family: Arial, 'MS Sans Serif', sans-serif;
  font-size: 11px;
  background: #C0C0C0; color: #000;
  border: none; cursor: pointer;
  padding: 2px 8px; min-width: 28px;
  white-space: nowrap; text-align: center;
  box-shadow:
    inset -1px -1px 0 #000, inset 1px 1px 0 #fff,
    inset -2px -2px 0 #808080, inset 2px 2px 0 #dfdfdf;
}
button:active {
  box-shadow:
    inset 1px 1px 0 #000, inset -1px -1px 0 #fff,
    inset 2px 2px 0 #808080, inset -2px -2px 0 #dfdfdf;
  padding: 3px 7px 1px 9px;
}
button.act {
  box-shadow:
    inset 1px 1px 0 #000, inset -1px -1px 0 #fff,
    inset 2px 2px 0 #808080, inset -2px -2px 0 #dfdfdf;
  color: #000080; font-weight: bold;
}

/* ── Status bar ── */
.statusbar {
  display: flex; gap: 3px;
  padding: 2px 4px 1px 4px;
}
.sp {
  box-shadow: inset 1px 1px 0 #808080, inset -1px -1px 0 #fff;
  padding: 0 6px;
  font-family: 'VT323', monospace; font-size: 15px;
  color: #000080; background: #C0C0C0;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  line-height: 20px; height: 20px;
}
.sp.era  { flex: 1; }
.sp.dist { flex: 0 0 auto; min-width: 100px; text-align: right; }

.hint {
  font-size: 10px; color: #555;
  padding: 1px 4px 0 4px;
}
</style>
</head>
<body>

<div class="w95">

  <div class="titlebar">
    <div class="tb-title">
      <span class="tb-icon">☀</span>
      TRISOLARIS.EXE — Alpha Centauri N-Body Simulation
    </div>
    <div class="tb-btns">
      <div class="tb-btn">_</div>
      <div class="tb-btn">□</div>
      <div class="tb-btn">✕</div>
    </div>
  </div>

  <div class="screen-wrap">
    <canvas id="c" height="490"></canvas>
  </div>

  <div class="ctrl-area">
    <div class="ctrl-row">
      <span class="ctrl-lbl">Speed:</span>
      <button class="spd" data-v="1">1x</button>
      <button class="spd" data-v="2">2x</button>
      <button class="spd act" data-v="4">4x</button>
      <button class="spd" data-v="8">8x</button>
      <button class="spd" data-v="16">16x</button>
      <button class="spd" data-v="32">32x</button>
      <div class="ctrl-sep"></div>
      <span class="ctrl-lbl">Trail:</span>
      <button class="trl act" data-v="1">Normal</button>
      <button class="trl" data-v="2.5">Long</button>
      <button class="trl" data-v="0.3">Short</button>
      <div class="ctrl-sep"></div>
      <button id="pauBtn">Pause</button>
      <button id="rstBtn">Reset</button>
    </div>
    <div class="hint">Click a star to nudge it &nbsp;·&nbsp; trail color: orange=scorching · green=habitable · blue=frozen</div>
  </div>

  <div class="statusbar">
    <div class="sp era"  id="eraLabel">CHAOTIC ERA — fate uncertain</div>
    <div class="sp dist" id="eraSub">dist: —</div>
  </div>

</div>

<script>
const canvas = document.getElementById('c');
const ctx    = canvas.getContext('2d');
const SH = 490;
const G=1e5, SOFT=10, DT=0.016, SPF=20;
const mA=1.1, mB=0.907, mProx=0.1221, mPl=1e-6;
const M_TOTAL = mA+mB+mProx;

let speedMul=4, paused=false, trailScale=1;
let bodies=[], bgStars=[];
let eraState='chaotic', stableCount=0, burnCount=0, frozenCount=0;
let particleT=0, flickerVal=0;

const STAR_DEF=[
  {name:'A CEN A', color:'#FFE47A', glow:'#FFFBE0', r:11, m:mA},
  {name:'A CEN B', color:'#FF9B40', glow:'#FFE0B0', r: 8, m:mB},
  {name:'PROXIMA', color:'#FF3B1A', glow:'#FF9977', r: 5, m:mProx},
];

function hr(h){return`${parseInt(h.slice(1,3),16)},${parseInt(h.slice(3,5),16)},${parseInt(h.slice(5,7),16)}`;}

function makeBgStars(){
  bgStars=[];
  for(let i=0;i<120;i++)
    bgStars.push({
      x:Math.random()*canvas.width, y:Math.random()*SH,
      r:Math.random()*1.1+0.15,
      a:Math.random()*0.22+0.04,
      tw:Math.random()*Math.PI*2
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
    name:'PLANET', color:'#4DD0E1', glow:'#B3EBF5', r:3.5, m:mPl,
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

/* CRT phosphor flicker */
function drawFlicker(W){
  flickerVal += (Math.random() - 0.5) * 0.012;
  flickerVal = Math.max(-0.018, Math.min(0.018, flickerVal));
  if(Math.abs(flickerVal) > 0.002){
    ctx.fillStyle = flickerVal > 0
      ? `rgba(255,255,255,${flickerVal.toFixed(4)})`
      : `rgba(0,0,0,${(-flickerVal).toFixed(4)})`;
    ctx.fillRect(0,0,W,SH);
  }
  /* occasional horizontal scanline glitch */
  if(Math.random() < 0.008){
    const y = Math.random()*SH|0;
    const h = (Math.random()*3+1)|0;
    ctx.fillStyle='rgba(255,255,255,0.04)';
    ctx.fillRect(0,y,W,h);
  }
}

function drawBurningOverlay(W){
  const p=pulse(2.1,0);
  ctx.fillStyle=`rgba(200,40,0,${(0.07+0.04*p).toFixed(3)})`;
  ctx.fillRect(0,0,W,SH);
  const t=Math.round(14*(0.6+0.3*p));
  for(let i=0;i<t;i++){
    ctx.fillStyle=`rgba(255,80,0,${(0.05*(1-i/t)).toFixed(3)})`;
    ctx.fillRect(0,i,W,1); ctx.fillRect(0,SH-1-i,W,1);
  }
  ctx.font=`bold 20px 'VT323',monospace`;
  ctx.fillStyle=`rgba(255,80,0,${(0.9+0.1*p).toFixed(2)})`;
  ctx.fillText('> WARNING: SURFACE TEMP CRITICAL',12,26);
  ctx.font=`16px 'VT323',monospace`;
  ctx.fillStyle=`rgba(255,130,40,${(0.7+0.15*p).toFixed(2)})`;
  ctx.fillText('> DEHYDRATION PROTOCOL ENGAGED',12,46);
}

function drawFrozenOverlay(W){
  const p=pulse(1.3,0);
  ctx.fillStyle=`rgba(0,20,110,${(0.08+0.04*p).toFixed(3)})`;
  ctx.fillRect(0,0,W,SH);
  const t=Math.round(14*(0.6+0.3*p));
  for(let i=0;i<t;i++){
    ctx.fillStyle=`rgba(30,80,220,${(0.05*(1-i/t)).toFixed(3)})`;
    ctx.fillRect(0,i,W,1); ctx.fillRect(0,SH-1-i,W,1);
  }
  ctx.font=`bold 20px 'VT323',monospace`;
  ctx.fillStyle=`rgba(80,160,255,${(0.9+0.1*p).toFixed(2)})`;
  ctx.fillText('> WARNING: SUB-ZERO TEMPERATURES',12,26);
  ctx.font=`16px 'VT323',monospace`;
  ctx.fillStyle=`rgba(100,180,255,${(0.7+0.15*p).toFixed(2)})`;
  ctx.fillText('> HIBERNATION PROTOCOL ENGAGED',12,46);
}

function drawStableOverlay(){
  ctx.font=`bold 20px 'VT323',monospace`;
  ctx.fillStyle='rgba(0,220,80,0.55)';
  ctx.fillText('> STABLE ERA — CIVILIZATION DEVELOPING',12,26);
}

function drawPlanetEffects(plx,ply,pl,cat,temp){
  const[pr,pg,pbl]=tempRGB(temp);
  if(cat==='burning'){
    const scale=1+0.4*pulse(3,0);
    for(const[rr,aa] of [[pl.r*7*scale,0.03],[pl.r*5*scale,0.07],[pl.r*3,0.13],[pl.r*1.8,0.22]]){
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
  ctx.beginPath();ctx.arc(plx-pl.r*.25,ply-pl.r*.25,pl.r*.3,0,Math.PI*2);
  ctx.fillStyle='rgba(255,255,255,0.18)';ctx.fill();
}

const ERA_CFG={
  stable: {dot:'#00DC50', lt:'STABLE ERA — CIVILIZATION DEVELOPING',   st:d=>`DIST: ${d}`},
  burning:{dot:'#FF4010', lt:'CALAMITY: SCORCHING — DEHYDRATE AND FOLD',st:d=>`DIST: ${d} [CRITICAL]`},
  frozen: {dot:'#40A0FF', lt:'CALAMITY: ICE AGE — HIBERNATION',         st:d=>`DIST: ${d} [CRITICAL]`},
  chaotic:{dot:'#FFB000', lt:'CHAOTIC ERA — FATE UNCERTAIN',             st:d=>`DIST: ${d}`},
};

function updateEraUI(cat,minD){
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
  document.getElementById('eraLabel').textContent=c.lt;
  document.getElementById('eraSub').textContent=c.st(d);
  /* color the status panels */
  const colors={stable:'#004400',burning:'#440000',frozen:'#000044',chaotic:'#000080'};
  document.getElementById('eraLabel').style.color=
  document.getElementById('eraSub').style.color=colors[eraState]||'#000080';
}

function draw(){
  const W=canvas.width;
  particleT+=0.05*speedMul;
  ctx.fillStyle='#020208'; ctx.fillRect(0,0,W,SH);

  /* background stars with subtle twinkle */
  for(const s of bgStars){
    const a=s.a*(0.7+0.3*Math.sin(particleT*0.35+s.tw));
    ctx.beginPath();ctx.arc(s.x,s.y,s.r,0,Math.PI*2);
    ctx.fillStyle=`rgba(255,255,255,${a.toFixed(3)})`;ctx.fill();
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
    for(const[rr,aa] of [[b.r*9,0.018],[b.r*5,0.06],[b.r*2.5,0.16],[b.r*1.6,0.28]]){
      ctx.beginPath();ctx.arc(bx,by,rr,0,Math.PI*2);
      ctx.fillStyle=`rgba(${b.rgb},${aa})`;ctx.fill();
    }
    ctx.beginPath();ctx.arc(bx,by,b.r,0,Math.PI*2);ctx.fillStyle=b.color;ctx.fill();
    ctx.beginPath();ctx.arc(bx-b.r*.22,by-b.r*.22,b.r*.32,0,Math.PI*2);ctx.fillStyle=b.glow;ctx.fill();
    ctx.font=`14px 'VT323',monospace`;
    ctx.fillStyle='rgba(255,255,200,0.55)';
    ctx.fillText(b.name,bx+b.r+5,by+5);
  }

  /* planet */
  const pl=bodies[3],[plx,ply]=toS(pl.x,pl.y);
  const{cat,temp,minD}=pState();
  drawPlanetEffects(plx,ply,pl,cat,temp);
  ctx.font=`13px 'VT323',monospace`;
  ctx.fillStyle='rgba(200,240,255,0.45)';
  ctx.fillText('PLANET',plx+pl.r+3,ply+5);

  /* era overlays */
  if(eraState==='burning') drawBurningOverlay(W);
  else if(eraState==='frozen') drawFrozenOverlay(W);
  else if(eraState==='stable') drawStableOverlay();

  /* CRT phosphor flicker */
  drawFlicker(W);

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
  paused=!paused;
  document.getElementById('pauBtn').textContent=paused?'Resume':'Pause';
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
  canvas.width=canvas.offsetWidth;
  canvas.height=SH;
  makeBgStars();
  initBodies();
}
window.addEventListener('resize', resize);
document.fonts.ready.then(()=>{ resize(); });
resize();
requestAnimationFrame(loop);
</script>
</body>
</html>
"""

components.html(SIMULATION_HTML, height=640, scrolling=False)
