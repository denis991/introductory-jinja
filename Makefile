# Makefile для Flask + Jinja2 проекта
# ---------------------------------------------------
# Targets:
#   venv     — создать виртуальное окружение
#   install  — установить зависимости из requirements.txt
#   run      — запустить dev-сервер на порту 5006
#   kill-port — убить процесс на указанном порту (по умолчанию 5006)
#   kill-all-ports — убить все процессы на всех портах
#   freeze   — зафиксировать текущие зависимости
#   clean    — удалить окружение и кэш
#   docker-dev — запустить всё в Docker (разработка)
#   docker-prod — запустить всё в Docker (продакшн)
#   docker-stop — остановить Docker контейнеры
#   docker-clean — очистить Docker контейнеры и образы
# ---------------------------------------------------

# Shell
SHELL := /bin/bash

# Имя виртуального окружения
VENV := .venv

# Python-интерпретатор внутри venv
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
FLASK := $(VENV)/bin/flask

# Файл с зависимостями
REQ := requirements.txt

# Порт по умолчанию
DEFAULT_PORT := 5006

.PHONY: all venv install run kill-port kill-all-ports freeze clean help setup dev test test-unit test-integration docker-dev docker-prod docker-stop docker-clean docker-build docker-run docker-compose-up docker-compose-down init-db seed-db

all: venv install run

help: ## Показать справку
	@echo "Доступные команды:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

venv: ## Создать виртуальное окружение
	@echo "⚙️  Создаём виртуальное окружение .venv..."
	@python3 -m venv .venv
	@echo "✅ Окружение готово."

install: ## Установить зависимости
	@echo "📦 Устанавливаем зависимости из requirements.txt..."
	@.venv/bin/pip install --upgrade pip
	@.venv/bin/pip install -r requirements.txt
	@echo "✅ Зависимости установлены."
# source .venv/bin/activate

run: ## Запустить приложение
	@echo "🔫 Очищаем порт $(DEFAULT_PORT)..."
	@lsof -ti:$(DEFAULT_PORT) | xargs kill -9 2>/dev/null || true
	@echo "✅ Порт $(DEFAULT_PORT) свободен."
	@echo "🚀 Запуск Flask на порту $(DEFAULT_PORT)..."
	@echo "# Экспортируем переменные окружения:"
	@echo "FLASK_APP=run.py \\"
	@echo "        FLASK_ENV=development \\"
	@echo "        FLASK_RUN_PORT=$(DEFAULT_PORT) \\"
	@echo "        .venv/bin/flask run"
	@FLASK_APP=run.py \
		FLASK_ENV=development \
		FLASK_RUN_PORT=$(DEFAULT_PORT) \
		.venv/bin/flask run

setup: install init-db seed-db ## Полная настройка проекта

dev: setup run ## Настройка и запуск для разработки

test: ## Запустить тесты
	@.venv/bin/python -m pytest tests/ -v

test-unit: ## Запустить unit тесты
	@.venv/bin/python -m pytest tests/unit/ -v

test-integration: ## Запустить integration тесты
	@.venv/bin/python -m pytest tests/integration/ -v

clean: ## Очистить кэш Python
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete

# Docker команды
docker-dev: ## Запустить всё в Docker (разработка)
	@echo "🐳 Запускаем приложение в Docker (разработка)..."
	@docker-compose up --build -d
	@echo "⏳ Ждём запуска приложения..."
	@sleep 10
	@echo "✅ Приложение запущено на http://localhost:$(DEFAULT_PORT)"
	@echo "📊 База данных доступна на localhost:5432"
	@echo "🔍 Логи: docker-compose logs -f"

docker-prod: ## Запустить всё в Docker (продакшн)
	@echo "🐳 Запускаем приложение в Docker (продакшн)..."
	@FLASK_ENV=production docker-compose -f docker-compose.yml up --build -d
	@echo "✅ Приложение запущено в продакшн режиме"

