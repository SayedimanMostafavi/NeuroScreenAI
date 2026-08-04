import warnings
warnings.filterwarnings("ignore")

import time
import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_validate

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import mutual_info_classif

from sklearn.preprocessing import StandardScaler

from sklearn.pipeline import Pipeline

from sklearn.metrics import make_scorer
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.svm import SVC

from config import RESULTS_DIR
from config import MODELS_DIR

try:
    from xgboost import XGBClassifier
    HAS_XGB = True
except:
    HAS_XGB = False

try:
    from catboost import CatBoostClassifier
    HAS_CAT = True
except:
    HAS_CAT = False

data = np.load(
    RESULTS_DIR / "eo_subject_features.npz",
    allow_pickle=True,
)

X = data["X"]
y = data["y"]

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42,
)

scoring = {
    "accuracy": make_scorer(accuracy_score),
    "precision": make_scorer(precision_score),
    "recall": make_scorer(recall_score),
    "f1": make_scorer(f1_score),
}

models = {
    "RandomForest": RandomForestClassifier(
        n_estimators=500,
        random_state=42,
        n_jobs=-1,
    ),
    "ExtraTrees": ExtraTreesClassifier(
        n_estimators=500,
        random_state=42,
        n_jobs=-1,
    ),
    "SVM": SVC(
        kernel="rbf",
        probability=True,
    ),
}

if HAS_XGB:
    models["XGBoost"] = XGBClassifier(
        n_estimators=500,
        learning_rate=0.05,
        eval_metric="logloss",
        random_state=42,
    )

if HAS_CAT:
    models["CatBoost"] = CatBoostClassifier(
        iterations=500,
        learning_rate=0.05,
        verbose=False,
        random_seed=42,
    )

results = []

best_score = 0
best_pipeline = None

for name, model in models.items():

    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)

    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("selector", SelectKBest(
            mutual_info_classif,
            k=150,
        )),
        ("model", model),
    ])

    start = time.time()

    scores = cross_validate(
        pipe,
        X,
        y,
        cv=cv,
        scoring=scoring,
        n_jobs=-1,
    )

    acc = scores["test_accuracy"].mean()
    pre = scores["test_precision"].mean()
    rec = scores["test_recall"].mean()
    f1 = scores["test_f1"].mean()

    print(f"Accuracy : {acc:.4f}")
    print(f"Precision: {pre:.4f}")
    print(f"Recall   : {rec:.4f}")
    print(f"F1       : {f1:.4f}")

    results.append({
        "Model": name,
        "Accuracy": acc,
        "Precision": pre,
        "Recall": rec,
        "F1": f1,
    })

    if acc > best_score:
        best_score = acc
        best_pipeline = pipe

print("\nTraining best model...")

best_pipeline.fit(X, y)

MODELS_DIR.mkdir(exist_ok=True)

joblib.dump(
    best_pipeline,
    MODELS_DIR / "best_subject_model.pkl",
)

df = pd.DataFrame(results)

df.sort_values(
    "Accuracy",
    ascending=False,
    inplace=True,
)

print(df)

df.to_csv(
    RESULTS_DIR / "subject_model_results.csv",
    index=False,
)

print("\nSaved best_subject_model.pkl")
