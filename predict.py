import pickle
import os
from text_preprocess import clean_text

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "model", "phishing_model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "model", "vectorizer.pkl")

# ✅ SAFE LOAD
try:
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    with open(vectorizer_path, "rb") as f:
        vectorizer = pickle.load(f)

except Exception as e:
    raise Exception(f"❌ Model loading failed: {str(e)}")


def predict_email(text):
    cleaned = clean_text(text)
    vector = vectorizer.transform([cleaned])

    prediction = model.predict(vector)[0]
    probability = model.predict_proba(vector)[0].max()

    return prediction, probability