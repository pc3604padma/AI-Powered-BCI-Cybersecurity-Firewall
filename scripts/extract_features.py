import os
import mne
import numpy as np
import pandas as pd
from scipy.signal import welch

DATA_PATH = "data/raw/"
OUTPUT_PATH = "data/processed/eeg_features.csv"

# -----------------------------
# Helper function: band power
# -----------------------------
def bandpower(data, sf, band):
    low, high = band
    freqs, psd = welch(data, sf, nperseg=int(sf * 2))
    idx = np.logical_and(freqs >= low, freqs <= high)
    return np.mean(psd[idx])

# -----------------------------
# Load one EEG file
# -----------------------------
subjects = [s for s in os.listdir(DATA_PATH) if s.startswith("S")]
first_subject = subjects[0]
subject_path = os.path.join(DATA_PATH, first_subject)

edf_files = [f for f in os.listdir(subject_path) if f.endswith(".edf")]
file_path = os.path.join(subject_path, edf_files[0])

print(f"Loading EEG file: {file_path}")

raw = mne.io.read_raw_edf(file_path, preload=True, verbose=False)

# -----------------------------
# Filtering (safety)
# -----------------------------
raw.filter(0.5, 40, verbose=False)
raw.notch_filter(50, verbose=False)

data = raw.get_data()
sf = raw.info["sfreq"]

features = []

# -----------------------------
# Feature extraction per channel
# -----------------------------
for ch in range(data.shape[0]):
    ch_data = data[ch]

    feature_dict = {
        "mean": np.mean(ch_data),
        "std": np.std(ch_data),
        "var": np.var(ch_data),
        "rms": np.sqrt(np.mean(ch_data ** 2)),
        "delta": bandpower(ch_data, sf, (0.5, 4)),
        "theta": bandpower(ch_data, sf, (4, 8)),
        "alpha": bandpower(ch_data, sf, (8, 13)),
        "beta": bandpower(ch_data, sf, (13, 30)),
        "gamma": bandpower(ch_data, sf, (30, 40))
    }

    features.append(feature_dict)

# -----------------------------
# Save features
# -----------------------------
df_features = pd.DataFrame(features)

os.makedirs("data/processed", exist_ok=True)
df_features.to_csv(OUTPUT_PATH, index=False)

print("Feature extraction completed successfully")
print(f"Features saved to: {OUTPUT_PATH}")
print(df_features.head())
