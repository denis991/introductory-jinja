from typing import List, Optional

from app.domain.entities import Product
from app.domain.interfaces import ProductRepository


class ProductService:
    """Service layer for products page business logic"""

    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def get_all_products(self) -> List[Product]:
        """Get all products with business logic applied"""
        products = self.product_repository.get_all_products()

        # Business logic: sort products by rating (highest first)
        return sorted(products, key=lambda p: p.rating or 0, reverse=True)

    def get_products_by_category(self, category: str) -> List[Product]:
        """Get products by category"""
        return self.product_repository.get_products_by_category(category)

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Get product by ID"""
        return self.product_repository.get_product_by_id(product_id)

    def get_available_categories(self) -> List[str]:
        """Get all available product categories"""
        products = self.product_repository.get_all_products()
        return list(set(product.category for product in products))
