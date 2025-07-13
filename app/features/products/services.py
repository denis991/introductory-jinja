"""
Сервисы для работы с товарами
Содержит как класс ProductService для UI, так и функции для API
"""
from typing import List, Optional

from app.domain.entities import Product
from app.domain.interfaces import ProductRepository
from app.infra.db.repositories import SQLAlchemyProductRepository
from app.infra.db.models import Product as ProductModel
from app.core.extensions import db


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


# API функции (используют реальные репозитории)
def get_all_products():
    """Получить все товары"""

    repository = SQLAlchemyProductRepository()
    return repository.get_all_products()

def get_product_by_id(product_id):
    """Получить товар по ID"""
    repository = SQLAlchemyProductRepository()
    return repository.get_product_by_id(product_id)

def create_product(name, description=None, price=0.0, category_ids=None):
    """Создать новый товар"""


    product = ProductModel(
        name=name,
        price=price,
        category=description or "General",  # Используем description как category
        in_stock=True,
        rating=0.0
    )

    db.session.add(product)
    db.session.commit()

    return product.to_domain()

def update_product(product_id, name=None, description=None, price=None, category_ids=None):
    """Обновить товар"""

    product = ProductModel.query.get(product_id)
    if not product:
        return None

    if name is not None:
        product.name = name
    if description is not None:
        product.category = description  # Используем description как category
    if price is not None:
        product.price = price

    db.session.commit()
    return product.to_domain()

def delete_product(product_id):
    """Удалить товар"""

    product = ProductModel.query.get(product_id)
    if not product:
        return False

    db.session.delete(product)
    db.session.commit()
    return True
