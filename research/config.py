from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_DIR / "data" / "depression" / "raw" / "edf"

RESULTS_DIR = PROJECT_DIR / "research" / "results"

MODELS_DIR = PROJECT_DIR / "research" / "models"

RANDOM_STATE = 42

TEST_SIZE = 0.20

VALID_SIZE = 0.20

WINDOW_SEC = 4

OVERLAP = 0.50

FS = 256

LOWCUT = 1

HIGHCUT = 40

NOTCH = 50

BANDS = {
    "delta": (1,4),
    "theta": (4,8),
    "alpha": (8,13),
    "beta": (13,30),
    "gamma": (30,40),
}
