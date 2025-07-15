"""
Сервисы для работы с пользователями
Используют реальные репозитории и модели
"""

from app.core.extensions import db
from app.infra.db.models import User as UserModel


def get_all_users():
    """Получить всех пользователей"""

    users = UserModel.query.all()
    return [user.to_domain() for user in users]


def get_user_by_id(user_id):
    """Получить пользователя по ID"""

    user = UserModel.query.get(user_id)
    return user.to_domain() if user else None


def create_user(username, email, first_name=None, last_name=None):
    """Создать нового пользователя"""

    # Используем username как name, так как в модели User нет поля username
    user = UserModel(name=username, email=email, is_admin=False)

    db.session.add(user)
    db.session.commit()

    return user.to_domain()


def update_user(
    user_id, username=None, email=None, first_name=None, last_name=None, is_active=None
):
    """Обновить пользователя"""
    user = UserModel.query.get(user_id)
    if not user:
        return None

    if username is not None:
        user.name = username
    if email is not None:
        user.email = email
    if is_active is not None:
        user.is_admin = is_active  # Используем is_admin как is_active

    db.session.commit()
    return user.to_domain()


def delete_user(user_id):
    """Удалить пользователя"""
    user = UserModel.query.get(user_id)
    if not user:
        return False

    db.session.delete(user)
    db.session.commit()
    return True
