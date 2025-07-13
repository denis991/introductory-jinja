# Здесь реализуются репозитории — классы для доступа к данным в базе данных (CRUD-операции).
# Репозитории инкапсулируют работу с ORM и позволяют отделить бизнес-логику от деталей хранения данных.
from datetime import datetime
from typing import List, Optional, Tuple
import math

from app.domain.entities import Product, ProjectStats, TeamMember, User, Category
from app.domain.interfaces import (ProductRepository, TeamRepository,
                                  UserRepository, CategoryRepository)

from .models import Product as ProductModel
from .models import User as UserModel
from .models import Category as CategoryModel


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
    """SQLAlchemy implementation of CategoryRepository"""

    def get_all_categories(self) -> List[Category]:
        categories = CategoryModel.query.all()
        return [category.to_domain() for category in categories]

    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        category = CategoryModel.query.get(category_id)
        return category.to_domain() if category else None

    def create_category(self, name: str, description: Optional[str] = None) -> Category:
        category = CategoryModel(name=name, description=description)
        from app.core.extensions import db
        db.session.add(category)
        db.session.commit()
        return category.to_domain()

    def update_category(self, category_id: int, name: Optional[str] = None, description: Optional[str] = None) -> Optional[Category]:
        from app.core.extensions import db
        category = CategoryModel.query.get(category_id)
        if not category:
            return None
        if name is not None:
            category.name = name
        if description is not None:
            category.description = description
        db.session.commit()
        return category.to_domain()

    def delete_category(self, category_id: int) -> bool:
        from app.core.extensions import db
        category = CategoryModel.query.get(category_id)
        if not category:
            return False
        db.session.delete(category)
        db.session.commit()
        return True

    def get_categories_paginated(self, page: int = 1, per_page: int = 12) -> Tuple[List[Category], int, int, int]:
        """
        Get categories with pagination

        Args:
            page: Page number (starting from 1)
            per_page: Number of items per page

        Returns:
            Tuple[list_of_categories, total_count, current_page, total_pages]
        """
        from app.core.extensions import db

        # Get total count
        total_count = CategoryModel.query.count()

        # Calculate total pages
        total_pages = math.ceil(total_count / per_page) if total_count > 0 else 1

        # Ensure page is within valid range
        page = max(1, min(page, total_pages))

        # Get paginated results
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
