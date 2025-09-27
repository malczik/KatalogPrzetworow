# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from import_export.txt_importer import TxtImporter
from import_export.docx_importer import DocxImporter
from import_export.pdf_importer import PdfImporter
from core.recipe import Ingredient
from utils.validators import Validators

class RecipeEditorTab:
    """Zakładka do edycji przepisu z funkcją obliczania słoików"""
    
    def __init__(self, parent, calculator):
        self.calculator = calculator
        self.frame = ttk.Frame(parent)
        self.txt_importer = TxtImporter()
        self.docx_importer = DocxImporter()
        self.pdf_importer = PdfImporter()
        
        self.ingredient_rows = []
        
        self.create_widgets()
        self.load_recipe_data()
    
    def create_widgets(self):
        """Tworzy interfejs użytkownika z funkcją obliczania słoików"""
        main_container = ttk.Frame(self.frame)
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.create_button_section(main_container)
        self.create_parameters_section(main_container)
        self.create_ingredients_section(main_container)
    
    def create_button_section(self, parent):
        """Tworzy sekcję przycisków"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill='x', pady=(0, 10))
        
        import_frame = ttk.LabelFrame(button_frame, text="Import przepisu")
        import_frame.pack(side='left', padx=(0, 10))
        
        btn_import_txt = ttk.Button(import_frame, text="Importuj z TXT", command=self.import_txt)
        btn_import_txt.pack(side='left', padx=2)
        
        btn_import_docx = ttk.Button(import_frame, text="Importuj z DOCX", command=self.import_docx)
        btn_import_docx.pack(side='left', padx=2)
        
        btn_import_pdf = ttk.Button(import_frame, text="Importuj z PDF", command=self.import_pdf)
        btn_import_pdf.pack(side='left', padx=2)
        
        help_frame = ttk.LabelFrame(button_frame, text="Pomoc")
        help_frame.pack(side='left', padx=(0, 10))
        
        btn_help = ttk.Button(help_frame, text="Otwórz pomoc", command=self.show_help)
        btn_help.pack(side='left', padx=2)
        
        btn_template = ttk.Button(help_frame, text="Szablon TXT", command=self.show_template)
        btn_template.pack(side='left', padx=2)
        
        manage_frame = ttk.LabelFrame(button_frame, text="Zarządzanie przepisem")
        manage_frame.pack(side='left')
        
        btn_add_ingredient = ttk.Button(manage_frame, text="Dodaj składnik", command=self.add_ingredient_row)
        btn_add_ingredient.pack(side='left', padx=2)
        
        btn_save = ttk.Button(manage_frame, text="Zapisz przepis", command=self.save_recipe)
        btn_save.pack(side='left', padx=2)
        
        btn_clear = ttk.Button(manage_frame, text="Wyczyść", command=self.clear_recipe)
        btn_clear.pack(side='left', padx=2)
    
    def create_parameters_section(self, parent):
        """Tworzy sekcję parametrów z kalkulatorem słoików"""
        params_frame = ttk.LabelFrame(parent, text="Parametry przepisu i obliczenia")
        params_frame.pack(fill='x', pady=(0, 10))
        
        # Oryginalne parametry przepisu
        original_frame = ttk.Frame(params_frame)
        original_frame.pack(fill='x', pady=5)
        
        ttk.Label(original_frame, text="Pojemność słoika (ml):").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.jar_capacity_var = tk.StringVar(value="500")
        self.entry_jar_cap = ttk.Entry(original_frame, textvariable=self.jar_capacity_var, width=10)
        self.entry_jar_cap.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        ttk.Label(original_frame, text="Liczba słoików:").grid(row=0, column=2, padx=5, pady=5, sticky='e')
        self.jar_count_var = tk.StringVar(value="5")
        self.entry_jar_count = ttk.Entry(original_frame, textvariable=self.jar_count_var, width=10)
        self.entry_jar_count.grid(row=0, column=3, padx=5, pady=5, sticky='w')
        
        btn_update_params = ttk.Button(original_frame, text="Aktualizuj parametry", command=self.update_recipe_params)
        btn_update_params.grid(row=0, column=4, padx=5, pady=5)
        
        self.volume_label = ttk.Label(original_frame, text="Całkowita objętość: - ml")
        self.volume_label.grid(row=1, column=0, columnspan=2, padx=5, pady=2, sticky='w')
        
        btn_auto_jars = ttk.Button(original_frame, text="Auto-oblicz słoiki", command=self.auto_calculate_jars)
        btn_auto_jars.grid(row=1, column=3, columnspan=2, padx=5, pady=2, sticky='e')
        
        # Separator
        ttk.Separator(params_frame, orient='horizontal').pack(fill='x', padx=5, pady=10)
        
        # Kalkulator słoików dla dowolnej pojemności
        calc_frame = ttk.Frame(params_frame)
        calc_frame.pack(fill='x', pady=5)
        
        ttk.Label(calc_frame, text="KALKULATOR SŁOIKÓW - Oblicz ile słoików potrzebujesz:", 
                 font=('Arial', 9, 'bold')).grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky='w')
        
        ttk.Label(calc_frame, text="Pojemność Twoich słoików (ml):").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.custom_capacity_var = tk.StringVar(value="50")
        entry_custom_cap = ttk.Entry(calc_frame, textvariable=self.custom_capacity_var, width=10)
        entry_custom_cap.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        
        btn_calc_custom = ttk.Button(calc_frame, text="Oblicz liczbę słoików", command=self.calculate_custom_jars)
        btn_calc_custom.grid(row=1, column=2, padx=5, pady=5)
        
        self.custom_result_label = ttk.Label(calc_frame, text="Wprowadź pojemność i kliknij 'Oblicz'", 
                                           foreground='blue')
        self.custom_result_label.grid(row=2, column=0, columnspan=3, padx=5, pady=2, sticky='w')
        
        # Konfiguracja grid
        for i in range(3):
            calc_frame.columnconfigure(i, weight=1)
    
    def calculate_custom_jars(self):
        """Oblicza liczbę słoików dla dowolnej pojemności"""
        try:
            capacity_str = self.custom_capacity_var.get().replace(',', '.')
            
            if not Validators.validate_number(capacity_str, 1, 10000):
                messagebox.showerror("Błąd", "Pojemność słoika musi być liczbą od 1 do 10000 ml.")
                return
            
            capacity = float(capacity_str)
            total_volume = self.calculator.recipe.calculate_total_volume(self.calculator.unit_converter)
            
            if total_volume == 0:
                messagebox.showwarning("Ostrzeżenie", "Brak składników do obliczenia objętości. Dodaj najpierw składniki.")
                return
            
            jars_needed = total_volume / capacity
            # Zaokrąglij w górę
            jars_needed = int(jars_needed) + 1 if jars_needed % 1 > 0 else int(jars_needed)
            
            result_text = (f"Potrzebujesz {jars_needed} słoików o pojemności {capacity} ml\n"
                          f"(całkowita objętość przepisu: {total_volume:.0f} ml)")
            
            self.custom_result_label.config(text=result_text)
            
        except ValueError:
            messagebox.showerror("Błąd", "Pojemność musi być liczbą.")
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd: {str(e)}")
    
    def create_ingredients_section(self, parent):
        """Tworzy sekcję składników"""
        ingredients_frame = ttk.LabelFrame(parent, text="Składniki")
        ingredients_frame.pack(fill='both', expand=True)
        
        header_frame = ttk.Frame(ingredients_frame)
        header_frame.pack(fill='x', padx=5, pady=5)
        
        headers = [('Nazwa składnika', 300), ('Ilość', 100), ('Jednostka', 120), ('Forma', 120), ('Akcje', 100)]
        
        for i, (header, width) in enumerate(headers):
            label = ttk.Label(header_frame, text=header, font=('Arial', 9, 'bold'))
            label.pack(side='left', padx=2, ipadx=5, ipady=2)
            if width:
                label.configure(width=width//10)
        
        container = ttk.Frame(ingredients_frame)
        container.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.canvas = tk.Canvas(container, height=300)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def add_ingredient_row(self, ingredient=None):
        """Dodaje wiersz składnika"""
        row_index = len(self.ingredient_rows)
        row_frame = ttk.Frame(self.scrollable_frame)
        row_frame.pack(fill='x', padx=2, pady=1)
        
        # Nazwa
        name_var = tk.StringVar(value=ingredient.name if ingredient else "")
        entry_name = ttk.Entry(row_frame, textvariable=name_var)
        entry_name.pack(side='left', padx=2, fill='x', expand=True)
        
        # Ilość
        amount_var = tk.StringVar(value=str(ingredient.amount) if ingredient else "0")
        entry_amount = ttk.Entry(row_frame, textvariable=amount_var, width=8)
        entry_amount.pack(side='left', padx=2)
        
        # Jednostka
        unit_var = tk.StringVar(value=ingredient.unit if ingredient else "g")
        combo_unit = ttk.Combobox(row_frame, textvariable=unit_var, 
                                 values=self.calculator.unit_converter.get_available_units(), 
                                 width=10, state="readonly")
        combo_unit.pack(side='left', padx=2)
        combo_unit.set(unit_var.get())
        
        # Forma
        form_var = tk.StringVar(value=ingredient.form if ingredient else "")
        combo_form = ttk.Combobox(row_frame, textvariable=form_var,
                                 values=self.calculator.unit_converter.get_available_forms(),
                                 width=10, state="readonly")
        combo_form.pack(side='left', padx=2)
        combo_form.set(form_var.get())
        
        # Przycisk usuwania
        btn_delete = ttk.Button(row_frame, text="Usuń", 
                               command=lambda: self.delete_ingredient_row(row_frame))
        btn_delete.pack(side='left', padx=2)
        
        # Funkcja do pokazywania/ukrywania formy
        def update_form_visibility(event=None):
            if combo_unit.get() == 'szt':
                combo_form.pack(side='left', padx=2)
            else:
                combo_form.pack_forget()
        
        combo_unit.bind('<<ComboboxSelected>>', lambda e: update_form_visibility())
        update_form_visibility()
        
        self.ingredient_rows.append({
            'frame': row_frame,
            'vars': [name_var, amount_var, unit_var, form_var],
            'widgets': [entry_name, entry_amount, combo_unit, combo_form, btn_delete]
        })
        
        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def delete_ingredient_row(self, row_frame):
        """Usuwa wiersz składnika"""
        for i, row_data in enumerate(self.ingredient_rows):
            if row_data['frame'] == row_frame:
                row_data['frame'].destroy()
                self.ingredient_rows.pop(i)
                break
        
        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def import_txt(self):
        """Importuje przepis z pliku TXT"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Plik tekstowy", "*.txt"), ("Wszystkie pliki", "*.*")]
        )
        
        if file_path:
            try:
                recipe = self.txt_importer.import_recipe(file_path)
                self.calculator.recipe = recipe
                self.load_recipe_data()
                messagebox.showinfo("Sukces", "Przepis został zaimportowany z TXT!")
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się zaimportować przepisu: {str(e)}")

    def import_docx(self):
        """Importuje przepis z pliku DOCX"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Pliki Word", "*.docx"), ("Wszystkie pliki", "*.*")]
        )
        
        if file_path:
            try:
                recipe = self.docx_importer.import_recipe(file_path)
                self.calculator.recipe = recipe
                self.load_recipe_data()
                messagebox.showinfo("Sukces", "Przepis został zaimportowany z DOCX!")
            except Exception as e:
                messagebox.showerror("Błąd", f"Błąd importu DOCX: {str(e)}")

    def import_pdf(self):
        """Importuje przepis z pliku PDF"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Pliki PDF", "*.pdf"), ("Wszystkie pliki", "*.*")]
        )
        
        if file_path:
            try:
                recipe = self.pdf_importer.import_recipe(file_path)
                self.calculator.recipe = recipe
                self.load_recipe_data()
                messagebox.showinfo("Sukces", "Przepis został zaimportowany z PDF!")
            except Exception as e:
                messagebox.showerror("Błąd", f"Błąd importu PDF: {str(e)}")

    def show_help(self):
        """Pokazuje plik pomocy"""
        help_file = "pomoc.txt"
        if not os.path.exists(help_file):
            self.create_help_file(help_file)
        
        try:
            os.startfile(help_file)
        except:
            try:
                import subprocess
                subprocess.call(['open', help_file])
            except:
                import subprocess
                subprocess.call(['xdg-open', help_file])

    def show_template(self):
        """Pokazuje szablon przepisu"""
        template_file = "szablon_przepisu.txt"
        if not os.path.exists(template_file):
            self.create_template_file(template_file)
        
        try:
            os.startfile(template_file)
        except:
            try:
                import subprocess
                subprocess.call(['open', template_file])
            except:
                import subprocess
                subprocess.call(['xdg-open', template_file])

    def create_help_file(self, filename):
        """Tworzy plik pomocy"""
        help_content = """INSTRUKCJA OBSŁUGI KALKULATORA PRZETWORÓW

1. IMPORT PRZEPISU
   - Użyj przycisków Importuj z TXT/DOCX/PDF aby wczytać istniejący przepis
   - Plik TXT powinien zawierać listę składników w formacie:
        nazwa_składnika ilość jednostka

2. EDYCJA PRZEPISU
   - Wprowadź pojemność słoików i ich liczbę dla oryginalnego przepisu
   - Dodaj składniki używając przycisku "Dodaj składnik"
   - Dla owoców/warzyw w sztukach wybierz formę: całe, cząstki lub tarte

3. KALKULATOR SŁOIKÓW
   - W sekcji "KALKULATOR SŁOIKÓW" wpisz pojemność swoich słoików (np. 50 ml dla dżemów)
   - Kliknij "Oblicz liczbę słoików" aby dowiedzieć się ile słoików potrzebujesz
   - Program obliczy całkowitą objętość przepisu i poda dokładną liczbę słoików

4. AUTO-OBLICZANIE
   - Użyj "Auto-oblicz słoiki" aby program dobrał optymalne parametry

5. PRZELICZANIE
   - Przejdź do zakładki "Przeliczanie"
   - Wybierz profil obliczeń (dokładny lub porcja obiadowa)
   - Wprowadź parametry docelowych słoików lub użyj auto-doboru
   - Kliknij "Przelicz" aby otrzymać wynik

6. EKSPORT
   - Wynik można wyeksportować do TXT, DOCX lub PDF

JEDNOSTKI:
- Masa: g, kg, szczypta
- Objętość: ml, l, łyżka, łyżeczka, szklanka
- Sztuki: szt, ząbek, plaster, porcja

FORMY PRZYGOTOWANIA:
- całe - całe owoce/warzywa
- cząstki - pokrojone na kawałki
- tarte - starte na tarce
- kostka - pokrojone w kostkę

PRZYKŁAD POPRAWNEGO PLIKU TXT:
Nazwa Przepisu
pomidory 2 kg
cebula 3 szt
czosnek 2 ząbki
oliwa 100 ml
cukier 1 łyżka
sól 1 łyżeczka

WSKAZÓWKI:
- Dla dżemów używaj małych słoików 50-100 ml
- Dla warzyw w zalewie używaj słoików 250-500 ml
- Zawsze przygotuj 1-2 dodatkowe słoiki na zapas"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(help_content)

    def create_template_file(self, filename):
        """Tworzy szablon przepisu"""
        template_content = """SZABLON PRZEPISU DO IMPORTU
