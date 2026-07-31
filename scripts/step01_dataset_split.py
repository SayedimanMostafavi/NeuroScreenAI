#!/usr/bin/env python3
"""
=========================================================
NeuroScreenAI
Step 01 : Subject-Level Dataset Split
=========================================================

This script:

1. Reads all EDF recordings of a selected dataset.
2. Groups recordings by subject.
3. Performs subject-level stratified train/test split.
4. Copies ALL recordings belonging to each subject.
5. Saves split summaries.

Example
-------
python scripts/step01_dataset_split.py --dataset depression

Author:
NeuroScreenAI Project
"""

from pathlib import Path
from collections import defaultdict
from sklearn.model_selection import train_test_split
from shutil import copy2, rmtree
import pandas as pd
import re

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_DIR / "data"
RESULTS_DIR = PROJECT_DIR / "results"

TEST_SIZE = 0.20
RANDOM_STATE = 42

# Active dataset
DATASET = "depression"

# Dataset paths
RAW_DIR = DATA_DIR / DATASET / "raw" / "edf"
TRAIN_DIR = DATA_DIR / DATASET / "train"
TEST_DIR = DATA_DIR / DATASET / "test"
RESULT_DIR = RESULTS_DIR / DATASET

# ---------------------------------------------------------
# Clean previous split
# ---------------------------------------------------------

if TRAIN_DIR.exists():
    rmtree(TRAIN_DIR)

if TEST_DIR.exists():
    rmtree(TEST_DIR)

TRAIN_DIR.mkdir(parents=True, exist_ok=True)
TEST_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

# Change this when you want to work with another dataset
DATASET = "depression"
# ---------------------------------------------------------
# Verify folders
# ---------------------------------------------------------

if not RAW_DIR.exists():
    raise FileNotFoundError(
        f"\nDataset not found:\n{RAW_DIR}"
    )

RESULT_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------
# Filename parser
# ---------------------------------------------------------

def parse_filename(file_path):
    """
    Parse EDF filename.

    Examples
    --------
    H S10 EC.edf

    H S10 EO.edf

    MDD S13 TASK.edf

    Returns
    -------
    dict
    """

    name = file_path.stem

    # remove duplicated spaces

    name = re.sub(r"\s+", " ", name).strip()

    tokens = name.split(" ")

    if len(tokens) < 3:
        return None

    label = tokens[0]

    subject = tokens[1]

    recording = tokens[2]

    return {
        "file": file_path,
        "label": label,
        "subject": subject,
        "recording": recording,
        "subject_key": f"{label}_{subject}"
    }


# ---------------------------------------------------------
# Scan EDF files
# ---------------------------------------------------------

print("\nScanning dataset ...")

edf_files = sorted(RAW_DIR.glob("*.edf"))

if len(edf_files) == 0:
    raise RuntimeError("No EDF files found.")


subjects = defaultdict(list)

labels = {}

skipped_files = []


for file in edf_files:

    info = parse_filename(file)

    if info is None:
        skipped_files.append(file.name)
        continue

    key = info["subject_key"]

    subjects[key].append(info)

    labels[key] = info["label"]


print(f"Found EDF files : {len(edf_files)}")
print(f"Found subjects  : {len(subjects)}")


# ---------------------------------------------------------
# Create subject table
# ---------------------------------------------------------

subject_df = pd.DataFrame({
    "subject": list(subjects.keys()),
    "label": [labels[s] for s in subjects]
})

print("\nClass distribution")

print(subject_df["label"].value_counts())

















# ---------------------------------------------------------
# Stratified subject split
# ---------------------------------------------------------

train_subjects, test_subjects = train_test_split(
    subject_df["subject"],
    test_size=TEST_SIZE,
    random_state=RANDOM_STATE,
    stratify=subject_df["label"]
)

train_subjects = sorted(train_subjects.tolist())
test_subjects = sorted(test_subjects.tolist())

print("\nTrain subjects :", len(train_subjects))
print("Test subjects  :", len(test_subjects))


# ---------------------------------------------------------
# Label mapping
# ---------------------------------------------------------

label_map = {}

