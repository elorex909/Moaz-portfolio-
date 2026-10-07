(()=>{"use strict";

const PIECE_SPRITE=`<svg xmlns="http://www.w3.org/2000/svg" width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>
<symbol id="pc-p" viewBox="0 0 45 45"><g class="pcs"><circle cx="22.5" cy="13.5" r="5.6"/><path d="M17.2 22.6h10.6c-.4 2.2-1.2 3.6-2.4 4.6 3.4 2.6 5.4 6.4 5.6 10.8H14c.2-4.4 2.2-8.2 5.6-10.8-1.2-1-2-2.4-2.4-4.6z"/><rect x="12" y="36.6" width="21" height="3.6" rx="1.8"/></g></symbol>
<symbol id="pc-r" viewBox="0 0 45 45"><g class="pcs"><path d="M12 8.5h6v4h3v-4h3v4h3v-4h6v9.6l-4 3.4v11l4 3.4V37H12v-3.1l4-3.4v-11l-4-3.4z"/><rect x="10.5" y="36.6" width="24" height="3.6" rx="1.8"/></g><path class="pcd" d="M16 21.5h13M16 31h13"/></symbol>
<symbol id="pc-b" viewBox="0 0 45 45"><g class="pcs"><circle cx="22.5" cy="7.6" r="2.6"/><path d="M22.5 10.2c-4.6 3.4-8 7.6-8 12.6 0 2.8 1.2 5 3.2 6.6l-3.6 4.4v3.2h16.8v-3.2l-3.6-4.4c2-1.6 3.2-3.8 3.2-6.6 0-5-3.4-9.2-8-12.6z"/><rect x="11" y="36.6" width="23" height="3.6" rx="1.8"/></g><path class="pcd" d="M25.8 14.2l-6.6 9"/></symbol>
<symbol id="pc-n" viewBox="0 0 45 45"><g class="pcs"><path d="M12.6 35.4C12.2 29.8 14.6 25.6 19.2 22.8c-2.4.4-4.2 1.8-5.6 3-1.2 1-3 .6-4.4-.8C8 23.8 7.6 22 8.2 20.6c.8-2 3.2-4 4.8-6.2.6-1.4.8-3 .6-4.8l1-3.4 3.4 2.8c1.4-1.2 2.8-2 4.4-2 6.4 1.6 12 8.2 11.2 18.2-.4 3.4-.2 6-.2 9.2z"/><path d="M11.4 33.8h22.4l1.8 2v4.4H9.6V35.8z"/></g><path class="pcd" d="M23.6 10.8c3.6-.2 6.8 1.6 8.8 5M26.6 13.6c2.6 1.2 4.6 3.4 5.4 6.6M29.4 17c1.6 1.4 2.6 3.4 2.8 6"/><path class="pcd" d="M19.4 22.6c1.6-2.2 2-4.6 1.2-7"/><ellipse class="pcdf" cx="16.4" cy="13.6" rx="1.3" ry=".9" transform="rotate(-25 16.4 13.6)"/><ellipse class="pcdf" cx="9.6" cy="21.8" rx=".8" ry=".5" transform="rotate(35 9.6 21.8)"/></symbol>
<symbol id="pc-q" viewBox="0 0 45 45"><g class="pcs"><circle cx="8.6" cy="14.2" r="2.7"/><circle cx="15.8" cy="9.4" r="2.7"/><circle cx="22.5" cy="8" r="2.7"/><circle cx="29.2" cy="9.4" r="2.7"/><circle cx="36.4" cy="14.2" r="2.7"/><path d="M8.6 16.8l4.6 14.8-1.6 4.4h21.8l-1.6-4.4 4.6-14.8-6.6 9.6-1.4-14.4-5 12-5-12-1.4 14.4z"/><rect x="10.5" y="36.6" width="24" height="3.6" rx="1.8"/></g><path class="pcd" d="M14 31.6h17"/></symbol>
<symbol id="pc-k" viewBox="0 0 45 45"><g class="pcs"><path d="M20.8 3.4h3.4v3h3v3.2h-3v3h-3.4v-3h-3V6.4h3z"/><path d="M22.5 12.6c-6.8 0-11.6 4.6-11.6 10.4 0 3.6 2 6.4 4.4 8.2L13 36h19l-2.3-4.8c2.4-1.8 4.4-4.6 4.4-8.2 0-5.8-4.8-10.4-11.6-10.4z"/><rect x="9.5" y="36.4" width="26" height="3.8" rx="1.9"/></g><path class="pcd" d="M22.5 20v9M18.6 24.5h7.8"/></symbol>
</defs></svg>`;

document.body.insertAdjacentHTML("afterbegin",PIECE_SPRITE);
const rm=matchMedia('(prefers-reduced-motion: reduce)').matches,$=id=>document.getElementById(id);

window.MV_='e2e4:e4 e7e5:e5 g1f3:Nf3 d7d6:d6 d2d4:d4 c8g4:Bg4 d4e5:dxe5 g4f3:Bxf3 d1f3:Qxf3 d6e5:dxe5 f1c4:Bc4 g8f6:Nf6 f3b3:Qb3 d8e7:Qe7 b1c3:Nc3 c7c6:c6 c1g5:Bg5 b7b5:b5 c3b5:Nxb5 c6b5:cxb5 c4b5:Bxb5+ b8d7:Nbd7 e1c1:O-O-O a8d8:Rd8 d1d7:Rxd7 d8d7:Rxd7 h1d1:Rd1 e7e6:Qe6 b5d7:Bxd7+ f6d7:Nxd7 b3b8:Qb8+ d7b8:Nxb8 d1d8:Rd8#'.split(' ').map(s=>s.split(':'));

const it=$('intro');let seen=0;try{seen=sessionStorage.seen;sessionStorage.seen=1}catch(e){}
if(it&&!rm&&!seen){document.body.classList.add('lock');setTimeout(()=>{it.classList.add('out');document.body.classList.remove('lock')},1500);setTimeout(()=>it.remove(),2300)}else if(it)it.remove();

document.querySelectorAll('.mv').forEach((m,i)=>m.innerHTML='Game '+(i+1)+' &nbsp;·&nbsp; Result <b>'+['1–0','1–0','½–½','1–0'][i]+'</b>');

if(matchMedia('(pointer:fine)').matches&&!rm){const c=$('cur');addEventListener('pointermove',e=>{c.style.transform=`translate(${e.clientX}px,${e.clientY}px)`;c.classList.add('on');c.classList.toggle('big',!!e.target.closest('a,button,.pc,input,textarea'))});
document.querySelectorAll('.btn').forEach(b=>{b.addEventListener('pointermove',e=>{const r=b.getBoundingClientRect();b.style.translate=((e.clientX-r.left-r.width/2)*.18)+'px '+((e.clientY-r.top-r.height/2)*.3)+'px'});b.addEventListener('pointerleave',()=>b.style.translate='')})}
})();
