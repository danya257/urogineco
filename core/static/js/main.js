/* main.js — urogineco redesign v4 "motion" */
(function () {
  'use strict';
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  document.addEventListener('DOMContentLoaded', function () {
    headerAndProgress();
    ambientParticles();
    revealOnScroll();
    countUp();
    if (!reduced) magneticButtons();
    mobileMenu();
    smoothScroll();
  });

  /* ---------- Header scroll state + progress bar ---------- */
  var header = document.querySelector('header');
  var progress = document.getElementById('scrollProgress');
  var heroC = document.querySelector('#hero .container');
  function onScroll() {
    var y = window.scrollY || document.documentElement.scrollTop || 0;
    if (header) header.classList.toggle('scrolled', y > 60);
    if (progress) {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      progress.style.width = (h > 0 ? (y / h) * 100 : 0) + '%';
    }
    if (!reduced && heroC && y < window.innerHeight) {
      heroC.style.transform = 'translateY(' + (y * 0.22) + 'px)';
      heroC.style.opacity = String(Math.max(0, 1 - (y / window.innerHeight) * 1.1));
    }
  }
  function headerAndProgress() {
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ---------- Ambient particles ---------- */
  function ambientParticles() {
    if (reduced) return;
    var box = document.getElementById('particles');
    if (!box) return;
    for (var i = 0; i < 14; i++) {
      var p = document.createElement('div');
      p.className = 'particle';
      var s = Math.random() * 90 + 30;
      p.style.width = p.style.height = s + 'px';
      p.style.left = Math.random() * 100 + '%';
      p.style.top = Math.random() * 100 + '%';
      p.style.animationDuration = (Math.random() * 22 + 16) + 's';
      p.style.animationDelay = (-Math.random() * 20) + 's';
      box.appendChild(p);
    }
  }

  /* ---------- Reveal on scroll (staggered) ---------- */
  function revealOnScroll() {
    var sel = '.spec-card, .useful-block, section:not(#hero) > .container > h2,' +
              ' #about .container > p, #events-preview h3, #contact .footer-wrap > *';
    var els = Array.prototype.slice.call(document.querySelectorAll(sel));
    if (!els.length) return;
    // stagger inside grids
    document.querySelectorAll('.spec-grid').forEach(function (grid) {
      Array.prototype.slice.call(grid.children).forEach(function (c, i) {
        c.dataset.delay = (Math.min(i, 6) * 80) + 'ms';
      });
    });
    if (reduced || !('IntersectionObserver' in window)) {
      els.forEach(function (el) { el.classList.add('reveal', 'visible'); });
      return;
    }
    els.forEach(function (el) { el.classList.add('reveal'); });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (ent) {
        if (ent.isIntersecting) {
          ent.target.style.transitionDelay = ent.target.dataset.delay || '0ms';
          ent.target.classList.add('visible');
          io.unobserve(ent.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
    els.forEach(function (el) { io.observe(el); });
  }

  /* ---------- Count-up numbers ---------- */
  function countUp() {
    var nums = document.querySelectorAll('.stat-num[data-count]');
    if (!nums.length) return;
    if (reduced || !('IntersectionObserver' in window)) {
      nums.forEach(function (el) { el.textContent = (el.dataset.count || '') + (el.dataset.suffix || ''); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (ent) {
        if (!ent.isIntersecting) return;
        var el = ent.target; io.unobserve(el);
        var target = parseFloat(el.dataset.count) || 0;
        var suffix = el.dataset.suffix || '';
        var dur = 1700, startT = null;
        function step(ts) {
          if (startT === null) startT = ts;
          var p = Math.min((ts - startT) / dur, 1);
          var eased = 1 - Math.pow(1 - p, 3);
          el.textContent = Math.round(target * eased) + suffix;
          if (p < 1) requestAnimationFrame(step);
        }
        requestAnimationFrame(step);
      });
    }, { threshold: 0.5 });
    nums.forEach(function (n) { io.observe(n); });
  }

  /* ---------- Magnetic buttons ---------- */
  function magneticButtons() {
    document.querySelectorAll('.btn').forEach(function (btn) {
      btn.addEventListener('mousemove', function (e) {
        var r = btn.getBoundingClientRect();
        var mxx = e.clientX - r.left - r.width / 2;
        var myy = e.clientY - r.top - r.height / 2;
        btn.style.transform = 'translate(' + (mxx * 0.18) + 'px,' + (myy * 0.3) + 'px)';
      });
      btn.addEventListener('mouseleave', function () { btn.style.transform = ''; });
    });
  }

  /* ---------- Mobile menu ---------- */
  function mobileMenu() {
    var toggle = document.querySelector('.mobile-menu-toggle');
    var nav = document.getElementById('main-nav');
    if (!toggle || !nav) return;
    function setIcon(open) {
      var ic = toggle.querySelector('i');
      if (!ic) return;
      ic.classList.toggle('fa-bars', !open);
      ic.classList.toggle('fa-times', open);
    }
    function openMenu() {
      nav.classList.add('active'); document.body.classList.add('menu-open'); setIcon(true);
      if (lenis) lenis.stop();
    }
    function closeMenu() {
      nav.classList.remove('active'); document.body.classList.remove('menu-open'); setIcon(false);
      if (lenis) lenis.start();
    }
    toggle.addEventListener('click', function (e) {
      e.stopPropagation(); e.preventDefault();
      if (nav.classList.contains('active')) closeMenu(); else openMenu();
    });
    document.addEventListener('click', function (e) {
      if (nav.classList.contains('active') && !nav.contains(e.target) && !toggle.contains(e.target)) closeMenu();
    });
    nav.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', closeMenu); });
    window.addEventListener('resize', function () {
      if (window.innerWidth > 1200 && nav.classList.contains('active')) closeMenu();
    });
  }

  /* ---------- Smooth scroll (Lenis) + anchors ---------- */
  var lenis = null;
  function smoothScroll() {
    if (!reduced && window.Lenis) {
      lenis = new window.Lenis({ duration: 1.1, smoothWheel: true, wheelMultiplier: 0.9 });
      function raf(t) { lenis.raf(t); requestAnimationFrame(raf); }
      requestAnimationFrame(raf);
      lenis.on('scroll', onScroll);
    }
    document.querySelectorAll('a[href^="#"], a[href^="/#"]').forEach(function (link) {
      link.addEventListener('click', function (e) {
        var href = link.getAttribute('href');
        var onHome = location.pathname === '/' || location.pathname === '';
        var hash = href.indexOf('/#') === 0 ? href.slice(1) : href;
        if (href.indexOf('/#') === 0 && !onHome) return;
        if (!hash || hash === '#') return;
        var t = document.querySelector(hash);
        if (t) {
          e.preventDefault();
          if (lenis) lenis.scrollTo(t, { offset: -70 });
          else t.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    });
  }

  /* ---------- 3D hero: breathing particle sphere ---------- */
  function heroScene() {
    var canvas = document.getElementById('hero-canvas');
    if (!canvas || !window.THREE) return;
    var renderer;
    try {
      renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
    } catch (e) { return; }
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));

    var scene = new THREE.Scene();
    var camera = new THREE.PerspectiveCamera(60, 1, 0.1, 100);
    camera.position.z = 14;

    var COUNT = 2600, R = 6.2;
    var geo = new THREE.BufferGeometry();
    var pos = new Float32Array(COUNT * 3);
    var base = new Float32Array(COUNT * 3);
    var col = new Float32Array(COUNT * 3);
    var cA = new THREE.Color(0x6FE0E0), cB = new THREE.Color(0x1F6E78);
    for (var i = 0; i < COUNT; i++) {
      var t = i / COUNT;
      var inc = Math.acos(1 - 2 * t);
      var az = Math.PI * (1 + Math.sqrt(5)) * i;
      var x = R * Math.sin(inc) * Math.cos(az);
      var y = R * Math.sin(inc) * Math.sin(az);
      var z = R * Math.cos(inc);
      pos[i * 3] = base[i * 3] = x;
      pos[i * 3 + 1] = base[i * 3 + 1] = y;
      pos[i * 3 + 2] = base[i * 3 + 2] = z;
      var c = cA.clone().lerp(cB, (y / R + 1) / 2);
      col[i * 3] = c.r; col[i * 3 + 1] = c.g; col[i * 3 + 2] = c.b;
    }
    geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    geo.setAttribute('color', new THREE.BufferAttribute(col, 3));
    var mat = new THREE.PointsMaterial({
      size: 0.07, vertexColors: true, transparent: true, opacity: 0.92,
      blending: THREE.AdditiveBlending, depthWrite: false
    });
    var points = new THREE.Points(geo, mat);
    scene.add(points);

    var wire = new THREE.Mesh(
      new THREE.IcosahedronGeometry(4.0, 1),
      new THREE.MeshBasicMaterial({ color: 0x46C2C9, wireframe: true, transparent: true, opacity: 0.07 })
    );
    scene.add(wire);

    var mx = 0, my = 0, tmx = 0, tmy = 0;
    window.addEventListener('mousemove', function (e) {
      tmx = e.clientX / window.innerWidth - 0.5;
      tmy = e.clientY / window.innerHeight - 0.5;
    });

    function resize() {
      var w = canvas.clientWidth || canvas.offsetWidth;
      var h = canvas.clientHeight || canvas.offsetHeight;
      if (!w || !h) return;
      renderer.setSize(w, h, false);
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
    }
    resize();
    window.addEventListener('resize', resize);

    var running = true;
    document.addEventListener('visibilitychange', function () { running = !document.hidden; });

    var arr = geo.attributes.position.array;
    function animate(time) {
      requestAnimationFrame(animate);
      if (!running) return;
      var s = time * 0.0004;
      for (var i = 0; i < COUNT; i++) {
        var bx = base[i * 3], by = base[i * 3 + 1], bz = base[i * 3 + 2];
        var n = Math.sin(s * 2 + bx * 0.6 + by * 0.4) * 0.35 + Math.cos(s * 1.5 + bz * 0.5) * 0.25;
        var k = 1 + n * 0.06;
        arr[i * 3] = bx * k; arr[i * 3 + 1] = by * k; arr[i * 3 + 2] = bz * k;
      }
      geo.attributes.position.needsUpdate = true;
      points.rotation.y = s * 0.6;
      points.rotation.x = Math.sin(s * 0.3) * 0.15;
      wire.rotation.y = -s * 0.4;
      wire.rotation.x = s * 0.2;
      mx += (tmx - mx) * 0.05; my += (tmy - my) * 0.05;
      camera.position.x = mx * 3; camera.position.y = -my * 2;
      camera.lookAt(0, 0, 0);
      renderer.render(scene, camera);
    }
    requestAnimationFrame(animate);
  }
})();
