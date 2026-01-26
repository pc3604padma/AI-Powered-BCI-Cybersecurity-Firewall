import joblib
import pandas as pd
from datetime import datetime
import os
from collections import defaultdict

# -----------------------------
# Paths
# -----------------------------
MODEL_PATH = "models/isolation_forest.pkl"
LOG_PATH = "logs/firewall.log"

# -----------------------------
# Load model
# -----------------------------
model = joblib.load(MODEL_PATH)

# -----------------------------
# Ensure logs directory
# -----------------------------
os.makedirs("logs", exist_ok=True)

# -----------------------------
# Policy configuration
# -----------------------------
ANOMALY_THRESHOLD = 3
session_anomaly_count = defaultdict(int)

# -----------------------------
# Alert handler
# -----------------------------
def raise_alert(level, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[ALERT - {level}] {timestamp} | {message}")

# -----------------------------
# Firewall decision engine
# -----------------------------
def firewall_decision(eeg_features, session_id="SESSION_1"):
    preds = model.predict(eeg_features)
    decisions = []

    for i, p in enumerate(preds):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if p == -1:
            session_anomaly_count[session_id] += 1

            if session_anomaly_count[session_id] >= ANOMALY_THRESHOLD:
                decision = "QUARANTINE"
                reason = "Repeated anomalies detected"
                raise_alert("CRITICAL", f"{session_id} quarantined due to repeated EEG anomalies")
            else:
                decision = "BLOCK"
                reason = "Anomalous EEG pattern detected"
                raise_alert("WARNING", f"Anomalous EEG detected in {session_id}")

        else:
            decision = "ALLOW"
            reason = "Normal EEG pattern"

        log_entry = (
            f"{timestamp} | {session_id} | Packet {i+1} | "
            f"{decision} | {reason}\n"
        )

        with open(LOG_PATH, "a") as log_file:
            log_file.write(log_entry)

        decisions.append(decision)

    return decisions

# -----------------------------
# Test run
# -----------------------------
if __name__ == "__main__":
    test_data = pd.read_csv("data/processed/eeg_features_labeled.csv")
    X_test = test_data.drop(columns=["label"]).head(10)

    results = firewall_decision(X_test, session_id="EEG_STREAM_01")

    for i, res in enumerate(results):
        print(f"EEG Packet {i+1}: {res}")
