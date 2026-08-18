const progress = document.getElementById('progress');

window.addEventListener('scroll', () => {
  const max = document.documentElement.scrollHeight - window.innerHeight;
  progress.style.width = `${max > 0 ? (window.scrollY / max) * 100 : 0}%`;
}, {passive:true});

/* Мобильное меню */
const burger = document.getElementById('burger');
const mobileNav = document.getElementById('mobile-nav');
const desktop = window.matchMedia('(min-width: 821px)');

const setNav = (open) => {
  burger.setAttribute('aria-expanded', String(open));
  burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  mobileNav.hidden = !open;
  document.body.classList.toggle('nav-open', open);
};

burger.addEventListener('click', () => setNav(burger.getAttribute('aria-expanded') !== 'true'));

/* Уход по якорю закрывает меню */
mobileNav.addEventListener('click', (e) => { if (e.target.closest('a')) setNav(false); });

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && burger.getAttribute('aria-expanded') === 'true') {
    setNav(false);
    burger.focus();
  }
});

/* На десктопе меню не должно оставаться открытым и блокировать скролл */
desktop.addEventListener('change', (e) => { if (e.matches) setNav(false); });

setNav(false);
