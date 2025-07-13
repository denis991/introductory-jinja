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

docker-clean: ## Очистить Docker контейнеры и образы
	@echo "🧹 Очищаем Docker контейнеры и образы..."
	@docker-compose down -v --rmi all
	@docker system prune -f
	@echo "✅ Docker очищен"

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

docker-compose-down: ## Остановить Docker Compose
	@docker-compose down

# ----------------------------------------------------------
# Для локальной разработки:
# make migrate-init — инициализация
# make migrate-create — создать миграцию
# make migrate — применить
# make migrate-downgrade — откатить
# Порядок действий:
# Сначала выполни make migrate-init-docker
# Потом make migrate-create-docker
# Затем make migrate-docker

init-db: ## Инициализировать базу данных
	@FLASK_APP=run.py .venv/bin/flask init-db

seed-db: ## Заполнить базу данных тестовыми данными (локально)
	@unset DATABASE_URL && FLASK_APP=app.core:create_app .venv/bin/flask seed-db

seed-db-docker: ## Заполнить базу данных тестовыми данными в Docker
	@docker-compose exec web flask seed-db

migrate-init: ## Инициализировать Flask-Migrate (создать папку migrations)
	@unset DATABASE_URL && FLASK_APP=app.core:create_app .venv/bin/flask db init

migrate-create: ## Создать новую миграцию
	@unset DATABASE_URL && FLASK_APP=app.core:create_app .venv/bin/flask db migrate -m "Auto migration"

migrate: ## Применить миграции Alembic/Flask-Migrate (локально)
	@unset DATABASE_URL && FLASK_APP=app.core:create_app .venv/bin/flask db upgrade

##################Docker
migrate-downgrade: ## Откатить миграцию Alembic/Flask-Migrate (локально)
	@unset DATABASE_URL && FLASK_APP=app.core:create_app .venv/bin/flask db downgrade prev

migrate-docker: ## Применить миграции внутри Docker-контейнера
	@docker-compose exec web flask db upgrade

migrate-downgrade-docker: ## Откатить миграцию внутри Docker-контейнера
	@docker-compose exec web flask db downgrade prev

migrate-init-docker: ## Инициализировать Flask-Migrate в Docker
	@docker-compose exec web flask db init

migrate-create-docker: ## Создать новую миграцию в Docker
	@docker-compose exec web flask db migrate -m "Auto migration"

migrate-status: ## Показать статус миграций
	@docker-compose exec web flask db current

migrate-history: ## Показать историю миграций
	@docker-compose exec web flask db history

migrate-downgrade-all: ## Откатить все миграции до начала (base)
	@docker-compose exec web flask db downgrade base

migrate-clean: ## Полностью очистить базу данных (удалить все данные)
	@docker-compose exec web flask drop-db

migrate-reset: ## Полный сброс: очистить БД, применить миграции, накатить сиды
	@echo "🔄 Полный сброс базы данных..."
	@docker-compose exec web flask drop-db
	@docker-compose exec web flask db migrate -m "Initial migration" || true
	@docker-compose exec web flask db upgrade
	@docker-compose exec web flask seed-db
	@echo "✅ База данных сброшена и заполнена тестовыми данными"

migrate-reset-local: ## Полный сброс локально (SQLite)
	@echo "🔄 Полный сброс локальной базы данных..."
	@unset DATABASE_URL && FLASK_APP=app.core:create_app .venv/bin/flask drop-db
	@unset DATABASE_URL && FLASK_APP=app.core:create_app .venv/bin/flask db migrate -m "Initial migration" || true
	@unset DATABASE_URL && FLASK_APP=app.core:create_app .venv/bin/flask db upgrade
	@unset DATABASE_URL && FLASK_APP=app.core:create_app .venv/bin/flask seed-db
	@echo "✅ Локальная база данных сброшена и заполнена тестовыми данными"

# ----------------------------------------------------------

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
