import warnings
warnings.filterwarnings("ignore")

import time
import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier

from sklearn.svm import SVC

from sklearn.model_selection import GroupKFold
from sklearn.model_selection import cross_validate

from sklearn.metrics import make_scorer
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score

from config import RESULTS_DIR
from config import MODELS_DIR

try:
    from xgboost import XGBClassifier
    HAS_XGB = True
except:
    HAS_XGB = False

try:
    from lightgbm import LGBMClassifier
    HAS_LGBM = True
except:
    HAS_LGBM = False

try:
    from catboost import CatBoostClassifier
    HAS_CAT = True
except:
    HAS_CAT = False


print("="*70)
print("Loading dataset")
print("="*70)

data = np.load(
    RESULTS_DIR/"eo_features_selected.npz",
    allow_pickle=True,
)

X = data["X"]
y = data["y"]
subjects = data["subjects"]

groups = subjects

cv = GroupKFold(
    n_splits=5
)

scoring = {

    "accuracy":
        make_scorer(accuracy_score),

    "precision":
        make_scorer(precision_score),

    "recall":
        make_scorer(recall_score),

    "f1":
        make_scorer(f1_score),

}

models = {

    "RandomForest":

        RandomForestClassifier(

            n_estimators=500,

            random_state=42,

            n_jobs=-1,

        ),

    "ExtraTrees":

        ExtraTreesClassifier(

            n_estimators=500,

            random_state=42,

            n_jobs=-1,

        ),

    "SVM":

        SVC(

            kernel="rbf",

            probability=True,

            C=1,

            gamma="scale",

        ),

}

if HAS_XGB:

    models["XGBoost"] = XGBClassifier(

        n_estimators=500,

        learning_rate=0.05,

        max_depth=6,

        subsample=0.8,

        colsample_bytree=0.8,

        eval_metric="logloss",

        random_state=42,

    )

if HAS_LGBM:

    models["LightGBM"] = LGBMClassifier(

        n_estimators=500,

        learning_rate=0.05,

        random_state=42,

    )

if HAS_CAT:

    models["CatBoost"] = CatBoostClassifier(

        iterations=500,

        learning_rate=0.05,

        depth=6,

        random_seed=42,

        verbose=False,

    )

results = []

best_model = None

best_score = 0

for name, model in models.items():

    print()

    print("="*70)
    print(name)
    print("="*70)

    start = time.time()

    scores = cross_validate(

        model,

        X,

        y,

        cv=cv,

        groups=groups,

        scoring=scoring,

        n_jobs=-1,

    )

    acc = scores["test_accuracy"].mean()

    pre = scores["test_precision"].mean()

    rec = scores["test_recall"].mean()

    f1 = scores["test_f1"].mean()

    elapsed = time.time() - start

    print(f"Accuracy : {acc:.4f}")
    print(f"Precision: {pre:.4f}")
    print(f"Recall   : {rec:.4f}")
    print(f"F1 Score : {f1:.4f}")
    print(f"Time     : {elapsed:.1f} sec")

    results.append({

        "Model":name,

        "Accuracy":acc,

        "Precision":pre,

        "Recall":rec,

        "F1":f1,

        "Time":elapsed,

    })

    if acc > best_score:

        best_score = acc

        best_model = model

print()

print("="*70)
print("Training Best Model")
print("="*70)

best_model.fit(

    X,

    y,

)

MODELS_DIR.mkdir(exist_ok=True)

joblib.dump(

    best_model,

    MODELS_DIR/"best_model.pkl",

)

df = pd.DataFrame(results)

df = df.sort_values(

    "Accuracy",

    ascending=False,

)

df.to_csv(

    RESULTS_DIR/"model_comparison.csv",

    index=False,

)

print()

print(df)

print()

print("Best model saved.")
