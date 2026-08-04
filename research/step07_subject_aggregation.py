import numpy as np
import pandas as pd

from config import RESULTS_DIR


print("=" * 70)
print("Loading window features")
print("=" * 70)

data = np.load(
    RESULTS_DIR / "eo_features_selected.npz",
    allow_pickle=True,
)

X = data["X"]
y = data["y"]
subjects = data["subjects"]

print("Window feature matrix:", X.shape)

############################################################

unique_subjects = np.unique(subjects)

subject_features = []
subject_labels = []
subject_ids = []

############################################################

for subject in unique_subjects:

    idx = np.where(subjects == subject)[0]

    F = X[idx]

    mean = np.mean(F, axis=0)

    std = np.std(F, axis=0)

    median = np.median(F, axis=0)

    minimum = np.min(F, axis=0)

    maximum = np.max(F, axis=0)

    feature_vector = np.concatenate([

        mean,

        std,

        median,

        minimum,

        maximum,

    ])

    subject_features.append(feature_vector)

    subject_labels.append(y[idx][0])

    subject_ids.append(subject)

############################################################

subject_features = np.asarray(
    subject_features,
    dtype=np.float32,
)

subject_labels = np.asarray(
    subject_labels,
    dtype=np.int64,
)

subject_ids = np.asarray(subject_ids)

############################################################

print()

print("=" * 70)
print("SUBJECT DATASET")
print("=" * 70)

print("Subjects :", len(subject_ids))
print("Features :", subject_features.shape)

############################################################

np.savez_compressed(

    RESULTS_DIR / "eo_subject_features.npz",

    X=subject_features,

    y=subject_labels,

    subjects=subject_ids,

)

print()

print("Saved:")
print(RESULTS_DIR / "eo_subject_features.npz")
