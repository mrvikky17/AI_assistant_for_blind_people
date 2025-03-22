document.addEventListener('DOMContentLoaded', () => {
    // Animate on scroll if needed in future (e.g., testimonials, features)
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
        }
      });
    });
  
    document.querySelectorAll('.fade-in').forEach(el => {
      observer.observe(el);
    });
  });
  