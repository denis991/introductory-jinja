"""
Swagger/OpenAPI документация для Flask приложения
Настройка Flask-RESTX для автоматической генерации API документации
"""

from flask import current_app
from flask_restx import Api, Namespace, Resource, fields

# Создаем основной API объект
api = Api(
    title="🏪 Introductory Jinja API",
    version="1.0.0",
    description="""
# 🚀 Introductory Jinja API Documentation

> **RESTful API для управления товарами и категориями**

## 📋 Основные возможности

### 🏷️ Управление категориями
- **Создание** новых категорий товаров
- **Редактирование** существующих категорий
- **Удаление** категорий
- **Просмотр** списка всех категорий
- **Детальная информация** о конкретной категории

### 📦 Управление товарами
- **Создание** новых товаров с привязкой к категориям
- **Редактирование** существующих товаров
- **Удаление** товаров
- **Просмотр** списка всех товаров с фильтрацией
- **Детальная информация** о конкретном товаре

### 👥 Управление пользователями
- **Регистрация** новых пользователей
- **Авторизация** существующих пользователей
- **Просмотр** профиля пользователя
- **Управление** пользователями (для администраторов)

## 🚀 Быстрый старт

### 1. Получение списка категорий
```bash
curl -X GET "http://localhost:5006/api/categories" \\
  -H "Content-Type: application/json"
```

### 2. Создание новой категории
```bash
curl -X POST "http://localhost:5006/api/categories" \\
  -H "Content-Type: application/json" \\
  -d '{
    "name": "Новая категория",
    "description": "Описание категории"
  }'
```

### 3. Получение списка товаров
```bash
curl -X GET "http://localhost:5006/api/products" \\
  -H "Content-Type: application/json"
```

### 4. Создание нового товара
```bash
curl -X POST "http://localhost:5006/api/products" \\
  -H "Content-Type: application/json" \\
  -d '{
    "name": "Новый товар",
    "description": "Описание товара",
    "price": 99.99,
    "category_ids": [1, 2]
  }'
```

## 📊 Коды ответов

| Код | Статус | Описание |
|-----|--------|----------|
| `200` | ✅ OK | Успешный запрос |
| `201` | ✅ Created | Ресурс успешно создан |
| `400` | ❌ Bad Request | Неверный запрос |
| `404` | ❌ Not Found | Ресурс не найден |
| `409` | ❌ Conflict | Конфликт (например, категория уже существует) |
| `500` | ❌ Internal Server Error | Внутренняя ошибка сервера |

## 🔧 Настройки и ограничения

- **Максимальная длина названия**: 100 символов
- **Максимальная длина описания**: 500 символов
- **Минимальная цена товара**: 0.01
- **Максимальная цена товара**: 999999.99
- **Пагинация**: 20 элементов по умолчанию

## 💡 Примеры использования

### Получение категории по ID
```bash
curl -X GET "http://localhost:5006/api/categories/1" \\
  -H "Content-Type: application/json"
```

### Обновление категории
```bash
curl -X PUT "http://localhost:5006/api/categories/1" \\
  -H "Content-Type: application/json" \\
  -d '{
    "name": "Обновленное название",
    "description": "Обновленное описание"
  }'
```

### Удаление категории
```bash
curl -X DELETE "http://localhost:5006/api/categories/1" \\
  -H "Content-Type: application/json"
```

### Получение товара по ID
```bash
curl -X GET "http://localhost:5006/api/products/1" \\
  -H "Content-Type: application/json"
```

### Обновление товара
```bash
curl -X PUT "http://localhost:5006/api/products/1" \\
  -H "Content-Type: application/json" \\
  -d '{
    "name": "Обновленный товар",
    "description": "Обновленное описание",
    "price": 149.99,
    "category_ids": [1, 3]
  }'
```

### Удаление товара
```bash
curl -X DELETE "http://localhost:5006/api/products/1" \\
  -H "Content-Type: application/json"
```

---
Очищены шаблоны templates/docs/index.html
Очищены шаблоны templates/docs/help.html
❓[**справочник по API**](http://localhost:5006/docs/help)
**📝 Последнее обновление**: $(date)
**🌐 Веб-интерфейс**: [Главная страница](http://localhost:5006/)
**📚 Дополнительная документация**: [GitHub](https://github.com/denis991/introductory-jinja)
    """,
    doc="/swagger/",
    prefix="/api",
    contact={
        "name": "Introductory Jinja Support",
        "email": "support@example.com",
        "url": "https://example.com/support",
    },
    license={"name": "MIT License", "url": "https://opensource.org/licenses/MIT"},
    default="default",
    default_label="Основные операции",
    validate=True,
    # Добавляем кастомные CSS для красивого отображения
    custom_css="""
    .swagger-ui .topbar { display: none; }
    .swagger-ui .info .title { font-size: 2.5em; margin-bottom: 0.5em; }
    .swagger-ui .info .description { font-size: 1.1em; line-height: 1.6; }
    .swagger-ui .info .description h1 { color: #2c3e50; border-bottom: 2px solid #3498db; }
    .swagger-ui .info .description h2 { color: #34495e; margin-top: 1.5em; }
    .swagger-ui .info .description h3 { color: #7f8c8d; }
    .swagger-ui .info .description code { background: #f8f9fa; color: #e74c3c; }
    .swagger-ui .info .description pre { background: #f8f9fa; border-left: 4px solid #3498db; }
    .swagger-ui .info .description table { border-collapse: collapse; width: 100%; }
    .swagger-ui .info .description th, .swagger-ui .info .description td {
        border: 1px solid #ddd; padding: 8px; text-align: left;
    }
    .swagger-ui .info .description th { background-color: #f2f2f2; }
    """,
)

