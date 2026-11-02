const burger = document.getElementById('burger');
const nav = document.getElementById('nav');
const navOverlay = document.getElementById('navOverlay');
const navClose = document.getElementById('navClose');

const openMenu = () => {
    if (nav) nav.classList.add('active');
    document.body.style.overflow = 'hidden';
};

const closeMenu = () => {
    if (nav) nav.classList.remove('active');
    document.body.style.overflow = '';
};

if (burger) {
    burger.addEventListener('click', openMenu);
}
if (navOverlay) {
    navOverlay.addEventListener('click', closeMenu);
}
if (navClose) {
    navClose.addEventListener('click', closeMenu);
}

const navLinks = document.querySelectorAll('.nav__link');
navLinks.forEach(link => {
    link.addEventListener('click', closeMenu);
});

const scrollTopBtn = document.getElementById('scrollTop');
const toggleScrollTop = () => {
    if (scrollTopBtn) scrollTopBtn.classList.toggle('show', window.scrollY > 600);
};

if (scrollTopBtn) {
    window.addEventListener('scroll', toggleScrollTop, { passive: true });
    toggleScrollTop();
    scrollTopBtn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
}

const track = (name) => {
    if (typeof ym === 'function') ym(114024474, 'reachGoal', name);
    if (typeof gtag === 'function') gtag('event', name);
};

document.addEventListener('click', (e) => {
    const link = e.target.closest('a');
    if (!link) return;
    const href = link.getAttribute('href') || '';
    if (href.startsWith('tel:')) track('phone_click');
    else if (href.startsWith('viber://')) track('viber_click');
    else if (href.indexOf('wa.me') !== -1) track('whatsapp_click');
    else if (href.indexOf('t.me') !== -1) track('telegram_click');
    else if (href.indexOf('#order') !== -1) track('order_click');
});

const feedbackForm = document.querySelector('.feedback-form');
if (feedbackForm) {
    feedbackForm.addEventListener('submit', () => track('lead_submit'));
}

if (document.querySelector('.messages .message--success')) {
    track('lead_success');
}
