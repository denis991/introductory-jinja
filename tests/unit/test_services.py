import unittest
from datetime import datetime
from unittest.mock import Mock

from app.domain.entities import Product, ProjectStats, TeamMember, User
from app.features.about.services import AboutService
from app.features.home.services import HomeService
from app.features.products.services import ProductService


class TestHomeService(unittest.TestCase):
    """Test cases for HomeService"""

    def setUp(self):
        self.mock_user_repo = Mock()
        self.mock_product_repo = Mock()
        self.home_service = HomeService(self.mock_user_repo, self.mock_product_repo)

    def test_get_home_data(self):
        """Test getting home page data"""
        # Arrange
        mock_user = User(
            id=1,
            name="Alice",
            email="alice@example.com",
            is_admin=True,
            join_date=datetime(2024, 1, 15),
        )
        mock_products = [
            Product(
                id=1, name="Laptop", price=999.99, category="Electronics", in_stock=True
            ),
            Product(id=2, name="Book", price=19.99, category="Books", in_stock=True),
        ]

        self.mock_user_repo.get_current_user.return_value = mock_user
        self.mock_product_repo.get_all_products.return_value = mock_products

        # Act
        result = self.home_service.get_home_data()

        # Assert
        self.assertEqual(result["user"], mock_user)
        self.assertEqual(result["products"], mock_products)
        self.assertEqual(result["categories"], ["Electronics", "Books"])
        self.assertEqual(
            result["items"], ["Apple", "Banana", "Cherry", "Orange", "Mango"]
        )


class TestProductService(unittest.TestCase):
    """Test cases for ProductService"""

    def setUp(self):
        self.mock_product_repo = Mock()
        self.product_service = ProductService(self.mock_product_repo)

    def test_get_all_products_sorted_by_rating(self):
        """Test that products are sorted by rating"""
        # Arrange
        mock_products = [
            Product(
                id=1,
                name="Laptop",
                price=999.99,
                category="Electronics",
                in_stock=True,
                rating=4.0,
            ),
            Product(
                id=2,
                name="Book",
                price=19.99,
                category="Books",
                in_stock=True,
                rating=4.5,
            ),
            Product(
                id=3,
                name="Mug",
                price=12.50,
                category="Kitchen",
                in_stock=False,
                rating=3.8,
            ),
        ]
        self.mock_product_repo.get_all_products.return_value = mock_products

        # Act
        result = self.product_service.get_all_products()

        # Assert
        self.assertEqual(result[0].rating, 4.5)  # Book should be first
        self.assertEqual(result[1].rating, 4.0)  # Laptop should be second
        self.assertEqual(result[2].rating, 3.8)  # Mug should be last


class TestAboutService(unittest.TestCase):
    """Test cases for AboutService"""

    def setUp(self):
        self.mock_team_repo = Mock()
        self.about_service = AboutService(self.mock_team_repo)

    def test_get_about_data(self):
        """Test getting about page data"""
        # Arrange
        mock_team_members = [
            TeamMember(name="Alice", role="Developer", skills=["Python", "Flask"])
        ]
        mock_project_stats = ProjectStats(
            start_date="2025-03-17",
            version="1.0.0",
            features=["Feature 1", "Feature 2"],
        )

        self.mock_team_repo.get_team_members.return_value = mock_team_members
        self.mock_team_repo.get_project_stats.return_value = mock_project_stats

        # Act
        result = self.about_service.get_about_data()

        # Assert
        self.assertEqual(result["team_members"], mock_team_members)
        self.assertEqual(result["project_stats"], mock_project_stats)


if __name__ == "__main__":
    unittest.main()
