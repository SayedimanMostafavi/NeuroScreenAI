#!/usr/bin/env python3
"""
============================================================
NeuroScreenAI
Step 04 - Spectral Feature Extraction (Frontal Cortex)
============================================================
"""

from pathlib import Path
from shutil import rmtree

import numpy as np
import pandas as pd
from scipy.signal import welch
from tqdm import tqdm

# ============================================================
# Paths
# ============================================================

PROJECT_DIR = Path("/home/iman/Downloads/Project/NeuroScreenAI")

WINDOW_DIR = PROJECT_DIR / "data" / "depression" / "windows"

FEATURE_DIR = PROJECT_DIR / "data" / "depression" / "features"

RESULT_DIR = (
    PROJECT_DIR
    / "results"
    / "depression"
    / "feature_extraction"
)

if FEATURE_DIR.exists():
    rmtree(FEATURE_DIR)

FEATURE_DIR.mkdir(parents=True, exist_ok=True)
RESULT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# EEG Configuration
# ============================================================


FRONTAL_CHANNELS = [
    "Fp1",
    "Fp2",
    "F7",
    "F3",
    "Fz",
    "F4",
    "F8"
]

# Original channel order in the 31-channel recordings

ALL_CHANNELS = [
    "Fp1","Fp2",
    "F7","F3","Fz","F4","F8",
    "FC5","FC1","FC2","FC6",
    "T7","C3","Cz","C4","T8",
    "CP5","CP1","CP2","CP6",
    "P7","P3","Pz","P4","P8",
    "O1","Oz","O2",
    "PO9","PO10","Iz"
]

CHANNEL_INDEX = {
    ch: i
    for i, ch in enumerate(ALL_CHANNELS)
}

SELECTED_INDEX = [
    CHANNEL_INDEX[ch]
    for ch in FRONTAL_CHANNELS
]

# ============================================================
# Frequency Bands
# ============================================================

BANDS = {
    "delta": (1,4),
    "theta": (4,8),
    "alpha": (8,13),
    "beta":  (13,30),
    "gamma": (30,40)
}

FEATURE_NAMES = []

for ch in FRONTAL_CHANNELS:

    for band in BANDS:

        FEATURE_NAMES.append(
            f"{ch}_{band}"
        )

# ============================================================
# Relative Spectral Power
# ============================================================

def relative_band_power(signal, sfreq):

    freqs, psd = welch(
        signal,
        fs=sfreq,
        window="hann",
        nperseg=256,
        noverlap=128,
        scaling="density"
    )

    total_mask = (freqs >= 1) & (freqs <= 40)

    total_power = np.trapz(
        psd[total_mask],
        freqs[total_mask]
    )

    if total_power <= 0:
        total_power = 1e-12

    features = []

    for low, high in BANDS.values():

        mask = (freqs >= low) & (freqs < high)

        band_power = np.trapz(
            psd[mask],
            freqs[mask]
        )

        features.append(
            band_power / total_power
        )

    return features
    
    
    



# ============================================================
# One EEG Window
# ============================================================

def extract_window_features(window, sfreq):

    feature_vector = []

    frontal_window = window[SELECTED_INDEX]

    for signal in frontal_window:

        feature_vector.extend(
            relative_band_power(signal, sfreq)
        )

    return np.asarray(
        feature_vector,
        dtype=np.float32
    )
# ============================================================
# Metadata
# ============================================================

def parse_information(file):

    split = file.parts[-3]

    label = file.parts[-2]

    recording = file.stem

    return split, label, recording
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# ============================================================
# Dataset Processing
# ============================================================

def process_dataset(split_name):

    print("\n")
    print("=" * 60)
    print(split_name.upper())
    print("=" * 60)

    files = sorted(
        WINDOW_DIR.glob(f"{split_name}/**/*.npz")
    )

    print(f"Found recordings : {len(files)}")

    X = []
    y = []

    recordings = []
    window_ids = []
    labels = []

    failed = []

    for file in tqdm(files):

        try:

            split, label, recording = parse_information(file)

            data = np.load(
                file,
                allow_pickle=True
            )

            windows = data["windows"]
            sfreq = float(data["sfreq"])

            for i, window in enumerate(windows):

                features = extract_window_features(
                    window,
                    sfreq
                )

                X.append(features)

                if label.lower() == "mdd":
                    y.append(1)
                else:
                    y.append(0)

                recordings.append(recording)
                window_ids.append(i)
                labels.append(label)

        except Exception as e:

            failed.append({
                "file": str(file),
                "error": str(e)
            })

    X = np.asarray(
        X,
        dtype=np.float32
    )

    y = np.asarray(
        y,
        dtype=np.int32
    )

    np.savez_compressed(

        FEATURE_DIR / f"{split_name}_features.npz",

        X=X,

        y=y,

        recording=np.asarray(recordings),

        window=np.asarray(window_ids),

        label=np.asarray(labels),

        feature_names=np.asarray(FEATURE_NAMES)
    )

    summary = pd.DataFrame({

        "Split": [split_name],

        "Samples": [len(X)],

        "Features": [X.shape[1]],

        "Classes": [len(np.unique(y))]
    })

    summary.to_csv(

        RESULT_DIR / f"{split_name}_summary.csv",

        index=False
    )

    if len(failed):

        pd.DataFrame(failed).to_csv(

            RESULT_DIR / f"{split_name}_failed.csv",

            index=False
        )

    return {

        "split": split_name,

        "samples": len(X),

        "features": X.shape[1],

        "failed": len(failed)
    }
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# ============================================================
# Main
# ============================================================

def main():

    print("\n")
    print("=" * 60)
    print("NeuroScreenAI")
    print("Step 04 - Spectral Feature Extraction")
    print("Frontal Cortex (7 Channels)")
    print("=" * 60)

    train_result = process_dataset("train")
    test_result = process_dataset("test")

    report = pd.DataFrame([
        train_result,
        test_result
    ])

    report.to_csv(
        RESULT_DIR / "feature_summary.csv",
        index=False
    )

    print("\n")
    print("=" * 60)
    print("Finished")
    print("=" * 60)

    print(f"Train samples : {train_result['samples']}")
    print(f"Test samples  : {test_result['samples']}")
    print(f"Features      : {train_result['features']}")
    print(f"Failed files  : {train_result['failed'] + test_result['failed']}")

    print("\nFeature Vector")
    print("----------------------------")
    print(f"Channels        : {len(FRONTAL_CHANNELS)}")
    print(f"Bands           : {len(BANDS)}")
    print(f"Total Features  : {len(FEATURE_NAMES)}")

    print("\nChannels Used")
    print("----------------------------")
    print(", ".join(FRONTAL_CHANNELS))

    print("\nSaved Files")
    print("----------------------------")
    print(FEATURE_DIR / "train_features.npz")
    print(FEATURE_DIR / "test_features.npz")

    print("\nReports")
    print("----------------------------")
    print(RESULT_DIR)

    print("=" * 60)


if __name__ == "__main__":
    main()
