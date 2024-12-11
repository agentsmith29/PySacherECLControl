# -*- mode: python ; coding: utf-8 -*-
import pathlib

epos_dll_path =   pathlib.Path('../src/SacherECLControl/libs/SacherLib/PythonMotorControlClass/EposCmd64.dll')
sacher_pyd_path = pathlib.Path('../src/SacherECLControl/libs/SacherLib/PythonMotorControlClass/lib/Python312/SacherMotorControl.pyd')

a = Analysis(
    ['../src/lasercontrol_scope.py'],
    pathex=[],
    binaries=[
        (str(epos_dll_path), '.'),
        (str(sacher_pyd_path), '.'),
    ],
    datas=[ ('../pyproject.toml', '.'),
            (str(epos_dll_path), '.'),
            (str(sacher_pyd_path), '.')
        ],
    hiddenimports=['tkinter'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
    onefile=True,
    windowed=True,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='lasercontrol_scope',
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
