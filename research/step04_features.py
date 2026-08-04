import numpy as np

from common.features import FeatureExtractor

from config import RESULTS_DIR


data = np.load(

    RESULTS_DIR / "eo_windows.npz",

    allow_pickle=True,

)

X = data["X"]

y = data["y"]

subjects = data["subjects"]

recordings = data["recordings"]

extractor = FeatureExtractor()

features = []

for i, window in enumerate(X):

    if (i + 1) % 500 == 0:

        print(f"{i+1}/{len(X)}")

    features.append(

        extractor.extract(window)

    )

features = np.asarray(

    features,

    dtype=np.float32,

)

print()

print("=" * 60)

print("FEATURE MATRIX")

print("=" * 60)

print(features.shape)

np.savez_compressed(

    RESULTS_DIR / "eo_features.npz",

    X=features,

    y=y,

    subjects=subjects,

    recordings=recordings,

)

print()

print("Saved:")

print(RESULTS_DIR / "eo_features.npz")
