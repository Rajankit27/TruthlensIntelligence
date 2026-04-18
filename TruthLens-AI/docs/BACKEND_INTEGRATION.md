# Backend Integration — TruthLens Intelligence

This document explains how the backend works, how it integrates the ML model with the frontend, and where to find the implementation in the repository. It is intended for quick reading and hands‑on reference.

---

## Summary (one‑line)
Flask app loads a trained Logistic Regression model + TF‑IDF vectorizer, exposes a `/predict` JSON API that preprocesses incoming text, vectorizes it, performs inference, and returns `{ prediction, confidence }` to the frontend.

---

## Key files
- `backend/app.py` — Flask application, routes, artifact loading, and request handling.
- `ml/train_model.py` — preprocessing (`preprocess_text`) and training pipeline (creates `model.pkl`, `vectorizer.pkl`).
- `artifacts/` — saved `model.pkl` and `vectorizer.pkl` (created by training).
- `templates/index.html` — frontend that POSTs to `/predict` and displays results.
- `scripts/predict_short.py` & `test_prediction.py` — local CLI/test helpers.

---

## API specification
- Endpoint: `POST /predict`
- Request: `Content-Type: application/json`
  - Body: `{ "text": "<article text>" }`
- Successful response: `200 OK`
  - Body: `{ "prediction": "FAKE"|"REAL", "confidence": 0.0–1.0 }`
- Common error responses:
  - `400` — invalid JSON / missing or empty `text`
  - `500` — server error during processing

Example request (curl):

```
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"The mayor announced new park renovations."}'
```

---

## Inference pipeline (step‑by‑step)
1. Request received in `backend/app.py` at `/predict`.
2. `ensure_model_loaded()` loads `model.pkl` and `vectorizer.pkl` if not already in memory.
3. Input validation: JSON decode, presence and non‑emptiness of `text`.
4. Preprocessing: `preprocess_text(text)` (lowercase, regex cleanup, tokenize, lemmatize, stopword policy for short inputs).
5. Vectorize: `vectorizer.transform([processed_text])` — TF‑IDF (word + char n‑grams).
6. Predict: `model.predict(vec)` and `model.predict_proba(vec)` for confidence.
7. Response: JSON with uppercase `prediction` and `confidence` rounded to 4 decimals.

---

## How the backend integrates with the frontend
- Frontend (`index.html`) sends the text as JSON to `/predict` using `fetch()`.
- Backend returns prediction JSON which the frontend uses to update the UI (badge + confidence ring).
- The same preprocessing code (`preprocess_text`) is used by both training and inference to ensure consistency.

---

## How to run locally
1. Install dependencies: `pip install -r requirements.txt`.
2. Train model (if `artifacts/` is empty): `python ml/train_model.py`.
3. Start server: `python backend/app.py`.
4. Open `http://localhost:5000` and paste text into the UI.

---

## Important implementation notes
- Artifacts are loaded with Python `pickle` (fast, but treat as trusted input in production).
- `preprocess_text` lives in `ml/train_model.py` — same function used at inference time.
- Model uses `FeatureUnion` of TF‑IDF vectorizers (word + char) for robustness.
- Flask currently runs with `debug=True` in `app.py` for development — disable in production.

---

## Testing tips
- Use `scripts/predict_short.py` to run quick local checks against the serialized artifacts.
- Use `test_prediction.py` to inspect feature contributions for misclassified examples.
- Add unit tests for `preprocess_text` and the `/predict` endpoint (pytest + test client recommended).

---

## Production considerations & improvements
- Replace `pickle` with a safer artifact management strategy or ensure artifacts are loaded only from trusted storage.
- Serve behind a WSGI server (Gunicorn/uvicorn) and add HTTPS, rate limiting, and authentication for API access.
- Add `/health` and readiness checks for orchestration.
- Add logging, monitoring, and model versioning (model registry).

---

## Where to inspect code quickly
- Load model: `backend/app.py` — `load_artifacts()`
- Preprocessing: `ml/train_model.py` — `preprocess_text()`
- Prediction endpoint: `backend/app.py` — `predict()`
- Frontend request code: `templates/index.html` (JS `fetch('/predict')`)

---

If you want, I can add a short `/health` endpoint, a unit test for `/predict`, or a README link to this page. Which would you prefer next?