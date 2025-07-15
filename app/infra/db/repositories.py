# Здесь реализуются репозитории — классы для доступа к данным в базе данных (CRUD-операции).
# Репозитории инкапсулируют работу с ORM и позволяют отделить
# бизнес-логику от деталей хранения данных.
import math
from datetime import datetime
from typing import List, Optional, Tuple

from app.domain.entities import (Category, Product, ProjectStats, TeamMember,
                                User)
from app.domain.interfaces import (CategoryRepository, ProductRepository,
                                   TeamRepository, UserRepository)

from .models import Category as CategoryModel
from .models import Product as ProductModel
from .models import User as UserModel


class SQLAlchemyUserRepository(UserRepository):
    """SQLAlchemy implementation of UserRepository"""

    def get_current_user(self) -> User:
        """Get current user (mock implementation)"""
        # In a real app, this would get the user from session/token
        user_model = UserModel.query.filter_by(email="alice@example.com").first()
        if user_model:
            return user_model.to_domain()

        # Fallback to mock data
        return User(
            id=1,
            name="Alice",
            email="alice@example.com",
            is_admin=True,
            join_date=datetime(2024, 1, 15),
        )


class SQLAlchemyProductRepository(ProductRepository):
    """SQLAlchemy implementation of ProductRepository"""

    def get_all_products(self) -> List[Product]:
        """Get all products"""
        products = ProductModel.query.all()
        return [product.to_domain() for product in products]

    def get_products_by_category(self, category: str) -> List[Product]:
        """Get products by category"""
        products = ProductModel.query.filter_by(category=category).all()
        return [product.to_domain() for product in products]

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Get product by ID"""
        product = ProductModel.query.get(product_id)
        return product.to_domain() if product else None


class SQLAlchemyCategoryRepository(CategoryRepository):
    """SQLAlchemy implementation of CategoryRepository with performance optimizations"""

    def get_all_categories(self) -> List[Category]:
        """Get all categories with optimized query"""
        # Получаем полные объекты модели для совместимости
        categories = CategoryModel.query.all()
        return [category.to_domain() for category in categories]

    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        """Get category by ID with optimized query"""
        category = CategoryModel.query.filter_by(id=category_id).first()
        return category.to_domain() if category else None

    def create_category(self, name: str, description: Optional[str] = None) -> Category:
        """Create new category with optimized transaction"""
        from app.core.extensions import db

        try:
            category = CategoryModel(name=name, description=description)
            db.session.add(category)
            db.session.flush()  # Получаем ID без коммита
            db.session.commit()
            return category.to_domain()
        except Exception as e:
            db.session.rollback()
            raise e

    def update_category(
        self,
        category_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Optional[Category]:
        """Update category with optimized query"""
        from app.core.extensions import db

        try:
            # Используем update для оптимизации
            update_data = {}
            if name is not None:
                update_data["name"] = name
            if description is not None:
                update_data["description"] = description

            if update_data:
                rows_updated = CategoryModel.query.filter_by(id=category_id).update(
                    update_data
                )
                if rows_updated > 0:
                    db.session.commit()
                    return self.get_category_by_id(category_id)
            return None
        except Exception as e:
            db.session.rollback()
            raise e

    def delete_category(self, category_id: int) -> bool:
        """Delete category with optimized query"""
        from app.core.extensions import db

        try:
            rows_deleted = CategoryModel.query.filter_by(id=category_id).delete()
            if rows_deleted > 0:
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            raise e

    def get_categories_paginated(
        self, page: int = 1, per_page: int = 12
    ) -> Tuple[List[Category], int, int, int]:
        """
        Get categories with pagination and performance optimizations

        Args:
            page: Page number (starting from 1)
            per_page: Number of items per page

        Returns:
            Tuple[list_of_categories, total_count, current_page, total_pages]
        """
        from app.core.extensions import db

        # Подсчет общего количества
        total_count = CategoryModel.query.count()

        # Calculate total pages
        total_pages = math.ceil(total_count / per_page) if total_count > 0 else 1

        # Ensure page is within valid range
        page = max(1, min(page, total_pages))

        # Оптимизированный запрос с пагинацией
        offset = (page - 1) * per_page
        categories = CategoryModel.query.offset(offset).limit(per_page).all()

        # Convert to domain entities
        category_list = [category.to_domain() for category in categories]

        return category_list, total_count, page, total_pages


class MockTeamRepository(TeamRepository):
    """Mock implementation of TeamRepository"""

    def get_team_members(self) -> List[TeamMember]:
        """Get all team members"""
        return [
            TeamMember(
                name="Alice Johnson",
                role="Developer",
                skills=["Python", "Flask", "Jinja"],
            ),
            TeamMember(
                name="Bob Smith", role="Designer", skills=["CSS", "HTML", "UI/UX"]
            ),
            TeamMember(
                name="Carol Davis",
                role="Manager",
                skills=["Project Management", "Agile"],
            ),
        ]

    def get_project_stats(self) -> ProjectStats:
        """Get project statistics"""
        return ProjectStats(
            start_date="2025-03-17",
            version="1.0.0",
            features=[
                "Jinja Templates",
                "CSS Styling",
                "Flask Backend",
                "Responsive Design",
            ],
        )
