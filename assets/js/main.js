const GH="",LI="https://www.linkedin.com/in/moaz-ahmed-6a491a412/"; // GH: put your GitHub URL here to show the GitHub links
const EMAIL="mezoahme136@gmail.com",EMAIL_CC="elorex909@gmail.com"; // form messages go to EMAIL, with a copy to EMAIL_CC
// Web3Forms access keys (free, from web3forms.com). Key 1 = mezoahme136@gmail.com, Key 2 = elorex909@gmail.com (optional copy)
const W3F_KEYS=["46664b93-5fbe-4064-900d-85cc1754cd07","PASTE_KEY_FOR_elorex909"];
const rm=matchMedia('(prefers-reduced-motion: reduce)').matches;
document.querySelectorAll('[data-tilt]').forEach(el=>{
  const max=el.classList.contains('sq')?4:6;
  el.addEventListener('pointermove',e=>{
    if(rm||e.pointerType==='touch')return;
    if(el.classList.contains('win-animating')||el.classList.contains('win-closed')||el.classList.contains('win-minimized')||el.classList.contains('win-max')) return;
    if(e.target.closest('.tb')) { el.style.transform=''; return; }
    const r=el.getBoundingClientRect(),x=(e.clientX-r.left)/r.width,y=(e.clientY-r.top)/r.height;
    el.classList.remove('leave');
    el.style.transform=`perspective(1200px) rotateX(${(.5-y)*max*2}deg) rotateY(${(x-.5)*max*2}deg) scale(1.01)`;
    el.style.setProperty('--mx',x*100+'%');el.style.setProperty('--my',y*100+'%');el.style.setProperty('--ang',x*360+'deg');
  });
  el.addEventListener('pointerleave',()=>{
    if(el.classList.contains('win-animating')||el.classList.contains('win-closed')||el.classList.contains('win-minimized')||el.classList.contains('win-max')) return;
    el.classList.add('leave');el.style.transform='';
  });
});
document.querySelectorAll('.btn').forEach(b=>b.addEventListener('click',e=>{
  const r=b.getBoundingClientRect(),s=Math.max(r.width,r.height),d=document.createElement('span');
  d.className='rip';d.style.cssText=`width:${s}px;height:${s}px;left:${e.clientX-r.left-s/2}px;top:${e.clientY-r.top-s/2}px`;
  b.appendChild(d);setTimeout(()=>d.remove(),650);
}));
document.getElementById('cf').addEventListener('submit',async e=>{
  e.preventDefault();
  const f=e.target,btn=document.getElementById('send'),st=document.getElementById('fs'),
    n=f.n.value.trim(),em=f.e.value.trim(),m=f.m.value.trim();
  if(f._honey.value)return; // spam bot filled the hidden field
  btn.disabled=true;btn.textContent='Sending…';st.className='fs';st.textContent='';
  try{
    const keys=W3F_KEYS.filter(k=>k&&!k.startsWith('PASTE_'));
    if(!keys.length)throw new Error('Web3Forms access key is not set in main.js');
    const results=await Promise.allSettled(keys.map(async k=>{
      const r=await fetch('https://api.web3forms.com/submit',{method:'POST',
        headers:{'Content-Type':'application/json',Accept:'application/json'},
        body:JSON.stringify({access_key:k,name:n,email:em,message:m,replyto:em,from_name:'Portfolio',subject:'New portfolio message from '+n,botcheck:''})});
      const d=await r.json();
      if(!r.ok||d.success!==true)throw new Error(d.message||'failed');
      return d;
    }));
    if(!results.some(x=>x.status==='fulfilled')){throw new Error(results.map(x=>x.reason&&x.reason.message).join(' | '))}
    f.reset();st.className='fs ok';st.textContent='Message sent. Thank you, I will reply soon.';
  }catch(err){
    console.error('Contact form error:',err);
    st.className='fs err';
    st.innerHTML='Could not send it from here. <a href="mailto:'+EMAIL+'?cc='+EMAIL_CC+'&subject='+encodeURIComponent('Portfolio message from '+n)+'&body='+encodeURIComponent(m+'\n\nFrom: '+em)+'">Open it in your email app</a> instead.';
  }finally{btn.disabled=false;btn.textContent='Send message'}
});

