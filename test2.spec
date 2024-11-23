# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['test2.py'],
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
    name='test2',
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
    name='test2',
)
app = BUNDLE(
    coll,
    name='test2.app',
    icon=None,
    bundle_identifier=None,
)
