# ============================================================
# NeuroScreenAI
# Step 02 : EEG Preprocessing
# ============================================================

from pathlib import Path
import pandas as pd
import mne
import warnings

warnings.filterwarnings("ignore")

# ============================================================
# Configuration
# ============================================================

DATASET = "depression"

PROJECT_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_DIR / "data" / DATASET
RESULT_DIR = PROJECT_DIR / "results" / DATASET / "preprocessing"

TRAIN_DIR = DATA_DIR / "train"
TEST_DIR = DATA_DIR / "test"

PROCESSED_DIR = DATA_DIR / "processed"

RESULT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# EEG Parameters
# ============================================================

LOWCUT = 1.0
HIGHCUT = 40.0

NOTCH = 50

TARGET_SFREQ = None

# ============================================================
# Channel Standardization
# ============================================================

CHANNEL_MAP = {

    "FP1":"Fp1",
    "FP2":"Fp2",

    "FPZ":"Fpz",

    "FZ":"Fz",

    "CZ":"Cz",

    "PZ":"Pz",

    "OZ":"Oz",

}

# ============================================================
# Reports
# ============================================================

report = []

failed = []

# ============================================================
# Scan Files
# ============================================================

edf_files = sorted(TRAIN_DIR.rglob("*.edf"))
edf_files.extend(sorted(TEST_DIR.rglob("*.edf")))

print("="*60)
print("NeuroScreenAI - Step02")
print("="*60)
print("EDF files :",len(edf_files))
print()


from shutil import rmtree

if PROCESSED_DIR.exists():
    rmtree(PROCESSED_DIR)

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# Processing Loop
# ============================================================

for idx,edf in enumerate(edf_files,1):

    print(f"[{idx}/{len(edf_files)}] {edf.name}")

    try:

        raw = mne.io.read_raw_edf(
            edf,
            preload=True,
            verbose=False
        )

        # ----------------------------------------------------
        # Rename Channels
        # ----------------------------------------------------

        rename_dict = {}

        for ch in raw.ch_names:

            upper = ch.upper()

            if upper in CHANNEL_MAP:

                rename_dict[ch] = CHANNEL_MAP[upper]

        if len(rename_dict):

            raw.rename_channels(rename_dict)

        # ----------------------------------------------------
        # Keep EEG only
        # ----------------------------------------------------

        raw.pick("eeg")

        # ----------------------------------------------------
        # Montage
        # ----------------------------------------------------

        montage = mne.channels.make_standard_montage(
            "standard_1020"
        )

        raw.set_montage(
            montage,
            on_missing="ignore"
        )

        # ----------------------------------------------------
        # Resample
        # ----------------------------------------------------

        if TARGET_SFREQ is not None:

            raw.resample(TARGET_SFREQ)

        # ----------------------------------------------------
        # Bandpass
        # ----------------------------------------------------

        raw.filter(
            LOWCUT,
            HIGHCUT,
            verbose=False
        )

        # ----------------------------------------------------
        # Notch
        # ----------------------------------------------------

        raw.notch_filter(
            NOTCH,
            verbose=False
        )

        # ----------------------------------------------------
        # Average Reference
        # ----------------------------------------------------

        raw.set_eeg_reference(
            "average",
            verbose=False
        )

        # ----------------------------------------------------
        # Output Folder
        # ----------------------------------------------------

        relative = edf.relative_to(DATA_DIR)

        out = PROCESSED_DIR / relative

        out = out.with_suffix(".fif")

        out.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        raw.save(
            out,
            overwrite=True,
            verbose=False
        )

        duration = raw.times[-1]

        report.append({

            "file":edf.name,

            "split":relative.parts[0],

            "class":relative.parts[1],

            "channels":len(raw.ch_names),

            "sampling_rate":raw.info["sfreq"],

            "duration_sec":round(duration,2),

            "bad_channels":",".join(raw.info["bads"]),

            "output":str(out)

        })

    except Exception as e:

        print("FAILED")

        failed.append({

            "file":edf.name,

            "error":str(e)

        })

# ============================================================
# Save Reports
# ============================================================

pd.DataFrame(report).to_csv(

    RESULT_DIR/"preprocessing_report.csv",

    index=False

)

pd.DataFrame(failed).to_csv(

    RESULT_DIR/"failed_files.csv",

    index=False

)

# ============================================================
# Finish
# ============================================================

print()
print("="*60)

print("Finished")

print("Successful :",len(report))

print("Failed     :",len(failed))

print()

print("Reports")

print(RESULT_DIR)

print("="*60)














