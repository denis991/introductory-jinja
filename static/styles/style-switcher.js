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
        // Ищем навигацию
        const navbar = document.querySelector('.navbar-nav');
        // navbar-nav <-> nav-menu
        if (!navbar) return;

        // Создаем элемент переключателя
        const switcherContainer = document.createElement('li');
        switcherContainer.className = 'style-switcher-container';
        switcherContainer.innerHTML = `
            <div class="style-switcher">
                <label class="switcher-label">
                    <span class="switcher-text">🎨 Красивые стили</span>
                    <div class="switcher-toggle">
                        <input type="checkbox" id="style-switcher" ${this.isExtendedMode ? 'checked' : ''}>
                        <span class="switcher-slider"></span>
                    </div>
                </label>
            </div>
        `;

        // Добавляем в навигацию
        navbar.appendChild(switcherContainer);

        // Добавляем стили для переключателя
        this.addSwitcherStyles();
    }

    addSwitcherStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .style-switcher-container {
                display: flex;
                align-items: center;
                margin-left: auto;
            }

            .style-switcher {
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }

            .switcher-label {
                display: flex;
                align-items: center;
                gap: 0.5rem;
                cursor: pointer;
                font-size: 0.9rem;
                font-weight: 500;
                color: #4a5568;
                transition: all 0.3s ease;
            }

            .switcher-text {
                white-space: nowrap;
            }

            .switcher-toggle {
                position: relative;
                width: 50px;
                height: 24px;
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
                border-radius: 24px;
                box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
            }

            .switcher-slider:before {
                position: absolute;
                content: "";
                height: 18px;
                width: 18px;
                left: 3px;
                bottom: 3px;
                background: white;
                transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                border-radius: 50%;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            }

            .switcher-toggle input:checked + .switcher-slider {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2);
            }

            .switcher-toggle input:checked + .switcher-slider:before {
                transform: translateX(26px);
            }

            .switcher-label:hover .switcher-slider {
                transform: scale(1.05);
            }

            /* Анимация при переключении */
            .style-switching {
                transition: all 0.3s ease;
            }

            /* Адаптивность */
            @media (max-width: 768px) {
                .style-switcher-container {
                    margin-left: 0;
                    margin-top: 1rem;
                }

                .switcher-text {
                    font-size: 0.8rem;
                }
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
});