import numpy as np

from config import RESULTS_DIR


classic = np.load(

    RESULTS_DIR / "eo_features.npz",

    allow_pickle=True,

)

graph = np.load(

    RESULTS_DIR / "eo_connectivity_features.npz",

    allow_pickle=True,

)

X = np.concatenate(

    [

        classic["X"],

        graph["X"],

    ],

    axis=1,

)

print()

print("=" * 60)
print("MERGED FEATURE MATRIX")
print("=" * 60)

print(X.shape)

np.savez_compressed(

    RESULTS_DIR / "eo_full_features.npz",

    X=X,

    y=classic["y"],

    subjects=classic["subjects"],

    recordings=classic["recordings"],

)

print()

print("Saved:")
print(RESULTS_DIR / "eo_full_features.npz")
