"""
API ресурсы для Flask-RESTX
Реализация REST API эндпоинтов с автоматической документацией
"""

from flask import request, abort
from flask_restx import Resource
from datetime import datetime

from .swagger import (
    api, categories_ns, products_ns, users_ns,
    category_model, category_create_model, category_update_model,
    product_model, product_create_model, product_update_model,
    user_model, error_model, success_model, pagination_model
)

# Импортируем сервисы
from app.features.categories.services import (
    get_all_categories, get_category_by_id, create_category,
    update_category, delete_category
)
from app.features.products.services import (
    get_all_products, get_product_by_id, create_product,
    update_product, delete_product
)
from app.features.users.services import (
    get_all_users, get_user_by_id, create_user,
    update_user, delete_user
)


# ============================================================================
# API РЕСУРСЫ ДЛЯ КАТЕГОРИЙ
# ============================================================================

@categories_ns.route('/')
class CategoriesList(Resource):
    """Список всех категорий"""

    @categories_ns.doc('list_categories')
    @categories_ns.marshal_list_with(category_model)
    def get(self):
        """Получить список всех категорий"""
        try:
            categories = get_all_categories()
            # Преобразуем доменные сущности в словари для сериализации
            return [{
                'id': category.id,
                'name': category.name,
                'description': category.description,
                'created_at': None,  # Добавим позже
                'updated_at': None   # Добавим позже
            } for category in categories], 200
        except Exception as e:
            categories_ns.abort(500, f"Ошибка при получении категорий: {str(e)}")

    @categories_ns.doc('create_category')
    @categories_ns.expect(category_create_model)
    @categories_ns.marshal_with(category_model, code=201)
    def post(self):
        """Создать новую категорию"""
        try:
            data = request.get_json()
            name = data.get('name')
            description = data.get('description')

            if not name:
                categories_ns.abort(400, 'Название категории обязательно')

            category = create_category(name, description)
            return {
                'id': category.id,
                'name': category.name,
                'description': category.description,
                'created_at': None,
                'updated_at': None
            }, 201
        except Exception as e:
            categories_ns.abort(500, f"Ошибка при создании категории: {str(e)}")


@categories_ns.route('/<int:category_id>')
@categories_ns.param('category_id', 'ID категории')
class CategoryDetail(Resource):
    """Детальная информация о категории"""

    @categories_ns.doc('get_category')
    @categories_ns.marshal_with(category_model)
    def get(self, category_id):
        """Получить категорию по ID"""
        try:
            category = get_category_by_id(category_id)
            if not category:
                categories_ns.abort(404, 'Категория не найдена')
            return {
                'id': category.id,
                'name': category.name,
                'description': category.description,
                'created_at': None,
                'updated_at': None
            }, 200
        except Exception as e:
            categories_ns.abort(500, f"Ошибка при получении категории: {str(e)}")

    @categories_ns.doc('update_category')
    @categories_ns.expect(category_update_model)
    @categories_ns.marshal_with(category_model)
    def put(self, category_id):
        """Обновить категорию"""
        try:
            data = request.get_json()
            name = data.get('name')
            description = data.get('description')

            category = update_category(category_id, name, description)
            if not category:
                categories_ns.abort(404, 'Категория не найдена')
            return {
                'id': category.id,
                'name': category.name,
                'description': category.description,
                'created_at': None,
                'updated_at': None
            }, 200
        except Exception as e:
            categories_ns.abort(500, f"Ошибка при обновлении категории: {str(e)}")

    @categories_ns.doc('delete_category')
    @categories_ns.response(204, 'Категория удалена')
    def delete(self, category_id):
        """Удалить категорию"""
        try:
            success = delete_category(category_id)
            if not success:
                categories_ns.abort(404, 'Категория не найдена')
            return '', 204
        except Exception as e:
            categories_ns.abort(500, f"Ошибка при удалении категории: {str(e)}")


# ============================================================================
# API РЕСУРСЫ ДЛЯ ТОВАРОВ
# ============================================================================

