# Review 1 — Screenshot checklist

Purpose
- Short checklist for screenshots required during **Review 1** (demo, QA, integration & delivery).

Storage
- Path: `artifacts/review-1/screenshots/`
- Format: **PNG**, resolution >= 1280×720
- Naming: `review1_<NN>_<short-description>.png` (keeps order & clarity)

Must-have screenshots (save each to the path above)
1. `review1_01_ui_prediction.png` — App home with example input + prediction & confidence (Demo)
2. `review1_02_ui_flow.png` — Full UI input → prediction flow (Demo / Acceptance)
3. `review1_03_api_response.png` — HTTP request + JSON response for `/predict` (Integration)
4. `review1_04_dataset_preview.png` — Sample rows from `data/fake_or_real_news.csv` (Data validation)
5. `review1_05_training_metrics.png` — Training terminal/log with final metrics (Model training)
6. `review1_06_eval_plots.png` — Confusion matrix / ROC / evaluation plots (Evaluation)
7. `review1_07_model_artifact.png` — `artifacts/` listing showing saved model file(s) (Delivery)
8. `review1_08_tests_pass.png` — `pytest` or `python test_prediction.py` showing passing tests (QA)
9. `review1_09_error_case.png` — System response to invalid input (QA / edge cases)
10. `review1_10_deploy_run.png` — Server start / deployment verification (Demo / Deployment)

Capture guidelines
- Include reproduction info (command/URL and timestamp) in the image or caption.
- For API screenshots: show the full request (method, URL, headers/body) and response body/status.
- Annotate important areas (arrows/highlights) when possible.
- Prefer un-cropped terminal output for logs/metrics.

How to add and submit
1. Put screenshot files in `artifacts/review-1/screenshots/`.
2. Update `review1_screenshots.md` (in the same folder) with caption, command/URL and timestamp.
3. Commit with `docs: add review-1 screenshots` and open PR.

Tips
- Use browser DevTools → Network for API captures or terminal `curl` output.
- Use `Win+Shift+S` (Windows) or a screenshot tool and annotate.

---
