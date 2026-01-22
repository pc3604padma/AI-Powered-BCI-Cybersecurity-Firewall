import pandas as pd
import numpy as np
import joblib
import os

from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

# -----------------------------
# Paths
# -----------------------------
DATA_PATH = "data/processed/eeg_features_labeled.csv"
MODEL_PATH = "models/isolation_forest.pkl"

# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv(DATA_PATH)

X = df.drop(columns=["label"])
y = df["label"]

# -----------------------------
# Train-test split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# -----------------------------
# Train Isolation Forest
# -----------------------------
model = IsolationForest(
    n_estimators=200,
    contamination=0.5,   # because we injected 50% malicious
    random_state=42
)

model.fit(X_train)

# -----------------------------
# Prediction
# IsolationForest output:
#  1  -> normal
# -1  -> anomaly
# -----------------------------
y_pred_raw = model.predict(X_test)

# Convert to labels
# anomaly (-1) -> 1 (malicious)
# normal (1)   -> 0 (normal)
y_pred = np.where(y_pred_raw == -1, 1, 0)

# -----------------------------
# Evaluation
# -----------------------------
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# -----------------------------
# Save model
# -----------------------------
os.makedirs("models", exist_ok=True)
joblib.dump(model, MODEL_PATH)

print(f"\nModel saved to {MODEL_PATH}")
