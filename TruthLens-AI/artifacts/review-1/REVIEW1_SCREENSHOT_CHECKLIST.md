# Review 1 — Screenshot checklist (concise)

Purpose
- Quick, single-file checklist of screenshots to capture for **Review 1** (demo, QA, integration, delivery).

Storage
- Path: `artifacts/review-1/`
- Preferred format: `PNG` (1280×720 or larger)
- Naming convention: `review1_<NN>_<short-desc>.png`

Must-have screenshots
1. `review1_01_ui_prediction.png` — App home with example input, predicted label and confidence (Demo). Acceptance: prediction visible.
2. `review1_02_ui_flow.png` — Full UI input → processing → final result (Demo/Acceptance). Acceptance: all UI steps visible.
3. `review1_03_api_response.png` — HTTP request + JSON response for `/predict` (Integration). Acceptance: 200 OK + valid JSON.
4. `review1_04_dataset_preview.png` — Sample rows from `data/fake_or_real_news.csv` (Data validation). Acceptance: headers and sample rows visible.
5. `review1_05_training_metrics.png` — Training terminal/log showing final metrics (Model training). Acceptance: final epoch metrics present.
6. `review1_06_eval_plots.png` — Confusion matrix / ROC / other evaluation charts (Evaluation). Acceptance: axes and labels readable.
7. `review1_07_model_artifact.png` — `artifacts/` listing showing saved model file(s) (Delivery). Acceptance: model file(s) and sizes shown.
8. `review1_08_tests_pass.png` — `pytest` or `python test_prediction.py` output showing passing tests (QA). Acceptance: all tests pass.
9. `review1_09_error_case.png` — System response to invalid or edge-case input (QA). Acceptance: graceful error message or validation shown.
10. `review1_10_deploy_run.png` — Server start / deployment verification (Demo/Deployment). Acceptance: URL/port visible.

Optional / nice-to-have
- `review1_11_code.png` — Key code snippet (model load/predict).
- `review1_12_perf.png` — CPU/RAM during inference.

How to use
- Put screenshots in this folder and update `review1_screenshots.md` with caption, command/URL and timestamp.
- Commit with message: `docs: add review-1 screenshots` and open PR.

---
