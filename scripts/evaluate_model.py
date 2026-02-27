import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# -----------------------------
# Load Model
# -----------------------------
MODEL_PATH = "models/isolation_forest.pkl"
model = joblib.load(MODEL_PATH)

# -----------------------------
# Load Dataset
# -----------------------------
DATA_PATH = "data/processed/eeg_features_labeled.csv"
df = pd.read_csv(DATA_PATH)

X = df.drop(columns=["label"])
y_true = df["label"]

# -----------------------------
# Get Predictions
# -----------------------------
preds = model.predict(X)

# Convert IsolationForest output:
# 1 → Normal (0)
# -1 → Anomaly (1)
y_pred = [1 if p == -1 else 0 for p in preds]

# -----------------------------
# Evaluation Metrics
# -----------------------------
accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)
cm = confusion_matrix(y_true, y_pred)

# -----------------------------
# Print Results
# -----------------------------
print("\nModel Evaluation Results")
print("-" * 30)
print(f"Accuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")
print("\nConfusion Matrix:")
print(cm)
