#!/usr/bin/env python3
"""
============================================================
NeuroScreenAI
Step 06 - Recording Level Evaluation
============================================================
"""

from pathlib import Path

import numpy as np
import pandas as pd
import joblib

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

# ============================================================
# Paths
# ============================================================

PROJECT_DIR = Path("/home/iman/Downloads/Project/NeuroScreenAI")

FEATURE_FILE = (
    PROJECT_DIR /
    "data" /
    "depression" /
    "features" /
    "test_features.npz"
)

MODEL_FILE = (
    PROJECT_DIR /
    "models" /
    "depression" /
    "random_forest.pkl"
)

RESULT_DIR = (
    PROJECT_DIR /
    "results" /
    "depression" /
    "recording_evaluation"
)

RESULT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# Load
# ============================================================

print("\nLoading...")

data = np.load(
    FEATURE_FILE,
    allow_pickle=True
)

X = data["X"]
y = data["y"]

recordings = data["recording"]

model = joblib.load(MODEL_FILE)

print("Samples :", len(X))
print("Recordings :", len(np.unique(recordings)))

print("\nPredicting...")

window_probability = model.predict_proba(X)[:,1]
window_prediction = model.predict(X)





# ============================================================
# Recording Aggregation
# ============================================================

print("\nAggregating Recordings...")

rows = []

for rec in np.unique(recordings):

    idx = np.where(recordings == rec)[0]

    true_label = y[idx][0]

    mean_probability = np.mean(
        window_probability[idx]
    )

    prediction = int(
        mean_probability >= 0.5
    )

    rows.append({

        "Recording": rec,

        "True": true_label,

        "Prediction": prediction,

        "Probability": mean_probability,

        "Windows": len(idx)

    })

results = pd.DataFrame(rows)

results.to_csv(
    RESULT_DIR / "recording_predictions.csv",
    index=False
)

y_true = results["True"].values
y_pred = results["Prediction"].values
y_prob = results["Probability"].values

accuracy = accuracy_score(
    y_true,
    y_pred
)

precision = precision_score(
    y_true,
    y_pred
)

recall = recall_score(
    y_true,
    y_pred
)

f1 = f1_score(
    y_true,
    y_pred
)

auc = roc_auc_score(
    y_true,
    y_prob
)

cm = confusion_matrix(
    y_true,
    y_pred
)

print("\n")
print("=" * 60)
print("Recording Level Performance")
print("=" * 60)

print(f"Accuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")
print(f"ROC AUC   : {auc:.4f}")

print("\nConfusion Matrix")
print(cm)

pd.DataFrame(
    cm,
    index=["Healthy","Depression"],
    columns=["Healthy","Depression"]
).to_csv(
    RESULT_DIR / "confusion_matrix.csv"
)

pd.DataFrame(
    {
        "Metric":[
            "Accuracy",
            "Precision",
            "Recall",
            "F1",
            "ROC_AUC"
        ],
        "Value":[
            accuracy,
            precision,
            recall,
            f1,
            auc
        ]
    }
).to_csv(
    RESULT_DIR / "metrics.csv",
    index=False
)

pd.DataFrame(
    classification_report(
        y_true,
        y_pred,
        target_names=["Healthy","Depression"],
        output_dict=True
    )
).transpose().to_csv(
    RESULT_DIR / "classification_report.csv"
)





# ============================================================
# Finished
# ============================================================

print("\n")
print("=" * 60)
print("Finished")
print("=" * 60)

print(f"Recordings : {len(results)}")

print("\nPerformance")
print("----------------------------")
print(f"Accuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")
print(f"ROC AUC   : {auc:.4f}")

print("\nOutputs")
print("----------------------------")
print(RESULT_DIR / "recording_predictions.csv")
print(RESULT_DIR / "metrics.csv")
print(RESULT_DIR / "classification_report.csv")
print(RESULT_DIR / "confusion_matrix.csv")

print("=" * 60)

if __name__ == "__main__":
    pass
