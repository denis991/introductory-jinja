import os

from flask import Flask

from app.features.about.routes import about_bp
from app.features.home.routes import home_bp
from app.features.products.routes import products_bp
from app.interfaces.controllers.cli import register_commands

from .config import Config
from .extensions import db, migrate

from dotenv import load_dotenv
load_dotenv()


def create_app(config_class=Config):
    """Application factory pattern"""
    # Get the absolute path to the templates directory
    template_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "templates")
    )
    static_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "static")
    )

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
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
