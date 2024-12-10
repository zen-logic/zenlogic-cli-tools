# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['FileHunter.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['app.build_imports'],
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
    [],
    Tree('static', prefix='static'),
    Tree('templates', prefix='templates'),
    exclude_binaries=True,
    name='filehunter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='File Hunter',
)
app = BUNDLE(
    coll,
    name='File Hunter.app',
    icon=None,
    bundle_identifier=None,
)
