from dataclasses import dataclass
from typing import List


@dataclass
class AnalysisResult:

    prediction: int

    diagnosis: str

    probability: float

    windows: int

    channels: int

    sampling_rate: float

    duration: float

    elapsed_time: float

    channel_names: List[str]

    file_name: str
