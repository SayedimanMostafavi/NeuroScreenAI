from pathlib import Path
import sys
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from desktop.controllers.analysis_controller import AnalysisController

# -------------------------------------------------------
# CHANGE THIS TO YOUR TEST DATASET
# -------------------------------------------------------

TEST_DIR = Path(
    "/home/iman/Downloads/Project/NeuroScreenAI/data/depression/test"
)

controller = AnalysisController()

rows = []

edf_files = sorted(TEST_DIR.rglob("*.edf"))

print(f"\nFound {len(edf_files)} EDF files\n")

for i, edf in enumerate(edf_files, 1):

    print(f"[{i}/{len(edf_files)}] {edf.name}")

    try:

        result = controller.analyze(edf)

        folder = edf.parent.name.lower()

        if folder in ["control", "healthy", "hc"]:
            true_label = 0
        else:
            true_label = 1

        rows.append({

            "file": edf.name,

            "true": true_label,

            "pred": result.prediction,

            "probability": result.probability

        })

    except Exception as e:

        print(e)

df = pd.DataFrame(rows)

print("\n====================================")
print("Dataset")
print("====================================")
print(df.head())

y_true = df.true.values
y_pred = df.pred.values

print("\n====================================")
print("Metrics")
print("====================================")

print("Accuracy :", accuracy_score(y_true, y_pred))
print("Precision:", precision_score(y_true, y_pred))
print("Recall   :", recall_score(y_true, y_pred))
print("F1 Score :", f1_score(y_true, y_pred))

print("\n====================================")
print("Confusion Matrix")
print("====================================")

print(confusion_matrix(y_true, y_pred))

print("\n====================================")
print("Classification Report")
print("====================================")

print(classification_report(y_true, y_pred))

output = PROJECT_ROOT / "results" / "desktop_validation.csv"

output.parent.mkdir(exist_ok=True)

df.to_csv(output, index=False)

print("\nSaved to:")
print(output)
