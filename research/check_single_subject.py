import joblib
import numpy as np

from config import RESULTS_DIR, MODELS_DIR

data = np.load(
    RESULTS_DIR / "eo_subject_features.npz",
    allow_pickle=True,
)

subjects = data["subjects"]

print("=" * 70)
print("ALL SUBJECTS")
print("=" * 70)

for i, s in enumerate(subjects):
    print(f"{i:02d} : {repr(s)}")

print()
subject = input("Enter subject exactly as above: ").strip()

idx = np.where(subjects == subject)[0]

if len(idx) == 0:
    print("\nSubject not found.")
    exit()

X = data["X"][idx]
y = data["y"][idx]

model = joblib.load(
    MODELS_DIR / "best_subject_model.pkl"
)

prob = model.predict_proba(X)[0][1]

pred = int(prob >= 0.5)

print()
print("=" * 70)
print("RESULT")
print("=" * 70)
print("Subject      :", subject)
print("True Label   :", y[0])
print("Prediction   :", pred)
print("Probability  :", prob)
print("Diagnosis    :", "Depression" if pred else "Healthy")
