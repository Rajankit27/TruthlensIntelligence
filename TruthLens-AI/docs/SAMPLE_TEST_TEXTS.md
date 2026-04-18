# Sample Test Texts for TruthLens Intelligence

Use these sample texts to test the fake news detection system. Copy and paste them into the web interface or use them with the API.

---

## UPDATED — Dataset-driven sample texts (derived from latest dataset)

The examples below are curated to reflect topics, language patterns and edge-cases present in the updated training dataset (politics, health, technology, finance, sports, weather, satire). Use these to exercise the model across realistic and adversarial inputs.

### FAKE — dataset-style examples

#### 1) Sensational health claim (FAKE)
```
BREAKING: New clinical trial proves turmeric extract cures Alzheimer's in 48 hours — major pharma companies are suppressing the data. Patients recovered fully in an unnamed "secret study"; doctors are calling this a miracle. Share to save a life!
```

#### 2) Fabricated political leak (FAKE)
```
Leaked memo reveals top officials planned last year's vote-rigging strategy. An anonymous insider provided documents showing coordinated tampering and cover-ups that will shock the nation. This should be front-page news — they are hiding the truth.
```

#### 3) Celebrity hoax (FAKE)
```
URGENT: Global superstar reported dead after private accident — family refuses to comment. Fans are devastated; multiple unverified accounts confirm the tragic loss. Share to honor their legacy.
```

#### 4) Get-rich / financial scam (FAKE)
```
Make $5,000 per week with this one click trading secret — risk-free algorithm used by hedge funds. Deposit $50 today and double your money in days. Limited spots available.
```

#### 5) Pseudo‑science breakthrough (FAKE)
```
Scientists say they can reverse aging using a single injection — trial data shows 100% reversal of cellular age. Major journals refuse to publish because "it's too disruptive." Book your appointment now.
```

#### 6) Conspiracy / sensational tech claim (FAKE)
```
Your smartphone is secretly recording your thoughts with a hidden microphone chip — a whistleblower leaked firmware proving mind‑control is already being deployed. Delete your apps now!
```

#### 7) Misattributed authority/statistics (FAKE)
```
CDC study: vaccinated people are 3x more likely to develop heart disease — official figures suppressed. Public health agencies refuse to comment while hospital admissions spike.
```

#### 8) Fabricated disaster alert (FAKE)
```
ALERT: Major tsunami expected to hit inland metropolitan area tonight — officials issued emergency text ordering immediate evacuation. Roads will be closed in two hours.
```

#### 9) Political clickbait (FAKE)
```
Donald Trump Sends Out Embarrassing New Year’s Eve Message; This is Disturbing

Donald Trump just couldn’t wish all Americans a Happy New Year and leave it at that. Instead, he had to give a shout out to his enemies, haters and the very dishonest "fake news" media — exaggerated language and partisan framing intended to provoke shares and outrage.
```

---

### REAL — dataset-style examples

#### 1) Technology product announcement (REAL)
```
Tech startup announces new AI-assisted camera phone with 200MP sensor and 48-hour battery benchmark. Company CEO Maria Alvarez said, "We focused on battery and computational photography improvements." Pre-orders open April 15; MSRP $899.
```

#### 2) Government funding & infrastructure (REAL)
```
The Department of Transportation approved a $125 million grant to repair the Oakridge bridge. Transportation Secretary said the funds will "accelerate construction and improve safety"; work begins June 2026 with completion expected in 18 months.
```

#### 3) Peer‑reviewed study summary (REAL)
```
Researchers published a peer‑reviewed trial in the Journal of Clinical Medicine showing a 28% reduction in symptoms for a new chronic pain therapy. The randomized trial involved 420 participants over 12 months and passed independent safety review.
```

#### 4) Economic indicator release (REAL)
```
National statistics office reports Q4 GDP growth of 2.1% year‑over‑year, unemployment steady at 4.3%. Analysts cite resilient consumer spending and stronger export demand as drivers of growth.
```

#### 5) Weather advisory from official agency (REAL)
```
National Weather Service issues flood advisory for Riverside County through Saturday evening. Local authorities advise residents in low‑lying areas to prepare for possible evacuations; shelters will open at 1400 UTC.
```

