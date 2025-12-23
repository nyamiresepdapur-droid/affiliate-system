// Landing Page JavaScript

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Navbar scroll effect
let lastScroll = 0;
const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll > 100) {
        navbar.style.background = 'rgba(102, 126, 234, 0.98)';
        navbar.style.boxShadow = '0 5px 20px rgba(0,0,0,0.2)';
    } else {
        navbar.style.background = 'rgba(102, 126, 234, 0.95)';
        navbar.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
    }
    
    lastScroll = currentScroll;
});

// Plan selection
document.querySelectorAll('[data-plan]').forEach(button => {
    button.addEventListener('click', function(e) {
        const plan = this.getAttribute('data-plan');
        // Store selected plan in localStorage
        localStorage.setItem('selectedPlan', plan);
        // Redirect to register page
        window.location.href = 'register.html';
    });
});

// Intersection Observer for fade-in animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in-up');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe elements for animation
document.addEventListener('DOMContentLoaded', () => {
    const animateElements = document.querySelectorAll('.plan-card, .feature-card, .accordion-item');
    animateElements.forEach(el => observer.observe(el));
});

// FAQ Accordion - Auto close others
document.querySelectorAll('.accordion-button').forEach(button => {
    button.addEventListener('click', function() {
        const targetId = this.getAttribute('data-bs-target');
        const targetCollapse = document.querySelector(targetId);
        
        // Close other accordions
        document.querySelectorAll('.accordion-collapse').forEach(collapse => {
            if (collapse !== targetCollapse && collapse.classList.contains('show')) {
                const bsCollapse = new bootstrap.Collapse(collapse, {
                    toggle: false
                });
                bsCollapse.hide();
            }
        });
    });
});

// Stats counter animation
function animateCounter(element, target, duration = 2000) {
    let start = 0;
    const increment = target / (duration / 16);
    const timer = setInterval(() => {
        start += increment;
        if (start >= target) {
            element.textContent = target + (target >= 1000 ? '+' : '');
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(start) + (target >= 1000 ? '+' : '');
        }
    }, 16);
}

// Animate stats when in viewport
const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const statItems = entry.target.querySelectorAll('.stat-item h3');
            statItems.forEach(item => {
                const text = item.textContent;
                const number = parseInt(text.replace(/\D/g, ''));
                if (number) {
                    item.textContent = '0';
                    animateCounter(item, number);
                }
            });
            statsObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.5 });

const heroStats = document.querySelector('.hero-stats');
if (heroStats) {
    statsObserver.observe(heroStats);
}

// Mobile menu close on link click
document.querySelectorAll('.navbar-nav .nav-link').forEach(link => {
    link.addEventListener('click', () => {
        const navbarCollapse = document.querySelector('.navbar-collapse');
        if (navbarCollapse.classList.contains('show')) {
            const bsCollapse = new bootstrap.Collapse(navbarCollapse, {
                toggle: false
            });
            bsCollapse.hide();
        }
    });
});

// Form validation (if register form exists on this page)
const registerForm = document.getElementById('registerForm');
if (registerForm) {
    registerForm.addEventListener('submit', function(e) {
        e.preventDefault();
        // Validation logic here
        // Redirect to register page if needed
    });
}

// Console welcome message
console.log('%c🚀 Affiliate Management System', 'font-size: 20px; font-weight: bold; color: #667eea;');
console.log('%cWelcome to our landing page!', 'font-size: 14px; color: #764ba2;');

