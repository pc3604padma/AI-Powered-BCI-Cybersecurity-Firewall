import os
import mne

DATA_PATH = "data/raw/"

# Get subject folders
subjects = [s for s in os.listdir(DATA_PATH) if s.startswith("S")]

print(f"Subjects found: {len(subjects)}")

# Load one EEG file for filtering demo
first_subject = subjects[0]
subject_path = os.path.join(DATA_PATH, first_subject)

edf_files = [f for f in os.listdir(subject_path) if f.endswith(".edf")]
file_path = os.path.join(subject_path, edf_files[0])

print(f"Loading file: {file_path}")

raw = mne.io.read_raw_edf(file_path, preload=True)

# -----------------------------
# Step 1: Band-pass filter
# -----------------------------
print("Applying band-pass filter (0.5–40 Hz)...")
raw.filter(l_freq=0.5, h_freq=40)

# -----------------------------
# Step 2: Notch filter
# -----------------------------
print("Applying notch filter at 50 Hz...")
raw.notch_filter(freqs=50)

print("EEG filtering completed successfully")
print(raw)