#### 6) Sports signing with sourced quote (REAL)
```
Midfielder signs three‑year contract with City United for an undisclosed fee. Coach said, "We're excited to welcome a player with proven creativity and work rate." The transfer will be finalized after the medical.
```

#### 7) Corporate earnings report (REAL)
```
Quarterly earnings: Acme Corp reports revenue of $2.4B, up 11% YoY; EPS $1.12 beating analyst estimates. Company cited increased enterprise demand for its cloud services.
```

#### 8) Local public announcement (REAL)
```
City council approves zoning changes for downtown revitalization. Public consultation will begin next month and funding includes a $2M renovation grant for small businesses.
```

#### 9) Reuters-style report (REAL)
```
As U.S. budget fight looms, Republicans flip their fiscal script

WASHINGTON (Reuters) - The head of a conservative Republican faction in the U.S. Congress urged budget restraint and signaled a pivot on federal spending; lawmakers will begin trying to pass a federal budget when they return from the holidays.
```

---

### MIXED / EDGE CASES (use for calibration)

#### 1) Satire (likely FAKE by content, but intentionally humorous)
```
Satire: Mayor pledges to replace all streetlights with glittering disco balls to "boost civic morale." The city clarifies the story is a joke on April Fools' Day.
```

#### 2) Opinion / Editorial (ambiguous label)
```
Opinion: While new regulations aim to improve safety, they may also increase costs for small manufacturers. The author advocates for targeted subsidies to ease the transition.
```

#### 3) Early breaking report (ambiguous until verified)
```
Breaking: Emergency responders on scene after multiple-vehicle collision on I-95. Unconfirmed reports indicate several injuries; authorities urge drivers to avoid the area while investigations continue.
```

#### 4) Short social-media rumor (ambiguous)
```
Rumor: Local hospital postponing all elective surgeries due to staffing shortages — no official statement yet.
```

---

### Short test cases (quick checks)

- Very short (FAKE)
```
Miracle pill reverses aging overnight! Click here to buy!
```

- Very short (REAL)
```
School board meeting scheduled Thursday to discuss curriculum changes.
```

- Medium ambiguous (edge)
```
Claims circulate that a new campus policy will ban student laptops; university spokesperson says policy is under review and no changes are finalized.
```

---

## How to use these updated examples

- Paste any example into the web UI or send to `/predict` via API.
- Expected: clear FAKE/REAL examples → model prediction should match label with confidence ≥ 0.6.
- Edge cases (satire, early breaking) may return lower confidence — use for calibration and human review.

---

## FAKE News Examples

### Example 1: Sensational Health Claim
```
Scientists discover miracle cure for cancer in secret government lab. The FDA is hiding this breakthrough from the public because big pharma doesn't want you to know. This natural remedy has been proven to eliminate all cancer cells in just 24 hours. Share this immediately before they delete it!
```

### Example 2: Conspiracy Theory
```
BREAKING: Government officials have been secretly meeting with aliens for decades. A whistleblower just leaked classified documents proving that the moon landing was faked and NASA has been covering it up. The truth is finally coming out! This will change everything you know about space.
```

### Example 3: Celebrity Death Hoax
```
URGENT: Famous actor dies in tragic accident! Sources close to the family confirm that the beloved star passed away suddenly last night. The media is trying to keep this quiet, but we have exclusive photos. Prayers for the family. Share if you care!
```

### Example 4: Financial Scam
```
Make $10,000 in one week working from home! This secret method has been banned by banks because it's too effective. Click here to learn how to get rich quick using this one simple trick. No experience needed, just follow these steps and watch the money roll in!
```

### Example 5: Political Misinformation
```
Shocking revelation: Politician caught in massive scandal! Insider sources reveal that elected officials have been accepting bribes and hiding money offshore. The mainstream media won't report this, but we have the documents. Spread the word before they silence us!
```

---

## REAL News Examples

### Example 1: Technology News
```
Tech company announces new smartphone with advanced camera features. The device includes a 108-megapixel main camera and improved battery life. Pre-orders begin next month, with shipping expected in the following quarter. Industry analysts predict strong sales based on early reviews.
```

### Example 2: Economic Report
```
Federal Reserve releases quarterly economic growth report showing 2.3% increase in GDP. The report indicates steady job growth and controlled inflation rates. Economists note that the economy is performing better than initial projections, with unemployment at historic lows.
```

