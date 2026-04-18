"""
Run a curated set of updated sample texts through the saved model and print predictions.
"""
from pathlib import Path
import pickle
import textwrap
import sys

# ensure project root on path for local imports
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ml.train_model import preprocess_text

ARTIFACTS = Path(__file__).resolve().parents[1] / 'artifacts'
MODEL_PATH = ARTIFACTS / 'model.pkl'
VECTORIZER_PATH = ARTIFACTS / 'vectorizer.pkl'

with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)
with open(VECTORIZER_PATH, 'rb') as f:
    vectorizer = pickle.load(f)

SAMPLES = [
    {"expected": "FAKE", "name": "Sensational health claim", "text": "BREAKING: New clinical trial proves turmeric extract cures Alzheimer's in 48 hours — major pharma companies are suppressing the data. Patients recovered fully in an unnamed \"secret study\"; doctors are calling this a miracle. Share to save a life!"},
    {"expected": "FAKE", "name": "Fabricated political leak", "text": "Leaked memo reveals top officials planned last year's vote-rigging strategy. An anonymous insider provided documents showing coordinated tampering and cover-ups that will shock the nation. This should be front-page news — they are hiding the truth."},
    {"expected": "FAKE", "name": "Get-rich scam", "text": "Make $5,000 per week with this one click trading secret — risk-free algorithm used by hedge funds. Deposit $50 today and double your money in days. Limited spots available."},
    {"expected": "REAL", "name": "Tech product announcement", "text": "Tech startup announces new AI-assisted camera phone with 200MP sensor and 48-hour battery benchmark. Company CEO Maria Alvarez said, \"We focused on battery and computational photography improvements.\" Pre-orders open April 15; MSRP $899."},
    {"expected": "REAL", "name": "Infrastructure funding", "text": "The Department of Transportation approved a $125 million grant to repair the Oakridge bridge. Transportation Secretary said the funds will \"accelerate construction and improve safety\"; work begins June 2026 with completion expected in 18 months."},
    {"expected": "MIXED", "name": "Satire (edge)", "text": "Satire: Mayor pledges to replace all streetlights with glittering disco balls to \"boost civic morale.\" The city clarifies the story is a joke on April Fools' Day."},
    {"expected": "MIXED", "name": "Early breaking (edge)", "text": "Breaking: Emergency responders on scene after multiple-vehicle collision on I-95. Unconfirmed reports indicate several injuries; authorities urge drivers to avoid the area while investigations continue."},
    {"expected": "FAKE", "name": "Very short scam (FAKE)", "text": "Miracle pill reverses aging overnight! Click here to buy!"},
]

LINE = '-' * 90
print('\n' + LINE)
print('RUN: Predictions for updated sample texts')
print(LINE + '\n')

for s in SAMPLES:
    txt = s['text']
    proc = preprocess_text(txt)
    vec = vectorizer.transform([proc])
    proba = model.predict_proba(vec)[0]
    pred = model.predict(vec)[0]
    conf = float(max(proba))

    print(f"Name: {s['name']}")
    print(f"Expected (curated): {s['expected']}")
    print(f"Prediction: {pred}  |  Confidence: {conf:.4f}")
    print(f"Probability => FAKE: {proba[0]:.4f}  |  REAL: {proba[1]:.4f}")
    print('Text:')
    print(textwrap.fill(txt, width=100))
    print(LINE + '\n')

print('Done.')
