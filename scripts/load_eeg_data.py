import os
import mne

DATA_PATH = "data/raw/"

# List subject folders
subjects = [s for s in os.listdir(DATA_PATH) if s.startswith("S")]

print(f"Total subjects found: {len(subjects)}")

# Load first subject and first EDF file for validation
first_subject = subjects[0]
subject_path = os.path.join(DATA_PATH, first_subject)

edf_files = [f for f in os.listdir(subject_path) if f.endswith(".edf")]

file_path = os.path.join(subject_path, edf_files[0])

raw = mne.io.read_raw_edf(file_path, preload=True)

print("\nEEG DATA LOADED SUCCESSFULLY")
print(raw)