# Zapisz ten plik jako .txt i zaimportuj w programie

NAZWA PRZEPISU: Dżem truskawkowy

SKŁADNIKI:
truskawki 1 kg
cukier 0.5 kg
sok z cytryny 2 łyżki
żelatyna 1 łyżeczka

INSTRUKCJA IMPORTU:
1. Zapisz ten plik z rozszerzeniem .txt
2. W programie kliknij "Importuj z TXT"
3. Sprawdź czy wszystkie składniki zostały poprawnie rozpoznane
4. Wprowadź parametry słoików lub użyj kalkulatora
5. Zapisz przepis w programie

PRZYKŁADY POPRAWNYCH SKŁADNIKÓW:
- pomidory 2 kg
- cebula 3 szt (całe)
- czosnek 4 ząbki
- oliwa 100 ml
- cukier 1 szklanka
- sól 1 łyżeczka

DOSTĘPNE JEDNOSTKI:
g, kg, ml, l, łyżka, łyżeczka, szklanka, szt, ząbek, plaster, porcja

FORMY PRZYGOTOWANIA (dla sztuk):
całe, cząstki, tarte, kostka

PRZYKŁAD Z FORMĄ:
jabłka 6 szt (cząstki) - program uwzględni formę przygotowania przy obliczeniach"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(template_content)

    def load_recipe_data(self):
        """Ładuje dane przepisu do formularza"""
        recipe = self.calculator.recipe
        
        self.jar_capacity_var.set(str(recipe.original_jar_capacity))
        self.jar_count_var.set(str(recipe.original_jar_count))
        
        # Czyścimy stare wiersze
        for row_data in self.ingredient_rows:
            row_data['frame'].destroy()
        self.ingredient_rows = []
        
        # Dodajemy wiersze dla każdego składnika
        for ingredient in recipe.ingredients:
            self.add_ingredient_row(ingredient)
        
        self.update_volume_info()
    
    def save_recipe(self):
        """Zapisuje przepis z formularza"""
        try:
            # Aktualizuj parametry przepisu
            if not self.update_recipe_params(silent=True):
                return
            
            # Aktualizuj składniki
            new_ingredients = []
            for row_data in self.ingredient_rows:
                name = row_data['vars'][0].get().strip()
                if not name:
                    continue
                
                if not Validators.validate_ingredient_name(name):
                    messagebox.showerror("Błąd", f"Nieprawidłowa nazwa składnika: {name}")
                    return
                
                try:
                    amount_str = row_data['vars'][1].get().replace(',', '.')
                    if not Validators.validate_number(amount_str, 0, 10000):
                        messagebox.showerror("Błąd", f"Nieprawidłowa ilość dla składnika: {name}. Dopuszczalny zakres: 0-10000")
                        return
                    amount = float(amount_str)
                    
                    unit = row_data['vars'][2].get()
                    if not Validators.validate_unit(unit):
                        messagebox.showerror("Błąd", f"Nieprawidłowa jednostka dla składnika: {name}")
                        return
                    
                    form = row_data['vars'][3].get() if row_data['vars'][3].get() else None
                    
                    new_ingredients.append(Ingredient(name, amount, unit, form))
                except ValueError:
                    messagebox.showerror("Błąd", f"Nieprawidłowa ilość dla składnika: {name}")
                    return
            
            self.calculator.recipe.ingredients = new_ingredients
            self.update_volume_info()
            messagebox.showinfo("Sukces", "Przepis został zapisany!")
            
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd podczas zapisywania: {str(e)}")
    
    def clear_recipe(self):
        """Czyści cały przepis"""
        if messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz wyczyścić przepis? Wszystkie dane zostaną utracone."):
            self.calculator.recipe.ingredients = []
            self.load_recipe_data()
            messagebox.showinfo("Sukces", "Przepis został wyczyszczony!")
    
    def update_recipe_params(self, silent=False):
        """Aktualizuje parametry przepisu"""
        try:
            capacity_str = self.jar_capacity_var.get().replace(',', '.')
            count_str = self.jar_count_var.get().replace(',', '.')
            
            if not Validators.validate_number(capacity_str, 1, 10000):
                if not silent:
                    messagebox.showerror("Błąd", "Pojemność słoika musi być liczbą od 1 do 10000 ml.")
                return False
            if not Validators.validate_number(count_str, 1, 1000):
                if not silent:
                    messagebox.showerror("Błąd", "Liczba słoików musi być liczbą od 1 do 1000.")
                return False
            
            capacity = float(capacity_str)
            count = float(count_str)
            
            self.calculator.recipe.original_jar_capacity = capacity
            self.calculator.recipe.original_jar_count = count
            
            self.update_volume_info()
            
            if not silent:
                messagebox.showinfo("Sukces", "Parametry przepisu zostały zaktualizowane.")
            
            return True
                
        except ValueError:
            if not silent:
                messagebox.showerror("Błąd", "Pojemność i liczba słoików muszą być liczbami.")
            return False
    
    def auto_calculate_jars(self):
        """Automatycznie oblicza liczbę słoików na podstawie składników"""
        try:
            total_volume = self.calculator.recipe.calculate_total_volume(self.calculator.unit_converter)
            
            if total_volume == 0:
                messagebox.showwarning("Ostrzeżenie", "Brak składników do obliczenia objętości.")
                return
            
            standard_jars = [125, 250, 500, 750, 1000]
            best_jar = min(standard_jars, key=lambda x: abs(x - 500))
            jar_count = total_volume / best_jar * 1.1
            jar_count = max(1, int(jar_count) + 1)
            
            self.jar_capacity_var.set(str(best_jar))
            self.jar_count_var.set(str(jar_count))
            self.update_recipe_params(silent=True)
            
            messagebox.showinfo("Auto-obliczanie", 
                              f"Obliczono słoiki {best_jar} ml, liczba: {jar_count}\n"
                              f"Całkowita objętość: {total_volume:.0f} ml")
            
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się obliczyć słoików: {str(e)}")
    
    def update_volume_info(self):
        """Aktualizuje informację o całkowitej objętości"""
        total_volume = self.calculator.recipe.calculate_total_volume(self.calculator.unit_converter)
        self.volume_label.config(text=f"Całkowita objętość: {total_volume:.0f} ml")