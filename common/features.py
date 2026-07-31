"""
============================================================
NeuroScreenAI
Common Feature Extraction
============================================================

Reusable feature extraction module.

Used by:
    - Step 04 (training)
    - Web application
"""

import numpy as np
from scipy.signal import welch

# ============================================================
# Frontal Channels
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

# ============================================================
# Frequency Bands
# ============================================================

BANDS = {
    "delta": (1, 4),
    "theta": (4, 8),
    "alpha": (8, 13),
    "beta": (13, 30),
    "gamma": (30, 40)
}

# ============================================================
# Feature Names
# ============================================================

FEATURE_NAMES = []

for ch in FRONTAL_CHANNELS:
    for band in BANDS:
        FEATURE_NAMES.append(f"{ch}_{band}")

# ============================================================
# Relative Band Power
# ============================================================

def relative_band_power(signal, sfreq):
    """
    Compute relative band powers.
    """

    nperseg = min(256, len(signal))
    noverlap = nperseg // 2

    freqs, psd = welch(
        signal,
        fs=sfreq,
        window="hann",
        nperseg=nperseg,
        noverlap=noverlap,
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

    return np.asarray(features, dtype=np.float32)

# ============================================================
# Channel Mapping
# ============================================================

def build_channel_index(channel_names):
    """
    Create channel -> index dictionary.
    """

    normalized = []

    for ch in channel_names:

        name = ch.strip()

        if name.startswith("EEG "):
            name = name[4:]

        if name.endswith("-LE"):
            name = name[:-3]

        name = name.upper()

        mapping = {
            "FP1": "Fp1",
            "FP2": "Fp2",
            "F7": "F7",
            "F3": "F3",
            "FZ": "Fz",
            "F4": "F4",
            "F8": "F8",
            "T3": "T7",
            "T4": "T8",
            "T5": "P7",
            "T6": "P8",
            "C3": "C3",
            "CZ": "Cz",
            "C4": "C4",
            "P3": "P3",
            "PZ": "Pz",
            "P4": "P4",
            "O1": "O1",
            "O2": "O2"
        }

        normalized.append(
            mapping.get(name, name)
        )

    return {
        ch: i
        for i, ch in enumerate(normalized)
    }

# ============================================================
# One Window
# ============================================================

def extract_window_features(
    window,
    sfreq,
    channel_names
):
    """
    Extract one 35-dimensional feature vector.
    """

    channel_index = build_channel_index(channel_names)

    feature_vector = []

    for ch in FRONTAL_CHANNELS:

        if ch not in channel_index:
            raise ValueError(
                f"Missing channel: {ch}"
            )

        signal = window[
            channel_index[ch]
        ]

        feature_vector.extend(
            relative_band_power(
                signal,
                sfreq
            )
        )

    return np.asarray(
        feature_vector,
        dtype=np.float32
    )

# ============================================================
# Multiple Windows
# ============================================================

def extract_features_from_windows(
    windows,
    sfreq,
    channel_names
):
    """
    Parameters
    ----------
    windows :
        (n_windows, n_channels, samples)

    Returns
    -------
    ndarray
        (n_windows,35)
    """

    X = np.empty(
        (
            len(windows),
            len(FEATURE_NAMES)
        ),
        dtype=np.float32
    )

    for i, window in enumerate(windows):

        X[i] = extract_window_features(
            window,
            sfreq,
            channel_names
        )

    return X

# ============================================================
# One Recording
# ============================================================

def extract_recording_features(
    raw,
    create_windows_function
):
    """
    Convenience function.
    """

    windows, sfreq, channels, _ = create_windows_function(raw)

    return extract_features_from_windows(
        windows,
        sfreq,
        channels
    )

# ============================================================
# Utilities
# ============================================================

def get_feature_names():
    return FEATURE_NAMES.copy()


def number_of_features():
    return len(FEATURE_NAMES)
