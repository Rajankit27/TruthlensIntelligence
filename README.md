# 🔍 TruthLens Intelligence

> **AI-Powered Fake News Detection System**
> Detect and verify news articles using advanced Machine Learning and Natural Language Processing.

---

## 🌟 Overview

**TruthLens Intelligence** is a comprehensive fake news detection platform designed to identify and verify the authenticity of news content. In an era of rampant misinformation, TruthLens provides users with a reliable tool to distinguish between factual reporting and deceptive fabrications.

The system utilizes machine learning models to analyze linguistic patterns, source reputation, and real-time data to provide a **REAL** or **FAKE** verdict with a calibrated confidence score.

---

## ✨ Features

- **Fake vs Real News Classification**: High-accuracy detection using a calibrated Logistic Regression model.
- **Multiple News Source Verification**: Support for both raw text analysis and direct news URL scraping.
- **Explainable AI (XAI)**: Highlights the top "impact words" that influenced the model's prediction.
- **Clean UI Interface**: Modern dark-mode dashboard with real-time feedback and animations.
- **Admin Panel**: A centralized console for user management, dispute resolution, and 1-click model retraining.
- **Fast Prediction System**: Efficient preprocessing and inference pipeline for near-instant results.
- **Live Intelligence Feed**: Real-time rotating headlines from trusted global news sources (BBC).

---

## 🛠️ Tech Stack

- **Backend**: Python 3.11+, [Flask](https://flask.palletsprojects.com/) (REST API)
- **Machine Learning**: [scikit-learn](https://scikit-learn.org/), [NLTK](https://www.nltk.org/) (NLP Preprocessing)
- **Data Handling**: [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
- **Frontend**: Vanilla HTML5, CSS3 (Glassmorphism), Vanilla JavaScript
- **Database**: [MongoDB](https://www.mongodb.com/) (History & Disputes), [SQLite](https://www.sqlite.org/) (User Auth)
- **Scraping**: BeautifulSoup4, Requests

---

## 📊 Dataset

⚠️ **Note**: Dataset is not included in this repository due to GitHub file size limitations.

Please download the **Fake and Real News Dataset** from Kaggle:
👉 [Download Dataset on Kaggle](https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset)

### Setup Instructions:
1. Download the `Fake.csv` and `True.csv` files.
2. Place them inside the following directory:
   ```text
   TruthLens-AI/data/
   ```

---

## 🚀 How to Run

Follow these steps to set up the project locally:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Rajankit27/TruthlensIntelligence.git
   cd TruthlensIntelligence
   ```

2. **Install requirements**:
   ```bash
   pip install -r TruthLens-AI/requirements.txt
   ```

3. **Download and place dataset**:
   (See the [Dataset](#-dataset) section above).

4. **Train the initial model**:
   ```bash
   python TruthLens-AI/ml/train_model.py
   ```

5. **Run the application**:
   ```bash
   python TruthLens-AI/backend/app.py
   ```
   *The application will be available at:* `http://localhost:5002`

---

## 📁 Project Structure

```text
TruthLens-AI/
├── artifacts/          # Trained model and vectorizer pkl files
├── backend/            # Flask API, Auth, and Admin logic
├── data/               # Place your CSV datasets here (Fake.csv / True.csv)
├── ml/                 # ML Training pipeline and NLP preprocessing
├── static/             # CSS design system and Frontend JS
├── templates/          # HTML pages (Dashboard, Admin, Auth, etc.)
├── docs/               # Detailed technical documentation
└── scripts/            # Utility scripts for maintenance
```

---

## 📸 Screenshots

### Dashboard UI
<img src="screenshots/dashboard1.png" width="500"/>
<img src="screenshots/dashboard2.png" width="500"/>

### Analysis Result
<img src="screenshots/real-news.png" width="500"/>

### Admin Panel Overview
<img src="screenshots/admin-dashboard.png" width="500"/>
---

## 🔮 Future Improvements

- **Real-time API Integration**: Connect with news APIs (GNews, NewsAPI) for broader live verification.
- **Deep Learning Upgrade**: Transition from Logistic Regression to Transformer-based models (BERT/RoBERTa) for higher accuracy.
- **Multi-lingual Support**: Expand detection capabilities to languages beyond English.
- **Browser Extension**: A Chrome/Firefox extension for on-the-go news verification.

---

## 👤 Author

**AnkitRaj**
- GitHub: [@Rajankit27](https://github.com/Rajankit27)
- Project: TruthLens Intelligence

---
*Developed for academic demonstration and advanced news integrity research.*
