# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from datetime import datetime
from import_export.docx_exporter import DocxExporter
from import_export.pdf_exporter import PdfExporter
from utils.history_manager import HistoryManager
from utils.validators import Validators

class CalculatorTab:
    """Zakładka kalkulatora do przeliczania przepisów"""
    
    def __init__(self, parent, calculator):
        self.calculator = calculator
        self.frame = ttk.Frame(parent)
        self.history_manager = HistoryManager()
        self.last_calculation = None
        
        self.create_widgets()
    
    def create_widgets(self):
        """Tworzy interfejs użytkownika"""
        # Zmienna do przechowywania wybranego profilu
        self.profile_var = tk.StringVar(value="exact")
        
        # Ramka na wybór profilu
        profile_frame = ttk.LabelFrame(self.frame, text="Profil obliczeń")
        profile_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Radiobutton(profile_frame, text="Dokładna ilość", 
                       variable=self.profile_var, value="exact").pack(side='left', padx=5, pady=5)
        ttk.Radiobutton(profile_frame, text="Porcja obiadowa", 
                       variable=self.profile_var, value="dinner").pack(side='left', padx=5, pady=5)
        
        # Ramka na wybór liczby osób (tylko dla porcji obiadowej)
        self.people_frame = ttk.LabelFrame(profile_frame, text="Porcja obiadowa dla:")
        self.people_frame.pack(side='left', padx=10, pady=5)
        
        self.people_var = tk.StringVar(value="2")
        ttk.Radiobutton(self.people_frame, text="2 osoby", 
                       variable=self.people_var, value="2").pack(side='left', padx=5)
        ttk.Radiobutton(self.people_frame, text="4 osoby", 
                       variable=self.people_var, value="4").pack(side='left', padx=5)
        
        # Śledź zmianę profilu
        self.profile_var.trace('w', self.on_profile_change)
        
        # Ramka na docelowe słoiki
        target_frame = ttk.LabelFrame(self.frame, text="Docelowe słoiki")
        target_frame.pack(fill='x', padx=10, pady=10)
        
        # Pojemność docelowych słoików
        ttk.Label(target_frame, text="Pojemność słoików (ml):").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.target_capacity_var = tk.StringVar(value="250")
        self.entry_target_cap = ttk.Entry(target_frame, textvariable=self.target_capacity_var, width=10)
        self.entry_target_cap.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        # Liczba docelowych słoików
        ttk.Label(target_frame, text="Liczba słoików:").grid(row=0, column=2, padx=5, pady=5, sticky='e')
        self.target_count_var = tk.StringVar(value="10")
        self.entry_target_count = ttk.Entry(target_frame, textvariable=self.target_count_var, width=10)
        self.entry_target_count.grid(row=0, column=3, padx=5, pady=5, sticky='w')
        
        # Przycisk auto-doboru słoików
        btn_auto = ttk.Button(target_frame, text="Auto-dobór słoików", command=self.auto_select_jars)
        btn_auto.grid(row=0, column=4, padx=5, pady=5)
        
        # Ramka przycisków
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill='x', padx=10, pady=10)
        
        # Przyciski obliczeń
        calc_frame = ttk.Frame(button_frame)
        calc_frame.pack(side='left')
        
        btn_calculate = ttk.Button(calc_frame, text="Przelicz", command=self.calculate)
        btn_calculate.pack(side='left', padx=5)
        
        btn_history = ttk.Button(calc_frame, text="Historia", command=self.show_history)
        btn_history.pack(side='left', padx=5)
        
        # Przyciski eksportu
        export_frame = ttk.LabelFrame(button_frame, text="Eksport wyniku")
        export_frame.pack(side='left', padx=20)
        
        btn_export_txt = ttk.Button(export_frame, text="Eksportuj TXT", command=self.export_txt)
        btn_export_txt.pack(side='left', padx=2)
        
        btn_export_docx = ttk.Button(export_frame, text="Eksportuj DOCX", command=self.export_docx)
        btn_export_docx.pack(side='left', padx=2)
        
        btn_export_pdf = ttk.Button(export_frame, text="Eksportuj PDF", command=self.export_pdf)
        btn_export_pdf.pack(side='left', padx=2)
        
        # Pole na wyświetlenie wyniku
        self.result_text = scrolledtext.ScrolledText(self.frame, width=100, height=30)
        self.result_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Inicjalne ustawienie widoczności
        self.on_profile_change()
    
    def on_profile_change(self, *args):
        """Obsługuje zmianę profilu obliczeń"""
        if self.profile_var.get() == "dinner":
            self.people_frame.pack(side='left', padx=10, pady=5)
        else:
            self.people_frame.pack_forget()
    
    def auto_select_jars(self):
        """Automatycznie dobiera słoiki na podstawie całkowitej objętości"""
        try:
            total_volume = self.calculator.recipe.calculate_total_volume(self.calculator.unit_converter)
            
            if total_volume == 0:
                messagebox.showwarning("Ostrzeżenie", "Brak danych przepisu. Najpierw załaduj lub wprowadź przepis.")
                return
            
            # Standardowe pojemności słoików
            standard_jars = [125, 250, 500, 750, 1000]
            
            # Znajdź optymalną pojemność (najbliższą 250ml dla porcji lub 500ml dla dokładnej)
            target_size = 250 if self.profile_var.get() == "dinner" else 500
            best_jar = min(standard_jars, key=lambda x: abs(x - target_size))
            
            # Oblicz liczbę słoików (z zapasem 10%)
            jar_count = total_volume / best_jar * 1.1
            jar_count = max(1, int(jar_count) + 1)  # Zaokrąglij w górę + zapasowy
            
            self.target_capacity_var.set(str(best_jar))
            self.target_count_var.set(str(jar_count))
            
            messagebox.showinfo("Auto-dobór", 
                              f"Dobrano słoiki {best_jar} ml, liczba: {jar_count}\n"
                              f"Całkowita objętość: {total_volume:.0f} ml")
            
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się dobrać słoików: {str(e)}")
    
    def calculate(self):
        """Przelicza przepis na podstawie podanych parametrów"""
        try:
            # Walidacja danych wejściowych
            capacity_str = self.target_capacity_var.get().replace(',', '.')
            count_str = self.target_count_var.get().replace(',', '.')
            
            if not Validators.validate_number(capacity_str, 1, 10000):
                messagebox.showerror("Błąd", "Pojemność słoika musi być liczbą od 1 do 10000 ml.")
                return
            if not Validators.validate_number(count_str, 1, 1000):
                messagebox.showerror("Błąd", "Liczba słoików musi być liczbą od 1 do 1000.")
                return
            
            target_capacity = float(capacity_str)
            target_count = float(count_str)
            profile = self.profile_var.get()
            
            # Inicjalizacja people_count
            people_count = None
            if profile == "dinner":
                people_count = int(self.people_var.get())
                # Dla porcji obiadowej ustawiamy docelową pojemność na podstawie liczby osób
                dinner_jar_size = people_count * 125  # 125ml na osobę
                target_capacity = dinner_jar_size
            
            # Sprawdź czy przepis nie jest pusty
            if not self.calculator.recipe.ingredients:
                messagebox.showwarning("Ostrzeżenie", "Przepis jest pusty. Najpierw dodaj składniki.")
                return
            
            # Przelicz przepis
            scaled_recipe = self.calculator.scale_recipe(target_capacity, target_count, profile)
            self.last_calculation = scaled_recipe
            
            # Wyświetl wynik
            result = self.format_result(scaled_recipe, target_capacity, target_count, profile)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result)
            
            # Zapisz w historii
            calculation_params = {
                'profile': profile,
                'target_capacity': target_capacity,
                'target_count': target_count,
                'people_count': people_count
            }
            self.history_manager.add_calculation(scaled_recipe, calculation_params, result)
            
        except ValueError as e:
            messagebox.showerror("Błąd", "Pojemność i liczba słoików muszą być liczbami.")
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd podczas przeliczania: {str(e)}")
    
    def format_result(self, recipe, capacity, count, profile):
        """Formatuje wynik przeliczenia do czytelnej formy"""
        result = "=" * 70 + "\n"
        result += "PRZEPIS PO PRZELICZENIU\n"
        result += "=" * 70 + "\n\n"
        
        result += f"Profil: {'Dokładna ilość' if profile == 'exact' else 'Porcja obiadowa'}\n"
        result += f"Użyto słoików: {capacity} ml, liczba: {count}\n"
        result += f"Całkowita objętość: {capacity * count:.0f} ml\n"
        
        if profile == "dinner":
            people = self.people_var.get()
            result += f"Porcja obiadowa dla: {people} osób\n"
            result += f"Docelowa pojemność na słoik: {capacity} ml\n"
        
        result += f"Współczynnik przeliczenia: {recipe.scale_factor:.3f}\n"
        
        result += "-" * 70 + "\n"
        result += "SKŁADNIKI:\n"
        result += "-" * 70 + "\n"

        for ingredient in recipe.ingredients:
            # Formatowanie ilości
            if ingredient.amount.is_integer():
                amount_str = str(int(ingredient.amount))
            else:
                amount_str = f"{ingredient.amount:.2f}"
            
            # Dodanie formy jeśli istnieje
            unit_str = ingredient.unit
            if ingredient.form:
                unit_str += f" ({ingredient.form})"
            
            result += f"• {ingredient.name}: {amount_str} {unit_str}\n"

        result += "\n" + "=" * 70

        return result
    
    def export_txt(self):
        """Eksportuje wynik do pliku TXT"""
        result = self.result_text.get(1.0, tk.END)
        if not result.strip():
            messagebox.showwarning("Ostrzeżenie", "Brak wyników do eksportu.")
            return

        # Proponowana nazwa pliku z timestampem
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_name = f"przepis_przeliczony_{timestamp}.txt"

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Plik tekstowy", "*.txt")],
            initialfile=default_name
        )

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(result)
                messagebox.showinfo("Sukces", f"Wynik został zapisany do pliku:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się zapisać pliku: {str(e)}")

    def export_docx(self):
        """Eksportuje wynik do pliku DOCX"""
        if not self.last_calculation:
            messagebox.showwarning("Ostrzeżenie", "Brak danych do eksportu. Najpierw wykonaj przeliczenie.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".docx",
            filetypes=[("Pliki Word", "*.docx")],
            initialfile=f"przepis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
        )

        if file_path:
            try:
                result_text = self.result_text.get(1.0, tk.END)
                exporter = DocxExporter()
                exporter.export_recipe(self.last_calculation, file_path, result_text)
                messagebox.showinfo("Sukces", f"Przepis został wyeksportowany do DOCX!")
            except Exception as e:
                messagebox.showerror("Błąd", f"Błąd eksportu DOCX: {str(e)}")

    def export_pdf(self):
        """Eksportuje wynik do pliku PDF"""
        if not self.last_calculation:
            messagebox.showwarning("Ostrzeżenie", "Brak danych do eksportu. Najpierw wykonaj przeliczenie.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Pliki PDF", "*.pdf")],
            initialfile=f"przepis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )

        if file_path:
            try:
                result_text = self.result_text.get(1.0, tk.END)
                exporter = PdfExporter()
                exporter.export_recipe(self.last_calculation, file_path, result_text)
                messagebox.showinfo("Sukces", f"Przepis został wyeksportowany do PDF!")
            except Exception as e:
                messagebox.showerror("Błąd", f"Błąd eksportu PDF: {str(e)}")

    def show_history(self):
        """Pokazuje okno z historią obliczeń"""
        history_window = tk.Toplevel(self.frame)
        history_window.title("Historia obliczeń")
        history_window.geometry("800x500")
        
        # Nagłówek
        ttk.Label(history_window, text="Ostatnie obliczenia", font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Tworzymy listę z historią
        history_frame = ttk.Frame(history_window)
        history_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Kolumny
        columns = ('date', 'recipe', 'jars', 'profile')
        tree = ttk.Treeview(history_frame, columns=columns, show='headings', height=15)
        
        # Nagłówki kolumn
        tree.heading('date', text='Data')
        tree.heading('recipe', text='Przepis')
        tree.heading('jars', text='Słoiki')
        tree.heading('profile', text='Profil')
        
        tree.column('date', width=150)
        tree.column('recipe', width=300)
        tree.column('jars', width=150)
        tree.column('profile', width=100)
        
        # Pasek przewijania
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Wczytaj historię
        recent_calculations = self.history_manager.get_recent_calculations(20)
        for calc in recent_calculations:
            date = datetime.fromisoformat(calc['timestamp']).strftime("%Y-%m-%d %H:%M")
            recipe_name = calc.get('recipe_name', 'Przepis')
            jars_info = f"{calc['parameters']['target_capacity']}ml x {calc['parameters']['target_count']}"
            profile = 'Obiadowy' if calc['parameters']['profile'] == 'dinner' else 'Dokładny'
            
            tree.insert('', tk.END, values=(date, recipe_name, jars_info, profile))
        
        # Przyciski
        button_frame = ttk.Frame(history_window)
        button_frame.pack(pady=10)
        
        def view_selected():
            selection = tree.selection()
            if selection:
                index = tree.index(selection[0])
                selected_calc = recent_calculations[index]
                # Pokaż szczegóły w nowym oknie
                self.show_calculation_details(selected_calc)
        
        def clear_history():
            if messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz wyczyścić historię?"):
                self.history_manager.clear_history()
                history_window.destroy()
                messagebox.showinfo("Sukces", "Historia została wyczyszczona!")
        
        btn_view = ttk.Button(button_frame, text="Podgląd szczegółów", command=view_selected)
        btn_view.pack(side='left', padx=5)
        
        btn_clear = ttk.Button(button_frame, text="Wyczyść historię", command=clear_history)
        btn_clear.pack(side='left', padx=5)
        
        btn_close = ttk.Button(button_frame, text="Zamknij", command=history_window.destroy)
        btn_close.pack(side='left', padx=5)
    
    def show_calculation_details(self, calculation):
        """Pokazuje szczegóły wybranego obliczenia"""
        details_window = tk.Toplevel(self.frame)
        details_window.title("Szczegóły obliczenia")
        details_window.geometry("600x400")
        
        # Data
        date = datetime.fromisoformat(calculation['timestamp']).strftime("%Y-%m-%d %H:%M:%S")
        ttk.Label(details_window, text=f"Data: {date}", font=('Arial', 10, 'bold')).pack(pady=5)
        
        # Parametry
        params = calculation['parameters']
        ttk.Label(details_window, text=f"Profil: {'Porcja obiadowa' if params['profile'] == 'dinner' else 'Dokładna ilość'}").pack(pady=2)
        ttk.Label(details_window, text=f"Słoiki: {params['target_capacity']}ml x {params['target_count']}szt").pack(pady=2)
        
        if params['profile'] == 'dinner':
            ttk.Label(details_window, text=f"Dla: {params.get('people_count', '?')} osób").pack(pady=2)
        
        # Składniki (jeśli zapisane)
        if 'ingredients' in calculation:
            ttk.Label(details_window, text="Składniki:", font=('Arial', 10, 'bold')).pack(pady=5)
            ingredients_text = scrolledtext.ScrolledText(details_window, width=70, height=15)
            ingredients_text.pack(padx=10, pady=5, fill='both', expand=True)
            
            for ingredient in calculation['ingredients']:
                ingredients_text.insert(tk.END, f"• {ingredient}\n")
            
            ingredients_text.config(state=tk.DISABLED)
        
        ttk.Button(details_window, text="Zamknij", command=details_window.destroy).pack(pady=10)