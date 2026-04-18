# Frontend — TruthLens Intelligence

## Overview ✨
This document explains the frontend of the TruthLens-AI project: what files implement the UI, how the user flow works, how the client interacts with the Flask backend, and where to change or extend behavior.

Files to review:
- `templates/index.html` — single-page UI and client-side JavaScript.
- `static/style.css` — visual design, tokens, responsive rules, animations.
- `scripts/predict_short.py` — lightweight CLI usage example (reuses same preprocessing + model artifacts).
- `backend/app.py` — serves `index.html` and exposes the `/predict` API used by the frontend.

---

## Page structure & elements (what `index.html` contains) 🧩
- News ticker (top bar) — decorative status text animation.
- Main container with three areas:
  - Header (`.header`) — product title and subtitle.
  - Main (`.main`) — the interactive analysis terminal:
    - `#analyze-form` — single form containing the textarea and `Verify News` button.
    - `#loading` — hidden loading indicator shown during requests.
    - `#result` — hidden results panel with:
      - `#result-badge` — verdict text (`REAL` or `FAKE`).
      - Confidence meter — semi-circle SVG that is animated via stroke-dasharray.
      - `#result-confidence` / `#result-error` — numeric confidence or error text.
  - Footer (`.footer`) — build/version text.

Each visible component is toggled by adding/removing the `.hidden` class.

---

## Client-side logic (JS) — step-by-step 🔁
1. Form submit handler intercepts the default action (prevents page reload).
2. Input validation: trims textarea; if empty → show validation error via `showError()`.
3. UI state update: disables submit button, shows `#loading`, clears previous results.
4. Network request: `fetch('/predict', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ text }) })`.
5. Response handling:
   - If `response.ok`: parse JSON `{ prediction, confidence }` and call `showResult(prediction, confidence)`.
   - If non-OK or fetch error: display an error message in `#result-error`.
6. Finalize: hide loading indicator and re-enable the submit button.

showResult() responsibilities:
- Set verdict badge text and color class (`.real` / `.fake`).
- Update textual confidence (e.g., "87.3% confidence").
- Animate the semi-circle ring: compute fillLength = ARC_LENGTH * confidence and set `stroke-dasharray`.
- Change the ring color according to verdict.

Error handling:
- Network errors and bad responses display clear messages in the `#result` panel.

---

## Styling & UI behavior (`static/style.css`) 🎨
- Design tokens (CSS variables) live in `:root` and a `[data-theme="dark"]` block for theming.
- Visual language: glass panels (`backdrop-filter`), rounded radii, soft shadows, and monospace for the analysis feel.
- Interactive states: button hover/disabled styles, textarea focus, loading pulse animation.
- Confidence meter:
  - Implemented with a semi-circle SVG path.
  - `ARC_LENGTH` constant in the JS (~125.66) approximates π * r for 180° arc; JS uses this to animate `stroke-dasharray`.
- `.hidden` class toggles visibility across components.

---

## Backend integration (how frontend talks to server) 🔗
- Page served by `backend/app.py` via `render_template('index.html')` at `/`.
- Prediction endpoint: `POST /predict` — expects JSON `{ "text": "..." }` and returns `{ "prediction": "FAKE"|"REAL", "confidence": float }`.
- No CORS required because frontend and API are served from same origin.
- Client expects the API to return `response.ok` when inference succeeds and uses `data.error` for server-side messages.

---

## How to run & test locally ✅
- Start the backend (loads model artifacts):
  - From project root: `python backend/app.py` (or `flask run` if configured).
- Open `http://localhost:5000` and paste an article into the textarea.
- CLI check: `python scripts/predict_short.py` to validate model + preprocessing without the web UI.

---

## Where to change behavior / extend the frontend 🔧
- Change UI copy/layout: edit `templates/index.html`.
- Change styles / theme: edit `static/style.css` (tokens at top for color changes).
- Change the API route or response shape: update `backend/app.py` and adapt JS `fetch` accordingly.
- Add client-side validation or richer feedback (e.g., source extraction, highlighted phrases): extend JS with new helper functions and DOM slots in `index.html`.
- Add unit/E2E tests: create tests that hit `/predict` with example payloads and assert the DOM updates (use Playwright / Selenium / Cypress).

---

## Security & UX notes (quick suggestions) ⚠️
- Sanitize displayed text if you later render user content inside HTML (currently the UI shows only controlled strings `REAL`/`FAKE` and numeric confidence).
- Add size limits on client and server to avoid huge payloads.
- Consider showing more detailed explanation of the model decision (if available) — but avoid exposing raw model internals that leak training data.

---

## Short summary
The frontend is a lightweight single-page interface implemented in `index.html` + `style.css`. It performs a single JSON POST to `/predict`, displays a verdict badge and animated confidence meter, and handles errors gracefully. The code is intentionally small and easy to extend.

If you'd like, I can:
- Add unit tests for the frontend flow, or
- Add accessibility improvements (keyboard focus, ARIA attributes), or
- Implement a modal or timeline showing model reasoning.

---

Document created from the current source files: `templates/index.html`, `static/style.css`, `backend/app.py`.
