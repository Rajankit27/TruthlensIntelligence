"""scripts/merge_fake_true.py

Merge `data/Fake.csv` and `data/True.csv` into `data/fake_or_real_news.csv`.
- Creates a timestamped backup of any existing `fake_or_real_news.csv`.
- Adds a `label` column with values 'FAKE' / 'REAL'.
- Writes `title,text,label,subject,date` (if present).

Run: python scripts\merge_fake_true.py
"""
from pathlib import Path
import pandas as pd
import time
import shutil

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / 'data'
FAKE_P = DATA_DIR / 'Fake.csv'
REAL_P = DATA_DIR / 'True.csv'
OUT_P = DATA_DIR / 'fake_or_real_news.csv'

if not FAKE_P.exists() or not REAL_P.exists():
    raise SystemExit('Missing Fake.csv or True.csv in data/. Place the files and re-run this script.')

# Read samples (will infer columns)
fake = pd.read_csv(FAKE_P)
real = pd.read_csv(REAL_P)

# Add label column
fake['label'] = 'FAKE'
real['label'] = 'REAL'

# Select common columns (keep title,text,label and preserve others if present)
cols = []
for c in ['title','text','label','subject','date']:
    if c in fake.columns or c in real.columns:
        cols.append(c)

combined = pd.concat([fake[cols], real[cols]], ignore_index=True)

# Backup existing output if exists
if OUT_P.exists():
    ts = int(time.time())
    bak = OUT_P.with_name(OUT_P.stem + f'.bak.{ts}' + OUT_P.suffix)
    shutil.copy2(OUT_P, bak)
    print(f'Existing {OUT_P.name} backed up to {bak.name}')

combined.to_csv(OUT_P, index=False)
print(f'Merged datasets: {len(fake)} FAKE + {len(real)} REAL -> {OUT_P} ({len(combined)} rows)')
