# Clean Architecture + Repository + Service Layer

Этот проект демонстрирует Flask/Jinja-приложение, переписанное по принципам Clean (Hexagonal) архитектуры с использованием паттернов Repository и Service Layer.

## 🏗️ Архитектура

### Структура проекта

```tree
app/
├── core/                         # Ядро приложения
│   ├── __init__.py              # create_app()
│   ├── config.py                # Конфигурации
│   └── extensions.py            # Инициализация Flask, SQLAlchemy и др.
│
├── domain/                       # Доменный слой
│   ├── entities.py              # Бизнес-сущности
│   └── interfaces.py            # Интерфейсы репозиториев (порты)
│
├── infra/                        # Инфраструктура
│   └── db/
│       ├── models.py            # SQLAlchemy модели
│       ├── repositories.py      # Реализации репозиториев (адаптеры)
│       └── seed_data.py         # Данные для инициализации БД
│
├── features/                     # Модули-фичи
│   ├── home/
│   │   ├── routes.py            # Blueprint + маршруты
│   │   ├── services.py          # Бизнес-логика
│   │   └── templates/           # Jinja-шаблоны
│   ├── about/
│   └── products/
│
├── interfaces/                   # Интерфейсы
│   ├── controllers/             # CLI команды
│   └── templates/               # Общие макеты
│
├── shared/                       # Утилиты
│   └── utils.py                 # Общие функции
│
└── tests/                        # Тесты
    ├── unit/                    # Unit тесты
    └── integration/             # Integration тесты
```

## 🧩 Слои архитектуры

### 1. Domain Layer (Доменный слой)

- **entities.py**: Бизнес-сущности (User, Product, TeamMember)
- **interfaces.py**: Абстрактные интерфейсы репозиториев

### 2. Infrastructure Layer (Инфраструктурный слой)

- **models.py**: SQLAlchemy модели для базы данных
- **repositories.py**: Конкретные реализации репозиториев
- **seed_data.py**: Данные для инициализации БД

### 3. Features Layer (Слой фич)

Каждая фича содержит:

- **routes.py**: Flask маршруты и Blueprint
- **services.py**: Бизнес-логика
- **templates/**: Jinja шаблоны

### 4. Interfaces Layer (Интерфейсный слой)

- **controllers/**: CLI команды
- **templates/**: Общие шаблоны (base.html, header.html)

### 5. Shared Layer (Общий слой)

- **utils.py**: Переиспользуемые утилиты

## 🔄 Паттерны

### Repository Pattern

```python
# Интерфейс (порт)
class ProductRepository(ABC):
    @abstractmethod
    def get_all_products(self) -> List[Product]:
        pass

# Реализация (адаптер)
class SQLAlchemyProductRepository(ProductRepository):
    def get_all_products(self) -> List[Product]:
        products = ProductModel.query.all()
        return [product.to_domain() for product in products]
```

### Service Layer Pattern

```python
class ProductService:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def get_all_products(self) -> List[Product]:
        products = self.product_repository.get_all_products()
        # Бизнес-логика: сортировка по рейтингу
        return sorted(products, key=lambda p: p.rating or 0, reverse=True)
```

### Dependency Injection

```python
# В routes.py
product_repository = SQLAlchemyProductRepository()
product_service = ProductService(product_repository)
```

## 🚀 Запуск

### Локальная разработка

```bash
# Установка зависимостей
pip install -r requirements.txt

# Инициализация БД
flask init-db
flask seed-db

# Запуск приложения
python run.py
```

### Docker

```bash
# Запуск с PostgreSQL
docker-compose up --build

# Или только приложение
docker build -t jinja-app .
docker run -p 5006:5006 jinja-app
```

## 🧪 Тестирование

### Unit тесты

```bash
python -m pytest tests/unit/
```

### Integration тесты

```bash
python -m pytest tests/integration/
```

## 📋 CLI команды

```bash
# Инициализация БД
flask init-db

# Заполнение данными
flask seed-db

# Удаление всех таблиц
flask drop-db
```

## 🎯 Преимущества архитектуры

1. **Разделение ответственности**: Четкие границы между слоями
2. **Тестируемость**: Легко мокать зависимости
3. **Масштабируемость**: Новые фичи добавляются как модули
4. **Гибкость**: Можно легко заменить реализацию (например, БД)
5. **Читаемость**: Код организован логично и понятно

## 🔧 Конфигурация

Настройки в `app/core/config.py`:

- **DevelopmentConfig**: Для разработки
- **ProductionConfig**: Для продакшена
- **TestingConfig**: Для тестов

Переменные окружения:

- `FLASK_ENV`: Окружение (development/production)
- `DATABASE_URL`: URL базы данных
- `SECRET_KEY`: Секретный ключ Flask
