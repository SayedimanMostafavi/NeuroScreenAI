"""
============================================================
NeuroScreenAI
Common EEG Windowing
============================================================

Reusable window segmentation module.

Used by:
    - Step 03 (training)
    - Web application
    - Future EEG models

Input
-----
mne.io.Raw

Output
------
windows : ndarray
    Shape = (n_windows, n_channels, window_samples)

sfreq : float

channels : list[str]

starts : ndarray
"""

import numpy as np

# ============================================================
# Default Parameters
# ============================================================

DEFAULT_WINDOW_SEC = 4.0
DEFAULT_OVERLAP = 0.50


# ============================================================
# Compute Window Parameters
# ============================================================

def compute_window_parameters(
    sfreq,
    window_sec=DEFAULT_WINDOW_SEC,
    overlap=DEFAULT_OVERLAP
):
    """
    Compute window and step sizes.

    Returns
    -------
    window_samples
    step_samples
    """

    window_samples = int(window_sec * sfreq)

    step_samples = int(
        window_samples * (1.0 - overlap)
    )

    if step_samples <= 0:
        raise ValueError("Overlap is too large.")

    return window_samples, step_samples


# ============================================================
# Generate Window Start Indices
# ============================================================

def generate_start_indices(
    n_samples,
    window_samples,
    step_samples
):
    """
    Compute all valid window start indices.
    """

    return np.arange(
        0,
        n_samples - window_samples + 1,
        step_samples,
        dtype=np.int32
    )


# ============================================================
# Window Extraction
# ============================================================

def create_windows(
    raw,
    window_sec=DEFAULT_WINDOW_SEC,
    overlap=DEFAULT_OVERLAP
):
    """
    Segment an EEG recording into overlapping windows.

    Parameters
    ----------
    raw : mne.io.Raw

    window_sec : float

    overlap : float
        Between 0 and 1.

    Returns
    -------
    windows
    sfreq
    channels
    starts
    """

    sfreq = float(raw.info["sfreq"])

    data = raw.get_data()

    n_channels, n_samples = data.shape

    window_samples, step_samples = \
        compute_window_parameters(
            sfreq,
            window_sec,
            overlap
        )

    starts = generate_start_indices(
        n_samples,
        window_samples,
        step_samples
    )

    windows = np.empty(
        (
            len(starts),
            n_channels,
            window_samples
        ),
        dtype=np.float32
    )

    for i, start in enumerate(starts):

        stop = start + window_samples

        windows[i] = data[:, start:stop]

    return (
        windows,
        sfreq,
        list(raw.ch_names),
        starts
    )


# ============================================================
# Window Metadata
# ============================================================

def create_window_metadata(
    starts,
    sfreq,
    window_sec=DEFAULT_WINDOW_SEC
):
    """
    Convert sample indices into time values.

    Returns
    -------
    list of dictionaries
    """

    metadata = []

    for idx, start in enumerate(starts):

        metadata.append({

            "window": idx,

            "start_sample": int(start),

            "stop_sample": int(
                start + window_sec * sfreq
            ),

            "start_time": float(start / sfreq),

            "stop_time": float(
                (start / sfreq) + window_sec
            )

        })

    return metadata


# ============================================================
# Window Statistics
# ============================================================

def window_statistics(
    windows
):
    """
    Return basic statistics about a window set.
    """

    return {

        "n_windows": windows.shape[0],

        "n_channels": windows.shape[1],

        "window_samples": windows.shape[2]

    }


# ============================================================
# Validate Windows
# ============================================================

def validate_windows(
    windows
):
    """
    Basic sanity checks.
    """

    if windows.ndim != 3:
        raise ValueError(
            "Windows must be 3-dimensional."
        )

    if windows.shape[0] == 0:
        raise ValueError(
            "No windows generated."
        )

    if np.isnan(windows).any():
        raise ValueError(
            "NaN values detected."
        )

    return True