@products_ns.route('/')
class ProductsList(Resource):
    """Список всех товаров"""

    @products_ns.doc('list_products')
    @products_ns.marshal_list_with(product_model)
    def get(self):
        """Получить список всех товаров"""
        try:
            products = get_all_products()
            return [{
                'id': product.id,
                'name': product.name,
                'description': product.category,  # Используем category как description
                'price': product.price,
                'category_ids': [],
                'categories': [],
                'created_at': None,
                'updated_at': None
            } for product in products], 200
        except Exception as e:
            products_ns.abort(500, f"Ошибка при получении товаров: {str(e)}")

    @products_ns.doc('create_product')
    @products_ns.expect(product_create_model)
    @products_ns.marshal_with(product_model, code=201)
    def post(self):
        """Создать новый товар"""
        try:
            data = request.get_json()
            name = data.get('name')
            description = data.get('description')
            price = data.get('price')
            category_ids = data.get('category_ids', [])

            if not name:
                products_ns.abort(400, 'Название товара обязательно')
            if not price or price <= 0:
                products_ns.abort(400, 'Цена должна быть больше 0')

            product = create_product(name, description, price, category_ids)
            return {
                'id': product.id,
                'name': product.name,
                'description': product.category,
                'price': product.price,
                'category_ids': [],
                'categories': [],
                'created_at': None,
                'updated_at': None
            }, 201
        except Exception as e:
            products_ns.abort(500, f"Ошибка при создании товара: {str(e)}")


@products_ns.route('/<int:product_id>')
@products_ns.param('product_id', 'ID товара')
class ProductDetail(Resource):
    """Детальная информация о товаре"""

    @products_ns.doc('get_product')
    @products_ns.marshal_with(product_model)
    def get(self, product_id):
        """Получить товар по ID"""
        try:
            product = get_product_by_id(product_id)
            if not product:
                products_ns.abort(404, 'Товар не найден')
            return {
                'id': product.id,
                'name': product.name,
                'description': product.category,
                'price': product.price,
                'category_ids': [],
                'categories': [],
                'created_at': None,
                'updated_at': None
            }, 200
        except Exception as e:
            products_ns.abort(500, f"Ошибка при получении товара: {str(e)}")

    @products_ns.doc('update_product')
    @products_ns.expect(product_update_model)
    @products_ns.marshal_with(product_model)
    def put(self, product_id):
        """Обновить товар"""
        try:
            data = request.get_json()
            name = data.get('name')
            description = data.get('description')
            price = data.get('price')
            category_ids = data.get('category_ids')

            product = update_product(product_id, name, description, price, category_ids)
            if not product:
                products_ns.abort(404, 'Товар не найден')
            return {
                'id': product.id,
                'name': product.name,
                'description': product.category,
                'price': product.price,
                'category_ids': [],
                'categories': [],
                'created_at': None,
                'updated_at': None
            }, 200
        except Exception as e:
            products_ns.abort(500, f"Ошибка при обновлении товара: {str(e)}")

    @products_ns.doc('delete_product')
    @products_ns.response(204, 'Товар удален')
    def delete(self, product_id):
        """Удалить товар"""
        try:
            success = delete_product(product_id)
            if not success:
                products_ns.abort(404, 'Товар не найден')
            return '', 204
        except Exception as e:
            products_ns.abort(500, f"Ошибка при удалении товара: {str(e)}")


# ============================================================================
# API РЕСУРСЫ ДЛЯ ПОЛЬЗОВАТЕЛЕЙ
# ============================================================================

