(()=>{"use strict";
const rm=matchMedia('(prefers-reduced-motion: reduce)').matches,mob=matchMedia('(max-width:800px)').matches;
const s0=document.createElement('script');s0.src='https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js';
s0.onload=()=>{try{init()}catch(e){console.warn('3D disabled',e);const g=document.getElementById('gl');g&&g.remove()}};document.head.appendChild(s0);
function init(){
const T=THREE,cv=document.createElement('canvas');cv.id='gl';document.body.prepend(cv);
const R=new T.WebGLRenderer({canvas:cv,antialias:!mob,alpha:true});R.setPixelRatio(Math.min(devicePixelRatio,mob?1.5:2));R.outputEncoding=T.sRGBEncoding;R.toneMapping=T.ACESFilmicToneMapping;R.toneMappingExposure=1.15;
const S=new T.Scene();S.fog=new T.FogExp2(0x000000,.032);const C=new T.PerspectiveCamera(42,1,.1,80);
S.add(new T.AmbientLight(0xffffff,.12));
{const pm=new T.PMREMGenerator(R),es=new T.Scene(),bk=new T.Mesh(new T.SphereGeometry(60,24,12),new T.MeshBasicMaterial({side:T.BackSide,color:0x07080b}));es.add(bk);
[[0,24,0,36,1,36,0xfff1da,9],[-28,9,12,1,16,34,0xbfe4f2,4],[28,7,-14,1,18,30,0xe9c98a,6],[0,5,-34,44,12,1,0xffffff,2],[14,12,28,20,10,1,0xfff4e6,3]].forEach(a=>{const m=new T.Mesh(new T.BoxGeometry(a[3],a[4],a[5]),new T.MeshBasicMaterial({color:new T.Color(a[6]).multiplyScalar(a[7])}));m.position.set(a[0],a[1],a[2]);es.add(m)});
S.environment=pm.fromScene(es,.03).texture;pm.dispose()}
const l1=new T.PointLight(0xa9d6e5,.9,40),l2=new T.PointLight(0xdcb972,1.1,40),l3=new T.DirectionalLight(0xfff3e0,1.1);l1.position.set(-6,6,6);l2.position.set(6,5,-6);l3.position.set(3,8,4);S.add(l1,l2,l3);

const bm=[new T.MeshPhysicalMaterial({color:0x040507,metalness:.5,roughness:.14,clearcoat:1,clearcoatRoughness:.08}),new T.MeshPhysicalMaterial({color:0x262a31,metalness:.25,roughness:.3,clearcoat:1,clearcoatRoughness:.1})],bg=new T.BoxGeometry(.98,.2,.98);
for(let r=0;r<8;r++)for(let f=0;f<8;f++){const m=new T.Mesh(bg,bm[(f+r)%2?1:0]);m.position.set(f-3.5,-.1,3.5-r);S.add(m)}
const fr=new T.Mesh(new T.BoxGeometry(8.5,.3,8.5),new T.MeshStandardMaterial({color:0xb8975a,metalness:1,roughness:.32}));fr.position.y=-.32;S.add(fr);

const PR={p:[[0,0],[.36,0],[.36,.07],[.2,.15],[.14,.42],[.25,.5],[.2,.58],[.22,.68],[.12,.76],[0,.8]],r:[[0,0],[.4,0],[.4,.08],[.27,.2],[.22,.62],[.34,.7],[.34,.95],[.24,.95],[.24,.88],[0,.88]],b:[[0,0],[.4,0],[.4,.08],[.22,.2],[.15,.55],[.26,.7],[.2,.95],[.08,1.12],[0,1.15]],q:[[0,0],[.42,0],[.42,.08],[.24,.2],[.16,.7],[.3,.9],[.36,1.1],[.16,1.15],[.12,1.25],[0,1.3]],k:[[0,0],[.42,0],[.42,.08],[.24,.2],[.17,.7],[.32,.9],[.3,1.15],[.1,1.2],[0,1.2]],n:[[0,0],[.4,0],[.4,.08],[.24,.2],[.2,.42],[0,.46]]},G={};
for(const k in PR)G[k]=new T.LatheGeometry(PR[k].map(p=>new T.Vector2(p[0],p[1])),mob?28:72);
const MW=new T.MeshPhysicalMaterial({color:0xe4dccb,metalness:.05,roughness:.2,clearcoat:1,clearcoatRoughness:.12}),MB=new T.MeshPhysicalMaterial({color:0x101216,metalness:.85,roughness:.22,clearcoat:1,clearcoatRoughness:.08});
const bx=(w,h,d,m,x,y,z)=>{const o=new T.Mesh(new T.BoxGeometry(w,h,d),m);o.position.set(x,y,z);return o},ball=(r,m,y)=>{const o=new T.Mesh(new T.SphereGeometry(r,14,10),m);o.position.y=y;return o};
function mk(c){const w=c===c.toUpperCase(),k=c.toLowerCase(),m=w?MW:MB,g=new T.Group();g.add(new T.Mesh(G[k],m));
 if(k=='k')g.add(bx(.1,.34,.1,m,0,1.38,0),bx(.28,.1,.1,m,0,1.4,0));
 if(k=='q')g.add(ball(.1,m,1.36));if(k=='b')g.add(ball(.08,m,1.2));
 if(k=='n'){const sh=new T.Shape();[[-.2,.42],[-.24,.78],[-.14,1.02],[-.02,1.16],[.03,1.3],[.11,1.15],[.2,1.13],[.3,.98],[.36,.8],[.29,.7],[.16,.78],[.08,.72],[.13,.58],[.2,.42]].forEach((q,i)=>i?sh.lineTo(q[0],q[1]):sh.moveTo(q[0],q[1]));
  const eg=new T.ExtrudeGeometry(sh,{depth:.22,bevelEnabled:true,bevelSize:.05,bevelThickness:.07,bevelSegments:5,curveSegments:8});eg.translate(0,0,-.11);const h=new T.Mesh(eg,m);h.rotation.y=-Math.PI/2;g.add(h);g.rotation.y=w?Math.PI:0}
 return g}
const P=[],kind=[],sqm=[];
'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'.split('/').reverse().forEach((row,r)=>[...row].forEach((c,f)=>{if(/\d/.test(c))return;const g=mk(c);g.position.set(f-3.5,0,3.5-r);S.add(g);sqm[f+8*r]=P.length;kind.push(c.toLowerCase());P.push(g)}));

const SAN=window.MV_,MV=SAN.map(m=>m[0]),N=MV.length,sq=s=>s.charCodeAt(0)-97+8*(s[1]-1),snap=()=>{const a=P.map(()=>-1);sqm.forEach((id,s)=>{a[id]=s});return a},TJ=[snap()];
MV.forEach(m=>{const f=sq(m.slice(0,2)),t=sq(m.slice(2));sqm[t]=sqm[f];delete sqm[f];if(kind[sqm[t]]=='k'&&Math.abs(f-t)==2){const r=t>f?[t+1,t-1]:[t-2,t+1];sqm[r[1]]=sqm[r[0]];delete sqm[r[0]]}TJ.push(snap())});
const hm=new T.MeshBasicMaterial({color:0xdcb972,transparent:true,opacity:.34}),H=[0,1].map(()=>{const m=new T.Mesh(new T.PlaneGeometry(.96,.96),hm);m.rotation.x=-Math.PI/2;m.position.y=.02;m.visible=false;S.add(m);return m});
let dust=null;if(!mob){const a=new Float32Array(900);for(let i=0;i<900;i++)a[i]=(Math.random()-.5)*(i%3==1?8:26);const g=new T.BufferGeometry();g.setAttribute('position',new T.BufferAttribute(a,3));dust=new T.Points(g,new T.PointsMaterial({color:0x67e8f9,size:.05,transparent:true,opacity:.6}));S.add(dust)}

const K=[[[11.5,5.4,15],[-5.2,.1,.3]],[[-7.5,2.8,4.5],[0,.4,0]],[[6.5,1.5,3.2],[0,.5,-1]],[[-5,3.2,-5.6],[0,.4,0]],[[0,2.4,8],[0,.6,0]],[[1.6,2.6,.6],[0,.7,-3.4]]],
secs=['top','about','certs','projects','skills','contact'].map(id=>document.getElementById(id)),L=(a,b,t)=>a.map((v,j)=>v+(b[j]-v)*t);
let tops=[],max=1;const meas=()=>{max=Math.max(1,document.documentElement.scrollHeight-innerHeight);tops=secs.map(s=>Math.min(s.offsetTop,max));tops[tops.length-1]=max};
const rs=()=>{R.setSize(innerWidth,innerHeight,false);C.aspect=innerWidth/innerHeight;C.fov=innerWidth<innerHeight?62:42;C.updateProjectionMatrix();meas()};
rs();addEventListener('resize',rs);addEventListener('load',meas);new ResizeObserver(meas).observe(document.body);
const hud=document.createElement('div');hud.id='hud';document.body.appendChild(hud);
const cp=new T.Vector3(...K[0][0]),ct=new T.Vector3(...K[0][1]),tp=new T.Vector3(),tt=new T.Vector3();let mx=0,my=0,cur=-1;
addEventListener('pointermove',e=>{mx=e.clientX/innerWidth-.5;my=e.clientY/innerHeight-.5},{passive:true});
function setPly(n){cur=n;if(n){const m=MV[n-1];[m.slice(0,2),m.slice(2)].forEach((s,j)=>{const q=sq(s);H[j].position.x=q%8-3.5;H[j].position.z=3.5-(q>>3);H[j].visible=true})}else H.forEach(h=>h.visible=false);
 hud.textContent=n?'Opera Game, 1858 · '+((n+1>>1)+(n%2?'. ':'... ')+SAN[n-1][1]):'Opera Game, 1858 · scroll to play'}
(function frame(){requestAnimationFrame(frame);
 const y=scrollY;let i=0;while(i<tops.length-2&&y>=tops[i+1])i++;
 const t0=Math.min(1,Math.max(0,(y-tops[i])/((tops[i+1]-tops[i])||1))),t=t0*t0*(3-2*t0),A=L(K[i][0],K[i+1][0],t),B=L(K[i][1],K[i+1][1],t),k=rm?1:.07;
 tp.set(A[0]+mx*.9,A[1]-my*.5,A[2]);tt.set(B[0],B[1],B[2]);cp.lerp(tp,k);ct.lerp(tt,k);C.position.copy(cp);C.lookAt(ct);
 const ply=Math.round(Math.min(1,y/max*1.04)*N);if(ply!=cur)setPly(ply);
 P.forEach((g,id)=>{const s=TJ[cur][id],cap=s<0,tx=cap?g.position.x:s%8-3.5,tz=cap?g.position.z:3.5-(s>>3),dx=tx-g.position.x,dz=tz-g.position.z,q=rm?1:.12;
  g.position.x+=dx*q;g.position.z+=dz*q;g.position.y=Math.min(1.1,Math.hypot(dx,dz)*.55);
  const z=g.scale.x+((cap?.001:1)-g.scale.x)*(rm?1:.15);g.scale.setScalar(z);g.visible=z>.02});
 if(dust)dust.rotation.y+=.0006;R.render(S,C)})();
}})();
