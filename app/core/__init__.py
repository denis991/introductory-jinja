import os

from flask import Flask

from app.features.about.routes import about_bp  # Импортируем blueprint для страницы 'О нас'
from app.features.home.routes import home_bp    # Импортируем blueprint для главной страницы
from app.features.products.routes import products_bp  # Импортируем blueprint для продуктов
from app.interfaces.controllers.cli import register_commands  # Импортируем функцию для регистрации CLI-команд

from .config import Config  # Импортируем класс конфигурации
from .extensions import db, migrate  # Импортируем расширения для работы с БД и миграциями

from dotenv import load_dotenv  # Импортируем функцию для загрузки переменных окружения из .env файла
load_dotenv()  # Загружаем переменные окружения из .env файла


def create_app(config_class=Config):
    """Фабрика приложения Flask (Application factory pattern)"""
    # Получаем абсолютный путь к папке с шаблонами (templates)
    template_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "templates")
    )
    # Получаем абсолютный путь к папке со статикой (static)
    static_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "static")
    )

    # Создаём экземпляр Flask-приложения, указывая папки для шаблонов и статики
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config.from_object(config_class)  # Загружаем конфигурацию из класса Config

    # Инициализируем расширения (подключаем базу данных и миграции)
    db.init_app(app)  # Подключаем SQLAlchemy к приложению
    migrate.init_app(app, db)  # Подключаем Alembic (Flask-Migrate) к приложению и БД

    # Регистрируем blueprints (модули с роутами)
    app.register_blueprint(home_bp)      # Главная страница
    app.register_blueprint(about_bp)     # Страница 'О нас'
    app.register_blueprint(products_bp)  # Страница продуктов

    # Регистрируем кастомные CLI-команды
    register_commands(app)

    return app  # Возвращаем готовое Flask-приложение
