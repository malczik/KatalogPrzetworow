# -*- coding: utf-8 -*-
import PyPDF2
import re
from core.recipe import Recipe, Ingredient

class PdfImporter:
    """Klasa do importowania przepisów z plików PDF"""
    
    def import_recipe(self, file_path):
        """Importuje przepis z pliku PDF"""
        try:
            text = self._extract_text_from_pdf(file_path)
            lines = text.split('\n')
            
            return self._parse_text(lines)
            
        except Exception as e:
            raise Exception(f"Błąd importu PDF: {str(e)}")
    
    def _extract_text_from_pdf(self, file_path):
        """Wyodrębnia tekst z PDF"""
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    
    def _parse_text(self, lines):
        """Parsuje tekst na przepis (podobnie jak w DOCX)"""
        from .docx_importer import DocxImporter
        docx_importer = DocxImporter()
        return docx_importer._parse_text(lines)