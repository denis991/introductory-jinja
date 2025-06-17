from typing import Any, Dict

from app.domain.interfaces import ProductRepository, UserRepository


class HomeService:
    """Service layer for home page business logic"""

    def __init__(
        self, user_repository: UserRepository, product_repository: ProductRepository
    ):
        self.user_repository = user_repository
        self.product_repository = product_repository

    def get_home_data(self) -> Dict[str, Any]:
        """Get all data needed for home page"""
        user = self.user_repository.get_current_user()
        products = self.product_repository.get_all_products()

        # Business logic: get unique categories from products
        categories = list(set(product.category for product in products))

        # Business logic: create sample items list
        items = ["Apple", "Banana", "Cherry", "Orange", "Mango"]

        return {
            "user": user,
            "items": items,
            "products": products,
            "categories": categories,
        }
