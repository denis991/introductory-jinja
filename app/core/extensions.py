# Здесь инициализируются расширения Flask, такие как SQLAlchemy и Alembic (Flask-Migrate).
# Эти объекты создаются один раз и затем инициализируются в create_app.
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
