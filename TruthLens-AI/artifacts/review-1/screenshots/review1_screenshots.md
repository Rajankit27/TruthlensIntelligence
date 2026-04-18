# Review 1 — Screenshot captions & template

Use this file to add a short caption, reproduction steps, and timestamp for each saved screenshot. Place the image file in this folder and update the fields below.

Template entries (copy one block per screenshot and complete the fields):

---

## 1 — UI prediction
- **Filename:** `review1_01_ui_prediction.png`
- **Image:** ![UI prediction](review1_01_ui_prediction.png)
- **Caption:** _e.g. Home page with sample input and predicted label + confidence._
- **Command / URL to reproduce:** _e.g. `python backend/app.py` → http://127.0.0.1:5000/_
- **Timestamp:** _YYYY-MM-DD HH:MM_
- **Repro steps:**
  1. Start server
  2. Open `/` in browser
  3. Enter sample text and click `Predict`
- **Acceptance criteria:** Prediction label visible, confidence shown
- **Status:** - [ ] Captured

---

## 2 — End-to-end UI flow
- **Filename:** `review1_02_ui_flow.png`
- **Image:** ![UI flow](review1_02_ui_flow.png)
- **Caption:** _Shows input → processing → final result._
- **Command / URL to reproduce:**
- **Timestamp:**
- **Repro steps:**
- **Acceptance criteria:** All UI steps visible and reproducible
- **Status:** - [ ] Captured

---

## 3 — API response
- **Filename:** `review1_03_api_response.png`
- **Image:** ![API response](review1_03_api_response.png)
- **Caption:** _HTTP request + JSON response for `/predict`._
- **Command / URL to reproduce:** _e.g. `curl -X POST http://127.0.0.1:5000/predict -d "text=..."`_
- **Timestamp:**
- **Repro steps:**
- **Acceptance criteria:** 200 OK and valid JSON with prediction/confidence
- **Status:** - [ ] Captured

---

## 4 — Dataset preview
- **Filename:** `review1_04_dataset_preview.png`
- **Image:** ![Dataset preview](review1_04_dataset_preview.png)
- **Caption:** _First rows of `data/fake_or_real_news.csv`._
- **Timestamp:**
- **Repro steps:**
- **Acceptance criteria:** Headers and sample rows visible
- **Status:** - [ ] Captured

---

## 5 — Training metrics
- **Filename:** `review1_05_training_metrics.png`
- **Image:** ![Training metrics](review1_05_training_metrics.png)
- **Caption:** _Final training output with loss/accuracy/F1._
- **Timestamp:**
- **Repro steps:** Run `python ml/train_model.py` (or show saved log)
- **Acceptance criteria:** Final epoch metrics visible
- **Status:** - [ ] Captured

---

## 6 — Evaluation plots
- **Filename:** `review1_06_eval_plots.png`
- **Image:** ![Eval plots](review1_06_eval_plots.png)
- **Caption:** _Confusion matrix / ROC or other evaluation charts._
- **Status:** - [ ] Captured

---

## 7 — Model artifact
- **Filename:** `review1_07_model_artifact.png`
- **Image:** ![Model artifact](review1_07_model_artifact.png)
- **Caption:** _Contents of `artifacts/` showing saved model file(s)._ 
- **Status:** - [ ] Captured

---

## 8 — Tests passing
- **Filename:** `review1_08_tests_pass.png`
- **Image:** ![Tests passing](review1_08_tests_pass.png)
- **Caption:** _`pytest` or `python test_prediction.py` output showing passing tests._
- **Status:** - [ ] Captured

---

## 9 — Error / edge-case handling
- **Filename:** `review1_09_error_case.png`
- **Image:** ![Error case](review1_09_error_case.png)
- **Caption:** _System response to invalid or edge-case input._
- **Status:** - [ ] Captured

---

## 10 — Deployment / run verification
- **Filename:** `review1_10_deploy_run.png`
- **Image:** ![Deployment run](review1_10_deploy_run.png)
- **Caption:** _Server start, port and URL visible._
- **Status:** - [ ] Captured

---

How to update: add image file to this folder, edit the corresponding block above, check the `Status` box, commit and open a PR.
