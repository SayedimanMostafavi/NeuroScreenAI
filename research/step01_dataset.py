from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

from config import *

rows = []

for edf in sorted(DATA_DIR.glob("*.edf")):

    name = edf.stem.strip()

    tokens = name.split()

    # Label
    if tokens[0] == "H":
        label = 0
    elif tokens[0] == "MDD":
        label = 1
    else:
        continue

    # Subject ID
    subject = "_".join(tokens[:-1])

    # Recording type
    recording = tokens[-1]

    rows.append({

        "file": str(edf),

        "filename": edf.name,

        "subject": subject,

        "recording": recording,

        "label": label

    })

df = pd.DataFrame(rows)

print(df.head())

print()

print("Total recordings :", len(df))

print("Subjects :", df.subject.nunique())

subjects = df[["subject","label"]].drop_duplicates()

train_subjects, test_subjects = train_test_split(

    subjects,

    test_size=TEST_SIZE,

    stratify=subjects["label"],

    random_state=RANDOM_STATE

)

train_subjects, valid_subjects = train_test_split(

    train_subjects,

    test_size=VALID_SIZE,

    stratify=train_subjects["label"],

    random_state=RANDOM_STATE

)

train = df.merge(train_subjects)

valid = df.merge(valid_subjects)

test = df.merge(test_subjects)

RESULTS_DIR.mkdir(exist_ok=True)

train.to_csv(RESULTS_DIR / "train.csv", index=False)
valid.to_csv(RESULTS_DIR / "validation.csv", index=False)
test.to_csv(RESULTS_DIR / "test.csv", index=False)

print()

print("================================")
print("Train")
print("================================")
print(train.subject.nunique(), "subjects")
print(len(train), "recordings")

print()

print("================================")
print("Validation")
print("================================")
print(valid.subject.nunique(), "subjects")
print(len(valid), "recordings")

print()

print("================================")
print("Test")
print("================================")
print(test.subject.nunique(), "subjects")
print(len(test), "recordings")
