from datetime import datetime
from typing import List, Optional
from app.core.extensions import db
from app.domain.interfaces import UserRepository, ProductRepository, TeamRepository
from app.domain.entities import User, Product, TeamMember, ProjectStats
from .models import User as UserModel, Product as ProductModel


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
            join_date=datetime(2024, 1, 15)
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


class MockTeamRepository(TeamRepository):
    """Mock implementation of TeamRepository"""

    def get_team_members(self) -> List[TeamMember]:
        """Get all team members"""
        return [
            TeamMember(
                name="Alice Johnson",
                role="Developer",
                skills=["Python", "Flask", "Jinja"]
            ),
            TeamMember(
                name="Bob Smith",
                role="Designer",
                skills=["CSS", "HTML", "UI/UX"]
            ),
            TeamMember(
                name="Carol Davis",
                role="Manager",
                skills=["Project Management", "Agile"]
            )
        ]

    def get_project_stats(self) -> ProjectStats:
        """Get project statistics"""
        return ProjectStats(
            start_date="2024-01-01",
            version="1.0.0",
            features=["Jinja Templates", "CSS Styling", "Flask Backend", "Responsive Design"]
        )