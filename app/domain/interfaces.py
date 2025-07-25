# Здесь определяются интерфейсы (абстракции) для репозиториев и сервисов.
# Это контракты, которые описывают, какие методы должны быть реализованы
# для работы с данными или бизнес-логикой.
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from .entities import Category, Product, ProjectStats, TeamMember, User


class UserRepository(ABC):
    """User repository interface"""

    @abstractmethod
    def get_current_user(self) -> User:
        """Get current user"""
        pass


class ProductRepository(ABC):
    """Product repository interface"""

    @abstractmethod
    def get_all_products(self) -> List[Product]:
        """Get all products"""
        pass

    @abstractmethod
    def get_products_by_category(self, category: str) -> List[Product]:
        """Get products by category"""
        pass

    @abstractmethod
    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Get product by ID"""
        pass


class TeamRepository(ABC):
    """Team repository interface"""

    @abstractmethod
    def get_team_members(self) -> List[TeamMember]:
        """Get all team members"""
        pass

    @abstractmethod
    def get_project_stats(self) -> ProjectStats:
        """Get project statistics"""
        pass


class CategoryRepository(ABC):
    """Category repository interface"""

    @abstractmethod
    def get_all_categories(self) -> List[Category]:
        """Get all categories"""
        pass

    @abstractmethod
    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        """Get category by ID"""
        pass

    @abstractmethod
    def create_category(self, name: str, description: Optional[str] = None) -> Category:
        """Create a new category"""
        pass

    @abstractmethod
    def update_category(
        self,
        category_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Optional[Category]:
        """Update an existing category"""
        pass

    @abstractmethod
    def delete_category(self, category_id: int) -> bool:
        """Delete a category by ID"""
        pass

    @abstractmethod
    def get_categories_paginated(
        self, page: int = 1, per_page: int = 12
    ) -> Tuple[List[Category], int, int, int]:
        """
        Get categories with pagination

        Args:
            page: Page number (starting from 1)
            per_page: Number of items per page

        Returns:
            Tuple[list_of_categories, total_count, current_page, total_pages]
        """
        pass
