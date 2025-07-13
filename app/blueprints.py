# Централизованная регистрация всех blueprints приложения
# Здесь импортируем и регистрируем все blueprints в одном месте

def register_blueprints(app):
    """Регистрирует все blueprints приложения"""
    from app.features.home.routes import home_bp
    from app.features.about.routes import about_bp
    from app.features.products.routes import products_bp
    from app.features.categories.routes import bp as categories_bp
    from app.features.docs.routes import docs_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(about_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(docs_bp)