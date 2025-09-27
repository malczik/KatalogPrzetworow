# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
from core.calculator import Calculator
from .recipe_editor import RecipeEditorTab
from .calculator_tab import CalculatorTab

class MainWindow:
    """Główne okno aplikacji"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Kalkulator Przetworów v1.0")
        self.root.geometry("1100x800")
        
        # Inicjalizacja kalkulatora
        self.calculator = Calculator()
        
        # Tworzenie zakładek
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Zakładka edycji przepisu
        self.recipe_editor = RecipeEditorTab(self.notebook, self.calculator)
        self.notebook.add(self.recipe_editor.frame, text='Edycja przepisu')
        
        # Zakładka kalkulatora
        self.calculator_tab = CalculatorTab(self.notebook, self.calculator)
        self.notebook.add(self.calculator_tab.frame, text='Przeliczanie')