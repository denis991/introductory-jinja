// 🎨 Переключатель стилей между оптимизированными и расширенными

class StyleSwitcher {
    constructor() {
        this.isExtendedMode = localStorage.getItem('extendedStyles') === 'true';
        this.init();
    }

    init() {
        // Создаем переключатель в навигации
        this.createSwitcher();

        // Применяем текущий режим
        this.applyStyles();

        // Добавляем обработчики событий
        this.addEventListeners();
    }

    createSwitcher() {
        // Ищем контейнер футера
        const footerContainer = document.querySelector('.footer .container');
        if (!footerContainer) return;

        // Создаем элемент переключателя
        const switcherContainer = document.createElement('div');
        switcherContainer.className = 'style-switcher-footer';
        switcherContainer.innerHTML = `
            <div class="style-switcher compact">
                <label class="switcher-label">
                    <span class="switcher-text">🎨 Styles</span>
                    <div class="switcher-toggle">
                        <input type="checkbox" id="style-switcher" ${this.isExtendedMode ? 'checked' : ''}>
                        <span class="switcher-slider"></span>
                    </div>
                </label>
            </div>
        `;

        // Добавляем в футер
        footerContainer.appendChild(switcherContainer);

        // Добавляем стили для переключателя
        this.addSwitcherStyles();
    }

    addSwitcherStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .style-switcher-footer {
                display: flex;
                justify-content: center;
                align-items: center;
                margin-top: 0.5rem;
            }
            .style-switcher.compact {
                display: flex;
                align-items: center;
                gap: 0.3rem;
                font-size: 0.8rem;
            }
            .switcher-label {
                display: flex;
                align-items: center;
                gap: 0.3rem;
                cursor: pointer;
                font-size: 0.8rem;
                font-weight: 500;
                color: #4a5568;
                transition: all 0.3s ease;
            }
            .switcher-text {
                white-space: nowrap;
                font-size: 0.8rem;
            }
            .switcher-toggle {
                position: relative;
                width: 32px;
                height: 16px;
            }
            .switcher-toggle input {
                opacity: 0;
                width: 0;
                height: 0;
            }
            .switcher-slider {
                position: absolute;
                cursor: pointer;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e0 100%);
                transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                border-radius: 16px;
                box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.08);
            }
            .switcher-slider:before {
                position: absolute;
                content: "";
                height: 12px;
                width: 12px;
                left: 2px;
                bottom: 2px;
                background: white;
                transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                border-radius: 50%;
                box-shadow: 0 1px 2px rgba(0, 0, 0, 0.12);
            }
            .switcher-toggle input:checked + .switcher-slider {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.13);
            }
            .switcher-toggle input:checked + .switcher-slider:before {
                transform: translateX(16px);
            }
            .switcher-label:hover .switcher-slider {
                transform: scale(1.04);
            }
            @media (max-width: 768px) {
                .style-switcher-footer { margin-top: 0.3rem; }
                .switcher-label, .switcher-text { font-size: 0.7rem; }
                .switcher-toggle { width: 26px; height: 13px; }
                .switcher-slider:before { height: 9px; width: 9px; left: 2px; bottom: 2px; }
            }
        `;
        document.head.appendChild(style);
    }

    addEventListeners() {
        const switcher = document.getElementById('style-switcher');
        if (switcher) {
            switcher.addEventListener('change', (e) => {
                this.isExtendedMode = e.target.checked;
                this.applyStyles();
                this.savePreference();
                this.showNotification();
            });
        }
    }

    applyStyles() {
        const body = document.body;

        if (this.isExtendedMode) {
            // Включаем расширенные стили
            body.classList.add('extended-styles');
            body.classList.remove('optimized-styles');

            // Загружаем расширенные CSS файлы
            this.loadExtendedStyles();
        } else {
            // Включаем оптимизированные стили
            body.classList.add('optimized-styles');
            body.classList.remove('extended-styles');

            // Удаляем расширенные CSS файлы
            this.removeExtendedStyles();
        }
    }

    loadExtendedStyles() {
        const styles = [
            '/static/styles/extended/style.css',
            '/static/styles/extended/categories.css',
            '/static/styles/extended/pagination.css'
        ];

        styles.forEach(href => {
            if (!document.querySelector(`link[href="${href}"]`)) {
                const link = document.createElement('link');
                link.rel = 'stylesheet';
                link.href = href;
                link.className = 'extended-style';
                document.head.appendChild(link);
            }
        });
    }

    removeExtendedStyles() {
        const extendedStyles = document.querySelectorAll('.extended-style');
        extendedStyles.forEach(style => style.remove());
    }

    savePreference() {
        localStorage.setItem('extendedStyles', this.isExtendedMode);
    }

    showNotification() {
        // Создаем уведомление о переключении
        const notification = document.createElement('div');
        notification.className = 'style-notification';
        notification.innerHTML = `
            <div class="notification-content">
                <span class="notification-icon">${this.isExtendedMode ? '🎨' : '⚡'}</span>
                <span class="notification-text">
                    ${this.isExtendedMode ? 'Включены красивые стили' : 'Включены оптимизированные стили'}
                </span>
            </div>
        `;

        // Добавляем стили для уведомления
        const style = document.createElement('style');
        style.textContent = `
            .style-notification {
                position: fixed;
                top: 20px;
                right: 20px;
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                border-radius: 15px;
                padding: 1rem 1.5rem;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                z-index: 10000;
                transform: translateX(100%);
                transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            }

            .notification-content {
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }

            .notification-icon {
                font-size: 1.2rem;
            }

            .notification-text {
                font-weight: 600;
                color: #2d3748;
            }

            .style-notification.show {
                transform: translateX(0);
            }
        `;
        document.head.appendChild(style);

        document.body.appendChild(notification);

        // Показываем уведомление
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);

        // Скрываем через 3 секунды
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 3000);
    }
}

// Инициализируем переключатель при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    new StyleSwitcher();

    // Мобильное бургер-меню для header/nav
    const burger = document.querySelector('.burger');
    const navMenu = document.querySelector('.nav-menu');
    if (burger && navMenu) {
        burger.addEventListener('click', function() {
            const isOpen = navMenu.classList.toggle('open');
            burger.classList.toggle('active', isOpen);
            burger.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
        });
        // Закрытие меню по клику вне nav-menu (на мобильных)
        document.addEventListener('click', function(e) {
            if (window.innerWidth <= 1024 && navMenu.classList.contains('open')) {
                if (!navMenu.contains(e.target) && !burger.contains(e.target)) {
                    navMenu.classList.remove('open');
                    burger.classList.remove('active');
                    burger.setAttribute('aria-expanded', 'false');
                }
            }
        });
    }
});