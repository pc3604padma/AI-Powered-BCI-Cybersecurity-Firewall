import os
import mne
import numpy as np
from sklearn.preprocessing import StandardScaler

DATA_PATH = "data/raw/"

# Load one EEG file for demonstration
subjects = [s for s in os.listdir(DATA_PATH) if s.startswith("S")]
first_subject = subjects[0]
subject_path = os.path.join(DATA_PATH, first_subject)

edf_files = [f for f in os.listdir(subject_path) if f.endswith(".edf")]
file_path = os.path.join(subject_path, edf_files[0])

print(f"Loading file: {file_path}")
raw = mne.io.read_raw_edf(file_path, preload=True)

# -----------------------------
# Step 1: Band-pass + Notch (ensure clean input)
# -----------------------------
raw.filter(l_freq=0.5, h_freq=40)
raw.notch_filter(freqs=50)

# -----------------------------
# Step 2: Simple artifact rejection
# -----------------------------
print("Applying amplitude-based artifact rejection...")
raw_data = raw.get_data()

# Clip extreme amplitudes (in volts)
raw_data = np.clip(raw_data, -100e-6, 100e-6)

# Replace cleaned data back
raw._data = raw_data

# -----------------------------
# Step 3: Normalization (Z-score)
# -----------------------------
print("Normalizing EEG data (Z-score)...")

scaler = StandardScaler()
normalized_data = scaler.fit_transform(raw_data.T).T

raw._data = normalized_data

print("Artifact handling and normalization completed")
print(raw)
