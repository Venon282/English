# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['..\\english.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\esto5\\anaconda3\\envs\\PIP\\Lib\\site-packages\\user_agent', './user_agent/'), ('D:\\Folders\\Code\\Python\\English\\data.txt', './'), ('D:\\Folders\\Code\\Python\\English\\WordListTranslate.txt', './'), ('D:\\Folders\\Code\\Python\\English\\WordList.txt', './')],
    hiddenimports=[],
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
    [],
    name='english',
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