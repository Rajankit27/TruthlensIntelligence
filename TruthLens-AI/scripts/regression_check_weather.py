"""scripts/regression_check_weather.py

Verify that the canonical weather advisory sample is classified as REAL after retraining.
Exits non-zero / raises AssertionError if the regression check fails.

Run:
    python scripts\regression_check_weather.py
"""
from pathlib import Path
import pickle
from ml.train_model import preprocess_text

ARTIFACTS = Path(__file__).resolve().parents[1] / "artifacts"
MODEL_PATH = ARTIFACTS / "model.pkl"
VECTORIZER_PATH = ARTIFACTS / "vectorizer.pkl"

if not MODEL_PATH.exists() or not VECTORIZER_PATH.exists():
    raise SystemExit("Model artifacts not found. Run `python ml/train_model.py` to train and create artifacts/")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)
with open(VECTORIZER_PATH, "rb") as f:
    vectorizer = pickle.load(f)

SAMPLE = (
    "National Weather Service issues flood advisory for Riverside County through "
    "Saturday evening. Local authorities advise residents in low‑lying areas to prepare "
    "for possible evacuations; shelters will open at 1400 UTC."
)

proc = preprocess_text(SAMPLE)
vec = vectorizer.transform([proc])
proba = model.predict_proba(vec)[0]
pred = model.predict(vec)[0]
conf = float(max(proba))

print(f"Sample prediction: {pred}  |  Confidence: {conf:.4f}")
print(f"Probabilities => FAKE: {proba[0]:.4f}, REAL: {proba[1]:.4f}")

# Expect REAL with confidence >= 0.6
if str(pred).upper() != "REAL" or conf < 0.6:
    raise AssertionError("Regression check FAILED: sample not classified as REAL with confidence >= 0.6")

print("Regression check PASSED: sample classified as REAL with sufficient confidence.")
