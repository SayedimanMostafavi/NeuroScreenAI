from pathlib import Path

import joblib
import numpy as np

from common.resource_path import resource_path

from desktop.controllers.analysis_controller import AnalysisController
from research.common.preprocessing import EEGPreprocessor
from research.common.windowing import WindowGenerator
from research.common.features import FeatureExtractor


EDF = Path(
    resource_path(
        "data/depression/raw/edf/H S16 EO.edf"
    )
)

controller = AnalysisController()

result = controller.analyze(EDF)

print("\nDesktop Prediction")
print(result)

pre = EEGPreprocessor()

win = WindowGenerator()

ext = FeatureExtractor()

raw = pre.run(EDF)

windows = win.generate(raw)

print("\nWindows:", windows.shape)

features = np.asarray(
    [ext.extract(w) for w in windows],
    dtype=np.float32,
)

print("Raw features :", features.shape)

scaler = joblib.load(
    resource_path(
        "research/models/scaler.pkl"
    )
)

selector = joblib.load(
    resource_path(
        "research/models/feature_selector.pkl"
    )
)

features = scaler.transform(features)

features = selector.transform(features)

print("Selected features :", features.shape)

subject = np.concatenate([
    features.mean(0),
    features.std(0),
    np.median(features, 0),
    features.min(0),
    features.max(0),
])

print("Subject vector :", subject.shape)
