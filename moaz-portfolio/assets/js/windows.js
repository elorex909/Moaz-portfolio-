/* Safari-style window bar (red, yellow, green) on every glass panel */
(()=>{
const skip='nav,.metrics';
document.querySelectorAll('main .glass').forEach(el=>{
  if(el.closest(skip)&&!el.matches('.about,.gr,.holo,.card,.binfo,.contact'))return;
  if(el.parentElement&&el.parentElement.classList.contains('metrics'))return;
  const sec=el.closest('section'),h2=sec&&sec.querySelector('h2'),h3=el.querySelector('h3');
  const fixed={about:'About me',gr:'opera-game.pgn',contact:'New message',binfo:'Skills'};
  const key=Object.keys(fixed).find(k=>el.classList.contains(k));
  const title=el.dataset.title||(key?fixed[key]:((h3&&h3.textContent.trim())||(h2&&h2.textContent.trim())||''));
  const bar=document.createElement('div');bar.className='tb';bar.setAttribute('aria-hidden','true');
  bar.innerHTML='<span class="dots"><i class="r"></i><i class="y"></i><i class="g"></i></span><span class="tt"></span>';
  bar.querySelector('.tt').textContent=title;
  el.classList.add('win');el.prepend(bar);
});
})();
