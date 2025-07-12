# 🧠 Mindmap: Introductory Jinja Project

## 📁 **PROJECT ROOT**
```
introductory-jinja/
├── 📂 app/                    # Основное приложение
├── 📂 static/                 # Статические файлы
├── 📂 templates/              # HTML шаблоны
├── 📂 tests/                  # Тесты
├── 📂 resources/              # Документация и ресурсы
├── 📄 requirements.txt        # Зависимости Python
├── 📄 run.py                  # Точка входа
├── 📄 app.py                  # Альтернативная точка входа
└── 📄 README.md               # Описание проекта
```

## 🏗️ **APP ARCHITECTURE**
```
app/
├── 📂 core/                   # Ядро приложения
│   ├── 📄 __init__.py
│   ├── 📄 config.py          # Конфигурация
│   └── 📄 extensions.py      # Flask расширения
├── 📂 domain/                 # Бизнес-логика (чистая архитектура)
│   ├── 📄 __init__.py
│   ├── 📄 entities.py        # Бизнес-сущности
│   └── 📄 interfaces.py      # Интерфейсы/абстракции
├── 📂 features/               # Модули функциональности
│   ├── 📂 about/             # Страница "О нас"
│   │   ├── 📄 __init__.py
│   │   ├── 📄 routes.py      # URL маршруты
│   │   └── 📄 services.py    # Бизнес-логика
│   ├── 📂 home/              # Главная страница
│   │   ├── 📄 __init__.py
│   │   ├── 📄 routes.py
│   │   └── 📄 services.py
│   └── 📂 products/          # Продукты
│       ├── 📄 __init__.py
│       ├── 📄 routes.py
│       └── 📄 services.py
├── 📂 infra/                  # Инфраструктура
│   ├── 📄 __init__.py
│   └── 📂 db/                # База данных
│       ├── 📄 __init__.py
│       ├── 📄 models.py      # SQLAlchemy модели
│       ├── 📄 repositories.py # CRUD операции
│       └── 📄 seed_data.py   # Начальные данные
├── 📂 interfaces/             # Интерфейсы пользователя
│   ├── 📄 __init__.py
│   ├── 📂 controllers/       # Контроллеры
│   │   └── 📄 cli.py         # CLI команды
│   ├── 📂 static/            # Статика
│   │   └── 📄 style.css
│   └── 📂 templates/         # Шаблоны
│       └── 📂 partials/
│           └── 📄 header.html
├── 📂 models/                 # Модели (устаревшие)
├── 📂 shared/                 # Общие утилиты
│   ├── 📄 __init__.py
│   └── 📄 utils.py           # Вспомогательные функции
└── 📄 __init__.py            # Инициализация приложения
```

## 🎨 **TEMPLATES STRUCTURE**
```
templates/
├── 📄 base.html              # Базовый шаблон
├── 📂 about/
│   └── 📄 about.html         # Страница "О нас"
├── 📂 home/
│   └── 📄 index.html         # Главная страница
├── 📂 products/
│   ├── 📄 products.html      # Список продуктов
│   └── 📄 product_detail.html # Детали продукта
└── 📂 partials/
    └── 📄 header.html        # Частичный шаблон - заголовок
```

## 🎯 **STATIC FILES**
```
static/
├── 📄 style.css              # Основные стили
└── 📂 img/                   # Изображения
    ├── 📄 favicon.ico        # Иконка сайта
    ├── 📄 favicon-16x16.png  # Маленькая иконка
    ├── 📄 favicon-32x32.png  # Средняя иконка
    ├── 📄 apple-touch-icon.png # Иконка для iOS
    ├── 📄 android-chrome-192x192.png # Иконка для Android
    ├── 📄 android-chrome-512x512.png # Большая иконка для Android
    └── 📄 site.webmanifest   # PWA манифест
```

## 🧪 **TESTING STRUCTURE**
```
tests/
├── 📄 __init__.py
├── 📂 integration/           # Интеграционные тесты
│   ├── 📄 __init__.py
│   └── 📄 test_routes.py     # Тесты маршрутов
└── 📂 unit/                  # Модульные тесты
    ├── 📄 __init__.py
    └── 📄 test_services.py   # Тесты сервисов
```

## 📚 **RESOURCES**
```
resources/
├── 📄 py+jinfa.md           # Гайд по изучению Python
├── 📄 ARCHITECTURE.md       # Описание архитектуры
├── 📄 CLEANUP_README.md     # Инструкции по очистке
├── 📄 new-architecture.md   # Новая архитектура
└── 📄 project-mindmap.md    # Этот файл
```

## 🔄 **DATA FLOW**
```
🌐 Browser Request
    ↓
📍 URL Route (routes.py)
    ↓
🔧 Service Layer (services.py)
    ↓
🗄️ Repository (repositories.py)
    ↓
📊 Database Model (models.py)
    ↓
💾 Database (PostgreSQL)
    ↓
📊 Model → Repository → Service → Route
    ↓
🎨 Template Rendering (Jinja2)
    ↓
🌐 HTML Response
```

## 🏛️ **ARCHITECTURE PATTERNS**

### **Clean Architecture Layers:**
1. **🎨 Interface Layer** (templates/, static/)
2. **🔧 Application Layer** (features/, services.py)
3. **🏢 Domain Layer** (domain/, entities.py)
4. **🗄️ Infrastructure Layer** (infra/, db/)

### **Feature-Based Organization:**
- Each feature has its own module (about/, home/, products/)
- Each module contains routes, services, and templates
- Shared code goes to shared/ or core/

### **Dependency Inversion:**
- Domain entities don't depend on infrastructure
- Services depend on interfaces, not concrete implementations
- Repositories implement domain interfaces

## 🛠️ **TECHNOLOGY STACK**

### **Backend:**
- 🐍 **Python 3.x**
- 🌶️ **Flask** - Web framework
- 🗄️ **SQLAlchemy** - ORM
- 🐘 **PostgreSQL** - Database

### **Frontend:**
- 🎨 **Jinja2** - Template engine
- 🎯 **HTML/CSS** - Markup and styling
- 📱 **PWA** - Progressive Web App support

### **Development:**
- 🧪 **pytest** - Testing framework
- 🐳 **Docker** - Containerization
- 📦 **pip** - Package management

## 🎯 **KEY CONCEPTS**

### **Blueprint Pattern:**
- Modular Flask applications
- Each feature is a separate blueprint
- Routes are registered with blueprints

### **Repository Pattern:**
- Abstraction over data access
- Business logic doesn't know about database details
- Easy to swap data sources

### **Service Layer:**
- Business logic encapsulation
- Transaction management
- Data validation and processing

### **Template Inheritance:**
- Base template with common layout
- Child templates extend base
- Partial templates for reusable components

## 🚀 **DEPLOYMENT**

### **Development:**
```bash
pip install -r requirements.txt
python run.py
```

### **Production:**
```bash
docker-compose up -d
```

## 📈 **LEARNING PATH**

1. **🔍 Explore** - Run the app, click around
2. **📖 Read** - Study the code structure
3. **✏️ Modify** - Make small changes
4. **➕ Add** - Create new features
5. **🧪 Test** - Write and run tests
6. **🏗️ Refactor** - Improve the code
7. **🚀 Deploy** - Put it in production

---

*This mindmap shows the complete structure and relationships in the Introductory Jinja project.*