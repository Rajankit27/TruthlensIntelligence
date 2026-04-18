"""
Script to download the Fake and Real News dataset for analysis.
"""
import urllib.request
import os
from pathlib import Path

# Create data directory if it doesn't exist
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
DATA_PATH = DATA_DIR / "fake_or_real_news.csv"

# Dataset URL
ISOT_DATASET_URL = "https://github.com/GeorgeMcIntire/fake_real_news_dataset/raw/master/fake_or_real_news.csv"

print("=" * 60)
print("Downloading Fake and Real News Dataset")
print("=" * 60)
print(f"Source: {ISOT_DATASET_URL}")
print(f"Destination: {DATA_PATH}")
print()

try:
    print("Downloading...")
    urllib.request.urlretrieve(ISOT_DATASET_URL, DATA_PATH)
    
    # Check file size
    file_size = os.path.getsize(DATA_PATH) / (1024 * 1024)  # MB
    print(f"✓ Dataset downloaded successfully!")
    print(f"  File size: {file_size:.2f} MB")
    print(f"  Location: {DATA_PATH}")
    print()
    print("Dataset is ready for analysis!")
    
except Exception as e:
    print(f"✗ Error downloading dataset: {e}")
    print()
    print("Manual download instructions:")
    print("1. Visit: https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset")
    print("2. Download the dataset")
    print(f"3. Place 'fake_or_real_news.csv' in: {DATA_DIR}")
    raise
