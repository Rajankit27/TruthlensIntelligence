# backend/app.py — Detailed code logic and explanation

This file explains the logic of `backend/app.py` **only** (line‑by‑line / section‑by‑section) so you can quickly understand how the backend works internally.

---

## 1. Purpose
`backend/app.py` is the Flask application that:
- serves the frontend (`index.html`),
- loads the trained ML `model` and `vectorizer` artifacts,
- exposes the `/predict` API endpoint which runs preprocessing → vectorization → inference,
- performs basic input validation and error handling.

All inference uses the same preprocessing function from `ml/train_model.py` to avoid training/inference mismatch.

---

## 2. Top‑level imports & project path setup
- Flask imports: `Flask`, `jsonify`, `render_template`, `request` — used for web routing and JSON handling.
- `PROJECT_ROOT` is calculated from `Path(__file__).resolve().parent.parent` and added to `sys.path` so local modules (`ml.train_model`) can be imported cleanly.

Why: allows the backend module to import project modules without installing a package.

---

## 3. Shared preprocessing import
`from ml.train_model import preprocess_text`

Meaning: the exact same `preprocess_text()` used during training is reused here to ensure consistent input transformation.

---

## 4. Flask app initialization and template/static folders
```
app = Flask(
    __name__,
    template_folder=PROJECT_ROOT / "templates",
    static_folder=PROJECT_ROOT / "static",
)
```
- Configures Flask to serve `index.html` and static CSS from project folders.

---

## 5. Artifact paths and global variables
- `ARTIFACTS_DIR` points to `artifacts/` where `model.pkl` and `vectorizer.pkl` live.
- `model = None` and `vectorizer = None` are module‑level globals so the loaded objects persist between requests.

Design rationale: loading artifacts once (lazy or at startup) avoids repeated disk I/O per request.

---

## 6. load_artifacts() — what it does and why
Key steps:
1. Checks existence of `MODEL_PATH` and `VECTORIZER_PATH` and raises FileNotFoundError with instructions if missing.
2. Uses `pickle.load()` to set the global `model` and `vectorizer` variables.
3. Prints a confirmation message.

Important notes:
- Uses `pickle` for simplicity (fast, Python native). Only load artifacts from trusted sources.
- This function centralizes artifact loading logic so it can be called at startup or lazily before requests.

---

## 7. index() route — serve UI
```
@app.route("/")
def index():
    return render_template("index.html")
```
- Serves the main frontend page.

---

## 8. predict() route — full request → inference logic
High‑level flow inside `predict()`:
1. Read JSON payload: `request.get_json(force=True, silent=True)`
   - Returns 400 if JSON missing/invalid.
2. Validate `text` field: must exist and be non‑empty; return 400 otherwise.
3. Preprocess: `processed = preprocess_text(text)`
   - If preprocessing yields no meaningful tokens → return 400.
4. Vectorize: `vec = vectorizer.transform([processed])`
5. Predict: `prediction = model.predict(vec)[0]` and `proba = model.predict_proba(vec)[0]`
6. Compute `confidence = float(max(proba))` and return response JSON:
   - `{ "prediction": "FAKE"|"REAL", "confidence": 0.0–1.0 }`
7. Exception handling: unhandled exceptions produce a 500 with the error message.

Validation specifics:
- Empty or whitespace input gets a helpful 400 response.
- Errors return clear messages for client debugging.

Why design it this way:
- Ensures the same preprocessing pipeline is enforced before inference.
- Provides concise user‑facing error messages.
- Returns classification confidence for UI display.

---

## 9. ensure_model_loaded() — safety before serving requests
```
@app.before_request
def ensure_model_loaded():
    if request.path.startswith("/static"):
        return
    if model is None or vectorizer is None:
        load_artifacts()
```
- This runs before every non‑static request.
- It performs **lazy loading**: if artifacts aren't loaded yet (e.g., after a restart), they will be loaded on the first incoming request.

Benefits:
- Simplifies local development (you can `app.run()` without preloading artifacts).
- Ensures model availability during runtime.

---

## 10. Running as main — startup behavior
```
if __name__ == "__main__":
    load_artifacts()
    app.run(debug=True, host="0.0.0.0", port=5000)
```
- Calls `load_artifacts()` immediately when file run directly (so the model is ready before accepting requests).
- Starts Flask dev server on port 5000 with `debug=True` (development only).

Production note: replace dev server and set `debug=False`.

---

## 11. Error handling & HTTP responses
- Input and preprocessing errors → HTTP 400 with descriptive JSON.
- Unexpected exceptions → HTTP 500 including the exception string (developer friendly but consider hiding details in prod).

How to improve:
- Replace plaintext exception messages with structured logging + friendly client messages.
- Add input size limits to avoid extremely long requests.

---

## 12. Security, concurrency & practical considerations
- `pickle.load()` is unsafe for untrusted sources — only load artifacts you control.
- Scikit‑learn models are safe to read concurrently in multiple threads; avoid mutating global model objects.
- Add `/health` endpoint, request logging, and rate limiting for production readiness.

---

## 13. Example usage
- curl example:
```
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d '{"text":"City council approves new park."}'
```
- Quick script: `python scripts/predict_short.py` (loads artifacts directly and prints prediction).

---

## 14. Quick troubleshooting checklist
- "Model artifacts not found" → run `python ml/train_model.py`.
- 500 server error → check server console for exception details.
- Browser shows CORS/network error → ensure server is running and POST path is `/predict`.

---

## 15. Where to read the referenced code
- `load_artifacts()` — search in `backend/app.py`
- `preprocess_text()` — `ml/train_model.py`
- `/predict` implementation — `backend/app.py`
- Frontend POST call — `templates/index.html` (JS `fetch('/predict')`)

---

If you'd like, I can now:
- add an inline comment block inside `backend/app.py` summarizing this logic, or
- implement a `/health` endpoint and a unit test for `/predict`.

Which should I do next?