# -*- coding: utf-8 -*-
import re

class Validators:
    """Klasa z metodami walidacji danych"""
    
    @staticmethod
    def validate_number(value, min_val=0, max_val=10000):
        """Waliduje czy wartość jest liczbą w zakresie"""
        try:
            num = float(str(value).replace(',', '.'))
            return min_val <= num <= max_val
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_required(text):
        """Waliduje czy tekst nie jest pusty"""
        return bool(str(text).strip())
    
    @staticmethod
    def validate_ingredient_name(name):
        """Waliduje nazwę składnika"""
        name = str(name).strip()
        if not name:
            return False
        # Sprawdź czy zawiera tylko dozwolone znaki
        return bool(re.match(r'^[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ\s\-]+$', name))
    
    @staticmethod
    def validate_unit(unit):
        """Waliduje jednostkę"""
        valid_units = ['g', 'kg', 'ml', 'l', 'łyżka', 'łyżeczka', 'szklanka', 'szt', 'ząbek', 'plaster', 'porcja']
        return unit in valid_units