"""scripts/augment_weather_examples.py

Append synthetic REAL weather/advisory examples to data/fake_or_real_news.csv
- Makes a timestamped backup before modifying
- Adds configurable number of paraphrases

Run:
    python scripts\augment_weather_examples.py
"""
from pathlib import Path
import pandas as pd
import shutil
import time

ROOT = Path(__file__).resolve().parents[1]
DATA_CSV = ROOT / "data" / "fake_or_real_news.csv"
NUM_TO_ADD = 250

if not DATA_CSV.exists():
    raise SystemExit(f"Dataset not found at {DATA_CSV}. Place 'fake_or_real_news.csv' in the data/ folder first.")

# Make a safe timestamped backup
ts = int(time.time())
backup = DATA_CSV.with_name(DATA_CSV.stem + f".bak.{ts}" + DATA_CSV.suffix)
shutil.copy2(DATA_CSV, backup)
print(f"Backup created: {backup}")

# Load existing CSV (preserve columns)
df = pd.read_csv(DATA_CSV)
required_cols = {"title", "text", "label"}
if not required_cols.issubset(set(df.columns)):
    raise SystemExit(f"CSV is missing required columns: {required_cols - set(df.columns)}")

# Templates and variation pools
templates = [
    "National Weather Service issues {event} for {place} through {time}. Local authorities advise residents in low‑lying areas to prepare for possible evacuations; shelters will open at {time2}.",
    "{agency} issues {event} for {place}; residents should avoid flooded roads and follow official guidance. Shelters will be available at community centers.",
    "Weather alert: {event} in {place} until {time}. Emergency services advise residents to move to higher ground and monitor local media for updates.",
]

places = ["Riverside County", "Ventura County", "Oakridge County", "Marin County", "King County", "Boulder County", "Jefferson County"]
events = ["flood advisory", "severe thunderstorm watch", "flash flood warning", "coastal storm warning", "flood warning", "winter storm advisory", "heat advisory"]
times = ["Saturday evening", "through Monday morning", "until 2200 UTC", "for the next 24 hours", "until further notice"]
agencies = ["National Weather Service", "NOAA", "State DOT", "County Emergency Management"]

new_rows = []
for i in range(NUM_TO_ADD):
    tmpl = templates[i % len(templates)]
    row = {
        "title": f"{events[i % len(events)].title()} — {places[i % len(places)]}",
        "text": tmpl.format(
            event=events[i % len(events)],
            place=places[i % len(places)],
            time=times[i % len(times)],
            time2="1400 UTC",
            agency=agencies[i % len(agencies)],
        ),
        "label": "REAL",
    }
    new_rows.append(row)

out_df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)
out_df.to_csv(DATA_CSV, index=False)
print(f"Appended {len(new_rows)} REAL weather/advisory examples to {DATA_CSV}")
print("If you plan to retrain, run: python ml\\train_model.py")
