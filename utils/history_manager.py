# -*- coding: utf-8 -*-
import json
import os
from datetime import datetime

class HistoryManager:
    """Manager historii obliczeń"""
    
    def __init__(self, history_file="calculation_history.json"):
        self.history_file = history_file
        self.history = self.load_history()
    
    def load_history(self):
        """Ładuje historię z pliku"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_history(self):
        """Zapisuje historię do pliku"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Błąd zapisu historii: {e}")
    
    def add_calculation(self, recipe, parameters, result):
        """Dodaje obliczenie do historii"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'parameters': parameters,
            'recipe_name': recipe.name,
            'ingredients_count': len(recipe.ingredients),
            'result_preview': result[:100] + '...' if len(result) > 100 else result
        }
        
        self.history.append(entry)
        # Zachowaj tylko ostatnie 50 wpisów
        self.history = self.history[-50:]
        self.save_history()
    
    def get_recent_calculations(self, limit=10):
        """Pobiera ostatnie obliczenia"""
        return self.history[-limit:][::-1]  # Odwróć kolejność (najnowsze pierwsze)
    
    def clear_history(self):
        """Czyści całą historię"""
        self.history = []
        self.save_history()