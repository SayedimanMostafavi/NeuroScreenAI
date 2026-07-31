"""
============================================================
NeuroScreenAI
Common EEG Preprocessing
============================================================

Reusable preprocessing pipeline.

Used by:
    - Step 2 (training)
    - Web application
    - Future EEG models

Input:
    mne.io.Raw

Output:
    preprocessed mne.io.Raw
"""

import warnings
import mne

warnings.filterwarnings("ignore")

# ============================================================
# EEG Parameters
# ============================================================

LOWCUT = 1.0
HIGHCUT = 40.0

NOTCH_FREQ = 50.0

TARGET_SFREQ = None

# ============================================================
# Channel Name Mapping
# ============================================================

CHANNEL_MAP = {

    "EEG FP1-LE": "Fp1",
    "EEG FP2-LE": "Fp2",

    "EEG F7-LE": "F7",
    "EEG F3-LE": "F3",
    "EEG FZ-LE": "Fz",
    "EEG F4-LE": "F4",
    "EEG F8-LE": "F8",

    "EEG FC5-LE": "FC5",
    "EEG FC1-LE": "FC1",
    "EEG FC2-LE": "FC2",
    "EEG FC6-LE": "FC6",

    "EEG T7-LE": "T7",
    "EEG C3-LE": "C3",
    "EEG CZ-LE": "Cz",
    "EEG C4-LE": "C4",
    "EEG T8-LE": "T8",

    "EEG CP5-LE": "CP5",
    "EEG CP1-LE": "CP1",
    "EEG CP2-LE": "CP2",
    "EEG CP6-LE": "CP6",

    "EEG P7-LE": "P7",
    "EEG P3-LE": "P3",
    "EEG PZ-LE": "Pz",
    "EEG P4-LE": "P4",
    "EEG P8-LE": "P8",

    "EEG O1-LE": "O1",
    "EEG OZ-LE": "Oz",
    "EEG O2-LE": "O2",

    "EEG PO9-LE": "PO9",
    "EEG PO10-LE": "PO10",
    "EEG IZ-LE": "Iz",

    "EEG A2-A1": "A2-A1",

    # already-standard names
    "FP1": "Fp1",
    "FP2": "Fp2",
    "FPZ": "Fpz",

    "FZ": "Fz",
    "CZ": "Cz",
    "PZ": "Pz",
    "OZ": "Oz",
}

# ============================================================
# Standardize Channel Names
# ============================================================

def normalize_channel_names(raw):
    """
    Rename EEG channels to standard 10-20 names.
    """

    rename_dict = {}

    for ch in raw.ch_names:

        key = ch.strip().upper()

        if key in CHANNEL_MAP:
            rename_dict[ch] = CHANNEL_MAP[key]

    if rename_dict:
        raw.rename_channels(rename_dict)

    return raw


# ============================================================
# Keep EEG Channels
# ============================================================

def keep_eeg_only(raw):
    """
    Remove non-EEG channels.
    """

    raw.pick("eeg")

    return raw


# ============================================================
# Apply Standard Montage
# ============================================================

def apply_montage(raw):
    """
    Apply the international 10-20 montage.
    """

    montage = mne.channels.make_standard_montage(
        "standard_1020"
    )

    raw.set_montage(
        montage,
        on_missing="ignore"
    )

    return raw


# ============================================================
# Resample
# ============================================================

def resample(raw):

    if TARGET_SFREQ is not None:

        raw.resample(
            TARGET_SFREQ
        )

    return raw


# ============================================================
# Bandpass Filter
# ============================================================

def bandpass_filter(raw):

    raw.filter(
        LOWCUT,
        HIGHCUT,
        verbose=False
    )

    return raw


# ============================================================
# Notch Filter
# ============================================================

def notch_filter(raw):

    raw.notch_filter(
        NOTCH_FREQ,
        verbose=False
    )

    return raw


# ============================================================
# Average Reference
# ============================================================

def average_reference(raw):

    raw.set_eeg_reference(
        "average",
        verbose=False
    )

    return raw


# ============================================================
# Complete Pipeline
# ============================================================

def preprocess_raw(raw):
    """
    Complete preprocessing pipeline.

    Parameters
    ----------
    raw : mne.io.Raw

    Returns
    -------
    mne.io.Raw
    """

    raw = raw.copy()

    raw = normalize_channel_names(raw)

    raw = keep_eeg_only(raw)

    raw = apply_montage(raw)

    raw = resample(raw)

    raw = bandpass_filter(raw)

    raw = notch_filter(raw)

    raw = average_reference(raw)

    return raw
