// ── Mobile nav toggle ──
const toggle = document.querySelector('.nav-toggle');
const navLinks = document.querySelector('.nav-links');

toggle.addEventListener('click', () => {
  const open = navLinks.classList.toggle('open');
  toggle.setAttribute('aria-expanded', open);
});
navLinks.querySelectorAll('a').forEach(a => {
  a.addEventListener('click', () => {
    navLinks.classList.remove('open');
    toggle.setAttribute('aria-expanded', false);
  });
});

// ── Active nav highlight on scroll ──
const sections = document.querySelectorAll('section[id]');
const navAs = document.querySelectorAll('.nav-links a[href^="#"]');

new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting)
      navAs.forEach(a => a.classList.toggle('active', a.getAttribute('href') === '#' + e.target.id));
  });
}, { rootMargin: '-40% 0px -55% 0px' }).observe && sections.forEach(s =>
  new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting)
        navAs.forEach(a => a.classList.toggle('active', a.getAttribute('href') === '#' + e.target.id));
    });
  }, { rootMargin: '-40% 0px -55% 0px' }).observe(s)
);

// ── Scroll reveal ──
const revealObserver = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('visible'); revealObserver.unobserve(e.target); }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

// ── Stat counters ──
function easeOut(t) { return 1 - Math.pow(1 - t, 3); }

function animateStat(el) {
  const target = +el.dataset.target;
  const suffix = el.dataset.suffix || '';
  const duration = 1500;
  const start = performance.now();
  (function step(now) {
    const p = Math.min((now - start) / duration, 1);
    const v = Math.round(easeOut(p) * target);
    el.textContent = (target >= 1000 ? v.toLocaleString() : v) + suffix;
    if (p < 1) requestAnimationFrame(step);
  })(start);
}

new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) { animateStat(e.target); statObs.unobserve(e.target); }
  });
}, { threshold: 0.5 });

const statObs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) { animateStat(e.target); statObs.unobserve(e.target); }
  });
}, { threshold: 0.5 });
document.querySelectorAll('.stat-num').forEach(el => statObs.observe(el));

// ── Contact form ──
const form = document.getElementById('contactForm');
const successMsg = document.getElementById('formSuccess');

form.addEventListener('submit', async e => {
  e.preventDefault();
  const btn = form.querySelector('.btn-send');
  btn.textContent = 'Sending…';
  btn.disabled = true;
  try {
    const res = await fetch(form.action, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } });
    if (res.ok) { form.reset(); successMsg.hidden = false; btn.textContent = 'Sent ✓'; }
    else { btn.textContent = 'Try again'; btn.disabled = false; }
  } catch { btn.textContent = 'Try again'; btn.disabled = false; }
});
