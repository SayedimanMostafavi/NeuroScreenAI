import numpy as np
import pandas as pd

from common.preprocessing import EEGPreprocessor
from common.windowing import WindowGenerator

from config import RESULTS_DIR


train = pd.read_csv(

    RESULTS_DIR / "train.csv"

)

processor = EEGPreprocessor()

generator = WindowGenerator()

all_windows = []

all_labels = []

all_subjects = []

all_recordings = []

total = 0

for i, row in train.iterrows():

    if row.recording != "EO":
        continue

    raw = processor.run(row.file)

    windows = generator.generate(raw)

    print(

        f"[{i+1}/{len(train)}] "

        f"{row.filename:<20}"

        f"{len(windows)} windows"

    )

    total += len(windows)

    all_windows.append(windows)

    all_labels.extend(

        [row.label] * len(windows)

    )

    all_subjects.extend(

        [row.subject] * len(windows)

    )

    all_recordings.extend(

        [row.filename] * len(windows)

    )

X = np.concatenate(

    all_windows,

    axis=0,

)

y = np.asarray(

    all_labels,

    dtype=np.int64,

)

subjects = np.asarray(

    all_subjects,

)

recordings = np.asarray(

    all_recordings,

)

np.savez_compressed(

    RESULTS_DIR / "eo_windows.npz",

    X=X,

    y=y,

    subjects=subjects,

    recordings=recordings,

)

print()

print("=" * 60)

print("WINDOW DATASET")

print("=" * 60)

print("Shape :", X.shape)

print("Labels:", y.shape)

print("Subjects:", len(np.unique(subjects)))

print("Windows:", total)

print()

print("Saved to")

print(RESULTS_DIR / "eo_windows.npz")
