// main.js

// Частицы
document.addEventListener('DOMContentLoaded', () => {
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

  // Галерея: клик → убрать блюр + модалка
  const galleryItems = document.querySelectorAll('.gallery-item');
  galleryItems.forEach(item => {
    item.addEventListener('click', () => {
      item.classList.add('revealed');
      const imgUrl = item.getAttribute('data-modal-src');
      if (imgUrl) {
        const modal = document.getElementById('imageModal');
        const modalImg = document.getElementById('modalImage');
        modalImg.src = imgUrl;
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
      }
    });
  });

  // Закрытие модального окна
  const modal = document.getElementById('imageModal');
  const closeModalBtn = document.getElementById('closeModal');
  
  if (closeModalBtn) {
    closeModalBtn.addEventListener('click', () => {
      modal.classList.remove('active');
      document.body.style.overflow = 'auto';
    });
  }

  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        modal.classList.remove('active');
        document.body.style.overflow = 'auto';
      }
    });
  }

  // Theme toggle
  const themeToggle = document.getElementById('themeToggle');
  const themeIcon = themeToggle ? themeToggle.querySelector('i') : null;

  if (themeToggle && themeIcon) {
    themeToggle.addEventListener('click', () => {
      const isDark = document.body.getAttribute('data-theme') === 'dark';
      document.body.setAttribute('data-theme', isDark ? 'light' : 'dark');
      themeIcon.className = isDark ? 'fas fa-moon' : 'fas fa-sun';
    });
  }

  // Форма
  const contactForm = document.getElementById('contactForm');
  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();
      alert('✅ Спасибо за заявку!\n\nАдминистратор свяжется с вами в течение 24 часов.');
      contactForm.reset();
    });
  }
});