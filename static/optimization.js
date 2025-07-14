// Оптимизация производительности для страницы категорий

document.addEventListener('DOMContentLoaded', function() {

    // 1. Оптимизация скролла с throttling
    let ticking = false;

    function updateOnScroll() {
        // Здесь можно добавить логику для оптимизации скролла
        ticking = false;
    }

    function requestTick() {
        if (!ticking) {
            requestAnimationFrame(updateOnScroll);
            ticking = true;
        }
    }

    // Используем passive: true для лучшей производительности
    window.addEventListener('scroll', requestTick, { passive: true });

    // 2. Ленивая загрузка изображений (если будут добавлены)
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }

    // 3. Оптимизация анимаций
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const animationObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Применяем к карточкам категорий
    document.querySelectorAll('.category-card').forEach(card => {
        animationObserver.observe(card);
    });

    // 4. Оптимизация форм
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.textContent = 'Отправка...';
            }
        });
    });

    // 5. Оптимизация селектора количества элементов
    const perPageSelect = document.querySelector('.per-page-select');
    if (perPageSelect) {
        perPageSelect.addEventListener('change', function() {
            // Добавляем индикатор загрузки
            const container = document.querySelector('.categories-container');
            if (container) {
                container.style.opacity = '0.7';
                container.style.pointerEvents = 'none';
            }
        });
    }

    // 6. Оптимизация пагинации
    const paginationLinks = document.querySelectorAll('.pagination-item');
    paginationLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (this.classList.contains('disabled')) {
                e.preventDefault();
                return;
            }

            // Добавляем индикатор загрузки
            const container = document.querySelector('.categories-container');
            if (container) {
                container.style.opacity = '0.7';
                container.style.pointerEvents = 'none';
            }
        });
    });

    // 7. Оптимизация hover эффектов
    const cards = document.querySelectorAll('.category-card');
    cards.forEach(card => {
        let hoverTimeout;

        card.addEventListener('mouseenter', function() {
            clearTimeout(hoverTimeout);
            this.style.transform = 'translateY(-5px)';
        });

        card.addEventListener('mouseleave', function() {
            hoverTimeout = setTimeout(() => {
                this.style.transform = 'translateY(0)';
            }, 100);
        });
    });

    // 8. Оптимизация для мобильных устройств
    function handleResize() {
        const isMobile = window.innerWidth <= 768;
        const cards = document.querySelectorAll('.category-card');

        cards.forEach(card => {
            if (isMobile) {
                card.style.transition = 'none';
            } else {
                card.style.transition = 'all 0.3s ease';
            }
        });
    }

    window.addEventListener('resize', handleResize);
    handleResize(); // Вызываем сразу

    // 9. Оптимизация для пользователей с предпочтением reduced motion
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        document.body.classList.add('reduced-motion');

        // Отключаем все анимации
        const style = document.createElement('style');
        style.textContent = `
            .reduced-motion * {
                animation: none !important;
                transition: none !important;
            }
        `;
        document.head.appendChild(style);
    }

    // 10. Оптимизация загрузки CSS
    function preloadCriticalCSS() {
        const criticalStyles = [
            'static/style.css',
            'static/categories.css',
            'static/pagination.css'
        ];

        criticalStyles.forEach(href => {
            const link = document.createElement('link');
            link.rel = 'preload';
            link.as = 'style';
            link.href = href;
            document.head.appendChild(link);
        });
    }

    preloadCriticalCSS();
});

// 11. Оптимизация для Service Worker (если используется)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js')
            .then(function(registration) {
                console.log('SW registered: ', registration);
            })
            .catch(function(registrationError) {
                console.log('SW registration failed: ', registrationError);
            });
    });
}