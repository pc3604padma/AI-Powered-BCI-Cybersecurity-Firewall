import pandas as pd
import numpy as np
import joblib

# -----------------------------
# Paths
# -----------------------------
MODEL_PATH = "models/isolation_forest.pkl"
DATA_PATH = "data/processed/eeg_features_labeled.csv"

# -----------------------------
# Load model and data
# -----------------------------
model = joblib.load(MODEL_PATH)
df = pd.read_csv(DATA_PATH)

X = df.drop(columns=["label"])
y_true = df["label"]

# -----------------------------
# Predict
# -----------------------------
y_pred_raw = model.predict(X)

# Convert IsolationForest output
#  1  -> normal
# -1  -> anomaly
y_pred = np.where(y_pred_raw == -1, 1, 0)

# -----------------------------
# Show sample results
# -----------------------------
results = df.copy()
results["predicted_label"] = y_pred

print("Sample test results:")
print(results.head(10))
