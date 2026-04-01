import pandas as pd
from scripts.lstm_detector import calculate_threshold

df = pd.read_csv("data/processed/eeg_features_labeled.csv")

X = df.drop(columns=["label"])

# 🔥 IMPORTANT: ensure enough rows
if len(X) < 20:
    print("Dataset too small!")
else:
    threshold, loss = calculate_threshold(X.values)

    print("Recommended Threshold:", threshold)