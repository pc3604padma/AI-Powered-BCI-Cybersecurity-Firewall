import numpy as np
import pandas as pd
import os

INPUT_PATH = "data/processed/eeg_features.csv"
OUTPUT_PATH = "data/processed/eeg_features_labeled.csv"

# -----------------------------
# Load normal EEG features
# -----------------------------
df = pd.read_csv(INPUT_PATH)

# Label normal EEG
df_normal = df.copy()
df_normal["label"] = 0  # normal

# -----------------------------
# Create malicious EEG
# -----------------------------
df_malicious = df.copy()

# 1. Amplitude scaling attack
df_malicious *= np.random.uniform(1.5, 3.0)

# 2. Frequency band distortion
for col in ["alpha", "beta", "gamma"]:
    df_malicious[col] *= np.random.uniform(2.0, 4.0)

# 3. Random noise injection
noise = np.random.normal(0, 0.5, df_malicious.shape)
df_malicious += noise

# Label malicious EEG
df_malicious["label"] = 1  # malicious

# -----------------------------
# Combine datasets
# -----------------------------
df_final = pd.concat([df_normal, df_malicious], ignore_index=True)

# Shuffle dataset
df_final = df_final.sample(frac=1).reset_index(drop=True)

# Save
os.makedirs("data/processed", exist_ok=True)
df_final.to_csv(OUTPUT_PATH, index=False)

print("Malicious EEG injection completed")
print(f"Labeled dataset saved to: {OUTPUT_PATH}")
print(df_final.head())
