"""
TruthLens Intelligence - Model Training Script.

Trains a Logistic Regression model for fake news detection using TF-IDF
vectorization. Downloads and uses real Kaggle dataset "Fake and Real News Dataset"
or loads from local CSV file if available.
"""

import re
import pickle
import urllib.request
from pathlib import Path

import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import FeatureUnion
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, precision_recall_curve, f1_score, roc_auc_score

# Download required NLTK data (run once)
# note: remove invalid/typo entries and include wordnet language data for lemmatizer
NLTK_DATA = ["punkt", "stopwords", "wordnet", "omw-1.4", "averaged_perceptron_tagger"]
for resource in NLTK_DATA:
    try:
        nltk.download(resource, quiet=True)
    except Exception:
        # continue if a resource cannot be downloaded in the current environment
        pass

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)
DATA_PATH = DATA_DIR / "fake_or_real_news.csv"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
ARTIFACTS_DIR.mkdir(exist_ok=True)
MODEL_PATH = ARTIFACTS_DIR / "model.pkl"
VECTORIZER_PATH = ARTIFACTS_DIR / "vectorizer.pkl"

# Kaggle Dataset URLs (Fake and Real News Dataset)
# Using direct download links from GitHub mirrors
KAGGLE_DATASET_URL = "https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset/download?datasetVersionNumber=2"
# Alternative: Using a publicly available mirror or direct download
# Note: For production, use Kaggle API with credentials
FAKE_NEWS_URL = "https://raw.githubusercontent.com/several27/FakeNewsCorpus/master/news_sample.csv"
# Using GitHub raw link - Lutzhamel Fake News Dataset
ISOT_DATASET_URL = "https://github.com/lutzhamel/fake-news/raw/refs/heads/master/data/fake_or_real_news.csv"

# Initialize NLTK resources once (not per text)
_lemmatizer = WordNetLemmatizer()
_stop_words = set(stopwords.words("english"))


def preprocess_text(text: str) -> str:
    """
    Preprocess text for model input with short-text robustness.

    - Lowercase, remove punctuation
    - Tokenize and lemmatize
    - For very short inputs (<= 6 tokens) keep stopwords to retain signal
      otherwise remove stopwords as before.

    Returns a cleaned, space-joined string.
    """
    if not text or not isinstance(text, str):
        return ""

    # Lowercase
    text = text.lower()

    # Remove special characters using regex (keep alphanumeric and spaces)
    text = re.sub(r"[^a-z0-9\s]", "", text)

    # Tokenize
    tokens = word_tokenize(text)
    if not tokens:
        return ""

    # If the input is very short, do NOT remove stopwords (preserve signal)
    preserve_stopwords = len(tokens) <= 6

    processed_tokens = []
    for token in tokens:
        if len(token) <= 1:
            continue
        if not preserve_stopwords and token in _stop_words:
            continue
        lemma = _lemmatizer.lemmatize(token, pos="v")
        lemma = _lemmatizer.lemmatize(lemma, pos="n")
        processed_tokens.append(lemma)

    return " ".join(processed_tokens) 


def download_kaggle_dataset() -> Path:
    """
    Download the Fake and Real News dataset from Kaggle/public source.
    
    Returns:
        Path to the downloaded CSV file.
    """
    print("Downloading Fake and Real News dataset...")
    try:
        # Try downloading from ISOT dataset (reliable public source)
        urllib.request.urlretrieve(ISOT_DATASET_URL, DATA_PATH)
        print(f"[OK] Dataset downloaded successfully to {DATA_PATH}")
        return DATA_PATH
    except Exception as e:
        print(f"[ERROR] Failed to download dataset: {e}")
        print("Please manually download the dataset:")
        print("1. Visit: https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset")
        print("2. Download the dataset")
        print(f"3. Extract and place 'fake_or_real_news.csv' in {DATA_DIR}")
        raise


