# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Odczytaj informacje o wersji jeśli plik istnieje
version_info = None
try:
    with open('version_info.txt', 'r') as f:
        version_info = f.read()
except:
    pass

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('pomoc.txt', '.'),
        ('szablon_przepisu.txt', '.'),
        ('core/*.py', 'core'),
        ('gui/*.py', 'gui'),
        ('import_export/*.py', 'import_export'),
        ('utils/*.py', 'utils'),
    ],
    hiddenimports=[
        'tkinter', 'tkinter.ttk', 'docx', 'docx.shared',
        'reportlab', 'reportlab.lib', 'reportlab.pdfgen',
        'reportlab.lib.pagesizes', 'reportlab.platypus',
        'reportlab.pdfbase', 'reportlab.pdfbase.ttfonts',
        'PyPDF2', 'json', 'os', 're', 'datetime', 'subprocess',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='KalkulatorPrzetworow',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',
    version=version_info if version_info else None,
)