for label in sorted(subject_df["label"].unique()):

    folder = label.lower()

    # nicer names for common datasets
    if folder == "h":
        folder = "control"

    label_map[label] = folder

print("\nDetected classes")

for k, v in label_map.items():
    print(f"{k}  -->  {v}")


# ---------------------------------------------------------
# Create output folders
# ---------------------------------------------------------

for folder in label_map.values():

    (TRAIN_DIR / folder).mkdir(parents=True, exist_ok=True)

    (TEST_DIR / folder).mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------
# Copy helper
# ---------------------------------------------------------

train_records = []

test_records = []


def copy_subject(subject_key, destination_root, table):

    label = labels[subject_key]

    class_folder = label_map[label]

    destination = destination_root / class_folder

    for recording in subjects[subject_key]:

        src = recording["file"]

        dst = destination / src.name

        copy2(src, dst)

        table.append({

            "subject": subject_key,

            "class": class_folder,

            "recording": recording["recording"],

            "filename": src.name

        })


# ---------------------------------------------------------
# Copy training data
# ---------------------------------------------------------

print("\nCopying training recordings ...")

for subject in train_subjects:

    copy_subject(
        subject,
        TRAIN_DIR,
        train_records
    )


# ---------------------------------------------------------
# Copy testing data
# ---------------------------------------------------------

print("Copying testing recordings ...")

for subject in test_subjects:

    copy_subject(
        subject,
        TEST_DIR,
        test_records
    )


print("\nFinished copying files.")

print(f"Training recordings : {len(train_records)}")
print(f"Testing recordings  : {len(test_records)}")














# ---------------------------------------------------------
# Save reports
# ---------------------------------------------------------

train_df = pd.DataFrame(train_records)
test_df = pd.DataFrame(test_records)

train_df.to_csv(
    RESULT_DIR / "train_subjects.csv",
    index=False
)

test_df.to_csv(
    RESULT_DIR / "test_subjects.csv",
    index=False
)

pd.DataFrame({
    "filename": skipped_files
}).to_csv(
    RESULT_DIR / "skipped_files.csv",
    index=False
)


# ---------------------------------------------------------
# Dataset summary
# ---------------------------------------------------------

summary = []

for label in sorted(label_map.keys()):

    folder = label_map[label]

    train_subject_count = sum(
        labels[s] == label
        for s in train_subjects
    )

    test_subject_count = sum(
        labels[s] == label
        for s in test_subjects
    )

    train_recording_count = sum(
        r["class"] == folder
        for r in train_records
    )

    test_recording_count = sum(
        r["class"] == folder
        for r in test_records
    )

    summary.append({

        "dataset": DATASET,

        "class": folder,

        "train_subjects": train_subject_count,

        "test_subjects": test_subject_count,

        "train_recordings": train_recording_count,

        "test_recordings": test_recording_count

    })


summary_df = pd.DataFrame(summary)

summary_df.to_csv(
    RESULT_DIR / "dataset_summary.csv",
    index=False
)


# ---------------------------------------------------------
# Console summary
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("NeuroScreenAI - Dataset Split Summary")
print("=" * 60)

print(f"Dataset              : {DATASET}")
print(f"EDF files            : {len(edf_files)}")
print(f"Subjects             : {len(subjects)}")
print(f"Training subjects    : {len(train_subjects)}")
print(f"Testing subjects     : {len(test_subjects)}")
print(f"Training recordings  : {len(train_records)}")
print(f"Testing recordings   : {len(test_records)}")
print(f"Skipped files        : {len(skipped_files)}")

print("\nClass distribution")

for label in sorted(label_map.keys()):

    folder = label_map[label]

    train_subject_count = sum(
        labels[s] == label
        for s in train_subjects
    )

    test_subject_count = sum(
        labels[s] == label
        for s in test_subjects
    )

    print(
        f"{folder:<15}"
        f"Train Subjects: {train_subject_count:<3}"
        f" Test Subjects: {test_subject_count:<3}"
    )

print("=" * 60)

print("\nReports saved to")

print(RESULT_DIR)

print("\nDone.\n")
