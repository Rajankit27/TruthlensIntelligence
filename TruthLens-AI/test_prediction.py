"""
Test script to analyze why a real news article is being classified as FAKE.
"""
import pickle
from pathlib import Path
import pandas as pd
from ml.train_model import preprocess_text
from sklearn.feature_extraction.text import TfidfVectorizer

# Load model and vectorizer
PROJECT_ROOT = Path(__file__).resolve().parent
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
MODEL_PATH = ARTIFACTS_DIR / "model.pkl"
VECTORIZER_PATH = ARTIFACTS_DIR / "vectorizer.pkl"

# Load artifacts
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)
with open(VECTORIZER_PATH, "rb") as f:
    vectorizer = pickle.load(f)

# Test text
test_text = "Tech company announces new smartphone with advanced camera features. The device includes a 108-megapixel main camera and improved battery life. Pre-orders begin next month, with shipping expected in the following quarter. Industry analysts predict strong sales based on early reviews."

print("=" * 70)
print("PREDICTION ANALYSIS")
print("=" * 70)
print(f"\nOriginal Text:")
print(test_text)
print()

# Preprocess
processed = preprocess_text(test_text)
print(f"Preprocessed Text:")
print(processed)
print()

# Vectorize
vec = vectorizer.transform([processed])
print(f"Vector Shape: {vec.shape}")
print(f"Non-zero features: {vec.nnz}")
print()

# Predict
prediction = model.predict(vec)[0]
proba = model.predict_proba(vec)[0]
confidence = float(max(proba))

print(f"Prediction: {prediction}")
print(f"Confidence: {confidence:.4f}")
print(f"Probability Distribution:")
print(f"  FAKE: {proba[0]:.4f}")
print(f"  REAL: {proba[1]:.4f}")
print()

# Get feature importance (top contributing features)
feature_names = vectorizer.get_feature_names_out()
coef = model.coef_[0]  # Logistic regression coefficients

# Get non-zero features for this text
non_zero_indices = vec.indices
non_zero_values = vec.data

# Calculate contribution of each feature
contributions = []
for idx, val in zip(non_zero_indices, non_zero_values):
    contribution = coef[idx] * val
    contributions.append((feature_names[idx], contribution, val, coef[idx]))

# Sort by absolute contribution
contributions.sort(key=lambda x: abs(x[1]), reverse=True)

print("=" * 70)
print("TOP CONTRIBUTING FEATURES (Why it's classified as FAKE)")
print("=" * 70)
print(f"{'Feature':<30} {'Contribution':<15} {'TF-IDF Value':<15} {'Coefficient':<15}")
print("-" * 70)
for feature, contrib, tfidf_val, coef_val in contributions[:20]:
    print(f"{feature:<30} {contrib:>12.6f} {tfidf_val:>12.6f} {coef_val:>12.6f}")

print("\n" + "=" * 70)
print("ANALYSIS")
print("=" * 70)
print("\nPositive contributions = towards FAKE")
print("Negative contributions = towards REAL")
print("\nIf prediction is FAKE, look for:")
print("- Many positive contributions (features associated with FAKE)")
print("- High TF-IDF values for FAKE-associated words")
print("- Low TF-IDF values for REAL-associated words")