document.querySelectorAll('[data-repo]').forEach(a=>a.href=GH+'/'+a.dataset.repo);
document.querySelectorAll('[data-soc]').forEach(a=>{const t=a.dataset.soc,u=t==='gh'?GH:t==='li'?LI:'mailto:'+EMAIL;if(!u){a.remove();return}a.href=u;if(t!=='mail'){a.target='_blank';a.rel='noopener'}});
const bar=document.getElementById('bar');
addEventListener('scroll',()=>{bar.style.width=scrollY/(document.documentElement.scrollHeight-innerHeight)*100+'%'},{passive:true});
const links=[...document.querySelectorAll('nav a')];
new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting)links.forEach(a=>a.classList.toggle('on',a.hash==='#'+e.target.id))}),{rootMargin:'-45% 0px -50% 0px'}).observe&&document.querySelectorAll('section').forEach(s=>new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting)links.forEach(a=>a.classList.toggle('on',a.hash==='#'+s.id))}),{rootMargin:'-45% 0px -50% 0px'}).observe(s));
const co=new IntersectionObserver(es=>es.forEach(e=>{if(!e.isIntersecting)return;co.unobserve(e.target);const el=e.target,to=+el.dataset.to,dec=(el.dataset.to.split('.')[1]||'').length,suf=el.dataset.suf||'';if(rm){return}const t0=performance.now();(function f(t){const p=Math.min(1,(t-t0)/1200),v=to*(1-Math.pow(1-p,3));el.textContent=v.toFixed(dec)+suf;if(p<1)requestAnimationFrame(f)})(t0)}),{threshold:.6});
document.querySelectorAll('.kpi').forEach(k=>co.observe(k));
function initThree(){try{
const st=document.getElementById('stage'),R=new THREE.WebGLRenderer({antialias:true,alpha:true});R.setPixelRatio(Math.min(devicePixelRatio,2));st.appendChild(R.domElement);st.classList.add('three');
const S=new THREE.Scene(),C=new THREE.PerspectiveCamera(38,1,.1,50);C.position.set(0,.4,8.5);
S.add(new THREE.AmbientLight(0xffffff,.35));const l1=new THREE.PointLight(0x06b6d4,2.2,30);l1.position.set(-5,3,5);const l2=new THREE.PointLight(0xf59e0b,2.4,30);l2.position.set(5,-1,4);S.add(l1,l2);
const pr=[[0,0],[1.1,0],[1.1,.15],[.85,.28],[.55,.7],[.42,1.3],[.52,1.4],[.75,1.55],[.52,1.68],[.58,2],[.8,2.25],[.62,2.45],[0,2.5]].map(p=>new THREE.Vector2(p[0],p[1]));
const G=new THREE.Group(),gold=new THREE.MeshStandardMaterial({color:0xf5b13a,metalness:.9,roughness:.25});
const body=new THREE.Mesh(new THREE.LatheGeometry(pr,48),gold);G.add(body);
const cr=new THREE.Mesh(new THREE.BoxGeometry(.16,.6,.16),gold);cr.position.y=2.85;const cb=new THREE.Mesh(new THREE.BoxGeometry(.5,.15,.16),gold);cb.position.y=2.9;G.add(cr,cb);
G.position.y=-1.5;const W=new THREE.Group();W.add(G);
const wf=new THREE.Mesh(new THREE.IcosahedronGeometry(2.7,2),new THREE.MeshBasicMaterial({color:0x06b6d4,wireframe:true,transparent:true,opacity:.28}));W.add(wf);
const ring=new THREE.Mesh(new THREE.TorusGeometry(3.3,.012,8,120),new THREE.MeshBasicMaterial({color:0xf59e0b}));ring.rotation.x=1.2;W.add(ring);
const pa=new Float32Array(600);for(let i=0;i<600;i++)pa[i]=(Math.random()-.5)*10;const pg=new THREE.BufferGeometry();pg.setAttribute('position',new THREE.BufferAttribute(pa,3));
const pts=new THREE.Points(pg,new THREE.PointsMaterial({color:0x67e8f9,size:.035,transparent:true,opacity:.7}));W.add(pts);S.add(W);
let tx=0,ty=0;addEventListener('pointermove',e=>{tx=(e.clientX/innerWidth-.5)*.6;ty=(e.clientY/innerHeight-.5)*.4});
function rs(){const w=st.clientWidth,h=st.clientHeight;R.setSize(w,h);C.aspect=w/h;C.updateProjectionMatrix()}rs();addEventListener('resize',rs);
let vis=true;new IntersectionObserver(e=>vis=e[0].isIntersecting).observe(st);
(function a(t){requestAnimationFrame(a);if(!vis)return;const s=rm?0:t/1000;G.rotation.y=s*.6;wf.rotation.y=-s*.15;wf.rotation.x=s*.08;pts.rotation.y=s*.05;ring.rotation.z=s*.3;W.rotation.x+=(ty-W.rotation.x)*.05;W.rotation.z+=(-tx*.3-W.rotation.z)*.05;W.position.y=Math.sin(s*1.2)*.12;R.render(S,C)})(0);
}catch(e){document.getElementById('stage').classList.remove('three')}}

