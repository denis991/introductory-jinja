from datetime import datetime
from app.core.extensions import db


class User(db.Model):
    """User SQLAlchemy model"""
    __tablename__ = 'users'

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
            join_date=self.join_date
        )


class Product(db.Model):
    """Product SQLAlchemy model"""
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    in_stock = db.Column(db.Boolean, default=True)
    rating = db.Column(db.Float, nullable=True)

    def to_domain(self):
        """Convert to domain entity"""
        from app.domain.entities import Product
        return Product(
            id=self.id,
            name=self.name,
            price=self.price,
            category=self.category,
            in_stock=self.in_stock,
            rating=self.rating
        )