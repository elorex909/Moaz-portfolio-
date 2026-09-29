/* Safari-style window bar + macOS window manager */
(()=>{
const skip='nav,.metrics';
const dock = document.createElement('aside');
dock.id = 'dock';
document.body.appendChild(dock);

document.querySelectorAll('main .glass').forEach(el=>{
  if(el.closest(skip)&&!el.matches('.about,.gr,.holo,.card,.binfo,.contact'))return;
  if(el.parentElement&&el.parentElement.classList.contains('metrics'))return;
  const sec=el.closest('section'),h2=sec&&sec.querySelector('h2'),h3=el.querySelector('h3');
  const fixed={about:'About me',gr:'opera-game.pgn',contact:'New message',binfo:'Skills'};
  const key=Object.keys(fixed).find(k=>el.classList.contains(k));
  const title=el.dataset.title||(key?fixed[key]:((h3&&h3.textContent.trim())||(h2&&h2.textContent.trim())||''));
  const bar=document.createElement('div');bar.className='tb';bar.setAttribute('aria-hidden','true');
  bar.innerHTML='<span class="dots"><button class="r" aria-label="Close"></button><button class="y" aria-label="Maximize"></button><button class="g" aria-label="Minimize"></button></span><span class="tt"></span>';
  bar.querySelector('.tt').textContent=title;
  el.classList.add('win');el.prepend(bar);

  const rBtn = bar.querySelector('.r'), yBtn = bar.querySelector('.y'), gBtn = bar.querySelector('.g');
  const FLY_MS = 500;

  // 1-3. Lock tilt, flatten the card and commit that flat state with NO transition.
  function freeze() {
    el.classList.add('win-animating');                       // main.js pointermove/pointerleave return early on this
    el.style.setProperty('transition', 'none', 'important'); // inline !important beats the stylesheet's !important
    el.style.transform = '';                                 // drop perspective/rotateX/rotateY
    el.getAnimations().forEach(a => a.cancel());             // kill any in-flight tilt transition
    void el.offsetWidth;                                     // reflow: the flat state is now the "before" state
  }
  function thaw() { el.style.removeProperty('transition'); } // hand control back to .win.win-animating
  function unfreeze() { el.classList.remove('win-animating'); }

  // Card centre -> dock button centre. Only valid while the card is flat and not minimized.
  function aimAtDock(btn) {
    const r = el.getBoundingClientRect(), d = btn.getBoundingClientRect();
    el.style.setProperty('--tx', `${(d.left + d.width / 2) - (r.left + r.width / 2)}px`);
    el.style.setProperty('--ty', `${(d.top + d.height / 2) - (r.top + r.height / 2)}px`);
  }

  // Run cb when the transform transition ends (timeout fallback if it never fires).
  function afterTransform(cb) {
    let done = false;
    const fin = () => { if (done) return; done = true; clearTimeout(t); el.removeEventListener('transitionend', on); cb(); };
    const on = ev => { if (ev.target === el && ev.propertyName === 'transform') fin(); };
    const t = setTimeout(fin, FLY_MS + 150);
    el.addEventListener('transitionend', on);
  }

  // Close (Red)
  rBtn.onclick = (e) => {
    e.preventDefault(); e.stopPropagation();
    freeze();
    requestAnimationFrame(() => { requestAnimationFrame(() => {
      thaw();
      el.classList.add('win-closed');
      setTimeout(() => { el.style.display = 'none'; unfreeze(); el.classList.remove('win-closed'); }, 500);
    }); });
  };

  // Maximize (Yellow)
  yBtn.onclick = (e) => {
    e.preventDefault(); e.stopPropagation();
    if (el.classList.contains('win-max')) {
      // Un-maximize
      freeze();
      requestAnimationFrame(() => { requestAnimationFrame(() => {
        thaw();
        el.classList.remove('win-max');
        document.body.style.overflow = '';
        document.body.classList.remove('has-max');
        setTimeout(() => { unfreeze(); }, 500);
      }); });
    } else {
      // Maximize
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

  // Minimize (Green)
  gBtn.onclick = (e) => {
    e.preventDefault(); e.stopPropagation();
    if (el.classList.contains('win-animating') || el.classList.contains('win-minimized')) return; // ignore clicks mid-flight
    if (el.classList.contains('win-max')) { el.classList.remove('win-max'); document.body.style.overflow = ''; document.body.classList.remove('has-max'); }

    const dBtn = document.createElement('button');
    dBtn.textContent = title.charAt(0).toUpperCase() || 'W';
    dBtn.title = title;
    dock.appendChild(dBtn);
    dock.classList.add('active');

    freeze();          // tilt off, flat, committed without a transition
    aimAtDock(dBtn);   // measure AFTER flattening: a tilted rect gives a skewed flight path

    requestAnimationFrame(() => {
      thaw();                                   // transition is back on...
      el.classList.add('win-minimized');        // ...and this change now animates from flat
      afterTransform(() => { el.style.visibility = 'hidden'; unfreeze(); });
    });

    // Restore on dock click
    dBtn.onclick = () => {
      if (el.classList.contains('win-animating')) return;
      el.classList.add('win-animating');
      el.style.setProperty('transition', 'none', 'important');
      el.style.visibility = '';
      // Re-aim: scroll or other dock changes may have moved the card or the button since minimizing.
      el.classList.remove('win-minimized'); void el.offsetWidth;   // measure the card at its natural spot
      aimAtDock(dBtn);
      el.classList.add('win-minimized'); void el.offsetWidth;      // back to the docked pose (no paint in between)

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
