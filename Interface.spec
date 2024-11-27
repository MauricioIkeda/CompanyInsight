# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['Interface.py'],
    pathex=['T:\\Faculdade\\Projeto Ageis\\CompanyInsight\\Interface'],  # Caminho do seu projeto
    binaries=[
        ('C:\\\\Users\\\\kingu\\\\AppData\\\\Local\\\\Programs\\\\Python\\\\Python312\\\\Lib\\\\site-packages\\\\mysql\\\\', 'mysql'),  # Inclui o MySQL
    ],
    datas=[
        ('T:\\Faculdade\\Projeto Ageis\\CompanyInsight\\Interface\\Botoes\\*.png', 'Botoes'),  # Inclui todos os arquivos PNG da pasta Botoes
        ('T:\\Faculdade\\Projeto Ageis\\CompanyInsight\\Treinar IA\\NovaIA', 'NovaIA'),  # Inclui o modelo treinado
    ],  
    hiddenimports=[],
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
    name='Interface',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Console desabilitado
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
