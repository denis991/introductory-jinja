# Здесь определяются модели базы данных (ORM-классы для SQLAlchemy).
# Эти классы отражают структуру таблиц в базе данных и используются для
# работы с данными через ORM.
from datetime import datetime

from app.core.extensions import db


class User(db.Model):
    """User SQLAlchemy model"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    join_date = db.Column(db.DateTime, default=datetime.utcnow)

    def to_domain(self):
        """Convert to domain entity"""
        from app.domain.entities import User

        return User(
            id=self.id,
            name=self.name,
            email=self.email,
            is_admin=self.is_admin,
            join_date=self.join_date,
        )


# Таблица-связка для many-to-many
product_category = db.Table(
    "product_category",
    db.Column("product_id", db.Integer, db.ForeignKey("products.id")),
    db.Column("category_id", db.Integer, db.ForeignKey("categories.id")),
)


class Product(db.Model):
    """Product SQLAlchemy model"""

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    in_stock = db.Column(db.Boolean, default=True)
    rating = db.Column(db.Float, nullable=True)
    # обратная связь
    categories = db.relationship(
        "Category", secondary=product_category, back_populates="products"
    )

    def to_domain(self):
        """Convert to domain entity"""
        from app.domain.entities import Product

        return Product(
            id=self.id,
            name=self.name,
            price=self.price,
            category=self.category,
            in_stock=self.in_stock,
            rating=self.rating,
        )


class Category(db.Model):
    """Category SQLAlchemy model"""

    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    products = db.relationship(
        "Product", secondary=product_category, back_populates="categories"
    )

    def to_domain(self):
        """Convert to domain entity"""
        from app.domain.entities import Category

        return Category(
            id=self.id,
            name=self.name,
            description=self.description,
        )