docker-stop: ## Остановить Docker контейнеры
	@echo "🛑 Останавливаем Docker контейнеры..."
	@docker-compose down
	@echo "✅ Контейнеры остановлены"

docker-clean: ## Очистить только данные и контейнеры этого проекта (без глобального prune!)
	@echo "🧹 Очищаем только контейнеры и volume этого проекта..."
	@docker-compose down -v
	@echo "✅ Контейнеры и volume проекта удалены"

docker-db-clean: ## Удалить только volume базы данных проекта
	@echo "🧹 Удаляем volume postgres_data..."
	@docker-compose down
	@docker volume rm introductory-jinja_postgres_data || true
	@echo "✅ Volume базы данных удалён"

docker-logs: ## Показать логи Docker контейнеров
	@docker-compose logs -f

docker-shell: ## Войти в контейнер приложения
	@docker-compose exec web bash

docker-db-shell: ## Войти в контейнер базы данных
	@docker-compose exec db psql -U postgres -d jinja_app

# Устаревшие команды (оставляем для совместимости)
docker-build: ## Собрать Docker образ
	@docker build -t jinja-app .

docker-run: ## Запустить Docker контейнер
	@docker run -p $(DEFAULT_PORT):$(DEFAULT_PORT) jinja-app

docker-compose-up: ## Запустить с Docker Compose
	@docker-compose up --build


# =====================[ DB Management ]=====================

# Выбор среды: local (по умолчанию) или docker
DB_ENV ?= local

# Строки подключения и команды для разных сред
ifeq ($(DB_ENV),docker)
	DB_EXEC = docker-compose exec web flask
else
	DB_EXEC = .venv/bin/flask
endif

# Инициализация БД
init-db: ## Инициализировать базу данных (локально или в Docker)
	@echo "Инициализация БД ($(DB_ENV))..."
	@FLASK_APP=run.py $(DB_EXEC) init-db

# Сидирование БД
seed-db: ## Заполнить базу данных тестовыми данными (локально или в Docker)
	@echo "Сидирование БД ($(DB_ENV))..."
	@FLASK_APP=app.core:create_app $(DB_EXEC) seed-db

# Миграции
migrate-init: ## Инициализировать Flask-Migrate (локально или в Docker)
	@echo "Инициализация миграций ($(DB_ENV))..."
	@FLASK_APP=app.core:create_app $(DB_EXEC) db init

migrate-create: ## Создать новую миграцию (локально или в Docker)
	@echo "Создание миграции ($(DB_ENV))..."
	@FLASK_APP=app.core:create_app $(DB_EXEC) db migrate -m "Auto migration"

migrate: ## Применить миграции (локально или в Docker)
	@echo "Применение миграций ($(DB_ENV))..."
	@FLASK_APP=app.core:create_app $(DB_EXEC) db upgrade

migrate-downgrade: ## Откатить миграцию (локально или в Docker)
	@echo "Откат миграции ($(DB_ENV))..."
	@FLASK_APP=app.core:create_app $(DB_EXEC) db downgrade prev

# Удалить локальную базу данных PostgreSQL
# Использует переменные окружения для имени БД, пользователя и хоста
PG_DB ?= jinja_app
PG_USER ?= postgres
PG_HOST ?= localhost

# Удалить базу данных локально
ifeq ($(DB_ENV),local)
drop-db-local: ## [LOCAL] Удалить базу данных PostgreSQL (jinja_app)
	@echo "Удаляем базу данных $(PG_DB)..."
	@PGPASSWORD=$(POSTGRES_PASSWORD) psql -U $(PG_USER) -h $(PG_HOST) -d postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '$(PG_DB)';" || true
	@PGPASSWORD=$(POSTGRES_PASSWORD) psql -U $(PG_USER) -h $(PG_HOST) -d postgres -c "DROP DATABASE IF EXISTS $(PG_DB);"

recreate-db-local: drop-db-local ## [LOCAL] Пересоздать базу данных PostgreSQL (jinja_app)
	@echo "Создаём базу данных $(PG_DB)..."
	@PGPASSWORD=$(POSTGRES_PASSWORD) psql -U $(PG_USER) -h $(PG_HOST) -d postgres -c "CREATE DATABASE $(PG_DB) OWNER $(PG_USER);"
