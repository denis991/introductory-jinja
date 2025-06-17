from flask import Blueprint, render_template, request

from app.features.products.services import ProductService
from app.infra.db.repositories import SQLAlchemyProductRepository

# Create blueprint
products_bp = Blueprint("products", __name__)

# Initialize repository and service
product_repository = SQLAlchemyProductRepository()
product_service = ProductService(product_repository)


@products_bp.route("/products")
def products():
    """Products page route"""
    category = request.args.get("category")

    if category:
        products = product_service.get_products_by_category(category)
    else:
        products = product_service.get_all_products()

    categories = product_service.get_available_categories()

    return render_template(
        "products/products.html",
        products=products,
        categories=categories,
        selected_category=category,
    )


@products_bp.route("/products/<int:product_id>")
def product_detail(product_id):
    """Product detail page route"""
    product = product_service.get_product_by_id(product_id)

    if not product:
        return "Product not found", 404

    return render_template("products/product_detail.html", product=product)
