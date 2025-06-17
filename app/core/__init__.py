from flask import Flask
from .config import Config
from .extensions import db, migrate
from app.features.home.routes import home_bp
from app.features.about.routes import about_bp
from app.features.products.routes import products_bp
from app.interfaces.controllers.cli import register_commands


def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(about_bp)
    app.register_blueprint(products_bp)

    # Register CLI commands
    register_commands(app)

    return app