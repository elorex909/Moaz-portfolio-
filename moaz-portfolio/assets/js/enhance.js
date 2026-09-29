(()=>{"use strict";
/* SVG chess set: one sprite, coloured through CSS variables so every theme and device renders identically */
const PIECE_SPRITE=`<svg xmlns="http://www.w3.org/2000/svg" width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>
<symbol id="pc-p" viewBox="0 0 45 45"><g class="pcs"><circle cx="22.5" cy="13.5" r="5.6"/><path d="M17.2 22.6h10.6c-.4 2.2-1.2 3.6-2.4 4.6 3.4 2.6 5.4 6.4 5.6 10.8H14c.2-4.4 2.2-8.2 5.6-10.8-1.2-1-2-2.4-2.4-4.6z"/><rect x="12" y="36.6" width="21" height="3.6" rx="1.8"/></g></symbol>
<symbol id="pc-r" viewBox="0 0 45 45"><g class="pcs"><path d="M12 8.5h6v4h3v-4h3v4h3v-4h6v9.6l-4 3.4v11l4 3.4V37H12v-3.1l4-3.4v-11l-4-3.4z"/><rect x="10.5" y="36.6" width="24" height="3.6" rx="1.8"/></g><path class="pcd" d="M16 21.5h13M16 31h13"/></symbol>
<symbol id="pc-b" viewBox="0 0 45 45"><g class="pcs"><circle cx="22.5" cy="7.6" r="2.6"/><path d="M22.5 10.2c-4.6 3.4-8 7.6-8 12.6 0 2.8 1.2 5 3.2 6.6l-3.6 4.4v3.2h16.8v-3.2l-3.6-4.4c2-1.6 3.2-3.8 3.2-6.6 0-5-3.4-9.2-8-12.6z"/><rect x="11" y="36.6" width="23" height="3.6" rx="1.8"/></g><path class="pcd" d="M25.8 14.2l-6.6 9"/></symbol>
<symbol id="pc-n" viewBox="0 0 45 45"><g class="pcs"><path d="M12.6 35.4C12.2 29.8 14.6 25.6 19.2 22.8c-2.4.4-4.2 1.8-5.6 3-1.2 1-3 .6-4.4-.8C8 23.8 7.6 22 8.2 20.6c.8-2 3.2-4 4.8-6.2.6-1.4.8-3 .6-4.8l1-3.4 3.4 2.8c1.4-1.2 2.8-2 4.4-2 6.4 1.6 12 8.2 11.2 18.2-.4 3.4-.2 6-.2 9.2z"/><path d="M11.4 33.8h22.4l1.8 2v4.4H9.6V35.8z"/></g><path class="pcd" d="M23.6 10.8c3.6-.2 6.8 1.6 8.8 5M26.6 13.6c2.6 1.2 4.6 3.4 5.4 6.6M29.4 17c1.6 1.4 2.6 3.4 2.8 6"/><path class="pcd" d="M19.4 22.6c1.6-2.2 2-4.6 1.2-7"/><ellipse class="pcdf" cx="16.4" cy="13.6" rx="1.3" ry=".9" transform="rotate(-25 16.4 13.6)"/><ellipse class="pcdf" cx="9.6" cy="21.8" rx=".8" ry=".5" transform="rotate(35 9.6 21.8)"/></symbol>
<symbol id="pc-q" viewBox="0 0 45 45"><g class="pcs"><circle cx="8.6" cy="14.2" r="2.7"/><circle cx="15.8" cy="9.4" r="2.7"/><circle cx="22.5" cy="8" r="2.7"/><circle cx="29.2" cy="9.4" r="2.7"/><circle cx="36.4" cy="14.2" r="2.7"/><path d="M8.6 16.8l4.6 14.8-1.6 4.4h21.8l-1.6-4.4 4.6-14.8-6.6 9.6-1.4-14.4-5 12-5-12-1.4 14.4z"/><rect x="10.5" y="36.6" width="24" height="3.6" rx="1.8"/></g><path class="pcd" d="M14 31.6h17"/></symbol>
<symbol id="pc-k" viewBox="0 0 45 45"><g class="pcs"><path d="M20.8 3.4h3.4v3h3v3.2h-3v3h-3.4v-3h-3V6.4h3z"/><path d="M22.5 12.6c-6.8 0-11.6 4.6-11.6 10.4 0 3.6 2 6.4 4.4 8.2L13 36h19l-2.3-4.8c2.4-1.8 4.4-4.6 4.4-8.2 0-5.8-4.8-10.4-11.6-10.4z"/><rect x="9.5" y="36.4" width="26" height="3.8" rx="1.9"/></g><path class="pcd" d="M22.5 20v9M18.6 24.5h7.8"/></symbol>
</defs></svg>`;

document.body.insertAdjacentHTML("afterbegin",PIECE_SPRITE);
const rm=matchMedia('(prefers-reduced-motion: reduce)').matches,$=id=>document.getElementById(id),NOTE={5:"Open the centre first.",11:"Bc4 aims straight at f7. Activity before material.",19:"A knight sacrificed to open lines. Sometimes you give up something small to see the whole board.",23:"Castling long brings a rook into the attack with tempo.",31:"The queen sacrifice. Black's knight must take, and the last piece clicks into place.",33:"Checkmate. Every move had a job."};
/* Opera Game replay (Morphy, 1858): coordinates:SAN */
const MV='e2e4:e4 e7e5:e5 g1f3:Nf3 d7d6:d6 d2d4:d4 c8g4:Bg4 d4e5:dxe5 g4f3:Bxf3 d1f3:Qxf3 d6e5:dxe5 f1c4:Bc4 g8f6:Nf6 f3b3:Qb3 d8e7:Qe7 b1c3:Nc3 c7c6:c6 c1g5:Bg5 b7b5:b5 c3b5:Nxb5 c6b5:cxb5 c4b5:Bxb5+ b8d7:Nbd7 e1c1:O-O-O a8d8:Rd8 d1d7:Rxd7 d8d7:Rxd7 h1d1:Rd1 e7e6:Qe6 b5d7:Bxd7+ f6d7:Nxd7 b3b8:Qb8+ d7b8:Nxb8 d1d8:Rd8#'.split(' ').map(s=>s.split(':'));
window.MV_=MV;const GL={k:'♚',q:'♛',r:'♜',b:'♝',n:'♞',p:'♟'},sq=s=>s.charCodeAt(0)-97+8*(s[1]-1);
function pos(n){const b=[];'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'.split('/').reverse().forEach((row,r)=>[...row].forEach((c,f)=>{if(!/\d/.test(c))b[f+8*r]=c}));
  for(let i=0;i<n;i++){const m=MV[i][0],f=sq(m.slice(0,2)),t=sq(m.slice(2));b[t]=b[f];delete b[f];
    if(/k/i.test(b[t])&&Math.abs(f-t)==2){const r=t>f?[t+1,t-1]:[t-2,t+1];b[r[1]]=b[r[0]];delete b[r[0]]}}return b}
let ply=0,timer,hb=$('hb'),mv=$('mv');
MV.forEach((m,i)=>{if(i%2==0){const n=document.createElement('li');n.className='n';n.textContent=(i/2+1)+'.';mv.appendChild(n)}
  const li=document.createElement('li'),b=document.createElement('button');b.textContent=m[1];b.onclick=()=>{stop();go(i+1)};li.appendChild(b);mv.appendChild(li)});
let flip=false;
function go(n){ply=Math.max(0,Math.min(MV.length,n));const b=pos(ply),last=ply?MV[ply-1][0]:'',h=last?[sq(last.slice(0,2)),sq(last.slice(2))]:[];
  hb.innerHTML=Array.from({length:64},(_,k)=>{const col=k&7,row=k>>3,fc=flip?7-col:col,fr=flip?row:7-row,i=fr*8+fc,p=b[i],d=(row+col)%2;
    const rank=col==0?`<b class="co r">${fr+1}</b>`:'',file=row==7?`<b class="co f">${'abcdefgh'[fc]}</b>`:'';
    return`<div class="gs${d?' d':''}${h.includes(i)?' lm':''}">${rank}${file}${p?`<svg class="gp ${p===p.toUpperCase()?'w':'b'}" viewBox="0 0 45 45" aria-hidden="true"><use href="#pc-${p.toLowerCase()}"/></svg>`:''}</div>`}).join('');
  mv.querySelectorAll('button').forEach((x,j)=>x.classList.toggle('on',j==ply-1));
  const on=mv.querySelector('button.on');if(on)mv.scrollTop=on.offsetTop-mv.offsetTop-40;
  $('cap').textContent=ply?(ply+1>>1)+(ply%2?'. ':'... ')+MV[ply-1][1]+(ply==MV.length?' Checkmate':''):'Starting position'}
function play(){stop();$('pp').textContent='❚❚';timer=setInterval(()=>{if(ply>=MV.length)return go(0);go(ply+1)},1300)}
function stop(){clearInterval(timer);timer=0;$('pp').textContent='▶'}
$('pv').onclick=()=>{stop();go(ply-1)};$('nx').onclick=()=>{stop();go(ply+1)};$('pp').onclick=()=>timer?stop():play();
go(0);if(rm)stop();else new IntersectionObserver((e,o)=>{if(e[0].isIntersecting){play();o.disconnect()}}).observe(hb);

const g0=go;go=function(n){g0(n);$('gc').textContent=NOTE[ply]||''};go(0);
/* intro */
const it=$('intro');let seen=0;try{seen=sessionStorage.seen;sessionStorage.seen=1}catch(e){}
if(it&&!rm&&!seen){document.body.classList.add('lock');setTimeout(()=>{it.classList.add('out');document.body.classList.remove('lock')},1500);setTimeout(()=>it.remove(),2300)}else if(it)it.remove();
/* game badges */
document.querySelectorAll('.mv').forEach((m,i)=>m.innerHTML='Game '+(i+1)+' &nbsp;·&nbsp; Result <b>'+['1–0','1–0','½–½','1–0'][i]+'</b>');
/* cursor + magnetic buttons */
if(matchMedia('(pointer:fine)').matches&&!rm){const c=$('cur');addEventListener('pointermove',e=>{c.style.transform=`translate(${e.clientX}px,${e.clientY}px)`;c.classList.add('on');c.classList.toggle('big',!!e.target.closest('a,button,.pc,input,textarea'))});
document.querySelectorAll('.btn').forEach(b=>{b.addEventListener('pointermove',e=>{const r=b.getBoundingClientRect();b.style.translate=((e.clientX-r.left-r.width/2)*.18)+'px '+((e.clientY-r.top-r.height/2)*.3)+'px'});b.addEventListener('pointerleave',()=>b.style.translate='')})}

/* material balance graph: the game as a dataset */
const VAL={p:1,n:3,b:3,r:5,q:9},N=MV.length,W=340,H=96,Hm=H/2;
const bal=[...Array(N+1)].map((_,n)=>{let s=0;pos(n).forEach(c=>{if(c&&c.toLowerCase()!='k')s+=(c==c.toUpperCase()?1:-1)*VAL[c.toLowerCase()]});return s});
const mx=Math.max(...bal.map(Math.abs),1)+1,X=i=>i/N*W,Y=v=>Hm-v/mx*Hm,pts=bal.map((v,i)=>X(i).toFixed(1)+','+Y(v).toFixed(1)).join(' ');
$('mg').innerHTML=`<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Material balance across the game"><line x1="0" x2="${W}" y1="${Hm}" y2="${Hm}" stroke="rgba(255,255,255,.25)" stroke-dasharray="3 4"/><path d="M0,${Hm} L${pts.replace(/ /g,' L')} L${W},${Hm}Z" fill="rgba(6,182,212,.16)"/><polyline points="${pts}" fill="none" stroke="#06b6d4" stroke-width="2" stroke-linejoin="round"/><circle id="mgd" r="5" fill="#f59e0b" cx="0" cy="${Hm}"/>${bal.map((_,i)=>`<rect x="${X(i)-W/N/2}" y="0" width="${W/N}" height="${H}" fill="transparent" data-i="${i}" style="cursor:pointer"/>`).join('')}</svg>`;
$('mg').onclick=e=>{const i=e.target.dataset.i;if(i!=null){clearInterval(timer);timer=0;$('pp').textContent='▶';go(+i)}};
const g1=go;go=function(n){g1(n);const v=bal[ply],d=$('mgd');d.setAttribute('cx',X(ply));d.setAttribute('cy',Y(v));$('mb').textContent=v==0?'Even':(v>0?'Cyan +':'Gold +')+Math.abs(v)};go(ply);
/* board themes */
document.querySelectorAll('#sw button[data-t]').forEach(b=>b.onclick=()=>{$('hb').dataset.t=b.dataset.t;document.querySelectorAll('#sw button[data-t]').forEach(x=>x.classList.toggle('on',x==b))});
/* v7: flip the board and step with the keyboard */
const fl=$('fl');if(fl)fl.onclick=()=>{flip=!flip;fl.setAttribute('aria-pressed',flip);go(ply)};
const room=document.querySelector('#game .gr');
if(room)room.addEventListener('keydown',e=>{if(/INPUT|TEXTAREA/.test(e.target.tagName))return;
  const k=e.key;if(k=='ArrowRight'){e.preventDefault();stop();go(ply+1)}else if(k=='ArrowLeft'){e.preventDefault();stop();go(ply-1)}else if(k=='Home'){e.preventDefault();stop();go(0)}else if(k=='End'){e.preventDefault();stop();go(MV.length)}});
})();
