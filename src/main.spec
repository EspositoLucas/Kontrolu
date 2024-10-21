#-*- mode: python ; coding: utf-8 -*-

import os

block_cipher = None

# Obtén la ruta absoluta al directorio de imágenes
imgs_path = os.path.join(os.path.dirname(os.path.abspath('__file__')), 'ui','base', 'imgs')

# Lista todos los archivos PNG en el directorio
image_files = [(os.path.join(imgs_path, f), 'ui/base/imgs') for f in os.listdir(imgs_path) if f.endswith('.png')]

# Ruta al archivo de ícono
icon_path = os.path.join(os.path.dirname(os.path.abspath('__file__')), 'logo.ico')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=image_files,  # Aquí especificamos los archivos de imagen
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='logo.ico'  # Aquí especificamos el ícono
)