endif

# Обновлённый полный сброс БД -> make migrate-reset DB_ENV=docker
migrate-reset: ## Полный сброс: удалить БД, применить миграции, накатить сиды (локально или в Docker)
	@echo "🔄 Полный сброс базы данных ($(DB_ENV))..."
ifeq ($(DB_ENV),local)
	$(MAKE) recreate-db-local
endif
	@FLASK_APP=app.core:create_app $(DB_EXEC) db upgrade
	@FLASK_APP=app.core:create_app $(DB_EXEC) seed-db
	@echo "✅ База данных сброшена и заполнена тестовыми данными"

# =====================[ End DB Management ]=====================

kill-port: ## Убить процесс на порту $(DEFAULT_PORT)
	@lsof -ti:$(DEFAULT_PORT) | xargs kill -9 2>/dev/null || echo "Порт $(DEFAULT_PORT) уже свободен"

kill-all-ports: ## Убить все процессы на портах 5000-5010
	@for port in {5000..5010}; do \
		lsof -ti:$$port | xargs kill -9 2>/dev/null || true; \
	done
	@echo "✅ Все порты 5000-5010 очищены"

freeze: ## Заморозить зависимости
	@.venv/bin/pip freeze > requirements.txt
	@echo "✅ Зависимости заморожены в requirements.txt"

# Для инициализации и наполнения БД
init-db-old:
	FLASK_APP=run.py flask init-db
	FLASK_APP=run.py flask seed-db

# Команды для очистки и архивирования проекта!!!!!!!!!!!!!!!!!!
clean-project: ## Очистить проект от временных файлов
	@echo "🧹 Очищаем проект от временных файлов..."
	@python clean_project.py

clean-all: clean clean-project ## Полная очистка (кэш + временные файлы)
	@echo "✅ Полная очистка завершена"

archive: clean-project ## Создать архив проекта
	@echo "📦 Создаём архив проекта..."
	@PROJECT_NAME=$$(basename $$(pwd)) && \
	ARCHIVE_NAME="$${PROJECT_NAME}_$(shell date +%Y%m%d_%H%M%S).tar.gz" && \
	tar --exclude='.git' --exclude='.venv' --exclude='venv' --exclude='node_modules' \
		--exclude='__pycache__' --exclude='*.pyc' --exclude='.pytest_cache' \
		--exclude='.coverage' --exclude='htmlcov' --exclude='.tox' \
		--exclude='.vscode' --exclude='.idea' --exclude='.DS_Store' \
		--exclude='*.log' --exclude='instance' --exclude='*.db' \
		--exclude='*.sqlite' --exclude='*.sqlite3' \
		-czf "$$ARCHIVE_NAME" . && \
	echo "✅ Архив создан: $$ARCHIVE_NAME" && \
	echo "📊 Размер архива: $$(du -h "$$ARCHIVE_NAME" | cut -f1)"

archive-clean: clean-all archive ## Очистить и создать архив

prepare-release: clean-project ## Подготовить проект к релизу
	@echo "🚀 Подготовка проекта к релизу..."
	@echo "✅ Проект готов к архивированию"
	@echo "📋 Следующие шаги:"
	@echo "   1. Проверьте код: make lint"
	@echo "   2. Запустите тесты: make test"
	@echo "   3. Создайте архив: make archive"

lint: ## Проверить код линтерами
	@echo "🔍 Проверяем код..."
	@flake8
	@echo "✅ Код проверен"

format: ## Отформатировать код
	@echo "🎨 Форматируем код..."
	@black .
	@isort .
	@echo "✅ Код отформатирован"

lint-fix: format ## Исправить проблемы с кодом
	@echo "🔧 Исправляем проблемы..."
	@autopep8 --in-place --recursive --aggressive --aggressive .
	@echo "✅ Проблемы исправлены"
# ---------------------------
