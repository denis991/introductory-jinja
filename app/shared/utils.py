# Здесь размещаются вспомогательные функции (утилиты), которые могут использоваться в разных частях приложения.
# Например, функции для форматирования данных, валидации и т.д.
from datetime import datetime
from typing import Any, Dict, List


def format_price(price: float) -> str:
    """Format price with 2 decimal places"""
    return f"${price:.2f}"


def format_date(date: datetime) -> str:
    """Format date in a readable format"""
    return date.strftime("%Y-%m-%d")


def get_unique_categories(products: List[Dict[str, Any]]) -> List[str]:
    """Get unique categories from products"""
    return list(set(product.get("category", "") for product in products))


def calculate_average_rating(ratings: List[float]) -> float:
    """Calculate average rating from list of ratings"""
    if not ratings:
        return 0.0
    return sum(ratings) / len(ratings)
