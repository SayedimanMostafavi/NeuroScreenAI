"""
============================================================
NeuroScreenAI
Common Inference Pipeline
============================================================

Shared prediction pipeline.

Used by:
    - FastAPI Web Application
    - Desktop GUI (future)
    - Batch Prediction (future)

Pipeline

Raw EDF
    │
    ▼
preprocess_raw()
    │
    ▼
create_windows()
    │
    ▼
extract_features_from_windows()
    │
    ▼
Random Forest
"""

import joblib
import numpy as np
import mne

from common.preprocessing import preprocess_raw
from common.windowing import create_windows
from common.features import extract_features_from_windows


class EEGPredictor:

    def __init__(self, model_path):

        self.model = joblib.load(model_path)

    # =====================================================
    # Predict from Raw object
    # =====================================================

    def predict_raw(self, raw):

        # -----------------------------
        # Step 1
        # -----------------------------

        raw = preprocess_raw(raw)

        # -----------------------------
        # Step 2
        # -----------------------------

        windows, sfreq, channels, starts = create_windows(raw)

        if len(windows) == 0:
            raise ValueError(
                "No EEG windows generated."
            )

        # -----------------------------
        # Step 3
        # -----------------------------

        X = extract_features_from_windows(
            windows,
            sfreq,
            channels
        )
        print("=" * 60)
        print("Feature Matrix")
        print("=" * 60)
        print("Shape:", X.shape)
        print("Mean :", X.mean())
        print("Std  :", X.std())
        print("Min  :", X.min())
        print("Max  :", X.max())
        print("First feature vector:")
        print(X[0])
        print("=" * 60)

        # -----------------------------
        # Step 4
        # -----------------------------

        probabilities = self.model.predict_proba(X)

        depression_probability = probabilities[:, 1]

        mean_probability = float(
            np.mean(depression_probability)
        )

        prediction = int(
            mean_probability >= 0.5
        )

        return {

            "prediction": prediction,

            "probability": mean_probability,

            "windows": len(windows),

            "channels": channels,

            "sampling_rate": sfreq,

            "window_probabilities": depression_probability

        }

    # =====================================================
    # Predict from EDF
    # =====================================================

    def predict_edf(self, edf_file):

        raw = mne.io.read_raw_edf(

            edf_file,

            preload=True,

            verbose=False

        )

        return self.predict_raw(raw)

    # =====================================================
    # Predict from FIF
    # =====================================================

    def predict_fif(self, fif_file):

        raw = mne.io.read_raw_fif(

            fif_file,

            preload=True,

            verbose=False

        )

        return self.predict_raw(raw)
