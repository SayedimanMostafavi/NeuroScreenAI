# ============================================================
# NeuroScreenAI
# Step 03 : Window Segmentation
# ============================================================

from pathlib import Path
from shutil import rmtree
import numpy as np
import pandas as pd
import mne

# ============================================================
# Configuration
# ============================================================

DATASET = "depression"

PROJECT_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_DIR / "data" / DATASET

PROCESSED_DIR = DATA_DIR / "processed"

WINDOW_DIR = DATA_DIR / "windows"

RESULT_DIR = PROJECT_DIR / "results" / DATASET / "windowing"

# ============================================================
# Clean previous windows
# ============================================================

if WINDOW_DIR.exists():
    rmtree(WINDOW_DIR)

WINDOW_DIR.mkdir(parents=True, exist_ok=True)

RESULT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# Window parameters
# ============================================================

WINDOW_SEC = 4

OVERLAP = 0.50

# ============================================================
# Scan files
# ============================================================

fif_files = sorted(PROCESSED_DIR.rglob("*.fif"))

print("=" * 60)
print("NeuroScreenAI - Step03")
print("=" * 60)
print("Processed files :", len(fif_files))
print()

# ============================================================
# Reports
# ============================================================

summary = []

failed = []

total_windows = 0

# ============================================================
# Processing
# ============================================================

for idx, file in enumerate(fif_files, 1):

    print(f"[{idx}/{len(fif_files)}] {file.name}")

    try:

        raw = mne.io.read_raw_fif(
            file,
            preload=False,
            verbose=False
        )

        sfreq = raw.info["sfreq"]

        win_samples = int(WINDOW_SEC * sfreq)

        step = int(win_samples * (1 - OVERLAP))

        data = raw.get_data()

        n_channels = data.shape[0]

        n_samples = data.shape[1]

        windows = []

        starts = []

        for start in range(0, n_samples - win_samples + 1, step):

            stop = start + win_samples

            windows.append(
                data[:, start:stop]
            )

            starts.append(start)

        windows = np.asarray(windows)

        relative = file.relative_to(PROCESSED_DIR)

        out = WINDOW_DIR / relative.parent

        out.mkdir(
            parents=True,
            exist_ok=True
        )

        out_file = out / (file.stem + ".npz")

        np.savez_compressed(

            out_file,

            windows=windows,

            sfreq=sfreq,

            channels=np.array(raw.ch_names),

            starts=np.array(starts)

        )

        total_windows += len(windows)

        summary.append({

            "file": file.name,

            "split": relative.parts[0],

            "class": relative.parts[1],

            "channels": n_channels,

            "sampling_rate": sfreq,

            "samples": n_samples,

            "window_seconds": WINDOW_SEC,

            "overlap": OVERLAP,

            "window_samples": win_samples,

            "number_of_windows": len(windows)

        })

    except Exception as e:

        failed.append({

            "file": file.name,

            "error": str(e)

        })

# ============================================================
# Save reports
# ============================================================

summary_df = pd.DataFrame(summary)

summary_df.to_csv(

    RESULT_DIR / "window_summary.csv",

    index=False

)

failed_df = pd.DataFrame(failed)

failed_df.to_csv(

    RESULT_DIR / "failed_files.csv",

    index=False

)

# ============================================================
# Finish
# ============================================================

print()

print("=" * 60)

print("Finished")

print("Processed recordings :", len(summary))

print("Generated windows    :", total_windows)

print("Failed recordings    :", len(failed))

print()

print("Reports")

print(RESULT_DIR)

print("=" * 60)
