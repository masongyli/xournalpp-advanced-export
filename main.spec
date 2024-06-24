# -*- mode: python ; coding: utf-8 -*-

# pyinstaller can't find modules imported by importlib
# so we need to use hiddenimports to explicitly tell pyinstaller to include these modules

from pathlib import Path

hidden_imports = []

for file in Path('src/operations').iterdir():
    if file.stem.startswith('operation_') and file.suffix == '.py':
        module_name = f"operations.{file.stem}"
        hidden_imports.append(module_name)


a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
