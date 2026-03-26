import pickle
import os
from text_preprocess import clean_text

# ✅ Get current directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ✅ Correct paths
model_path = os.path.join(BASE_DIR, "model", "phishing_model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "model", "vectorizer.pkl")

# 🔥 DEBUG (will show in logs)
print("Model path:", model_path)
print("Exists:", os.path.exists(model_path))

# ❌ If file missing → stop app with clear error
if not os.path.exists(model_path):
    raise FileNotFoundError(f"❌ Model not found at {model_path}")

# ✅ Load model
with open(model_path, "rb") as f:
    model = pickle.load(f)

with open(vectorizer_path, "rb") as f:
    vectorizer = pickle.load(f)


def predict_email(text):
    cleaned = clean_text(text)
    vector = vectorizer.transform([cleaned])

    prediction = model.predict(vector)[0]
    probability = model.predict_proba(vector)[0].max()

    return prediction, probability
