
(()=>{
const skip='nav,.metrics';
const dock = document.createElement('aside');
dock.id = 'dock';
document.body.appendChild(dock);

document.querySelectorAll('main .glass').forEach(el=>{
  if(el.closest(skip)&&!el.matches('.about,.gr,.holo,.card,.binfo,.contact'))return;
  if(el.parentElement&&el.parentElement.classList.contains('metrics'))return;
  const sec=el.closest('section'),h2=sec&&sec.querySelector('h2'),h3=el.querySelector('h3');
  const fixed={about:'About me',contact:'New message',binfo:'Skills'};
  const key=Object.keys(fixed).find(k=>el.classList.contains(k));
  const title=el.dataset.title||(key?fixed[key]:((h3&&h3.textContent.trim())||(h2&&h2.textContent.trim())||''));
  const bar=document.createElement('div');bar.className='tb';bar.setAttribute('aria-hidden','true');
  bar.innerHTML='<span class="dots"><button class="r" aria-label="Close"></button><button class="y" aria-label="Maximize"></button><button class="g" aria-label="Minimize"></button></span><span class="tt"></span>';
  bar.querySelector('.tt').textContent=title;
  el.classList.add('win');el.prepend(bar);

  const rBtn = bar.querySelector('.r'), yBtn = bar.querySelector('.y'), gBtn = bar.querySelector('.g');
  const FLY_MS = 500;

  function freeze() {
    el.classList.add('win-animating');
    el.style.setProperty('transition', 'none', 'important');
    el.style.transform = '';
    el.getAnimations().forEach(a => a.cancel());
    void el.offsetWidth;
  }
  function thaw() { el.style.removeProperty('transition'); }
  function unfreeze() { el.classList.remove('win-animating'); }

  function aimAtDock(btn) {
    const r = el.getBoundingClientRect(), d = btn.getBoundingClientRect();
    el.style.setProperty('--tx', `${(d.left + d.width / 2) - (r.left + r.width / 2)}px`);
    el.style.setProperty('--ty', `${(d.top + d.height / 2) - (r.top + r.height / 2)}px`);
  }

  function afterTransform(cb) {
    let done = false;
    const fin = () => { if (done) return; done = true; clearTimeout(t); el.removeEventListener('transitionend', on); cb(); };
    const on = ev => { if (ev.target === el && ev.propertyName === 'transform') fin(); };
    const t = setTimeout(fin, FLY_MS + 150);
    el.addEventListener('transitionend', on);
  }

  rBtn.onclick = (e) => {
    e.preventDefault(); e.stopPropagation();
    freeze();
    requestAnimationFrame(() => { requestAnimationFrame(() => {
      thaw();
      el.classList.add('win-closed');
      setTimeout(() => { el.style.display = 'none'; unfreeze(); el.classList.remove('win-closed'); }, 500);
    }); });
  };

  yBtn.onclick = (e) => {
    e.preventDefault(); e.stopPropagation();
    if (el.classList.contains('win-max')) {
      freeze();
      requestAnimationFrame(() => { requestAnimationFrame(() => {
        thaw();
        el.classList.remove('win-max');
        document.body.style.overflow = '';
        document.body.classList.remove('has-max');
        setTimeout(() => { unfreeze(); }, 500);
      }); });
    } else {
      freeze();
      requestAnimationFrame(() => { requestAnimationFrame(() => {
        thaw();
        el.classList.add('win-max');
        document.body.style.overflow = 'hidden';
        document.body.classList.add('has-max');
        setTimeout(() => { unfreeze(); }, 500);
      }); });
    }
  };

  gBtn.onclick = (e) => {
    e.preventDefault(); e.stopPropagation();
    if (el.classList.contains('win-animating') || el.classList.contains('win-minimized')) return;
    if (el.classList.contains('win-max')) { el.classList.remove('win-max'); document.body.style.overflow = ''; document.body.classList.remove('has-max'); }

    const dBtn = document.createElement('button');
    dBtn.textContent = title.charAt(0).toUpperCase() || 'W';
    dBtn.title = title;
    dock.appendChild(dBtn);
    dock.classList.add('active');

    freeze();
    aimAtDock(dBtn);

    requestAnimationFrame(() => {
      thaw();
      el.classList.add('win-minimized');
      afterTransform(() => { el.style.visibility = 'hidden'; unfreeze(); });
    });

    dBtn.onclick = () => {
      if (el.classList.contains('win-animating')) return;
      el.classList.add('win-animating');
      el.style.setProperty('transition', 'none', 'important');
      el.style.visibility = '';
      el.classList.remove('win-minimized'); void el.offsetWidth;
      aimAtDock(dBtn);
      el.classList.add('win-minimized'); void el.offsetWidth;

      dBtn.remove();
      if (dock.children.length === 0) dock.classList.remove('active');

      requestAnimationFrame(() => {
        thaw();
        el.classList.remove('win-minimized');
        afterTransform(unfreeze);
      });
    };
  };
});
})();