# Создаем пространства имен для разных модулей
categories_ns = Namespace("categories", description="Операции с категориями")
products_ns = Namespace("products", description="Операции с товарами")
users_ns = Namespace("users", description="Операции с пользователями")

# Модели для сериализации данных
category_model = api.model(
    "Category",
    {
        "id": fields.Integer(
            readonly=True, description="Уникальный идентификатор категории"
        ),
        "name": fields.String(
            required=True, description="Название категории", max_length=100
        ),
        "description": fields.String(description="Описание категории", max_length=500),
        "created_at": fields.DateTime(readonly=True, description="Дата создания"),
        "updated_at": fields.DateTime(
            readonly=True, description="Дата последнего обновления"
        ),
    },
)

category_create_model = api.model(
    "CategoryCreate",
    {
        "name": fields.String(
            required=True, description="Название категории", max_length=100
        ),
        "description": fields.String(description="Описание категории", max_length=500),
    },
)

category_update_model = api.model(
    "CategoryUpdate",
    {
        "name": fields.String(description="Название категории", max_length=100),
        "description": fields.String(description="Описание категории", max_length=500),
    },
)

product_model = api.model(
    "Product",
    {
        "id": fields.Integer(
            readonly=True, description="Уникальный идентификатор товара"
        ),
        "name": fields.String(
            required=True, description="Название товара", max_length=100
        ),
        "description": fields.String(description="Описание товара", max_length=500),
        "price": fields.Float(
            required=True, description="Цена товара", min=0.01, max=999999.99
        ),
        "category_ids": fields.List(fields.Integer, description="ID категорий товара"),
        "categories": fields.List(
            fields.Nested(category_model), readonly=True, description="Категории товара"
        ),
        "created_at": fields.DateTime(readonly=True, description="Дата создания"),
        "updated_at": fields.DateTime(
            readonly=True, description="Дата последнего обновления"
        ),
    },
)

product_create_model = api.model(
    "ProductCreate",
    {
        "name": fields.String(
            required=True, description="Название товара", max_length=100
        ),
        "description": fields.String(description="Описание товара", max_length=500),
        "price": fields.Float(
            required=True, description="Цена товара", min=0.01, max=999999.99
        ),
        "category_ids": fields.List(fields.Integer, description="ID категорий товара"),
    },
)

product_update_model = api.model(
    "ProductUpdate",
    {
        "name": fields.String(description="Название товара", max_length=100),
        "description": fields.String(description="Описание товара", max_length=500),
        "price": fields.Float(description="Цена товара", min=0.01, max=999999.99),
        "category_ids": fields.List(fields.Integer, description="ID категорий товара"),
    },
)

user_model = api.model(
    "User",
    {
        "id": fields.Integer(
            readonly=True, description="Уникальный идентификатор пользователя"
        ),
        "username": fields.String(
            required=True, description="Имя пользователя", max_length=80
        ),
        "email": fields.String(
            required=True, description="Email пользователя", max_length=120
        ),
        "first_name": fields.String(description="Имя", max_length=50),
        "last_name": fields.String(description="Фамилия", max_length=50),
        "is_active": fields.Boolean(description="Активен ли пользователь"),
        "created_at": fields.DateTime(readonly=True, description="Дата регистрации"),
        "updated_at": fields.DateTime(
            readonly=True, description="Дата последнего обновления"
        ),
    },
)

# Модели для ответов с ошибками
error_model = api.model(
    "Error",
    {
        "message": fields.String(required=True, description="Сообщение об ошибке"),
        "code": fields.String(description="Код ошибки"),
        "details": fields.Raw(description="Дополнительные детали ошибки"),
    },
)

# Модели для успешных ответов
success_model = api.model(
    "Success",
    {
        "message": fields.String(required=True, description="Сообщение об успехе"),
        "data": fields.Raw(description="Данные ответа"),
    },
)

# Модели для пагинации
pagination_model = api.model(
    "Pagination",
    {
        "page": fields.Integer(description="Текущая страница"),
        "per_page": fields.Integer(description="Количество элементов на странице"),
        "total": fields.Integer(description="Общее количество элементов"),
        "pages": fields.Integer(description="Общее количество страниц"),
        "has_next": fields.Boolean(description="Есть ли следующая страница"),
        "has_prev": fields.Boolean(description="Есть ли предыдущая страница"),
    },
)


# Функция для инициализации API
def init_swagger(app):
    """Инициализация Swagger документации"""
    api.init_app(app)

    # Добавляем пространства имен
    api.add_namespace(categories_ns)
    api.add_namespace(products_ns)
    api.add_namespace(users_ns)

    # Импортируем API ресурсы для регистрации маршрутов
    import app.shared.api_resources

    return api
