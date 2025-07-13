# Здесь определяются маршруты (routes) для главной страницы.
# Каждый маршрут — это функция, которая обрабатывает HTTP-запросы и возвращает ответ (HTML-страницу или данные).
from flask import Blueprint, render_template

from app.features.home.services import HomeService
from app.infra.db.repositories import (SQLAlchemyProductRepository,
                                      SQLAlchemyUserRepository)

# Create blueprint
home_bp = Blueprint("home", __name__)

# Initialize repositories and service
user_repository = SQLAlchemyUserRepository()
product_repository = SQLAlchemyProductRepository()
home_service = HomeService(user_repository, product_repository)


@home_bp.route("/")
def home():
    """Home page route"""
    data = home_service.get_home_data()
    return render_template("home/index.html", **data)
