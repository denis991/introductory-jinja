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

.PHONY: all venv install run kill-port kill-all-ports freeze clean help setup dev test test-unit test-integration docker-build docker-run docker-compose-up docker-compose-down init-db seed-db

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

docker-build: ## Собрать Docker образ
	@docker build -t jinja-app .

docker-run: ## Запустить Docker контейнер
	@docker run -p $(DEFAULT_PORT):$(DEFAULT_PORT) jinja-app

docker-compose-up: ## Запустить с Docker Compose
	@docker-compose up --build

docker-compose-down: ## Остановить Docker Compose
	@docker-compose down

init-db: ## Инициализировать базу данных
	@FLASK_APP=run.py .venv/bin/flask init-db

seed-db: ## Заполнить базу данных тестовыми данными
	@FLASK_APP=run.py .venv/bin/flask seed-db

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
init-db:
	FLASK_APP=run.py flask init-db
	FLASK_APP=run.py flask seed-db