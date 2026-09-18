(function () {
  'use strict';

  var root = document.documentElement;
  var body = document.body;
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Header shadow on scroll */
  var header = document.querySelector('.site-header');
  if (header) {
    var onScroll = function () { header.classList.toggle('scrolled', window.scrollY > 8); };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* Mobile drawer */
  var toggle = document.querySelector('.menu-toggle');
  var nav = document.getElementById('main-nav');
  var backdrop = document.querySelector('.nav-backdrop');

  function setMenu(open) {
    if (!toggle || !nav) return;
    body.classList.toggle('menu-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Закрыть меню' : 'Открыть меню');
    if (open) {
      var first = nav.querySelector('a');
      if (first) setTimeout(function () { first.focus({ preventScroll: true }); }, 250);
    }
  }

  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      setMenu(!body.classList.contains('menu-open'));
    });
    if (backdrop) backdrop.addEventListener('click', function () { setMenu(false); });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) setMenu(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && body.classList.contains('menu-open')) {
        setMenu(false);
        toggle.focus();
      }
    });
    window.matchMedia('(min-width: 1181px)').addEventListener('change', function (mq) {
      if (mq.matches) setMenu(false);
    });
  }

  /* Active nav item */
  if (nav) {
    var path = location.pathname;
    nav.querySelectorAll('a[href^="/"]').forEach(function (a) {
      var href = a.getAttribute('href');
      if (href.indexOf('#') !== -1 || a.classList.contains('nav-cta')) return;
      if ((href === '/' && path === '/') || (href !== '/' && path.indexOf(href) === 0)) a.classList.add('active');
    });
  }

  /* Reveal on scroll */
  window.__reveal = true;
  var revealEls = document.querySelectorAll('.reveal');
  function revealNow(scope) {
    (scope || document).querySelectorAll('.reveal').forEach(function (el) { el.classList.add('in'); });
  }
  if (revealEls.length && 'IntersectionObserver' in window && !reduceMotion) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.05, rootMargin: '0px 0px -4% 0px' });
    revealEls.forEach(function (el) { io.observe(el); });
    var revealHashTarget = function () {
      if (!location.hash || location.hash.length < 2) return;
      var target = document.getElementById(decodeURIComponent(location.hash.slice(1)));
      if (target) revealNow(target);
    };
    revealHashTarget();
    window.addEventListener('hashchange', revealHashTarget);
  } else {
    revealNow();
  }
  document.querySelectorAll('[data-stagger]').forEach(function (group) {
    Array.prototype.forEach.call(group.children, function (child, i) {
      child.style.setProperty('--d', Math.min(i * 0.08, 0.4) + 's');
    });
  });

  /* Accordions: on phones keep only the first open */
  var usefulCards = document.querySelectorAll('.useful-card');
  if (usefulCards.length && window.matchMedia('(max-width: 900px)').matches) {
    usefulCards.forEach(function (d, i) { if (i > 0) d.removeAttribute('open'); });
  }

  /* Toasts */
  document.querySelectorAll('.toast').forEach(function (t) {
    var close = function () {
      t.classList.add('hide');
      setTimeout(function () { t.remove(); }, 350);
    };
    var btn = t.querySelector('.toast-close');
    if (btn) btn.addEventListener('click', close);
    if (!t.classList.contains('error')) setTimeout(close, 7000);
  });

  /* Forms: prevent double submit */
  document.querySelectorAll('form[data-once]').forEach(function (form) {
    form.addEventListener('submit', function () {
      var btn = form.querySelector('button[type="submit"]');
      if (!btn) return;
      setTimeout(function () {
        btn.disabled = true;
        btn.dataset.label = btn.innerHTML;
        btn.textContent = 'Отправляем…';
      }, 0);
    });
  });

  /* Cookie notice */
  var cookie = document.getElementById('cookie');
  if (cookie) {
    var accepted = false;
    try { accepted = localStorage.getItem('cookies_accepted_v1') === '1'; } catch (e) {}
    if (!accepted) cookie.hidden = false;
    var ok = document.getElementById('cookie-ok');
    if (ok) ok.addEventListener('click', function () {
      try { localStorage.setItem('cookies_accepted_v1', '1'); } catch (e) {}
      cookie.hidden = true;
    });
  }
})();
