import pandas as pd
from scripts.bci_firewall import firewall_decision

# Load dataset
df = pd.read_csv("data/processed/eeg_features_labeled.csv")

# Split data
X_normal = df[df["label"] == 0].drop(columns=["label"])
X_mal = df[df["label"] == 1].drop(columns=["label"])

print("---------- NORMAL TEST ----------")
normal_results = firewall_decision(X_normal.head(50), session_id="TEST_NORMAL")
print(normal_results)

print("\n---------- MALICIOUS TEST ----------")
mal_results = firewall_decision(X_mal.head(50), session_id="TEST_ATTACK")
print(mal_results)