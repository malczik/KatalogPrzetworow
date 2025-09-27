# -*- coding: utf-8 -*-
from .recipe import Recipe, Ingredient
from .unit_converter import UnitConverter

class Calculator:
    """Główna klasa kalkulatora przetworów z obsługą małych słoików"""
    
    def __init__(self):
        self.unit_converter = UnitConverter()
        self.recipe = Recipe()
    
    def calculate_required_jars(self, jar_capacity_ml):
        """Oblicza potrzebną liczbę słoików - uwzględnia małe słoiki od 30 ml"""
        if jar_capacity_ml < 30:
            jar_capacity_ml = 30  # Minimalna obsługiwana pojemność
        
        total_volume = self.recipe.calculate_total_volume(self.unit_converter)
        jars_needed = total_volume / jar_capacity_ml
        
        # Zaokrąglij w górę i dodaj zapasowy słoik
        jars_needed = int(jars_needed) + 1 if jars_needed % 1 > 0 else int(jars_needed)
        jars_needed += 1  # Zapasowy słoik
        
        return max(1, jars_needed)  # Co najmniej 1 słoik
    
    def scale_recipe(self, target_jar_capacity_ml, target_jar_count, profile="exact"):
        """
        Skaluje przepis na podstawie docelowych parametrów słoików
        """
        # Walidacja minimalnej pojemności
        if target_jar_capacity_ml < 30:
            target_jar_capacity_ml = 30
        
        original_total_volume = self.recipe.original_jar_capacity * self.recipe.original_jar_count
        
        if original_total_volume <= 0:
            raise ValueError("Oryginalna objętość przepisu wynosi 0. Nie można przeliczyć. Sprawdź parametry słoików.")
        
        target_total_volume = target_jar_capacity_ml * target_jar_count
        
        if profile == "exact":
            scale_factor = target_total_volume / original_total_volume
        elif profile == "dinner":
            dinner_portion_ml = 250
            original_portions = original_total_volume / dinner_portion_ml
            target_portions = target_total_volume / dinner_portion_ml
            scale_factor = target_portions / original_portions
        else:
            scale_factor = 1.0
        
        scaled_recipe = Recipe()
        scaled_recipe.original_jar_capacity = target_jar_capacity_ml
        scaled_recipe.original_jar_count = target_jar_count
        scaled_recipe.scale_factor = scale_factor
        
        for ingredient in self.recipe.ingredients:
            scaled_amount = ingredient.amount * scale_factor
            scaled_ingredient = Ingredient(
                ingredient.name, 
                scaled_amount, 
                ingredient.unit, 
                ingredient.form
            )
            scaled_recipe.ingredients.append(scaled_ingredient)
        
        return scaled_recipe