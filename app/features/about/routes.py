# Здесь определяются маршруты (routes) для страницы 'О нас'.
# Каждый маршрут — это функция, которая обрабатывает HTTP-запросы и
# возвращает ответ (HTML-страницу или данные).
from flask import Blueprint, render_template

from app.features.about.services import AboutService
from app.infra.db.repositories import MockTeamRepository

# Create blueprint
about_bp = Blueprint("about", __name__)

# Initialize repository and service
team_repository = MockTeamRepository()
about_service = AboutService(team_repository)


@about_bp.route("/about")
def about():
    """About page route"""
    data = about_service.get_about_data()
    return render_template("about/about.html", **data)
