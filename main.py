# -*- coding: utf-8 -*-
import tkinter as tk
import os
from gui.main_window import MainWindow

def create_default_files():
    """Tworzy domyślne pliki pomocy jeśli nie istnieją"""
    if not os.path.exists("pomoc.txt"):
        with open("pomoc.txt", "w", encoding="utf-8") as f:
            f.write("""INSTRUKCJA OBSŁUGI KALKULATORA PRZETWORÓW
=========================================

WITAJ W KALKULATORZE PRZETWORÓW!
Program pomaga obliczyć ilość składników i potrzebnych słoików dla Twoich przepisów.

📁 IMPORT PRZEPISU
------------------
Program obsługuje import z trzech formatów:
- TXT (zalecany) - najprostszy format tekstowy
- DOCX - pliki Microsoft Word
- PDF - dokumenty PDF

Format pliku TXT powinien wyglądać tak:
Nazwa Przepisu
składnik1 ilość jednostka
składnik2 ilość jednostka
...

Przykład:
Dżem truskawkowy
truskawki 1 kg
cukier 0.5 kg
sok z cytryny 2 łyżki

✏️ EDYCJA PRZEPISU
------------------
W zakładce "Edycja przepisu" możesz:
- Ręcznie dodawać składniki przyciskiem "Dodaj składnik"
- Edytować istniejące składniki
- Ustawiać pojemność i liczbę słoików dla oryginalnego przepisu

🧮 KALKULATOR SŁOIKÓW
---------------------
W sekcji "KALKULATOR SŁOIKÓW" możesz obliczyć:
1. Wpisz pojemność swoich słoików (np. 50 ml dla dżemów)
2. Kliknij "Oblicz liczbę słoików"
3. Program poda dokładną liczbę potrzebnych słoików

Przykład: Jeśli masz przepis na 5 słoików 500 ml, a chcesz użyć słoików 125 ml,
program przeliczy że potrzebujesz 20 słoików.

📊 PRZELICZANIE PRZEPISU
------------------------
W zakładce "Przeliczanie" możesz:
1. Wybrać profil obliczeń:
   - DOKŁADNA ILOŚĆ - precyzyjne przeliczenie na nowe słoiki
   - PORCJA OBIADOWA - przeliczenie na porcje dla 2 lub 4 osób

2. Ustawić docelowe parametry słoików:
   - Pojemność (ml)
   - Liczbę słoików

3. Użyć "Auto-dobór słoików" - program sam dobierze optymalne parametry

💾 EKSPORT WYNIKÓW
------------------
Wyniki można wyeksportować do:
- TXT - prosty tekst
- DOCX - dokument Word
- PDF - dokument PDF

W eksportowanym pliku znajdziesz:
- Przeliczone składniki
- Informacje o słoikach
- Datę generowania

📏 OBSŁUGIWANE JEDNOSTKI
------------------------
MASA:
- g (gram)
- kg (kilogram)
- szczypta

OBJĘTOŚĆ:
- ml (mililitr)
- l (litr)
- łyżka (15 ml)
- łyżeczka (5 ml)
- szklanka (250 ml)

SZTUKI:
- szt (sztuka)
- ząbek (czosnku)
- plaster
- porcja

🔢 FORMY PRZYGOTOWANIA (dla składników w sztukach)
--------------------------------------------------
- CAŁE - całe owoce/warzywa
- CZĄSTKI - pokrojone na kawałki
- TARTE - starte na tarce
- KOSTKA - pokrojone w kostkę

Forma wpływa na obliczenia objętości!

💡 PRAKTYCZNE WSKAZÓWKI
-----------------------
DŻEMY I KONFITURY:
- Używaj małych słoików 50-100 ml
- Dżemy się nie psują szybko, ale małe porcje są praktyczniejsze

WARZYWA W ZALEWIE:
- Optymalne słoiki 250-500 ml
- Dobrze dobierz zalewę (około 30% objętości)

OWOCE W SYROPIE:
- Słoiki 250-750 ml
- Pamiętaj o cukrze w syropie

MIĘSA I PASZTETY:
- Większe słoiki 500-1000 ml
- Pasteryzuj dłużej dla bezpieczeństwa

ZALECENIA:
- Zawsze przygotuj 1-2 dodatkowe słoiki na zapas
- Zapasowy słoik przydaje się gdy przepis "nie wychodzi"
- Oznacz słoiki datą produkcji

🆘 ROZWIĄZYWANIE PROBLEMÓW
--------------------------
PROBLEM: Import nie działa
ROZWIĄZANIE: Sprawdź czy plik ma odpowiedni format. Użyj szablonu.

PROBLEM: Program nie rozpoznaje składników
ROZWIĄZANIE: Sprawdź pisownię jednostek. Użyj tylko obsługiwanych jednostek.

PROBLEM: Obliczenia wydają się nieprawidłowe
ROZWIĄZANIE: Sprawdź czy wszystkie składniki mają jednostki. Upewnij się że forma jest ustawiona dla sztuk.

PROBLEM: Eksport PDF ma problemy z polskimi znakami
ROZWIĄZANIE: Użyj eksportu DOCX lub TXT.

📞 POMOC TECHNICZNA
-------------------
Jeśli masz problemy z programem:
1. Sprawdź czy masz najnowszą wersję
2. Prześlij plik z przepisem do analizy
3. Sprawdź czy nie brakuje żadnych plików programu

Program został zaprojektowany z myślą o łatwości użytkowania.
Życzymy udanych przetworów!

🍅🍓🥒 HAPPY PRESERVING! 🥫🍯🍎""")
    
    if not os.path.exists("szablon_przepisu.txt"):
        with open("szablon_przepisu.txt", "w", encoding="utf-8") as f:
            f.write("""SZABLON PRZEPISU DO IMPORTU
===========================

INSTRUKCJA UŻYCIA:
1. Zapisz ten plik pod własną nazwą (np. "moj_przepis.txt")
2. Edytuj składniki według swojego przepisu
3. W programie kliknij "Importuj z TXT"
4. Sprawdź poprawność importu
5. Użyj kalkulatora słoików aby obliczyć potrzeby

FORMAT PLIKU:
- Pierwsza linia: NAZWA PRZEPISU
- Kolejne linie: SKŁADNIKI w formacie "nazwa ilość jednostka"
- Pusta linia oznacza koniec sekcji

PRZYKŁAD POPRAWNEGO PRZEPISU:
-----------------------------
Dżem truskawkowy
truskawki 1.5 kg
cukier 0.75 kg
sok z cytryny 3 łyżki
żelatyna 2 łyżeczki

PRZYKŁADY RÓŻNYCH PRZEPISÓW:
----------------------------

PRZEPIS 1: DŻEM TRUSKAWKOWY
Dżem truskawkowy na małe słoiki
truskawki 2 kg
cukier 1.5 kg
sok z cytryny 4 łyżki

PRZEPIS 2: OGÓRKI KISZONE
Ogórki kiszone w zalewie
ogórki 3 kg
woda 1.5 l
sól 3 łyżki
koper 2 baldachy
chrzan 2 plastry
czosnek 6 ząbków

PRZEPIS 3: KONFITURA ŚLIWKOWA
Konfitura ze śliwek węgierki
śliwki węgierki 2 kg
cukier 1 kg
goździki 5 szt
cynamon 1 laska

PRZEPIS 4: WARZYWA W OCCIE
Mieszanka warzywna w occie
kalafior 1 kg
marchew 0.5 kg
cebula 0.3 kg
ocet 0.5 l
woda 0.5 l
cukier 2 łyżki
sól 1 łyżka

PRZEPIS 5: SOS POMIDOROWY
Sos pomidorowy do spaghetti
pomidory 5 kg
cebula 0.5 kg
czosnek 10 ząbków
oliwa 100 ml
bazylia 2 łyżki
oregano 1 łyżka
cukier 1 łyżka
sól 2 łyżeczki

LISTA OBSŁUGIWANYCH JEDNOSTEK:
------------------------------
MASA: g, kg, szczypta
OBJĘTOŚĆ: ml, l, łyżka, łyżeczka, szklanka
SZTUKI: szt, ząbek, plaster, porcja

FORMY PRZYGOTOWANIA (dla sztuk):
--------------------------------
- (całe)    - całe owoce/warzywa
- (cząstki) - pokrojone na kawałki  
- (tarte)   - starte na tarce
- (kostka)  - pokrojone w kostkę

Przykład użycia formy:
jabłka 6 szt (cząstki)
marchew 3 szt (tarte)

WAŻNE WSKAZÓWKI:
----------------
1. ZAPISUJ DECYMALE Z KROPKĄ: 0.5 kg (NIE 0,5 kg)
2. UŻYWAJ PROSTYCH NAZW SKŁADNIKÓW: "cukier" zamiast "cukier kryształ"
3. JEDNOSTKI PISZ MAŁYMI LITERAMI: "kg" zamiast "KG"
4. DLA SKŁADNIKÓW W SZTUKACH PODAJ FORMĘ PRZYGOTOWANIA
5. NAZWA PRZEPISU NIE POWINNA ZAWIERAĆ LICZB

PRZYKŁADY POPRAWNYCH SKŁADNIKÓW:
--------------------------------
- pomidory 2.5 kg
- cebula 4 szt (całe)
- czosnek 8 ząbków
- oliwa 150 ml
- cukier 1 szklanka
- sól 2 łyżeczki
- marchew 0.5 kg
- jabłka 10 szt (cząstki)

PRZYKŁADY NIEPOPRAWNYCH SKŁADNIKÓW:
-----------------------------------
- pomidory 2,5 kg (użyj kropki zamiast przecinka)
- Cebula 3 SZT (użyj małych liter)
- cukier kryształ 200 g (użyj prostej nazwy "cukier")
- sól (brak ilości i jednostki)

KROKI PO IMPORCIE:
------------------
1. Sprawdź czy wszystkie składniki zostały poprawnie rozpoznane
2. Wprowadź oryginalne parametry słoików (pojemność i liczbę)
3. Użyj przycisku "Auto-oblicz słoiki" lub "Kalkulator słoików"
4. Zapisz przepis w programie przyciskiem "Zapisz przepis"
5. Przejdź do zakładki "Przeliczanie" aby dostosować do swoich potrzeb

ŻYCZENIA:
---------
Życzymy łatwego i przyjemnego tworzenia przetworów!
Pamiętaj o sterylizacji słoików i bezpiecznym pasteryzowaniu.

Smacznego! 🍅🥫🍓""")

def main():
    """Główna funkcja uruchamiająca aplikację"""
    try:
        create_default_files()
        
        root = tk.Tk()
        app = MainWindow(root)
        root.mainloop()
    except Exception as e:
        print(f"Błąd podczas uruchamiania aplikacji: {e}")
        input("Naciśnij Enter aby zakończyć...")

if __name__ == "__main__":
    main()