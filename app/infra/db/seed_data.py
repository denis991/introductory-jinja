# Этот файл содержит функции и данные для начального заполнения базы данных (seed).
# Используется для создания тестовых или стартовых данных при первом запуске приложения.
from datetime import datetime

from app.core.extensions import db
from app.infra.db.models import Product, User


def seed_database():
    """Seed the database with initial data"""

    # Create users
    users = [
        User(
            name="Alice",
            email="alice@example.com",
            is_admin=True,
            join_date=datetime(2024, 1, 15),
        ),
        User(
            name="Bob",
            email="bob@example.com",
            is_admin=False,
            join_date=datetime(2024, 2, 1),
        ),
    ]

    for user in users:
        db.session.add(user)

    # Create products
    products = [
        Product(
            name="Laptop",
            price=999.99,
            category="Electronics",
            in_stock=True,
            rating=4.5,
        ),
        Product(name="Book", price=19.99, category="Books", in_stock=True, rating=4.2),
        Product(
            name="Coffee Mug",
            price=12.50,
            category="Kitchen",
            in_stock=False,
            rating=3.8,
        ),
        Product(
            name="Headphones",
            price=89.99,
            category="Electronics",
            in_stock=True,
            rating=4.7,
        ),
        Product(
            name="Notebook", price=5.99, category="Office", in_stock=True, rating=4.0
        ),
        Product(
            name="Smartphone",
            price=699.99,
            category="Electronics",
            in_stock=True,
            rating=4.6,
        ),
    ]

    for product in products:
        db.session.add(product)

    db.session.commit()
    print("Database seeded successfully!")
