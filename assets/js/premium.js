(function(){
if(matchMedia('(prefers-reduced-motion:reduce)').matches)return;
document.documentElement.classList.add('js');
var els=[].slice.call(document.querySelectorAll('main h2,main .glass:not(.tilt):not(.metrics .glass),.marq'));
els.forEach(function(e){e.classList.add('rv')});
[].forEach.call(document.querySelectorAll('.tilt'),function(e){e.classList.add('rv2')});
var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}})},{threshold:.12,rootMargin:'0px 0px -6% 0px'});
document.querySelectorAll('.rv,.rv2').forEach(function(e){io.observe(e)});

var twEls = document.querySelectorAll('main h2, main .lead');
twEls.forEach(function(el){el.dataset.tw = el.textContent;el.textContent = '';el.classList.add('tw-wait');});
var twIo = new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){twIo.unobserve(x.target);x.target.classList.remove('tw-wait');x.target.classList.add('tw-typing');var txt = x.target.dataset.tw;var i = 0;var timer = setInterval(function(){x.target.textContent += txt.charAt(i);i++;if(i >= txt.length){clearInterval(timer);x.target.classList.remove('tw-typing');}}, x.target.tagName==='H2'? 70 : 35);}})},{threshold:.4,rootMargin:'0px 0px -5% 0px'});
twEls.forEach(function(e){twIo.observe(e)});

var heroEls = document.querySelectorAll('#top h1 .gold, #top h1 .cyan, #top .tl, #top .mut2, #top .sub');
heroEls.forEach(function(el){el.dataset.tw = el.textContent;el.textContent = '';el.classList.add('tw-wait');});
function typeHero(els, i, delay) {
  if(i >= els.length) return;
  setTimeout(function(){
    var el = els[i];
    el.classList.remove('tw-wait');
    el.classList.add('tw-typing');
    var txt = el.dataset.tw, j = 0;
    var speed = (el.tagName === 'SPAN') ? 70 : 35;
    var timer = setInterval(function(){
      el.textContent += txt.charAt(j);
      j++;
      if(j >= txt.length){
        clearInterval(timer);
        el.classList.remove('tw-typing');
        typeHero(els, i+1, 200);
      }
    }, speed);
  }, delay);
}
var heroDelay = sessionStorage.getItem('hero_tw') ? 0 : 1600;
sessionStorage.setItem('hero_tw', 1);
typeHero(heroEls, 0, heroDelay);

var h=document.querySelector('#top>div:not(.floor):not(.stage)');
if(h)addEventListener('scroll',function(){var y=scrollY;if(y<innerHeight)h.style.transform='translateY('+(y*.12)+'px)';h.style.opacity=Math.max(0,1-y/(innerHeight*.9))},{passive:true});
})();
