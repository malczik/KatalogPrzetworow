# -*- coding: utf-8 -*-
def validate_number(input_str):
    """Waliduje czy ciąg znaków jest liczbą"""
    try:
        float(input_str.replace(',', '.'))
        return True
    except ValueError:
        return False

def format_quantity(amount):
    """Formatuje ilość do ładnego wyświetlenia"""
    if amount.is_integer():
        return str(int(amount))
    else:
        return f"{amount:.2f}"

def safe_float_convert(value, default=0.0):
    """Bezpiecznie konwertuje string na float"""
    try:
        return float(str(value).replace(',', '.'))
    except (ValueError, TypeError):
        return default