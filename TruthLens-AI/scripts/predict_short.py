import sys
import pickle
from pathlib import Path
# Ensure project root is on sys.path so local packages (ml) can be imported
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ml.train_model import preprocess_text

ARTIFACTS = Path(__file__).resolve().parents[1] / 'artifacts'
M = pickle.load(open(ARTIFACTS / 'model.pkl','rb'))
V = pickle.load(open(ARTIFACTS / 'vectorizer.pkl','rb'))
text = "City council meeting scheduled for Tuesday evening to discuss budget proposals."
proc = preprocess_text(text)
vec = V.transform([proc])
proba = M.predict_proba(vec)[0]
print('Original:', text)
print('Preprocessed:', repr(proc))
print('Prediction probs: FAKE={:.4f}, REAL={:.4f}'.format(proba[0], proba[1]))
print('Confidence (max): {:.4f}'.format(max(proba)))
