# -*- coding: utf-8 -*-
class Recipe:
    """Klasa reprezentująca przepis na przetwory"""
    
    def __init__(self):
        self.name = "Nowy przepis"
        self.original_jar_capacity = 500  # ml
        self.original_jar_count = 5
        self.ingredients = []
        self.brine_percentage = 30  # Procent zalewy w stosunku do składników stałych
        self.scale_factor = 1.0  # Współczynnik skalowania
    
    def calculate_total_volume(self, unit_converter):
        """Oblicza całkowitą objętość przepisu w ml"""
        total_volume = 0
        
        for ingredient in self.ingredients:
            # Przelicz składnik na ml
            volume = unit_converter.convert_to_ml(
                ingredient.amount, 
                ingredient.unit, 
                ingredient.form
            )
            total_volume += volume
        
        # Dodaj objętość zalewy
        brine_volume = total_volume * (self.brine_percentage / 100)
        total_volume += brine_volume
        
        return total_volume
    
    def calculate_jars_needed(self, jar_capacity_ml, unit_converter):
        """Oblicza potrzebną liczbę słoików o danej pojemności"""
        total_volume = self.calculate_total_volume(unit_converter)
        jars_needed = total_volume / jar_capacity_ml
        return max(1, round(jars_needed))  # Co najmniej 1 słoik


class Ingredient:
    """Klasa reprezentująca pojedynczy składnik"""
    
    def __init__(self, name="", amount=0, unit="g", form=None):
        self.name = name
        self.amount = amount
        self.unit = unit
        self.form = form  # None, 'całe', 'cząstki', 'tarte'
    
    def __str__(self):
        if self.form:
            return f"{self.name}: {self.amount} {self.unit} ({self.form})"
        return f"{self.name}: {self.amount} {self.unit}"