# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for Ticket Manager.
#
# Build with:   pyinstaller ticket_manager.spec
# Output:       dist/TicketManager.exe   (Windows, one-file, no console)
#
# Must be run on the target OS: run this on Windows to get a .exe, on
# macOS for a .app, on Linux for a Linux binary — PyInstaller does not
# cross-compile.

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('ui', 'ui'),
        ('assets', 'assets'),
    ],
    hiddenimports=['PySide6.QtUiTools'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='TicketManager',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,          # no terminal window behind the GUI
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico',
)
