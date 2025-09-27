# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import shutil
from datetime import datetime

def build_executable():
    """Buduje plik wykonywalny z ikoną"""
    
    print("🛠️  Rozpoczynam budowanie Kalkulatora Przetworów...")
    
    # Sprawdź czy PyInstaller jest zainstalowany
    try:
        import PyInstaller
        print("✅ PyInstaller jest dostępny")
    except ImportError:
        print("❌ PyInstaller nie jest zainstalowany!")
        print("Instaluję PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Sprawdź wymagane biblioteki
    libraries = ['python-docx', 'reportlab', 'PyPDF2']
    for lib in libraries:
        try:
            __import__(lib.replace('-', '_'))
            print(f"✅ {lib} jest dostępna")
        except ImportError:
            print(f"❌ {lib} nie jest zainstalowana!")
            print(f"Instaluję {lib}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
    
    # Sprawdź czy ikona istnieje
    if not os.path.exists("icon.ico"):
        print("⚠️  Brak pliku icon.ico - tworzę podstawową ikonę...")
        create_default_icon()
    
    # Sprawdź czy plik spec istnieje
    if not os.path.exists("build.spec"):
        print("❌ Brak pliku build.spec!")
        return False
    
    # Czyść poprzednie buildy
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    
    # Buduj za pomocą PyInstaller
    print("🔨 Rozpoczynam kompilację...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "PyInstaller",
            "build.spec",
            "--onefile",
            "--windowed",
            "--clean"
        ], check=True, capture_output=True, text=True)
        
        print("✅ Kompilacja zakończona pomyślnie!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Błąd podczas kompilacji: {e}")
        print(f"Stderr: {e.stderr}")
        return False
    
    # Sprawdź czy plik został utworzony
    exe_path = "dist/KalkulatorPrzetworow.exe"
    if os.path.exists(exe_path):
        file_size = os.path.getsize(exe_path) / (1024 * 1024)  # Rozmiar w MB
        print(f"✅ Plik utworzony: {exe_path}")
        print(f"📦 Rozmiar pliku: {file_size:.2f} MB")
        
        # Kopiuj pliki pomocy do folderu dist
        for file in ["pomoc.txt", "szablon_przepisu.txt"]:
            if os.path.exists(file):
                shutil.copy2(file, "dist")
                print(f"📄 Skopiowano: {file}")
        
        print("\n🎉 BUDOWANIE ZAKOŃCZONE POMYŚLNIE!")
        print("Plik wykonywalny znajduje się w folderze 'dist'")
        return True
    else:
        print("❌ Plik wykonywalny nie został utworzony!")
        return False

def create_default_icon():
    """Tworzy podstawową ikonę jeśli nie istnieje"""
    try:
        from PIL import Image, ImageDraw
        print("✅ PIL jest dostępny - tworzę ikonę...")
    except ImportError:
        print("❌ PIL nie jest zainstalowany - pomijam tworzenie ikony")
        return
    
    # Utwórz prostą ikonę 64x64
    img = Image.new('RGB', (64, 64), color='green')
    d = ImageDraw.Draw(img)
    
    # Narysuj prosty słoik
    d.rectangle([15, 10, 49, 40], fill='white', outline='black', width=2)
    d.rectangle([20, 40, 44, 50], fill='yellow', outline='black', width=1)
    d.rectangle([25, 50, 39, 54], fill='brown', outline='black', width=1)
    
    # Zapisz jako ICO
    img.save('icon.ico', format='ICO')
    print("✅ Utworzono domyślną ikonę")

if __name__ == "__main__":
    build_executable()