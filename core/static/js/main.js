// main.js — Doctor Gvozdev site

document.addEventListener('DOMContentLoaded', () => {

  // ---- Scroll reveal ----
  const revealEls = document.querySelectorAll(
    'section, .card, .review-card, .clinic-card, .event-card, .useful-card, .blog-item, .stat-box, .hero-media, .hero-content'
  );
  revealEls.forEach(el => el.classList.add('reveal'));

  const io = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });

  revealEls.forEach(el => io.observe(el));

  // ---- Smooth-scroll for in-page anchors ----
  document.querySelectorAll('a[href^="#"], a[href^="/#"]').forEach(link => {
    link.addEventListener('click', (e) => {
      const href = link.getAttribute('href');
      const isHome = location.pathname === '/' || location.pathname === '';
      const hash = href.startsWith('/#') ? href.slice(1) : href;
      if (href.startsWith('/#') && !isHome) return;
      if (!hash || hash === '#') return;
      const target = document.querySelector(hash);
      if (!target) return;
      e.preventDefault();
      const top = target.getBoundingClientRect().top + window.pageYOffset - 80;
      window.scrollTo({ top, behavior: 'smooth' });
      history.pushState(null, '', hash);
    });
  });

  // ---- Mobile drawer menu ----
  const toggle = document.querySelector('.mobile-menu-toggle');
  const nav = document.getElementById('main-nav');
  const body = document.body;

  const closeMenu = () => {
    if (!nav || !toggle) return;
    nav.classList.remove('active');
    body.classList.remove('menu-open');
    toggle.setAttribute('aria-expanded', 'false');
    const icon = toggle.querySelector('i');
    if (icon) { icon.classList.remove('fa-times'); icon.classList.add('fa-bars'); }
  };

  if (toggle && nav) {
    toggle.addEventListener('click', (e) => {
      e.stopPropagation();
      const isOpen = nav.classList.toggle('active');
      body.classList.toggle('menu-open', isOpen);
      toggle.setAttribute('aria-expanded', String(isOpen));
      const icon = toggle.querySelector('i');
      if (icon) {
        icon.classList.toggle('fa-bars', !isOpen);
        icon.classList.toggle('fa-times', isOpen);
      }
    });

    document.addEventListener('click', (e) => {
      if (!nav.contains(e.target) && !toggle.contains(e.target)) closeMenu();
    });

    nav.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', closeMenu);
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closeMenu();
    });

    window.addEventListener('resize', () => {
      if (window.innerWidth > 900) closeMenu();
    });
  }

  // ---- Contact form (only on home) ----
  const form = document.getElementById('contactForm');
  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const name = form.name.value.trim();
      const phone = form.phone.value.trim();
      const message = form.message.value.trim();
      if (!name || !phone || !message) {
        alert('Пожалуйста, заполните все поля.');
        return;
      }
      const btn = form.querySelector('button[type=submit]');
      const original = btn ? btn.innerHTML : null;
      if (btn) { btn.innerHTML = 'Отправка…'; btn.disabled = true; }
      setTimeout(() => {
        alert('✓ Спасибо за заявку! Администратор свяжется с вами в течение 24 часов.');
        form.reset();
        if (btn) { btn.innerHTML = original; btn.disabled = false; }
      }, 400);
    });
  }
});
