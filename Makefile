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

.PHONY: all venv install run kill-port kill-all-ports freeze clean

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

kill-port:
	@echo "🔫 Очищаем порт $(or $(PORT),$(DEFAULT_PORT))..."
	@if lsof -ti:$(or $(PORT),$(DEFAULT_PORT)) > /dev/null 2>&1; then \
		echo "Найдены процессы на порту $(or $(PORT),$(DEFAULT_PORT)):"; \
		lsof -i:$(or $(PORT),$(DEFAULT_PORT)); \
		echo "Убиваем процессы..."; \
		lsof -ti:$(or $(PORT),$(DEFAULT_PORT)) | xargs kill -9; \
		echo "✅ Порт $(or $(PORT),$(DEFAULT_PORT)) очищен."; \
	else \
		echo "✅ Порт $(or $(PORT),$(DEFAULT_PORT)) свободен."; \
	fi

kill-all-ports:
	@echo "🔫 Очищаем все порты..."
	@echo "Внимание! Эта команда убьет ВСЕ процессы на ВСЕХ портах!"
	@echo "Используйте с осторожностью!"
	@read -p "Продолжить? (y/N): " confirm && [ "$$confirm" = "y" ] || exit 1
	@echo "Убиваем все процессы на портах..."
	@for port in $$(lsof -ti:1-65535 2>/dev/null); do \
		echo "Убиваем процесс $$port"; \
		kill -9 $$port 2>/dev/null || true; \
	done
	@echo "✅ Все порты очищены."

run: install kill-port
	@echo "🚀 Запуск Flask на порту $(DEFAULT_PORT)..."
	# Экспортируем переменные окружения:
	FLASK_APP=app.py \
	FLASK_ENV=development \
	FLASK_RUN_PORT=$(DEFAULT_PORT) \
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

# Дополнительные команды для разработки
help:
	@echo "Доступные команды:"
	@echo "  make install        - Установить зависимости"
	@echo "  make run           - Запустить приложение (автоматически очищает порт 5006)"
	@echo "  make kill-port     - Очистить порт 5006 (или указать PORT=8080)"
	@echo "  make kill-all-ports - Очистить ВСЕ порты (осторожно!)"
	@echo "  make clean         - Очистить проект"
	@echo ""
	@echo "Примеры использования:"
	@echo "  make kill-port PORT=8080  - Очистить порт 8080"
	@echo "  make kill-port            - Очистить порт 5006 (по умолчанию)"
