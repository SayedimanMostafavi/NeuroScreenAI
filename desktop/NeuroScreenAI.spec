# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import (
    collect_data_files,
    collect_submodules,
    collect_dynamic_libs,
)

hiddenimports = (
    collect_submodules("mne")
    + collect_submodules("mne_connectivity")
    + collect_submodules("sklearn")
    + collect_submodules("scipy")
    + collect_submodules("numpy")
    + collect_submodules("joblib")
    + collect_submodules("PySide6")
)

datas = (
    collect_data_files("mne")
    + collect_data_files("mne_connectivity")
    + collect_data_files("PySide6")
    + [
        ("../assets/models/best_subject_model.pkl", "assets/models"),
        ("../assets/models/scaler.pkl", "assets/models"),
        ("../assets/models/feature_selector.pkl", "assets/models"),
    ]
)

binaries = (
    collect_dynamic_libs("PySide6")
)

a = Analysis(
    ["main.py"],
    pathex=[
        ".",
        "..",
    ],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="NeuroScreenAI",
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name="NeuroScreenAI",
)
