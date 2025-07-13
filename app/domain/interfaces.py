# Здесь определяются интерфейсы (абстракции) для репозиториев и сервисов.
# Это контракты, которые описывают, какие методы должны быть реализованы для работы с данными или бизнес-логикой.
from abc import ABC, abstractmethod
from typing import List, Optional

from .entities import Product, ProjectStats, TeamMember, User


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
