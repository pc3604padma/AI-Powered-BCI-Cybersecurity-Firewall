from datetime import datetime

def healthcare_alert(decision, explanation=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if decision == "ALLOW":
        return None

    elif decision == "BLOCK":
        alert = {
            "level": "WARNING",
            "message": "Abnormal EEG detected. Patient requires observation.",
            "timestamp": timestamp,
            "details": explanation
        }

    elif decision == "QUARANTINE":
        alert = {
            "level": "EMERGENCY",
            "message": "Critical EEG abnormality detected. Immediate medical attention required.",
            "timestamp": timestamp,
            "details": explanation
        }

    print(f"[HEALTHCARE ALERT - {alert['level']}] {alert['timestamp']} | {alert['message']}")
    return alert
