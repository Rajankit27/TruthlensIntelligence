"""
Script to analyze the downloaded Fake and Real News dataset.
Provides detailed statistics and insights.
"""
import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).parent / "data" / "fake_or_real_news.csv"

print("=" * 70)
print("Fake and Real News Dataset - Analysis Report")
print("=" * 70)
print()

if not DATA_PATH.exists():
    print(f"✗ Dataset not found at: {DATA_PATH}")
    print()
    print("Please download the dataset first:")
    print("  Run: python download_dataset.py")
    print("  Or manually download from:")
    print("  https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset")
    exit(1)

# Load dataset
print("Loading dataset...")
df = pd.read_csv(DATA_PATH)

print("✓ Dataset loaded successfully!")
print()

# Basic Information
print("=" * 70)
print("1. DATASET OVERVIEW")
print("=" * 70)
print(f"Total Rows: {len(df):,}")
print(f"Total Columns: {len(df.columns)}")
print(f"File Size: {DATA_PATH.stat().st_size / (1024*1024):.2f} MB")
print()

# Column Information
print("=" * 70)
print("2. COLUMN INFORMATION")
print("=" * 70)
for i, col in enumerate(df.columns, 1):
    dtype = df[col].dtype
    non_null = df[col].notna().sum()
    null_count = df[col].isna().sum()
    null_pct = (null_count / len(df)) * 100
    
    print(f"{i}. {col}")
    print(f"   Type: {dtype}")
    print(f"   Non-null: {non_null:,} ({100-null_pct:.1f}%)")
    if null_count > 0:
        print(f"   Missing: {null_count:,} ({null_pct:.1f}%)")
    print()

# Label Distribution
if "label" in df.columns:
    print("=" * 70)
    print("3. LABEL DISTRIBUTION")
    print("=" * 70)
    label_counts = df["label"].value_counts()
    label_pct = df["label"].value_counts(normalize=True) * 100
    
    for label in label_counts.index:
        count = label_counts[label]
        pct = label_pct[label]
        print(f"{label:10s}: {count:6,} ({pct:5.2f}%)")
    print()
    print(f"Balance Ratio: {min(label_counts) / max(label_counts):.3f}")
    print()

# Text Statistics
text_cols = ["title", "text"]
for col in text_cols:
    if col in df.columns:
        print("=" * 70)
        print(f"4. {col.upper()} STATISTICS")
        print("=" * 70)
        
        # Character statistics
        df[f"{col}_len"] = df[col].fillna("").astype(str).str.len()
        print(f"Character Length:")
        print(f"  Mean:   {df[f'{col}_len'].mean():.1f}")
        print(f"  Median: {df[f'{col}_len'].median():.1f}")
        print(f"  Min:    {df[f'{col}_len'].min():,}")
        print(f"  Max:    {df[f'{col}_len'].max():,}")
        print()
        
        # Word count statistics
        df[f"{col}_words"] = df[col].fillna("").astype(str).str.split().str.len()
        print(f"Word Count:")
        print(f"  Mean:   {df[f'{col}_words'].mean():.1f}")
        print(f"  Median: {df[f'{col}_words'].median():.1f}")
        print(f"  Min:    {df[f'{col}_words'].min()}")
        print(f"  Max:    {df[f'{col}_words'].max()}")
        print()

# Subject Distribution (if exists)
if "subject" in df.columns:
    print("=" * 70)
    print("5. SUBJECT DISTRIBUTION")
    print("=" * 70)
    subject_counts = df["subject"].value_counts()
    for subject, count in subject_counts.items():
        pct = (count / len(df)) * 100
        print(f"{subject:20s}: {count:5,} ({pct:5.2f}%)")
    print()

# Date Statistics (if exists)
if "date" in df.columns:
    print("=" * 70)
    print("6. DATE STATISTICS")
    print("=" * 70)
    try:
        df["date_parsed"] = pd.to_datetime(df["date"], errors="coerce")
        valid_dates = df["date_parsed"].notna().sum()
        print(f"Valid dates: {valid_dates:,} ({valid_dates/len(df)*100:.1f}%)")
        if valid_dates > 0:
            print(f"Date range: {df['date_parsed'].min()} to {df['date_parsed'].max()}")
    except:
        print("Could not parse dates")
    print()

# Sample Articles
print("=" * 70)
print("7. SAMPLE ARTICLES")
print("=" * 70)

if "label" in df.columns:
    for label in df["label"].unique()[:2]:  # Show first 2 labels
        print(f"\n--- Sample {label} Article ---")
        sample = df[df["label"] == label].iloc[0]
        
        if "title" in df.columns:
            title = str(sample["title"])[:100]
            print(f"Title: {title}...")
        
        if "text" in df.columns:
            text = str(sample["text"])[:200]
            print(f"Text: {text}...")
        
        if "subject" in df.columns:
            print(f"Subject: {sample['subject']}")
        
        print()

# Missing Data Analysis
print("=" * 70)
print("8. MISSING DATA ANALYSIS")
print("=" * 70)
missing_data = df.isnull().sum()
missing_pct = (missing_data / len(df)) * 100
missing_df = pd.DataFrame({
    "Column": missing_data.index,
    "Missing Count": missing_data.values,
    "Missing %": missing_pct.values
})
missing_df = missing_df[missing_df["Missing Count"] > 0].sort_values("Missing Count", ascending=False)

if len(missing_df) > 0:
    print(missing_df.to_string(index=False))
else:
    print("No missing data found!")
print()

# Data Quality Checks
print("=" * 70)
print("9. DATA QUALITY CHECKS")
print("=" * 70)

# Check for empty texts
if "text" in df.columns:
    empty_texts = (df["text"].fillna("").astype(str).str.strip() == "").sum()
    print(f"Empty text fields: {empty_texts} ({empty_texts/len(df)*100:.2f}%)")

if "title" in df.columns:
    empty_titles = (df["title"].fillna("").astype(str).str.strip() == "").sum()
    print(f"Empty title fields: {empty_titles} ({empty_titles/len(df)*100:.2f}%)")

# Check for duplicates
duplicates = df.duplicated().sum()
print(f"Duplicate rows: {duplicates} ({duplicates/len(df)*100:.2f}%)")
print()

# Summary
print("=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"✓ Dataset contains {len(df):,} articles")
print(f"✓ {len(df.columns)} columns available")
if "label" in df.columns:
    print(f"✓ {df['label'].nunique()} label categories")
    print(f"✓ Dataset is {'balanced' if abs(df['label'].value_counts().iloc[0] - df['label'].value_counts().iloc[1]) < len(df)*0.1 else 'imbalanced'}")
print()
print("Dataset is ready for preprocessing and model training!")
print("=" * 70)
