import numpy as np

from common.connectivity import ConnectivityExtractor
from common.graph_features import GraphFeatureExtractor

from config import RESULTS_DIR


print("=" * 70)
print("Loading window dataset")
print("=" * 70)

data = np.load(
    RESULTS_DIR / "eo_windows.npz",
    allow_pickle=True,
)

windows = data["X"]
labels = data["y"]
subjects = data["subjects"]
recordings = data["recordings"]

conn = ConnectivityExtractor()

graph = GraphFeatureExtractor()

features = []

for i, window in enumerate(windows):

    if (i + 1) % 100 == 0:

        print(f"{i+1}/{len(windows)}")

    matrices = conn.compute(window)

    sample = []

    for band in [

        "delta",

        "theta",

        "alpha",

        "beta",

    ]:

        sample.extend(

            graph.extract(

                matrices[band]

            )

        )

    features.append(sample)

features = np.asarray(

    features,

    dtype=np.float32,

)

print()

print("=" * 70)
print("CONNECTIVITY FEATURES")
print("=" * 70)

print(features.shape)

np.savez_compressed(

    RESULTS_DIR / "eo_connectivity_features.npz",

    X=features,

    y=labels,

    subjects=subjects,

    recordings=recordings,

)

print()

print("Saved:")
print(RESULTS_DIR / "eo_connectivity_features.npz")
