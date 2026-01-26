import pandas as pd
import time
from bci_firewall import firewall_decision


# -----------------------------
# Load EEG feature stream
# -----------------------------
DATA_PATH = "data/processed/eeg_features_labeled.csv"
df = pd.read_csv(DATA_PATH)

# Separate features (drop label)
X_stream = df.drop(columns=["label"])

print("Starting real-time EEG simulation...\n")

# -----------------------------
# Simulate streaming
# -----------------------------
for i in range(len(X_stream)):
    packet = X_stream.iloc[[i]]  # single EEG packet

    decision = firewall_decision(packet, session_id="REALTIME_EEG_01")

    print(f"EEG Packet {i+1}: {decision[0]}")

    # Simulate time delay (1 second)
    time.sleep(1)

print("\nReal-time EEG simulation completed.")