const sp=document.getElementById('spot');addEventListener('pointermove',e=>{sp.style.transform=`translate(${e.clientX}px,${e.clientY}px)`});
const PC=[[7,0,'♜','rq','Rook','Predictive Analysis','Framing which customers or employees are likely to leave next.'],[7,1,'♞','kb','Knight','Pandas','Grouping, aggregation and transformation across all four projects.'],[7,2,'♝','kb','Bishop','EDA','Distributions, segments and relationships that show where to look.'],[7,3,'♛','rq','Queen','Machine Learning','Building the fundamentals toward churn and attrition models.'],[7,4,'♚','kg','King','Business Intelligence & Data Storytelling','KPI summaries and plain-language insights a business can act on.'],[7,5,'♝','kb','Bishop','Python','NumPy, Pandas, Matplotlib, Seaborn and SciPy inside Jupyter.'],[7,6,'♞','kb','Knight','Visualizations','Seaborn and Matplotlib charts, each built to answer one question.'],[7,7,'♜','rq','Rook','Statistical Testing','t-tests and p-values to separate real signal from noise.'],[6,2,'♟','pa','Pawn','SQL','Querying and aggregating tabular data.'],[6,3,'♟','pa','Pawn','Data Cleaning','Duplicates, missing values, invalid ages and inconsistent labels.'],[6,4,'♟','pa','Pawn','Data Wrangling','Reshaping raw tables into analysis-ready data.'],[6,5,'♟','pa','Pawn','Feature Engineering','Deriving profit, date and segment features from raw columns.']];
const bd=document.getElementById('bd'),it=document.getElementById('it'),inn=document.getElementById('in'),idd=document.getElementById('id'),bs=document.getElementById('bs');let cur,curB;
/* skill title chip: rises from the selected piece, title only (details stay in the side card) */
const lab=document.createElement('div');lab.className='sklab';lab.setAttribute('aria-hidden','true');lab.innerHTML='<span></span>';bs.appendChild(lab);const labT=lab.firstChild;
let raf=0,until=0;
const place=()=>{if(!curB)return;const s=curB.querySelector('svg').getBoundingClientRect(),r=bs.getBoundingClientRect(),w=lab.offsetWidth,m=8,x=s.left+s.width/2-r.left,c=Math.min(Math.max(x,w/2+m),Math.max(r.width-w/2-m,w/2+m));lab.style.setProperty('--x',c);lab.style.setProperty('--y',s.top-r.top+s.height*.1);lab.style.setProperty('--a',x-c)};
const track=()=>{place();raf=performance.now()<until?requestAnimationFrame(track):0};
const kick=(ms=500)=>{until=performance.now()+ms;if(!raf)raf=requestAnimationFrame(track)};
const showLab=(b,p)=>{if(curB===b)return;curB=b;labT.textContent=p[5];lab.dataset.k=p[3];lab.classList.remove('on');place();void lab.offsetWidth;lab.classList.add('on');kick()};
for(let r=5;r<8;r++)for(let c=0;c<8;c++){const q=document.createElement('div');q.className='sqr'+((r+c)%2?' d':'');const p=PC.find(x=>x[0]==r&&x[1]==c);
if(p){const b=document.createElement('button');b.className='pc '+p[3];b.innerHTML='<svg viewBox="0 0 45 45" aria-hidden="true"><use href="#pc-'+({'♜':'r','♞':'n','♝':'b','♛':'q','♚':'k','♟':'p'})[p[2]]+'"/></svg>';b.setAttribute('aria-label',p[5]);const sh=()=>{cur&&cur.classList.remove('sel');cur=q;q.classList.add('sel');it.textContent=p[4];inn.textContent=p[5];idd.textContent=p[6];showLab(b,p)};b.onmouseenter=b.onfocus=b.onclick=sh;q.appendChild(b);if(p[3]=='kg')sh()}bd.appendChild(q)}
bs.addEventListener('pointermove',e=>{if(rm||e.pointerType==='touch')return;const r=bs.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;bs.style.setProperty('--rx',38-y*12+'deg');bs.style.setProperty('--rz',-20+x*24+'deg');kick()});
addEventListener('resize',()=>kick(300));addEventListener('load',()=>kick(300));document.fonts&&document.fonts.ready.then(()=>kick(300));


const cp=document.getElementById('cp');cp.onclick=async()=>{try{await navigator.clipboard.writeText(EMAIL);cp.textContent='Copied ✓'}catch(e){cp.textContent=EMAIL}setTimeout(()=>cp.textContent='Copy email',2200)};
