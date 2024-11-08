from django import template

register = template.Library()

@register.filter
def price_exclude_vat(price, vat_rate):
    """
    Вычитает НДС из цены.
    vat_rate - ставка НДС в процентах (например, 20 для 20%)
    """
    try:
        vat_factor = 1 + (vat_rate / 100)
        return round(price / vat_factor, 2)
    except (TypeError, ValueError, ZeroDivisionError):
        return None