# Здесь определяются кастомные CLI-команды для управления приложением через терминал.
# Например, команды для инициализации базы данных, создания тестовых данных и т.д.
import click
from flask.cli import with_appcontext

from app.core.extensions import db
from app.infra.db.seed_data import seed_database


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Initialize the database."""
    db.create_all()
    click.echo("Initialized the database.")


@click.command("seed-db")
@with_appcontext
def seed_db_command():
    """Seed the database with initial data."""
    seed_database()
    click.echo("Database seeded successfully.")


@click.command("drop-db")
@with_appcontext
def drop_db_command():
    """Drop all database tables."""
    if click.confirm("Are you sure you want to drop all tables?"):
        db.drop_all()
        click.echo("Dropped all database tables.")


def register_commands(app):
    """Register CLI commands with the Flask app."""
    app.cli.add_command(init_db_command)
    app.cli.add_command(seed_db_command)
    app.cli.add_command(drop_db_command)