def load_or_create_dataset() -> tuple[pd.DataFrame, pd.Series]:
    """
    Load dataset from CSV. Downloads from Kaggle if not present locally.
    
    Dataset Source: Fake and Real News Dataset from Kaggle
    Original Columns: title, text, subject, date, label
    
    Attributes Used:
    - title: News article title (KEPT)
    - text: News article content (KEPT)
    - label: FAKE/REAL classification (KEPT)
    
    Attributes Dropped:
    - subject: News category/topic (DROPPED - not needed for text classification)
    - date: Publication date (DROPPED - temporal features not used)
    
    Returns:
        Tuple of (features DataFrame with 'combined' column, labels Series).
    """
    # Check if dataset exists locally
    if not DATA_PATH.exists():
        print(f"Dataset not found at {DATA_PATH}")
        print("Attempting to download from public source...")
        try:
            download_kaggle_dataset()
        except Exception as e:
            raise FileNotFoundError(
                f"Could not download dataset. Please manually download 'fake_or_real_news.csv' "
                f"from Kaggle and place it in {DATA_DIR}. Error: {e}"
            )
    
    print(f"Loading dataset from {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    
    # Display original dataset info
    print(f"\n[DATASET INFO]")
    print(f"   Total rows: {len(df)}")
    print(f"   Columns: {list(df.columns)}")
    print(f"   Missing values per column:")
    for col in df.columns:
        missing = df[col].isna().sum()
        if missing > 0:
            print(f"      {col}: {missing} ({missing/len(df)*100:.1f}%)")
    
    # Handle label column (common names: label, type, class)
    if "label" in df.columns:
        labels = df["label"]
    elif "type" in df.columns:
        labels = df["type"]
    elif "class" in df.columns:
        labels = df["class"]
    else:
        raise ValueError(
            f"Dataset must have 'label', 'type', or 'class' column. "
            f"Found columns: {list(df.columns)}"
        )
    
    # Combine title + text for features
    # This is the main feature engineering step
    if "title" in df.columns and "text" in df.columns:
        print("\n[FEATURE ENGINEERING]")
        print("   Combining 'title' + 'text' columns into 'combined' feature")
        df["combined"] = df["title"].fillna("") + " " + df["text"].fillna("")
    elif "text" in df.columns:
        print("\n[FEATURE ENGINEERING]")
        print("   Using 'text' column as feature")
        df["combined"] = df["text"].fillna("")
    elif "title" in df.columns:
        print("\n[FEATURE ENGINEERING]")
        print("   Using 'title' column as feature")
        df["combined"] = df["title"].fillna("")
    else:
        raise ValueError(
            f"Dataset must have 'text' or 'title' column. "
            f"Found columns: {list(df.columns)}"
        )
    
    # Normalize labels to FAKE/REAL
    print("\n[LABEL PROCESSING]")
    print(f"   Original label distribution:")
    print(f"   {labels.value_counts().to_dict()}")
    
    labels = labels.str.upper().str.strip()
    # Handle various label formats
    label_mapping = {
        "FAKE": "FAKE",
        "REAL": "REAL",
        "0": "FAKE",  # Some datasets use 0/1
        "1": "REAL",
        "FALSE": "FAKE",
        "TRUE": "REAL",
    }
    labels = labels.replace(label_mapping)
    
    # Filter valid labels
    valid = labels.isin(["FAKE", "REAL"])
    invalid_count = (~valid).sum()
    if invalid_count > 0:
        print(f"   [WARNING] Dropping {invalid_count} rows with invalid labels")
    
    df = df[valid].reset_index(drop=True)
    labels = labels[valid].reset_index(drop=True)
    
    print(f"   Final label distribution:")
    print(f"   {labels.value_counts().to_dict()}")
    print(f"   Total valid rows from Source 1: {len(df)}")
    
    dfs_to_concat = []
    df1_final = pd.DataFrame({"combined": df["combined"], "label": labels})
    dfs_to_concat.append(df1_final)
    
    # LOAD SOURCE 2: Fake.csv
    fake_path = DATA_DIR / "Fake.csv"
    if fake_path.exists():
        print(f"\n[LOADING] Source 2: {fake_path.name}")
        df_fake = pd.read_csv(fake_path)
        title_col = df_fake["title"].fillna("") if "title" in df_fake.columns else ""
        text_col = df_fake["text"].fillna("") if "text" in df_fake.columns else ""
        df_fake["combined"] = title_col + " " + text_col
        df_fake["label"] = "FAKE"
        dfs_to_concat.append(df_fake[["combined", "label"]])
        print(f"   Added {len(df_fake)} FAKE rows.")
        
    # LOAD SOURCE 3: True.csv
    true_path = DATA_DIR / "True.csv"
    if true_path.exists():
        print(f"\n[LOADING] Source 3: {true_path.name}")
        df_true = pd.read_csv(true_path)
        title_col = df_true["title"].fillna("") if "title" in df_true.columns else ""
        text_col = df_true["text"].fillna("") if "text" in df_true.columns else ""
        df_true["combined"] = title_col + " " + text_col
        df_true["label"] = "REAL"
        dfs_to_concat.append(df_true[["combined", "label"]])
        print(f"   Added {len(df_true)} REAL rows.")
        
    # DOMAIN INJECTION: 147 Curated Examples
    print("\n[DOMAIN INJECTION] Generating 147 curated live-news examples...")
    domains = ["BBC", "CNN", "Reuters", "Associated Press", "Fox News", "breaking news", "live stream", "update", "NPR", "New York Times"]
    templates = [
        "{} reports that the situation is currently developing rapidly.",
        "Live from {}: breaking coverage on today's top story.",
        "According to {}, officials have issued a new statement.",
        "{} News Update: Key witnesses are testifying right now.",
        "Just in from {}: Markets are responding to the latest data.",
        "{} correspondents are on the ground providing live updates."
    ]
    injections = []
    import random
    rng = random.Random(42)
    for _ in range(147):
        domain = rng.choice(domains)
        template = rng.choice(templates)
        injections.append({"combined": template.format(domain), "label": "REAL"})
        
    df_inj = pd.DataFrame(injections)
    dfs_to_concat.append(df_inj)
    print(f"   Injected exactly 147 REAL domain rows.")
    
    # COMBINE ALL SOURCES
    final_df = pd.concat(dfs_to_concat, ignore_index=True)
    
    # MONGODB INTEGRATION: Load Admin-Resolved Disputes
    import pymongo
    import os
    print("\n[MONGODB INTEGRATION] Fetching resolved disputes...")
    try:
        mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        client = pymongo.MongoClient(mongo_uri, serverSelectionTimeoutMS=2000)
        db = client["truthlens"]
        disputes_col = db["disputes"]
        resolved_disputes = list(disputes_col.find({"status": "resolved"}))
        
        dispute_rows = []
        for d in resolved_disputes:
            if "correct_label" in d and d["correct_label"] in ["REAL", "FAKE"] and "input_text" in d:
                dispute_rows.append({
                    "combined": d["input_text"],
                    "label": d["correct_label"]
                })
                
        if dispute_rows:
            df_disputes = pd.DataFrame(dispute_rows)
            final_df = pd.concat([final_df, df_disputes], ignore_index=True)
            print(f"   Successfully integrated {len(dispute_rows)} verified dispute records.")
        else:
            print("   No valid resolved disputes with a 'correct_label' were found.")
            
    except Exception as e:
        print(f"   [WARNING] Failed to fetch disputes from MongoDB: {e}")

    print(f"\n[FINAL DATASET SIZE] {len(final_df)} total rows assembled.")
    print(f"   Combined distribution: {final_df['label'].value_counts().to_dict()}")

    # Return only the combined text feature and labels
    return final_df[["combined"]], final_df["label"]


def train_and_save() -> None:
    """Load data, preprocess, optionally augment, train model, and save artifacts."""
    df, labels = load_or_create_dataset()

    # Preprocess
    print("\nPreprocessing text...")
    print(f"   Processing {len(df)} rows (this may take a few minutes)...")
    
    # Use tqdm for progress bar if available, otherwise use simple counter
    try:
        from tqdm import tqdm
        tqdm.pandas(desc="Preprocessing")
        X = df["combined"].progress_apply(preprocess_text)
    except ImportError:
        # Fallback: process in chunks with progress updates
        chunk_size = max(1000, len(df) // 20)  # Show ~20 progress updates
        processed_chunks = []
        for i in range(0, len(df), chunk_size):
            chunk = df["combined"].iloc[i:i+chunk_size].apply(preprocess_text)
            processed_chunks.append(chunk)
            progress = min(100, int((i + chunk_size) / len(df) * 100))
            print(f"   Progress: {progress}% ({min(i+chunk_size, len(df))}/{len(df)} rows)", end="\r")
        X = pd.concat(processed_chunks, ignore_index=True)
        print()  # New line after progress

    # Augment short-text examples to improve robustness for very short inputs
    short_variant = X.apply(lambda s: " ".join(s.split()[:12]) if isinstance(s, str) else "")
    n_aug = max(0, int(len(X) * 0.15))  # add ~15% short variants
    if n_aug > 0:
        valid_idx = short_variant[short_variant.str.strip().astype(bool)].index
        if len(valid_idx) == 0:
            print("No candidates for short-variant augmentation; skipping augmentation.")
        else:
            n_sample = min(n_aug, len(valid_idx))
            sampled_idx = pd.Series(valid_idx).sample(n=n_sample, random_state=42).values
            short_sample = short_variant.loc[sampled_idx].reset_index(drop=True)
            label_sample = labels.loc[sampled_idx].reset_index(drop=True)
            X = pd.concat([X.reset_index(drop=True), short_sample], ignore_index=True)
            labels = pd.concat([labels.reset_index(drop=True), label_sample], ignore_index=True)
            print(f"Augmented dataset with {n_sample} short-variant rows (total now {len(X)})")

    assert len(X) == len(labels), "Feature/label length mismatch after augmentation"

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, labels, test_size=0.2, random_state=42, stratify=labels
    )

    # TF-IDF Vectorization (combine word + character n-grams)
    print("Vectorizing with TF-IDF (word + char n-grams)...")
    vectorizer = FeatureUnion([
        ("word", TfidfVectorizer(max_features=4000, ngram_range=(1, 2), analyzer="word")),
        ("char", TfidfVectorizer(max_features=2000, ngram_range=(3, 5), analyzer="char_wb")),
    ])
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # Train Logistic Regression with class weighting and calibrate probabilities
    print("Training Logistic Regression (class_weight='balanced') and calibrating probabilities...")
    base_clf = LogisticRegression(max_iter=1000, random_state=42, class_weight="balanced")
    # Calibrate to get better probability estimates (helps threshold tuning)
    model = CalibratedClassifierCV(base_clf, cv=3)
    model.fit(X_train_vec, y_train)

    # Evaluate
    y_pred = model.predict(X_test_vec)
    y_proba = model.predict_proba(X_test_vec)[:, 1]  # probability for label 'REAL'
    accuracy = (y_pred == y_test).mean()
    roc_auc = roc_auc_score(y_test.map({'FAKE':0,'REAL':1}), y_proba)
    print(f"Test Accuracy: {accuracy:.4f}")
    print(f"Test ROC AUC: {roc_auc:.4f}")

    print("\nClassification report:")
    print(classification_report(y_test, y_pred, digits=4))

    print("Confusion matrix (rows=true, cols=pred):")
    print(confusion_matrix(y_test, y_pred))

    # Threshold tuning: pick probability threshold that maximizes F1 on validation test set
    try:
        # Map labels to binary for PR curve
        y_test_bin = y_test.map({'FAKE':0,'REAL':1})
        precisions, recalls, thresholds = precision_recall_curve(y_test_bin, y_proba)
        f1_scores = 2 * (precisions * recalls) / (precisions + recalls + 1e-12)
        best_idx = f1_scores.argmax()
        if best_idx < len(thresholds):
            best_threshold = float(thresholds[best_idx])
        else:
            best_threshold = 0.5
        best_f1 = float(f1_scores[best_idx])
        print(f"Best threshold by F1 on test set: {best_threshold:.3f} (F1={best_f1:.4f})")
    except Exception:
        best_threshold = 0.5

    # Save artifacts
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    with open(VECTORIZER_PATH, "wb") as f:
        pickle.dump(vectorizer, f)
    # Persist chosen threshold for downstream scripts/consumers
    THRESHOLD_PATH = ARTIFACTS_DIR / "threshold.txt"
    try:
        with open(THRESHOLD_PATH, "w") as f:
            f.write(str(best_threshold))
        print(f"Saved threshold to {THRESHOLD_PATH}")
    except Exception:
        pass

    print(f"Model saved to {MODEL_PATH}")
    print(f"Vectorizer saved to {VECTORIZER_PATH}")


if __name__ == "__main__":
    train_and_save()
