import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle
import os
from text_preprocess import clean_text

print("Starting training...")

# Create model folder
model_dir = "model"
os.makedirs(model_dir, exist_ok=True)

# Load dataset
df = pd.read_csv("data/emails.csv")

# Debug: check dataset
print("Original columns:", df.columns)
print(df.head())

# ✅ FIX: Your dataset format = [label, text]
df = df.rename(columns={
    df.columns[0]: "label",
    df.columns[1]: "text"
})

# Ensure correct types
df["label"] = df["label"].astype(int)
df["text"] = df["text"].astype(str)

# Remove missing values
df = df.dropna(subset=["text", "label"])

print("Dataset after cleaning:", df.shape)

# Stop if empty
if df.shape[0] == 0:
    print("❌ ERROR: Dataset is empty. Check CSV file.")
    exit()

# ✅ Text preprocessing
df["cleaned"] = df["text"].apply(clean_text)

# Feature extraction
vectorizer = TfidfVectorizer(stop_words="english", max_features=1000)
X = vectorizer.fit_transform(df["cleaned"])
y = df["label"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
model = MultinomialNB()
model.fit(X_train, y_train)

# Accuracy
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

# Save model
model_path = os.path.join(model_dir, "phishing_model.pkl")
vectorizer_path = os.path.join(model_dir, "vectorizer.pkl")

pickle.dump(model, open(model_path, "wb"))
pickle.dump(vectorizer, open(vectorizer_path, "wb"))

print("Model saved at:", model_path)
print("Training completed successfully!")