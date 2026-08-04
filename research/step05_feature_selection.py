import joblib
import numpy as np

from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import mutual_info_classif
from sklearn.preprocessing import StandardScaler

from config import RESULTS_DIR, MODELS_DIR

MODELS_DIR.mkdir(exist_ok=True)

print("Loading features...")

data = np.load(
    RESULTS_DIR / "eo_features.npz",
    allow_pickle=True,
)

X = data["X"]
y = data["y"]
subjects = data["subjects"]
recordings = data["recordings"]

print("Original shape:", X.shape)

############################################################
# Standardization
############################################################

scaler = StandardScaler()

X = scaler.fit_transform(X)

joblib.dump(
    scaler,
    MODELS_DIR / "scaler.pkl",
)

############################################################
# Remove constant features
############################################################

vt = VarianceThreshold()

X = vt.fit_transform(X)

print("After variance filter:", X.shape)

############################################################
# Mutual Information
############################################################

selector = SelectKBest(

    score_func=mutual_info_classif,

    k=100,

)

X = selector.fit_transform(

    X,

    y,

)

indices = selector.get_support(indices=True)

joblib.dump(

    selector,

    MODELS_DIR / "feature_selector.pkl",

)

joblib.dump(

    indices,

    MODELS_DIR / "selected_features.pkl",

)

print()

print("=" * 60)

print("FINAL FEATURE MATRIX")

print("=" * 60)

print(X.shape)

np.savez_compressed(

    RESULTS_DIR / "eo_features_selected.npz",

    X=X,

    y=y,

    subjects=subjects,

    recordings=recordings,

)

print()

print("Saved.")

print(RESULTS_DIR / "eo_features_selected.npz")
