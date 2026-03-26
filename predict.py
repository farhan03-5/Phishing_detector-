import pickle
import os
from text_preprocess import clean_text

# ✅ FIXED PATH (WORKS IN DEPLOY)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "model", "phishing_model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "model", "vectorizer.pkl")

# ✅ LOAD FILES SAFELY
model = pickle.load(open(model_path, "rb"))
vectorizer = pickle.load(open(vectorizer_path, "rb"))


def predict_email(text):
    cleaned = clean_text(text)
    vector = vectorizer.transform([cleaned])

    prediction = model.predict(vector)[0]
    probability = model.predict_proba(vector)[0].max()

    return prediction, probability
