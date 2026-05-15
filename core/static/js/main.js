// main.js

document.addEventListener('DOMContentLoaded', () => {
  // Частицы
  const particlesContainer = document.getElementById('particles');
  if (particlesContainer) {
    for (let i = 0; i < 15; i++) {
      const particle = document.createElement('div');
      particle.classList.add('particle');
      const size = Math.random() * 50 + 10;
      particle.style.width = `${size}px`;
      particle.style.height = `${size}px`;
      particle.style.top = `${Math.random() * 100}%`;
      particle.style.left = `${Math.random() * 100}%`;
      particle.style.animationDuration = `${Math.random() * 25 + 10}s`;
      particle.style.animationDelay = `${Math.random() * 5}s`;
      particlesContainer.appendChild(particle);
    }
  }

  // Анимация при скролле
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        entry.target.style.transitionDelay = `${i * 0.1}s`;
        entry.target.classList.add('visible');
      }
    });
  }, { threshold: 0.15 });

  document.querySelectorAll('section').forEach(section => {
    observer.observe(section);
  });

  // Плавный скролл по якорям
  document.querySelectorAll('a[href^="#"], a[href^="/#"]').forEach(link => {
    link.addEventListener('click', (e) => {
      const href = link.getAttribute('href');
      const isOnHome = location.pathname === '/' || location.pathname === '';
      let hash = href.startsWith('/#') ? href.slice(1) : href;
      if (href.startsWith('/#') && !isOnHome) return; // переход на главную с якорем
      if (!hash || hash === '#') return;
      const target = document.querySelector(hash);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // === Мобильное меню ===
  const mobileToggle = document.querySelector('.mobile-menu-toggle');
  const nav = document.getElementById('main-nav');

  const closeMenu = () => {
    if (!nav || !mobileToggle) return;
    nav.classList.remove('active');
    const icon = mobileToggle.querySelector('i');
    if (icon) {
      icon.classList.remove('fa-times');
      icon.classList.add('fa-bars');
    }
  };

  if (mobileToggle && nav) {
    mobileToggle.addEventListener('click', (e) => {
      e.stopPropagation();
      e.preventDefault();
      nav.classList.toggle('active');
      const icon = mobileToggle.querySelector('i');
      if (icon) {
        if (nav.classList.contains('active')) {
          icon.classList.remove('fa-bars');
          icon.classList.add('fa-times');
        } else {
          icon.classList.remove('fa-times');
          icon.classList.add('fa-bars');
        }
      }
    });

    document.addEventListener('click', (e) => {
      if (!nav.contains(e.target) && !mobileToggle.contains(e.target)) {
        closeMenu();
      }
    });

    nav.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', closeMenu);
    });

    window.addEventListener('resize', () => {
      if (window.innerWidth > 768 && nav.classList.contains('active')) {
        closeMenu();
      }
    });
  }
});
