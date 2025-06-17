#!/usr/bin/env python3
"""
Скрипт для очистки проекта перед архивированием.
Удаляет временные файлы, кэши и другие ненужные файлы.
"""

import os
import shutil
import sys
from pathlib import Path


def clean_project():
    """Очищает проект от временных файлов"""

    # Получаем корневую директорию проекта
    project_root = Path(__file__).parent

    # Список файлов и папок для удаления
    files_to_remove = [
        # Python кэш
        "__pycache__",
        "*.pyc",
        "*.pyo",
        "*.pyd",
        ".Python",

        # Временные файлы
        "*.tmp",
        "*.temp",
        "*.swp",
        "*.swo",
        "*~",

        # Логи
        "*.log",
        "logs/",

        # Coverage и тесты
        ".coverage",
        ".pytest_cache/",
        "htmlcov/",
        ".tox/",
        ".nox/",

        # IDE файлы
        ".vscode/",
        ".idea/",
        "*.sublime-*",

        # macOS
        ".DS_Store",
        "._*",

        # Windows
        "Thumbs.db",
        "ehthumbs.db",
        "Desktop.ini",

        # Linux
        "*~",
        ".fuse_hidden*",

        # Docker
        ".dockerignore",

        # Node.js (если есть)
        "node_modules/",
        "npm-debug.log*",
        "yarn-debug.log*",
        "yarn-error.log*",

        # Базы данных (если есть локальные)
        "*.db",
        "*.sqlite",
        "*.sqlite3",

        # Временные файлы проекта
        "instance/",
        ".webassets-cache",

        # Локальные настройки
        ".env.local",
        ".env.development",
        ".env.test",

        # Backup файлы
        "*.bak",
        "*.backup",
        "*_backup",

        # Архивы (если есть)
        "*.zip",
        "*.tar.gz",
        "*.rar",

        # Документация сборки
        "docs/_build/",
        "site/",

        # Jupyter
        ".ipynb_checkpoints",

        # mypy
        ".mypy_cache/",

        # pytype
        ".pytype/",

        # Cython
        "cython_debug/",
    ]

    # Список папок для удаления (рекурсивно)
    dirs_to_remove = [
        "__pycache__",
        ".pytest_cache",
        ".tox",
        ".nox",
        "htmlcov",
        ".vscode",
        ".idea",
        "node_modules",
        "instance",
        ".webassets-cache",
        "docs/_build",
        "site",
        ".ipynb_checkpoints",
        ".mypy_cache",
        ".pytype",
        "cython_debug",
        "logs",
    ]

    removed_count = 0

    print("🧹 Начинаю очистку проекта...")
    print(f"📁 Корневая директория: {project_root}")
    print()

    # Удаляем файлы
    for pattern in files_to_remove:
        if "*" in pattern:
            # Паттерн с wildcard
            for file_path in project_root.rglob(pattern):
                if file_path.is_file():
                    try:
                        file_path.unlink()
                        print(f"🗑️  Удален файл: {file_path.relative_to(project_root)}")
                        removed_count += 1
                    except Exception as e:
                        print(f"❌ Ошибка при удалении {file_path}: {e}")
        else:
            # Точное имя файла/папки
            file_path = project_root / pattern
            if file_path.exists():
                try:
                    if file_path.is_file():
                        file_path.unlink()
                        print(f"🗑️  Удален файл: {pattern}")
                    elif file_path.is_dir():
                        shutil.rmtree(file_path)
                        print(f"🗑️  Удалена папка: {pattern}")
                    removed_count += 1
                except Exception as e:
                    print(f"❌ Ошибка при удалении {pattern}: {e}")

    # Удаляем папки рекурсивно
    for dir_name in dirs_to_remove:
        for dir_path in project_root.rglob(dir_name):
            if dir_path.is_dir():
                try:
                    shutil.rmtree(dir_path)
                    print(f"🗑️  Удалена папка: {dir_path.relative_to(project_root)}")
                    removed_count += 1
                except Exception as e:
                    print(f"❌ Ошибка при удалении {dir_path}: {e}")

    print()
    print(f"✅ Очистка завершена! Удалено объектов: {removed_count}")

    # Показываем размер проекта
    total_size = get_directory_size(project_root)
    print(f"📊 Размер проекта: {format_size(total_size)}")

    return removed_count


def get_directory_size(directory):
    """Вычисляет размер директории в байтах"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                total_size += os.path.getsize(filepath)
            except (OSError, FileNotFoundError):
                pass
    return total_size


def format_size(size_bytes):
    """Форматирует размер в читаемом виде"""
    if size_bytes == 0:
        return "0 B"

    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1

    return f"{size_bytes:.1f} {size_names[i]}"


if __name__ == "__main__":
    try:
        clean_project()
    except KeyboardInterrupt:
        print("\n❌ Очистка прервана пользователем")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Ошибка при очистке: {e}")
        sys.exit(1)

# Создадим скрипт для очистки проекта: