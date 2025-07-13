# Этот файл содержит функции и данные для начального заполнения базы данных (seed).
# Используется для создания тестовых или стартовых данных при первом запуске приложения.
from datetime import datetime

from app.core.extensions import db
from app.infra.db.models import Product, User, Category


def seed_database():
    """Seed the database with initial data"""

    # Create users
    users = [
        User(
            name="Alice Johnson",
            email="alice@example.com",
            is_admin=True,
            join_date=datetime(2024, 1, 15),
        ),
        User(
            name="Bob Smith",
            email="bob@example.com",
            is_admin=False,
            join_date=datetime(2024, 2, 1),
        ),
        User(
            name="Carol Davis",
            email="carol@example.com",
            is_admin=False,
            join_date=datetime(2024, 3, 10),
        ),
    ]

    for user in users:
        db.session.add(user)

    # Create categories
    categories = [
        Category(
            name="Electronics",
            description="Electronic devices and gadgets"
        ),
        Category(
            name="Books",
            description="Books and literature"
        ),
        Category(
            name="Kitchen",
            description="Kitchen appliances and utensils"
        ),
        Category(
            name="Office",
            description="Office supplies and equipment"
        ),
        Category(
            name="Sports",
            description="Sports equipment and accessories"
        ),
        Category(
            name="Fashion",
            description="Clothing and fashion items"
        ),
    ]

    for category in categories:
        db.session.add(category)

    # Commit to get IDs
    db.session.commit()

    # Create products with category relationships
    products = [
        Product(
            name="Laptop",
            price=999.99,
            category="Electronics",
            in_stock=True,
            rating=4.5,
        ),
        Product(
            name="Book",
            price=19.99,
            category="Books",
            in_stock=True,
            rating=4.2
        ),
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
            name="Notebook",
            price=5.99,
            category="Office",
            in_stock=True,
            rating=4.0
        ),
        Product(
            name="Smartphone",
            price=699.99,
            category="Electronics",
            in_stock=True,
            rating=4.6,
        ),
        Product(
            name="Running Shoes",
            price=129.99,
            category="Sports",
            in_stock=True,
            rating=4.3,
        ),
        Product(
            name="T-Shirt",
            price=24.99,
            category="Fashion",
            in_stock=True,
            rating=4.1,
        ),
    ]

    for product in products:
        db.session.add(product)

    # Commit to get product IDs
    db.session.commit()

    # Set up many-to-many relationships
    # Get categories by name
    electronics = Category.query.filter_by(name="Electronics").first()
    books = Category.query.filter_by(name="Books").first()
    kitchen = Category.query.filter_by(name="Kitchen").first()
    office = Category.query.filter_by(name="Office").first()
    sports = Category.query.filter_by(name="Sports").first()
    fashion = Category.query.filter_by(name="Fashion").first()

    # Get products by name
    laptop = Product.query.filter_by(name="Laptop").first()
    book = Product.query.filter_by(name="Book").first()
    coffee_mug = Product.query.filter_by(name="Coffee Mug").first()
    headphones = Product.query.filter_by(name="Headphones").first()
    notebook = Product.query.filter_by(name="Notebook").first()
    smartphone = Product.query.filter_by(name="Smartphone").first()
    running_shoes = Product.query.filter_by(name="Running Shoes").first()
    t_shirt = Product.query.filter_by(name="T-Shirt").first()

    # Add categories to products
    if laptop and electronics:
        laptop.categories.append(electronics)

    if book and books:
        book.categories.append(books)

    if coffee_mug and kitchen:
        coffee_mug.categories.append(kitchen)

    if headphones and electronics:
        headphones.categories.append(electronics)

    if notebook and office:
        notebook.categories.append(office)

    if smartphone and electronics:
        smartphone.categories.append(electronics)

    if running_shoes and sports:
        running_shoes.categories.append(sports)

    if t_shirt and fashion:
        t_shirt.categories.append(fashion)

    # Final commit
    db.session.commit()
    print("Database seeded successfully!")
    print(f"Created {len(users)} users")
    print(f"Created {len(categories)} categories")
    print(f"Created {len(products)} products")
    print("Set up many-to-many relationships between products and categories")
