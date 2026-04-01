import pandas as pd
from datetime import datetime
import os
from collections import defaultdict

# LSTM detector
from scripts.lstm_detector import detect_anomaly

# Alerts
from scripts.healthcare_alerts import healthcare_alert
from scripts.email_alerts import send_email

# -----------------------------
# Configuration
# -----------------------------
LOG_PATH = "logs/firewall.log"
ANOMALY_THRESHOLD = 3
TIMESTEPS = 10  # must match LSTM training

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

    data = eeg_features.values

    results, scores = detect_anomaly(data)

    decisions = []

    for i, (res, score) in enumerate(zip(results, scores)):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # -----------------------------
        # 🔥 STRONG DECISION LOGIC
        # -----------------------------

        # Threshold tuning (IMPORTANT)
        if score > 0.05:   # strong anomaly
            session_anomaly_count[session_id] += 1

            if session_anomaly_count[session_id] >= ANOMALY_THRESHOLD:
                decision = "QUARANTINE"
                reason = f"Critical anomaly | Score: {round(score,5)}"
            else:
                decision = "BLOCK"
                reason = f"High anomaly detected | Score: {round(score,5)}"

        elif score > 0.01:   # mild anomaly
            decision = "BLOCK"
            reason = f"Suspicious pattern | Score: {round(score,5)}"

        else:
            decision = "ALLOW"
            reason = f"Normal EEG | Score: {round(score,5)}"

        # -----------------------------
        # DEBUG PRINT (REMOVE LATER)
        # -----------------------------
        print(f"[DEBUG] Score: {score:.5f} → {decision}")

        # -----------------------------
        # Logging
        # -----------------------------
        log_entry = (
            f"{timestamp} | {session_id} | Seq {i+1} | "
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
                f"Action: BLOCK\n"
                f"Score: {round(score,5)}\n"
                f"Time: {timestamp}"
            )

        elif decision == "QUARANTINE":
            send_email(
                "🚨 BCI Firewall EMERGENCY",
                f"Critical EEG anomaly detected.\n\n"
                f"Session: {session_id}\n"
                f"Action: QUARANTINE\n"
                f"Score: {round(score,5)}\n"
                f"Time: {timestamp}"
            )

        decisions.append(decision)

    return decisions

# -----------------------------
# Standalone Test Mode
# -----------------------------
if __name__ == "__main__":

    print("Running LSTM-based BCI Firewall...\n")

    test_data = pd.read_csv("data/processed/eeg_features_labeled.csv")

    X_test = test_data.drop(columns=["label"])

    # Use enough rows for sequence
    results = firewall_decision(X_test.head(50), session_id="EEG_STREAM_DEMO")

    for i, res in enumerate(results):
        print(f"Sequence {i+1}: {res}")