#!/usr/bin/env python3
"""
============================================================
NeuroScreenAI
Step 05 - Random Forest Classifier
============================================================
"""

from pathlib import Path
from shutil import rmtree
import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier

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

FEATURE_DIR = (
    PROJECT_DIR /
    "data" /
    "depression" /
    "features"
)

MODEL_DIR = (
    PROJECT_DIR /
    "models" /
    "depression"
)

RESULT_DIR = (
    PROJECT_DIR /
    "results" /
    "depression" /
    "classification"
)

if MODEL_DIR.exists():
    rmtree(MODEL_DIR)

MODEL_DIR.mkdir(parents=True, exist_ok=True)
RESULT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# Load Features
# ============================================================

print("\nLoading Features...")

train = np.load(
    FEATURE_DIR / "train_features.npz",
    allow_pickle=True
)

test = np.load(
    FEATURE_DIR / "test_features.npz",
    allow_pickle=True
)

X_train = train["X"]
y_train = train["y"]

X_test = test["X"]
y_test = test["y"]

feature_names = train["feature_names"]

print("Train :", X_train.shape)
print("Test  :", X_test.shape)

# ============================================================
# Random Forest
# ============================================================

print("\nTraining Random Forest...")

model = RandomForestClassifier(

    n_estimators=300,

    max_depth=None,

    min_samples_split=2,

    min_samples_leaf=1,

    random_state=42,

    n_jobs=-1
)

model.fit(
    X_train,
    y_train
)

print("Training Finished")

# ============================================================
# Prediction
# ============================================================

print("\nPredicting...")

y_pred = model.predict(X_test)

y_prob = model.predict_proba(X_test)[:,1]


















# ============================================================
# Evaluation
# ============================================================

print("\nEvaluating...")

accuracy = accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred
)

recall = recall_score(
    y_test,
    y_pred
)

f1 = f1_score(
    y_test,
    y_pred
)

auc = roc_auc_score(
    y_test,
    y_prob
)

cm = confusion_matrix(
    y_test,
    y_pred
)

print("\n")
print("=" * 60)
print("Performance")
print("=" * 60)

print(f"Accuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")
print(f"ROC AUC   : {auc:.4f}")

print("\nConfusion Matrix")
print(cm)

report = classification_report(
    y_test,
    y_pred,
    target_names=[
        "Healthy",
        "Depression"
    ],
    output_dict=True
)

pd.DataFrame(report).transpose().to_csv(
    RESULT_DIR / "classification_report.csv"
)

metrics = pd.DataFrame({

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

})

metrics.to_csv(
    RESULT_DIR / "metrics.csv",
    index=False
)

pd.DataFrame(
    cm,
    index=["Healthy","Depression"],
    columns=["Healthy","Depression"]
).to_csv(
    RESULT_DIR / "confusion_matrix.csv"
)

# ============================================================
# Feature Importance
# ============================================================

importance = pd.DataFrame({

    "Feature": feature_names,

    "Importance": model.feature_importances_

})

importance = importance.sort_values(
    "Importance",
    ascending=False
)

importance.to_csv(
    RESULT_DIR / "feature_importance.csv",
    index=False
)

print("\nTop 10 Features\n")
print(
    importance.head(10)
)
















# ============================================================
# Save Model
# ============================================================

joblib.dump(
    model,
    MODEL_DIR / "random_forest.pkl"
)

print("\nModel Saved")
print(MODEL_DIR / "random_forest.pkl")

# ============================================================
# Prediction Results
# ============================================================

results = pd.DataFrame({

    "True_Label": y_test,

    "Predicted_Label": y_pred,

    "Probability_Depression": y_prob

})

results.to_csv(

    RESULT_DIR / "predictions.csv",

    index=False
)

# ============================================================
# Finished
# ============================================================

print("\n")
print("=" * 60)
print("Finished")
print("=" * 60)

print(f"Train Samples : {len(X_train)}")
print(f"Test Samples  : {len(X_test)}")
print(f"Features      : {X_train.shape[1]}")

print("\nPerformance")
print("----------------------------")
print(f"Accuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")
print(f"ROC AUC   : {auc:.4f}")

print("\nOutputs")
print("----------------------------")
print("Model")
print(MODEL_DIR / "random_forest.pkl")

print("\nReports")
print(RESULT_DIR / "metrics.csv")
print(RESULT_DIR / "classification_report.csv")
print(RESULT_DIR / "confusion_matrix.csv")
print(RESULT_DIR / "feature_importance.csv")
print(RESULT_DIR / "predictions.csv")

print("=" * 60)
