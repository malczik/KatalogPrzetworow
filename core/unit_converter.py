# -*- coding: utf-8 -*-
class UnitConverter:
    """Klasa do konwersji między różnymi jednostkami kuchennymi"""
    
    def __init__(self):
        # Słownik konwersji do gramów (dla masy) i ml (dla objętości)
        self.conversions = {
            # Jednostki masy -> gramy
            'g': {'type': 'mass', 'factor': 1},
            'kg': {'type': 'mass', 'factor': 1000},
            'szczypta': {'type': 'mass', 'factor': 0.3},
            
            # Jednostki objętości -> ml
            'ml': {'type': 'volume', 'factor': 1},
            'l': {'type': 'volume', 'factor': 1000},
            'łyżka': {'type': 'volume', 'factor': 15},
            'łyżeczka': {'type': 'volume', 'factor': 5},
            'szklanka': {'type': 'volume', 'factor': 250},
            
            # Jednostki sztukowe - wymagają specjalnej konwersji
            'szt': {'type': 'piece', 'factor': 1},
            'ząbek': {'type': 'piece', 'factor': 1},
            'plaster': {'type': 'piece', 'factor': 1},
            'porcja': {'type': 'piece', 'factor': 1},
        }
        
        # Średnie wagi/objętości dla popularnych produktów (w gramach/ml na sztukę)
        self.piece_weights = {
            'bakłażan': 250,  # gramów
            'papryka': 150,
            'cukinia': 200,
            'ogórek': 100,
            'pomidor': 120,
            'cebula': 100,
            'ząbek czosnku': 5,
            'jabłko': 150,
            'gruszka': 150,
            'śliwka': 30,
            'śliwka węgierka': 25,
        }
        
        # Współczynniki form przygotowania
        self.form_factors = {
            'całe': 1.0,
            'cząstki': 0.8,    # Mniej miejsca między kawałkami
            'tarte': 0.7,      # Bardziej ubite
            'kostka': 0.85,    # Kostkowanie podobne do cząstek
        }
    
    def convert_to_ml(self, amount, unit, form=None):
        """Konwertuje dowolną jednostkę na mililitry"""
        if unit not in self.conversions:
            # Domyślnie traktuj jako gramy (1g ≈ 1ml dla wody/rzadkich przetworów)
            return amount
        
        conversion = self.conversions[unit]
        
        if conversion['type'] == 'mass':
            # Masa -> zakładamy 1g = 1ml dla uproszczenia
            return amount * conversion['factor']
        
        elif conversion['type'] == 'volume':
            # Objętość -> przelicz na ml
            return amount * conversion['factor']
        
        elif conversion['type'] == 'piece':
            # Sztuki -> przelicz na gramy/ml na podstawie typu produktu
            weight_per_piece = self._get_weight_per_piece(unit, amount, form)
            return weight_per_piece * amount
        
        return amount
    
    def _get_weight_per_piece(self, unit, amount, form):
        """Pobiera przybliżoną wagę/objętość dla produktów sztukowych"""
        # Domyślna wartość dla nieznanych produktów
        default_weights = {
            'szt': 100,    # 100g na sztukę domyślnie
            'ząbek': 5,    # 5g na ząbek czosnku
            'plaster': 20, # 20g na plaster
            'porcja': 150, # 150g na porcję
        }
        
        weight = default_weights.get(unit, 100)
        
        # Dostosuj wagę na podstawie formy
        if form and form in self.form_factors:
            weight *= self.form_factors[form]
        
        return weight
    
    def get_available_units(self):
        """Zwraca listę dostępnych jednostek"""
        return list(self.conversions.keys())
    
    def get_available_forms(self):
        """Zwraca listę dostępnych form przygotowania"""
        return list(self.form_factors.keys())