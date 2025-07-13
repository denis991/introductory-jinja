"""
Маршруты для документации API
Содержит редиректы и дополнительные страницы документации
"""
from flask import Blueprint, redirect, render_template

# Создаем Blueprint для документации
docs_bp = Blueprint('docs', __name__, url_prefix='/docs')


@docs_bp.route('/')
def docs_home():
    """Главная страница документации"""
    return render_template('docs/index.html')


# @docs_bp.route('/swagger')
# def swagger_redirect():
#     """Редирект с /docs/swagger на /docs/ для удобства доступа к Swagger документации"""
#     return redirect('/docs/')


@docs_bp.route('/api')
def api_redirect():
    """Редирект с /docs/api на /docs/ для удобства доступа к API документации"""
    return redirect('/docs/')


@docs_bp.route('/help')
def help_page():
    """Страница помощи по использованию API"""
    return render_template('docs/help.html')