### Example 3: Scientific Study
```
Researchers publish peer-reviewed study in scientific journal demonstrating new treatment method for diabetes. The clinical trial involved 500 participants over 18 months, showing significant improvement in blood sugar control. The study has been reviewed by independent medical experts and published in a reputable journal.
```

### Example 4: Weather Report
```
National Weather Service issues forecast for the upcoming week. Meteorologists predict sunny skies with temperatures ranging from 70 to 75 degrees Fahrenheit. The forecast is based on satellite data and computer models, with high confidence levels for the next five days.
```

### Example 5: Sports News
```
Professional sports team announces new head coach after extensive search process. The organization conducted interviews with multiple candidates and selected an experienced coach with a proven track record. The new coach will begin duties immediately, with the first game scheduled for next month.
```

---

## Mixed Examples (Test Edge Cases)

### Example 1: Satirical News (May be detected as FAKE)
```
Local man discovers that his pet goldfish can solve complex math problems. Scientists are baffled as the fish correctly answered calculus questions faster than a computer. The man plans to enter his fish in the next mathematics competition.
```

### Example 2: Opinion Piece (May vary)
```
Editorial: Recent policy changes have sparked debate among citizens. While some argue the changes are necessary for progress, others express concern about potential impacts. The discussion continues as lawmakers review public feedback and consider amendments.
```

### Example 3: Breaking News (Should be REAL)
```
Emergency services respond to major highway accident involving multiple vehicles. Authorities report several injuries but no fatalities. Traffic is being diverted as cleanup and investigation continue. Updates will be provided as more information becomes available.
```

---

## Short Test Cases

### Very Short Text (FAKE)
```
Amazing discovery! Scientists found the fountain of youth! Click now to learn the secret!
```

### Very Short Text (REAL)
```
City council meeting scheduled for Tuesday evening to discuss budget proposals.
```

### Live Domain Bias Check (REAL)
```
Live from BBC World Service: Markets are anticipating a major policy shift following the latest statements from the European Central Bank. Correspondents are on the ground providing live updates.
```

### Medium Length (FAKE)
```
You won't believe what happened! A secret government program has been monitoring your thoughts through your smartphone. They're using advanced technology to read your mind and control your decisions. This is why you feel tired all the time - it's not natural, it's mind control! Share this before they delete it!
```

### Medium Length (REAL)
```
Local university announces new scholarship program for students pursuing degrees in science and technology. The program will provide full tuition coverage for 50 students annually, with applications opening next semester. The scholarship is funded by a partnership between the university and several technology companies.
```

---

## How to Use These Examples

### Method 1: Web Interface
1. Start the Flask server: `py backend/app.py`
2. Open browser: http://localhost:5000
3. Copy any example text above
4. Paste into the text area
5. Click "Verify News"
6. View results (FAKE/REAL with confidence score)

### Method 2: API Testing (curl)
```bash
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d "{\"text\":\"Your sample text here\"}"
```

### Method 3: Python Script
```python
import requests

url = "http://localhost:5000/predict"
data = {"text": "Your sample text here"}
response = requests.post(url, json=data)
print(response.json())
```

---

## Expected Results

- **FAKE examples** should show: `"prediction": "FAKE"` with confidence > 0.5
- **REAL examples** should show: `"prediction": "REAL"` with confidence > 0.5
- **Confidence scores** typically range from 0.7 to 0.95 for clear cases
- **Edge cases** (satire, opinion) may have lower confidence scores

---

## Tips for Testing

1. **Test both categories** - Try FAKE and REAL examples
2. **Vary text length** - Test short, medium, and long articles
3. **Check edge cases** - Satirical content, opinion pieces
4. **Monitor confidence** - Higher confidence = more certain prediction
5. **Compare results** - See how different writing styles are classified

---

## Notes

- **Training Volume**: The model was trained on **~90,893** articles (TruthLens Triple-Source Super-Dataset).
- **Dataset Balance**: Mathematically balanced at **51% FAKE / 49% REAL**.
- **Bias Resistance**: Features live-domain synthetic injections (BBC, CNN, AP) so the AI correctly identifies modern breaking news without relying on legacy publisher boilerplates.
- Model focuses on deep linguistic semantic patterns, not real-time fact-checking.
- Results may vary for purely ambiguous or extremely short clickbait.
