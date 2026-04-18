# Dataset Download and Analysis Guide

## Quick Start

### Step 1: Download the Dataset

**Option A: Automatic Download (Recommended)**
```bash
python download_dataset.py
```

**Option B: Manual Download**
1. Visit: https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset
2. Click "Download" button
3. Extract the ZIP file
4. Place `fake_or_real_news.csv` in the `data/` folder

**Option C: Direct Download (GitHub Mirror)**
```bash
# The dataset will be automatically downloaded when you run:
python ml/train_model.py
```

---

### Step 2: Analyze the Dataset

```bash
python analyze_dataset.py
```

This will provide:
- Dataset overview (rows, columns, file size)
- Column information and data types
- Label distribution
- Text statistics (character length, word count)
- Subject distribution
- Date statistics
- Sample articles
- Missing data analysis
- Data quality checks

---

## Dataset Information

### Source
- **Kaggle Dataset:** Fake and Real News Dataset
- **URL:** https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset
- **Author:** Clément Bisaillon
- **License:** Public Domain / CC0

### Dataset Structure

| Column | Type | Description | Used? |
|--------|------|-------------|-------|
| `title` | string | News article headline | ✅ Yes (combined with text) |
| `text` | string | Full article content | ✅ Yes (combined with title) |
| `subject` | string | News category/topic | ❌ No (dropped) |
| `date` | string | Publication date | ❌ No (dropped) |
| `label` | string | Classification (FAKE/REAL) | ✅ Yes (target variable) |

### Expected Dataset Size
- **Rows:** ~6,000+ articles
- **File Size:** ~5-10 MB
- **Format:** CSV (comma-separated values)

---

## Analysis Script Output

The `analyze_dataset.py` script provides:

### 1. Dataset Overview
- Total number of rows
- Number of columns
- File size in MB

### 2. Column Information
- Data types for each column
- Non-null counts
- Missing value percentages

### 3. Label Distribution
- Count of FAKE vs REAL articles
- Percentage distribution
- Balance ratio

### 4. Text Statistics
- Character length (mean, median, min, max)
- Word count (mean, median, min, max)
- For both `title` and `text` columns

### 5. Subject Distribution
- Count of articles per subject category
- Percentage distribution

### 6. Date Statistics
- Date range
- Valid date count

### 7. Sample Articles
- Example FAKE article
- Example REAL article
- Shows title, text preview, subject

### 8. Missing Data Analysis
- Columns with missing values
- Count and percentage of missing data

### 9. Data Quality Checks
- Empty text fields
- Empty title fields
- Duplicate rows

---

## Integration with Training Pipeline

The dataset is automatically used when you run:

```bash
python ml/train_model.py
```

**What happens:**
1. Checks if dataset exists in `data/fake_or_real_news.csv`
2. If missing, automatically downloads it
3. Loads and processes the dataset
4. Displays dataset statistics
5. Shows which attributes are dropped
6. Preprocesses all articles
7. Trains the model
8. Saves model artifacts

---

## File Locations

```
TruthLens-AI/
├── data/
│   └── fake_or_real_news.csv    # Downloaded dataset (after download)
├── download_dataset.py           # Script to download dataset
├── analyze_dataset.py            # Script to analyze dataset
└── ml/
    └── train_model.py            # Training script (auto-downloads if needed)
```

---

## Troubleshooting

### Dataset Not Found
**Error:** `FileNotFoundError: Could not download dataset`

**Solution:**
1. Run `python download_dataset.py` manually
2. Or download from Kaggle and place in `data/` folder
3. Check internet connection

### Download Fails
**Error:** Network error or timeout

**Solution:**
1. Check internet connection
2. Try manual download from Kaggle
3. Use alternative mirror URL (update in `train_model.py`)

### Analysis Script Errors
**Error:** `ModuleNotFoundError: No module named 'pandas'`

**Solution:**
```bash
pip install pandas
```

Or install all requirements:
```bash
pip install -r requirements.txt
```

---

## Example Output

### Download Script Output:
```
============================================================
Downloading Fake and Real News Dataset
============================================================
Source: https://github.com/GeorgeMcIntire/fake_real_news_dataset/raw/master/fake_or_real_news.csv
Destination: a:\Cursor\TruthLens-AI\data\fake_or_real_news.csv

Downloading...
✓ Dataset downloaded successfully!
  File size: 6.45 MB
  Location: a:\Cursor\TruthLens-AI\data\fake_or_real_news.csv

Dataset is ready for analysis!
```

### Analysis Script Output:
```
======================================================================
Fake and Real News Dataset - Analysis Report
======================================================================

Loading dataset...
✓ Dataset loaded successfully!

======================================================================
1. DATASET OVERVIEW
======================================================================
Total Rows: 6,335
Total Columns: 5
File Size: 6.45 MB

======================================================================
2. COLUMN INFORMATION
======================================================================
1. title
   Type: object
   Non-null: 6,335 (100.0%)

2. text
   Type: object
   Non-null: 6,330 (99.9%)
   Missing: 5 (0.1%)

...

======================================================================
3. LABEL DISTRIBUTION
======================================================================
FAKE      :  3,171 (50.05%)
REAL      :  3,164 (49.95%)

Balance Ratio: 0.998
```

---

## Next Steps

After downloading and analyzing the dataset:

1. **Review the analysis** - Understand dataset characteristics
2. **Run training** - `python ml/train_model.py`
3. **Check preprocessing** - Review preprocessing statistics
4. **Train model** - Model will be saved to `artifacts/`
5. **Test predictions** - Use the Flask API to test predictions

---

## Additional Resources

- **Detailed Process Review:** See `PROCESS_REVIEW_DETAILED.md`
- **Preprocessing Documentation:** See `DATA_COLLECTION_PREPROCESSING.md`
- **Attribute Summary:** See `DATASET_ATTRIBUTES_SUMMARY.md`

---

## Support

If you encounter issues:
1. Check the error message
2. Review the troubleshooting section
3. Verify dataset file exists in `data/` folder
4. Check file permissions
5. Ensure sufficient disk space (~10 MB free)
