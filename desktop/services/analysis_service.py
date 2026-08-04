from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import joblib
import numpy as np

from common.resource_path import resource_path

from research.common.preprocessing import EEGPreprocessor
from research.common.windowing import WindowGenerator
from research.common.features import FeatureExtractor

from desktop.models.analysis_result import AnalysisResult


class AnalysisService:

    def __init__(self):

        self.preprocessor = EEGPreprocessor()

        self.window_generator = WindowGenerator()

        self.extractor = FeatureExtractor()

        self.selector = joblib.load(

            resource_path(
                "assets/models/feature_selector.pkl"
            )

        )

        self.scaler = joblib.load(

            resource_path(
                "assets/models/scaler.pkl"
            )

        )

        self.model = joblib.load(

            resource_path(
                "assets/models/best_subject_model.pkl"
            )

        )

    def analyze(self, edf_path):

        raw = self.preprocessor.run(edf_path)

        windows = self.window_generator.generate(raw)

        features = []

        for window in windows:

            features.append(

                self.extractor.extract(window)

            )

        features = np.asarray(

            features,

            dtype=np.float32,

        )

        features = self.scaler.transform(

            features

        )

        features = self.selector.transform(

            features

        )

        subject = np.concatenate([

            features.mean(axis=0),

            features.std(axis=0),

            np.median(features, axis=0),

            features.min(axis=0),

            features.max(axis=0),

        ])

        probability = self.model.predict_proba(

            subject.reshape(1, -1)

        )[0][1]

        prediction = int(

            probability >= 0.5

        )

        diagnosis = (

            "Depression"

            if prediction

            else

            "Healthy"

        )

        return AnalysisResult(

            prediction=prediction,

            diagnosis=diagnosis,

            probability=float(probability),

            windows=len(windows),

            channels=len(raw.ch_names),

            sampling_rate=float(raw.info["sfreq"]),

            duration=int(raw.times[-1]),

            elapsed_time=0,

            channel_names=raw.ch_names,

            file_name=Path(edf_path).name,

        )
