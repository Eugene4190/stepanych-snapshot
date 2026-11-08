const burger = document.getElementById('burger');
const nav = document.getElementById('nav');
const navOverlay = document.getElementById('navOverlay');
const navClose = document.getElementById('navClose');

const openMenu = () => {
    if (nav) nav.classList.add('active');
    if (burger) burger.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
};

const closeMenu = () => {
    if (nav) nav.classList.remove('active');
    if (burger) burger.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
};

if (burger) {
    burger.setAttribute('aria-expanded', 'false');
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

const analyticsConfig = window.SITE_ANALYTICS || {};
const consentKey = 'cookie_consent';
let analyticsLoaded = false;

const loadAnalytics = () => {
    if (analyticsLoaded) return;
    analyticsLoaded = true;

    if (analyticsConfig.metricaId) {
        (function (m, e, t, r, i, k, a) {
            m[i] = m[i] || function () { (m[i].a = m[i].a || []).push(arguments); };
            m[i].l = 1 * new Date();
            for (let j = 0; j < document.scripts.length; j++) {
                if (document.scripts[j].src === r) return;
            }
            k = e.createElement(t);
            a = e.getElementsByTagName(t)[0];
            k.async = 1;
            k.src = r;
            a.parentNode.insertBefore(k, a);
        })(window, document, 'script', 'https://mc.yandex.ru/metrika/tag.js?id=' + analyticsConfig.metricaId, 'ym');

        ym(analyticsConfig.metricaId, 'init', {
            ssr: true,
            webvisor: true,
            clickmap: true,
            ecommerce: 'dataLayer',
            referrer: document.referrer,
            url: location.href,
            accurateTrackBounce: true,
            trackLinks: true
        });
    }

    if (analyticsConfig.gaId) {
        const gaScript = document.createElement('script');
        gaScript.async = true;
        gaScript.src = 'https://www.googletagmanager.com/gtag/js?id=' + analyticsConfig.gaId;
        document.head.appendChild(gaScript);
        window.dataLayer = window.dataLayer || [];
        window.gtag = function () { window.dataLayer.push(arguments); };
        window.gtag('js', new Date());
        window.gtag('config', analyticsConfig.gaId);
    }
};

const cookieBanner = document.getElementById('cookieBanner');
const savedConsent = sessionStorage.getItem(consentKey);

if (savedConsent === 'accepted') {
    loadAnalytics();
} else if (cookieBanner && !savedConsent) {
    cookieBanner.hidden = false;
}

const closeCookieBanner = (choice) => {
    sessionStorage.setItem(consentKey, choice);
    if (cookieBanner) cookieBanner.hidden = true;
    if (choice === 'accepted') loadAnalytics();
};

const cookieAccept = document.getElementById('cookieAccept');
const cookieDecline = document.getElementById('cookieDecline');
if (cookieAccept) cookieAccept.addEventListener('click', () => closeCookieBanner('accepted'));
if (cookieDecline) cookieDecline.addEventListener('click', () => closeCookieBanner('declined'));

const track = (name) => {
    if (typeof ym === 'function' && analyticsConfig.metricaId) {
        ym(analyticsConfig.metricaId, 'reachGoal', name);
    }
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
    const tsField = feedbackForm.querySelector('[name="form_ts"]');
    if (tsField) tsField.value = Date.now();
    const pageField = feedbackForm.querySelector('[name="page"]');
    if (pageField) pageField.value = window.location.pathname;
    feedbackForm.addEventListener('submit', () => track('lead_submit'));
}

if (document.querySelector('.messages .message--success')) {
    track('lead_success');
}