@users_ns.route('/')
class UsersList(Resource):
    """Список всех пользователей"""

    @users_ns.doc('list_users')
    @users_ns.marshal_list_with(user_model)
    def get(self):
        """Получить список всех пользователей"""
        try:
            users = get_all_users()
            return [{
                'id': user.id,
                'username': user.name,  # Используем name как username
                'email': user.email,
                'first_name': None,
                'last_name': None,
                'is_active': user.is_admin,  # Используем is_admin как is_active
                'created_at': user.join_date,
                'updated_at': None
            } for user in users], 200
        except Exception as e:
            users_ns.abort(500, f"Ошибка при получении пользователей: {str(e)}")

    @users_ns.doc('create_user')
    @users_ns.expect(user_model)
    @users_ns.marshal_with(user_model, code=201)
    def post(self):
        """Создать нового пользователя"""
        try:
            data = request.get_json()
            username = data.get('username')
            email = data.get('email')
            first_name = data.get('first_name')
            last_name = data.get('last_name')

            if not username or not email:
                users_ns.abort(400, 'Имя пользователя и email обязательны')

            user = create_user(username, email, first_name, last_name)
            return {
                'id': user.id,
                'username': user.name,
                'email': user.email,
                'first_name': None,
                'last_name': None,
                'is_active': user.is_admin,
                'created_at': user.join_date,
                'updated_at': None
            }, 201
        except Exception as e:
            users_ns.abort(500, f"Ошибка при создании пользователя: {str(e)}")


@users_ns.route('/<int:user_id>')
@users_ns.param('user_id', 'ID пользователя')
class UserDetail(Resource):
    """Детальная информация о пользователе"""

    @users_ns.doc('get_user')
    @users_ns.marshal_with(user_model)
    def get(self, user_id):
        """Получить пользователя по ID"""
        try:
            user = get_user_by_id(user_id)
            if not user:
                users_ns.abort(404, 'Пользователь не найден')
            return {
                'id': user.id,
                'username': user.name,
                'email': user.email,
                'first_name': None,
                'last_name': None,
                'is_active': user.is_admin,
                'created_at': user.join_date,
                'updated_at': None
            }, 200
        except Exception as e:
            users_ns.abort(500, f"Ошибка при получении пользователя: {str(e)}")

    @users_ns.doc('update_user')
    @users_ns.expect(user_model)
    @users_ns.marshal_with(user_model)
    def put(self, user_id):
        """Обновить пользователя"""
        try:
            data = request.get_json()
            username = data.get('username')
            email = data.get('email')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            is_active = data.get('is_active')

            user = update_user(user_id, username, email, first_name, last_name, is_active)
            if not user:
                users_ns.abort(404, 'Пользователь не найден')
            return {
                'id': user.id,
                'username': user.name,
                'email': user.email,
                'first_name': None,
                'last_name': None,
                'is_active': user.is_admin,
                'created_at': user.join_date,
                'updated_at': None
            }, 200
        except Exception as e:
            users_ns.abort(500, f"Ошибка при обновлении пользователя: {str(e)}")

    @users_ns.doc('delete_user')
    @users_ns.response(204, 'Пользователь удален')
    def delete(self, user_id):
        """Удалить пользователя"""
        try:
            success = delete_user(user_id)
            if not success:
                users_ns.abort(404, 'Пользователь не найден')
            return '', 204
        except Exception as e:
            users_ns.abort(500, f"Ошибка при удалении пользователя: {str(e)}")


# ============================================================================
# ДОПОЛНИТЕЛЬНЫЕ API РЕСУРСЫ
# ============================================================================

@api.route('/health')
class HealthCheck(Resource):
    """Проверка состояния API"""

    @api.doc('health_check')
    @api.marshal_with(success_model)
    def get(self):
        """Проверить состояние API"""
        return {
            'message': 'API работает корректно',
            'data': {
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'version': '1.0.0'
            }
        }, 200


@api.route('/stats')
class Stats(Resource):
    """Статистика API"""

    @api.doc('get_stats')
    @api.marshal_with(success_model)
    def get(self):
        """Получить статистику API"""
        try:
            categories_count = len(get_all_categories())
            products_count = len(get_all_products())
            users_count = len(get_all_users())

            return {
                'message': 'Статистика получена',
                'data': {
                    'categories_count': categories_count,
                    'products_count': products_count,
                    'users_count': users_count,
                    'timestamp': datetime.now().isoformat()
                }
            }, 200
        except Exception as e:
            api.abort(500, f"Ошибка при получении статистики: {str(e)}")