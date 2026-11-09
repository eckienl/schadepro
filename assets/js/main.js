(() => {
  // Header bij scrollen
  const header = document.querySelector('.header');
  const onScroll = () => header.classList.toggle('is-scrolled', window.scrollY > 40);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  // Mobiel menu
  const burger = document.getElementById('burger');
  const nav = document.getElementById('nav');
  const setMenu = (open) => {
    nav.classList.toggle('is-open', open);
    burger.setAttribute('aria-expanded', String(open));
    burger.setAttribute('aria-label', open ? 'Menu sluiten' : 'Menu openen');
    document.body.style.overflow = open ? 'hidden' : '';
  };
  burger.addEventListener('click', () => setMenu(!nav.classList.contains('is-open')));
  nav.querySelectorAll('a').forEach((a) => a.addEventListener('click', () => setMenu(false)));
  nav.querySelectorAll('.nav__toggle').forEach((t) => t.addEventListener('click', () => {
    const sub = t.nextElementSibling;
    const open = !sub.classList.contains('is-open');
    sub.classList.toggle('is-open', open);
    t.setAttribute('aria-expanded', String(open));
  }));

  // Reveal-animaties
  const els = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e, i) => {
        if (e.isIntersecting) {
          e.target.style.transitionDelay = `${(i % 4) * 80}ms`;
          e.target.classList.add('is-in');
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    els.forEach((el) => io.observe(el));
  } else {
    els.forEach((el) => el.classList.add('is-in'));
  }

  // Lightbox
  const lb = document.getElementById('lightbox');
  const lbImg = lb.querySelector('img');
  const close = () => { lb.hidden = true; lbImg.src = ''; };
  document.querySelectorAll('[data-lightbox]').forEach((a) => {
    a.addEventListener('click', (e) => {
      e.preventDefault();
      lbImg.src = a.getAttribute('href');
      lbImg.alt = a.querySelector('img')?.alt || '';
      lb.hidden = false;
    });
  });
  lb.addEventListener('click', (e) => { if (e.target !== lbImg) close(); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') { close(); setMenu(false); } });

  // Contactformulier -> e-mail
  const form = document.getElementById('form');
  const err = document.getElementById('formError');
  if (form) form.addEventListener('submit', (e) => {
    e.preventDefault();
    const d = new FormData(form);
    let ok = true;
    ['naam', 'bericht'].forEach((n) => {
      const f = form.elements[n];
      const bad = !String(d.get(n) || '').trim();
      f.classList.toggle('is-invalid', bad);
      if (bad) ok = false;
    });
    if (!ok) { err.textContent = 'Vul a.u.b. uw naam en uw vraag in.'; return; }
    err.textContent = '';
    const subject = `Adviesaanvraag ${d.get('dienst')} – ${d.get('naam')}`;
    const body = [
      `Naam: ${d.get('naam')}`,
      `Telefoon: ${d.get('telefoon') || '-'}`,
      `Plaats: ${d.get('plaats') || '-'}`,
      `Klant: ${d.get('type')}`,
      `Soort klus: ${d.get('dienst')}`,
      '',
      String(d.get('bericht')),
    ].join('\n');
    window.location.href = `mailto:schadepro@ziggo.nl?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
  });

  document.getElementById('year').textContent = new Date().getFullYear();
})();
