# src/retrain.py
import os
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

os.makedirs("models", exist_ok=True)

# Tiny default dataset (small demo)
samples = [
    ("Your account has been suspended. Click here to verify: http://fake", 1),
    ("Important: update your billing info now", 1),
    ("Meeting tomorrow at 10am - agenda attached", 0),
    ("Lunch at 1? Let's meet", 0),
    ("Urgent: verify your account to avoid closure", 1),
    ("Invoice attached for your review", 0),
]

df = pd.DataFrame(samples, columns=["text", "label"])
X = df["text"].values
y = df["label"].values

vec = TfidfVectorizer(ngram_range=(1,2), max_features=2000)
Xv = vec.fit_transform(X)

model = LogisticRegression()
model.fit(Xv, y)

joblib.dump(vec, "models/vectorizer.joblib")
joblib.dump(model, "models/model.joblib")

print("Training complete. Model saved to models/")
