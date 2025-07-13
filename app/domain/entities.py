# Здесь определяются бизнес-сущности (например, Product, User и т.д.)
# Эти классы описывают основные объекты предметной области, не зависящие от инфраструктуры и фреймворков.
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class User:
    """User domain entity"""

    id: Optional[int]
    name: str
    email: str
    is_admin: bool
    join_date: datetime


@dataclass
class Product:
    """Product domain entity"""

    id: Optional[int]
    name: str
    price: float
    category: str
    in_stock: bool
    rating: Optional[float] = None


@dataclass
class TeamMember:
    """Team member domain entity"""

    name: str
    role: str
    skills: List[str]


@dataclass
class ProjectStats:
    """Project statistics domain entity"""

    start_date: str
    version: str
    features: List[str]
