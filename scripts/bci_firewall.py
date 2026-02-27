import joblib
import pandas as pd
from datetime import datetime
import os
from collections import defaultdict

# Corrected imports for Streamlit execution
from scripts.healthcare_alerts import healthcare_alert
from scripts.email_alerts import send_email

# -----------------------------
# Configuration
# -----------------------------
MODEL_PATH = "models/isolation_forest.pkl"
LOG_PATH = "logs/firewall.log"
ANOMALY_THRESHOLD = 3

# -----------------------------
# Load AI Model
# -----------------------------
model = joblib.load(MODEL_PATH)

# -----------------------------
# Ensure logs directory exists
# -----------------------------
os.makedirs("logs", exist_ok=True)

# -----------------------------
# Session anomaly tracking
# -----------------------------
session_anomaly_count = defaultdict(int)

# -----------------------------
# Firewall Decision Engine
# -----------------------------
def firewall_decision(eeg_features, session_id="SESSION_1"):
    """
    eeg_features : pandas DataFrame
    session_id   : identifier for EEG stream/session
    """

    predictions = model.predict(eeg_features)
    decisions = []

    for i, pred in enumerate(predictions):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # -----------------------------
        # Decision Logic
        # -----------------------------
        if pred == -1:  # anomaly detected
            session_anomaly_count[session_id] += 1

            if session_anomaly_count[session_id] >= ANOMALY_THRESHOLD:
                decision = "QUARANTINE"
                reason = "Repeated anomalies detected"
            else:
                decision = "BLOCK"
                reason = "Anomalous EEG pattern detected"

        else:
            decision = "ALLOW"
            reason = "Normal EEG pattern"

        # -----------------------------
        # Logging
        # -----------------------------
        log_entry = (
            f"{timestamp} | {session_id} | Packet {i+1} | "
            f"{decision} | {reason}\n"
        )

        with open(LOG_PATH, "a") as log_file:
            log_file.write(log_entry)

        # -----------------------------
        # Healthcare Alert
        # -----------------------------
        healthcare_alert(decision)

        # -----------------------------
        # Email Alerts
        # -----------------------------
        if decision == "BLOCK":
            send_email(
                "⚠ BCI Firewall Warning",
                f"Warning: Abnormal EEG detected.\n\n"
                f"Session: {session_id}\n"
                f"Action Taken: BLOCK\n"
                f"Time: {timestamp}"
            )

        elif decision == "QUARANTINE":
            send_email(
                "🚨 BCI Firewall EMERGENCY",
                f"Critical EEG anomaly detected.\n\n"
                f"Session: {session_id}\n"
                f"Action Taken: QUARANTINE\n"
                f"Time: {timestamp}"
            )

        decisions.append(decision)

    return decisions


# -----------------------------
# Standalone Test Mode
# -----------------------------
if __name__ == "__main__":

    print("Running BCI Firewall Standalone Mode...\n")

    test_data = pd.read_csv("data/processed/eeg_features_labeled.csv")
    X_test = test_data.drop(columns=["label"]).head(10)

    results = firewall_decision(X_test, session_id="EEG_STREAM_DEMO")

    for i, res in enumerate(results):
        print(f"Packet {i+1}: {res}")
