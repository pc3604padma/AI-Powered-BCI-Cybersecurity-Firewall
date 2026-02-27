import joblib
import shap
import pandas as pd

# -----------------------------
# Load model and data
# -----------------------------
MODEL_PATH = "models/isolation_forest.pkl"
DATA_PATH = "data/processed/eeg_features_labeled.csv"

model = joblib.load(MODEL_PATH)
df = pd.read_csv(DATA_PATH)

# Drop label column
X = df.drop(columns=["label"])

# -----------------------------
# SHAP Explainer
# -----------------------------
explainer = shap.Explainer(model, X)

# Pick one EEG packet (example: 5th row)
sample = X.iloc[[4]]

# Explain prediction
shap_values = explainer(sample)

# -----------------------------
# Display explanation
# -----------------------------
print("EEG Feature Contribution Explanation:\n")
print(shap_values)

# Optional visualization (if GUI supported)
shap.plots.waterfall(shap_values[0])
