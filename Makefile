# Makefile для Flask + Jinja2 проекта
# ---------------------------------------------------
# Targets:
#   venv     — создать виртуальное окружение
#   install  — установить зависимости из requirements.txt
#   run      — запустить dev-сервер на порту 5006
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

.PHONY: all venv install run freeze clean

all: venv install run

venv:
	@echo "⚙️  Создаём виртуальное окружение $(VENV)..."
	@test -d $(VENV) || python3 -m venv $(VENV)
	@echo "✅ Окружение готово."

install: venv
	@echo "📦 Устанавливаем зависимости из $(REQ)..."
	$(PIP) install --upgrade pip
	$(PIP) install -r $(REQ)
	@echo "✅ Зависимости установлены."

run: install
	@echo "🚀 Запуск Flask на порту 5006..."
	# Экспортируем переменные окружения:
	FLASK_APP=app.py \
	FLASK_ENV=development \
	FLASK_RUN_PORT=5006 \
	$(FLASK) run

freeze: venv
	@echo "📝 Замораживаем зависимости в $(REQ)..."
	$(PIP) freeze > $(REQ)
	@echo "✅ $(REQ) обновлён."

clean:
	@echo "🧹 Удаляем виртуальное окружение и кэш..."
	rm -rf $(VENV) __pycache__ .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "✅ Очистка завершена."
