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

// Close menu when clicking on link
const navLinks = document.querySelectorAll('.nav__link');
navLinks.forEach(link => {
    link.addEventListener('click', closeMenu);
});
