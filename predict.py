import pickle
import os
import re
from text_preprocess import clean_text

# Get current file directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load model safely
model_path = os.path.join(BASE_DIR, "model", "phishing_model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "model", "vectorizer.pkl")

model = pickle.load(open(model_path, "rb"))
vectorizer = pickle.load(open(vectorizer_path, "rb"))

# 🔹 Main prediction function
def predict_email(text):
    cleaned = clean_text(text)
    vector = vectorizer.transform([cleaned])
    
    prediction = model.predict(vector)[0]
    probability = model.predict_proba(vector)[0].max()

    return prediction, probability

# 🔹 Detect suspicious keywords
def check_keywords(text):
    suspicious_words = [
        "urgent", "verify", "password", "bank",
        "click", "login", "account", "update",
        "free", "win", "prize"
    ]
    found = [word for word in suspicious_words if word in text.lower()]
    return found

# 🔹 Detect URLs in email
def detect_urls(text):
    urls = re.findall(r'https?://\S+|www\.\S+', text)
    return urls