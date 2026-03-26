import os
import pickle
import re
from text_preprocess import clean_text

# ✅ Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "model", "phishing_model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "model", "vectorizer.pkl")

# ✅ Safe loading
model = None
vectorizer = None

try:
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    with open(vectorizer_path, "rb") as f:
        vectorizer = pickle.load(f)

except Exception as e:
    print("❌ Model loading error:", e)

# ---------------- PREDICT ----------------
def predict_email(text):
    if model is None or vectorizer is None:
        return 0, 0.0   # fallback

    cleaned = clean_text(text)
    vector = vectorizer.transform([cleaned])

    prediction = model.predict(vector)[0]
    probability = model.predict_proba(vector)[0].max()

    return prediction, probability

# ---------------- KEYWORDS ----------------
def check_keywords(text):
    keywords = ["urgent", "bank", "password", "click", "verify", "login"]
    found = [word for word in keywords if word in text.lower()]
    return found

# ---------------- URL DETECTION ----------------
def detect_urls(text):
    urls = re.findall(r'(https?://\S+)', text)
    return urls