# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import os

class PdfExporter:
    """Klasa do eksportowania przepisów do PDF z polskimi znakami"""
    
    def __init__(self):
        # Rejestracja czcionki z polskimi znakami
        try:
            # Próba znalezienia czcionki Arial
            arial_path = self._find_arial_font()
            if arial_path:
                pdfmetrics.registerFont(TTFont('Arial', arial_path))
                self.font_name = 'Arial'
            else:
                # Czcionka Helvetica może nie mieć polskich znaków
                self.font_name = 'Helvetica'
        except:
            self.font_name = 'Helvetica'
    
    def _find_arial_font(self):
        """Znajduje czcionkę Arial w systemie"""
        possible_paths = [
            'C:/Windows/Fonts/arial.ttf',
            'C:/Windows/Fonts/ARIAL.TTF',
            '/usr/share/fonts/truetype/msttcorefonts/arial.ttf',
            '/Library/Fonts/Arial.ttf'
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        return None
    
    def export_recipe(self, recipe, file_path, calculation_info=None):
        """Eksportuje przepis do pliku PDF"""
        try:
            doc = SimpleDocTemplate(file_path, pagesize=A4)
            styles = getSampleStyleSheet()
            
            # Styl z polskimi znakami
            polish_style = ParagraphStyle(
                'PolishStyle',
                parent=styles['Normal'],
                fontName=self.font_name,
                fontSize=10,
                encoding='utf-8'
            )
            
            title_style = ParagraphStyle(
                'TitleStyle',
                parent=styles['Heading1'],
                fontName=self.font_name,
                fontSize=16,
                spaceAfter=12,
                encoding='utf-8'
            )
            
            heading_style = ParagraphStyle(
                'HeadingStyle',
                parent=styles['Heading2'],
                fontName=self.font_name,
                fontSize=12,
                spaceAfter=6,
                encoding='utf-8'
            )
            
            content = []
            
            # Tytuł
            content.append(Paragraph('Przepis na przetwory', title_style))
            content.append(Paragraph(f"Wygenerowano: {datetime.now().strftime('%Y-%m-%d %H:%M')}", polish_style))
            content.append(Spacer(1, 0.2*inch))
            
            # Informacje o przeliczeniu
            if calculation_info:
                content.append(Paragraph('Informacje o przeliczeniu', heading_style))
                info_lines = calculation_info.split('\n')
                for line in info_lines[:6]:  # Pierwsze 6 linii
                    if line.strip():
                        content.append(Paragraph(line.strip(), polish_style))
                content.append(Spacer(1, 0.2*inch))
            
            # Parametry przepisu
            content.append(Paragraph('Parametry przepisu', heading_style))
            content.append(Paragraph(f"Pojemność słoików: {recipe.original_jar_capacity} ml", polish_style))
            content.append(Paragraph(f"Liczba słoików: {recipe.original_jar_count}", polish_style))
            content.append(Paragraph(f"Całkowita objętość: {recipe.original_jar_capacity * recipe.original_jar_count} ml", polish_style))
            content.append(Spacer(1, 0.2*inch))
            
            # Składniki
            content.append(Paragraph('Składniki', heading_style))
            for ingredient in recipe.ingredients:
                if ingredient.form:
                    line = f"• {ingredient.name}: {ingredient.amount} {ingredient.unit} ({ingredient.form})"
                else:
                    line = f"• {ingredient.name}: {ingredient.amount} {ingredient.unit}"
                content.append(Paragraph(line, polish_style))
            
            # Stopka
            content.append(Spacer(1, 0.3*inch))
            content.append(Paragraph("Wygenerowano przez Kalkulator Przetworów", polish_style))
            
            doc.build(content)
            return True
            
        except Exception as e:
            raise Exception(f"Błąd eksportu PDF: {str(e)}")