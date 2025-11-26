from django import template
from datetime import date

register = template.Library()

@register.filter
def age(birth_date):
    """Возвращает возраст в годах."""
    if not birth_date:
        return ""
    today = date.today()
    years = today.year - birth_date.year - (
        (today.month, today.day) < (birth_date.month, birth_date.day)
    )
    return years
