from typing import List, Optional, Tuple
from app.domain.entities import Category
from app.domain.interfaces import CategoryRepository

# Можно внедрять репозиторий через DI, но для простоты создаём экземпляр здесь
from app.infra.db.repositories import SQLAlchemyCategoryRepository
category_repo: CategoryRepository = SQLAlchemyCategoryRepository()


def get_all_categories() -> List[Category]:
    """Получить все категории"""
    return category_repo.get_all_categories()


def get_categories_paginated(page: int = 1, per_page: int = 12) -> Tuple[List[Category], int, int, int]:
    """
    Получить категории с пагинацией

    Args:
        page: Номер страницы (начиная с 1)
        per_page: Количество элементов на странице

    Returns:
        Tuple[список_категорий, общее_количество, текущая_страница, всего_страниц]
    """
    return category_repo.get_categories_paginated(page, per_page)


def get_category_by_id(category_id: int) -> Optional[Category]:
    """Получить категорию по ID"""
    return category_repo.get_category_by_id(category_id)


def create_category(name: str, description: Optional[str] = None) -> Category:
    """Создать новую категорию"""
    return category_repo.create_category(name, description)


def update_category(category_id: int, name: Optional[str] = None, description: Optional[str] = None) -> Optional[Category]:
    """Обновить существующую категорию"""
    return category_repo.update_category(category_id, name, description)


def delete_category(category_id: int) -> bool:
    """Удалить категорию по ID"""
    return category_repo.delete_category(category_id)