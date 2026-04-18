# TruthLens Intelligence — Review 2 Command Reference

This document contains all the terminal commands needed to run, test, and re-train the TruthLens AI platform. You can copy and paste these directly into your Windows Terminal / PowerShell.

---

## 1. System Startup

### Step 1: Ensure MongoDB is Running
MongoDB must be active to log your history and store user accounts. If it's installed as a Windows Service, it should already be running. If not, start it manually:
```powershell
mongod
```

### Step 2: Activate the Python Environment
Always ensure your virtual environment is active before running Python scripts.
```powershell
.\venv\Scripts\activate
```

### Step 3: Start the Backend Server
This will start the Flask server on port 5000. It will automatically load the Machine Learning `.pkl` files and connect to MongoDB.
```powershell
python backend\app.py
```

---

## 2. API Testing Commands (cURL)

You can test the backend directly from a new terminal window to ensure the API is responding correctly.

### 1. Register a New User
```powershell
curl -X POST http://127.0.0.1:5000/auth/register `
     -H "Content-Type: application/json" `
     -d "{\"username\": \"Reviewer2\", \"password\": \"secure123\"}"
```

### 2. Login to Get JWT Token
Running this command will return your `access_token`. You must copy that token to use in the subsequent requests!
```powershell
curl -X POST http://127.0.0.1:5000/auth/login `
     -H "Content-Type: application/json" `
     -d "{\"username\": \"Reviewer2\", \"password\": \"secure123\"}"
```

### 3. Test Text Prediction (Requires Token)
*Replace `<YOUR_TOKEN_HERE>` with the token you received in the previous step.*
```powershell
curl -X POST http://127.0.0.1:5000/predict `
     -H "Content-Type: application/json" `
     -H "Authorization: Bearer <YOUR_TOKEN_HERE>" `
     -d "{\"text\": \"Live from BBC World Service: Markets are anticipating a major policy shift following the latest statements. Correspondents are on the ground providing live updates.\"}"
```

### 4. Test URL Analysis (Requires Token)
```powershell
curl -X POST http://127.0.0.1:5000/analyze/url `
     -H "Content-Type: application/json" `
     -H "Authorization: Bearer <YOUR_TOKEN_HERE>" `
     -d "{\"url\": \"https://www.bbc.com/news/live/world\"}"
```

### 5. Fetch Your Intelligence Log (Requires Token)
```powershell
curl -X GET http://127.0.0.1:5000/history `
     -H "Authorization: Bearer <YOUR_TOKEN_HERE>"
```

### 6. Fetch Live Global News Ticker (No Token Needed)
```powershell
curl -X GET http://127.0.0.1:5000/news/global
```

---

## 3. Retraining the Machine Learning Model

If you ever add new data to `data/fake_or_real_news.csv`, `data/Fake.csv`, or `data/True.csv`, or if you simply want to force the system to recalculate its bias thresholds, run the Model Training script.

*(Note: Ensure your virtual environment is active before running this!)*

```powershell
# This will concatenate all dataset files, inject the live-domain debiasing anchors, 
# retrain the TF-IDF Vectorizer, and calculate the optimal dynamic threshold.
# Note: It may take 10-15 minutes to lemmatize all ~90,000 documents!
python ml\train_model.py
```
