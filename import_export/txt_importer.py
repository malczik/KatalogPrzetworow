# -*- coding: utf-8 -*-
import re
import os
from core.recipe import Recipe, Ingredient
from core.unit_converter import UnitConverter

class TxtImporter:
    """Klasa do importowania przepisów z plików TXT"""
    
    def __init__(self):
        self.unit_converter = UnitConverter()
    
    def import_recipe(self, file_path):
        """
        Importuje przepis z pliku TXT.
        Jeśli nie podano liczby słoików, oblicza ją automatycznie.
        """
        recipe = Recipe()
        
        try:
            # SPRAWDZENIE CZY PLIK ISTNIEJE
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Plik {file_path} nie istnieje!")
            
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Podziel na linie i wyczyść
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            
            # Szukaj nazwy przepisu (pierwsza linia)
            if lines and not any(char.isdigit() for char in lines[0]):
                recipe.name = lines[0]
                lines = lines[1:]
            
            # Parsuj składniki
            recipe.ingredients = self._parse_ingredients(lines)
            
            # Oblicz całkowitą objętość i zaproponuj słoiki
            total_volume = recipe.calculate_total_volume(self.unit_converter)
            recipe.original_jar_count = self._suggest_jar_count(total_volume)
            recipe.original_jar_capacity = 500  # Domyślna pojemność
            
            return recipe
            
        except Exception as e:
            raise Exception(f"Błąd importu pliku TXT: {str(e)}")
    
    def _parse_ingredients(self, lines):
        """Parsuje linie tekstu na listę składników"""
        ingredients = []
        unit_pattern = r'\b(' + '|'.join(re.escape(unit) for unit in self.unit_converter.get_available_units()) + r')\b'
        
        for line in lines:
            # Pomijaj linie które wyglądają jak nagłówki
            if any(keyword in line.lower() for keyword in ['składniki', 'skladniki', 'ingredients', 'porcja', 'słoiki']):
                continue
            
            # Spróbuj znaleźć ilość i jednostkę
            match = re.search(r'(\d+[.,]?\d*)\s*(' + unit_pattern + r')', line)
            if match:
                amount_str = match.group(1).replace(',', '.')
                unit = match.group(2)
                
                try:
                    amount = float(amount_str)
                    # Nazwa to wszystko przed liczbą
                    name = line[:match.start()].strip()
                    
                    # Określ formę na podstawie nazwy
                    form = self._detect_form(name, line)
                    
                    ingredient = Ingredient(name, amount, unit, form)
                    ingredients.append(ingredient)
                    
                except ValueError:
                    continue
        
        return ingredients
    
    def _detect_form(self, name, full_line):
        """Automatycznie wykrywa formę składnika na podstawie nazwy i kontekstu"""
        name_lower = name.lower()
        line_lower = full_line.lower()
        
        if any(word in line_lower for word in ['tarty', 'starte', 'utarte', 'tarte']):
            return 'tarte'
        elif any(word in line_lower for word in ['pokrojony', 'pokrojone', 'kawałki', 'cząstki', 'kostka']):
            return 'cząstki'
        elif any(word in name_lower for word in ['ząbek', 'ząbki', 'plaster', 'plastry']):
            return 'całe'
        
        return 'całe'  # Domyślnie
    
    def _suggest_jar_count(self, total_volume_ml):
        """Sugeruje liczbę słoików na podstawie całkowitej objętości"""
        # Standardowe pojemności słoików
        standard_jars = [125, 250, 500, 750, 1000]
        
        # Znajdź optymalną pojemność (najbliższą 500ml)
        best_jar = min(standard_jars, key=lambda x: abs(x - 500))
        
        # Oblicz liczbę słoików
        jar_count = total_volume_ml / best_jar
        
        # Zaokrąglij w górę i dodaj jeden zapasowy
        return max(1, int(jar_count) + 1)