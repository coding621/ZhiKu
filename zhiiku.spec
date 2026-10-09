# -*- mode: python ; coding: utf-8 -*-
# 知库 ZhiKu 打包配置：onedir 之外的单文件 exe
# 构建：venv\Scripts\python -m PyInstaller zhiiku.spec --noconfirm

a = Analysis(
    ['kb-server.py'],
    pathex=[],
    binaries=[],
    datas=[('static/index.html', 'static')],
    hiddenimports=[
        'webview.platforms.edgechromium',
        'webview.platforms.winforms',
        'webview.platforms.win32',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'unittest', 'pydoc_data'],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ZhiKu',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,          # 无控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
