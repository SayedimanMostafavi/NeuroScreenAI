# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = (
    collect_submodules("mne")
    + collect_submodules("mne_connectivity")
    + collect_submodules("sklearn")
    + collect_submodules("scipy")
    + collect_submodules("numpy")
    + collect_submodules("joblib")
)

datas = (
    collect_data_files("mne")
    + collect_data_files("mne_connectivity")
    + [
        ("../assets/models/best_subject_model.pkl", "assets/models"),
        ("../assets/models/scaler.pkl", "assets/models"),
        ("../assets/models/feature_selector.pkl", "assets/models"),
    ]
)

a = Analysis(
    ["main.py"],
    pathex=[
        ".",
        "..",
    ],
    binaries=[],
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
    upx=True,
    name="NeuroScreenAI",
)
