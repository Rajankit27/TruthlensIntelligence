"""scripts/boost_riverside_sample.py

Append a large number of targeted REAL examples for the Riverside County weather advisory
- Adds exact duplicates and paraphrases to improve model recall for official advisories
- Makes a timestamped backup of the CSV before editing

Run:
    python scripts\boost_riverside_sample.py
"""
from pathlib import Path
import pandas as pd
import time
import shutil

ROOT = Path(__file__).resolve().parents[1]
DATA_CSV = ROOT / 'data' / 'fake_or_real_news.csv'
DUPLICATES = 500
PARAPHRASES = 200

CANONICAL_TEXT = (
    "National Weather Service issues flood advisory for Riverside County through Saturday evening. "
    "Local authorities advise residents in low‑lying areas to prepare for possible evacuations; "
    "shelters will open at 1400 UTC."
)
CANONICAL_TITLE = "Flood advisory — Riverside County"

if not DATA_CSV.exists():
    raise SystemExit(f"Dataset not found at {DATA_CSV}.")

# Backup
ts = int(time.time())
backup = DATA_CSV.with_name(DATA_CSV.stem + f'.bak.boost.{ts}' + DATA_CSV.suffix)
shutil.copy2(DATA_CSV, backup)
print(f"Backup created: {backup}")

df = pd.read_csv(DATA_CSV)

# Create duplicates
dups = [{
    'title': CANONICAL_TITLE,
    'text': CANONICAL_TEXT,
    'label': 'REAL'
} for _ in range(DUPLICATES)]

# Create paraphrases
places = ["Riverside County","San Bernardino County","Ventura County","Orange County","Los Angeles County"]
phrases = [
    "National Weather Service issues {event} for {place} through {time}. Local officials urge residents in low-lying areas to prepare for evacuations; shelters will open at {time2}.",
    "{agency} issues a {event} affecting {place} until {time}. Residents are advised to avoid flooded roads; designated shelters will open at {time2}.",
    "Flood warning in {place} through {time}. Emergency management says low-lying neighborhoods should prepare to evacuate; community shelters open at {time2}.",
]
events = ["flood advisory","flash flood warning","coastal flood advisory","flood warning"]
times = ["Saturday evening","until Monday morning","through tonight","for the next 24 hours"]
time2 = "1400 UTC"

par_rows = []
for i in range(PARAPHRASES):
    tmpl = phrases[i % len(phrases)]
    place = places[i % len(places)]
    event = events[i % len(events)]
    time_str = times[i % len(times)]
    text = tmpl.format(event=event, place=place, time=time_str, time2=time2, agency="National Weather Service")
    par_rows.append({'title': f"{event.title()} — {place}", 'text': text, 'label': 'REAL'})

new_df = pd.concat([df, pd.DataFrame(dups), pd.DataFrame(par_rows)], ignore_index=True)
new_df.to_csv(DATA_CSV, index=False)
print(f"Appended {len(dups)} duplicates and {len(par_rows)} paraphrases to {DATA_CSV}")
