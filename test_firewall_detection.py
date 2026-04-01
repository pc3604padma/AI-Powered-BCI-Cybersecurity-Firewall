"""
🧪 BCI FIREWALL LSTM DETECTION TEST
Tests the anomaly detection on MIXED real-world scenarios
"""

import pandas as pd
import numpy as np
from scripts.bci_firewall import firewall_decision
from scripts.mixed_data_utils import create_mixed_test_data, print_test_summary

print("=" * 80)
print("🧪 LSTM FIREWALL DETECTION TEST - MIXED MODE")
print("=" * 80)

# ---------------------
# TEST 1: Pure Normal
# ---------------------
print(f"\n\n{'=' * 80}")
print("TEST 1️⃣  : PURE NORMAL EEG DATA (No attacks injected)")
print(f"{'=' * 80}")

df_normal, is_mal_normal = create_mixed_test_data(
    normal_samples=40,
    malicious_samples=0
)
print_test_summary(df_normal, is_mal_normal)

decisions_t1 = firewall_decision(df_normal, session_id="TEST1_NORMAL")

allowed_t1 = sum(1 for d in decisions_t1 if d == "ALLOW")
blocked_t1 = sum(1 for d in decisions_t1 if d in ["BLOCK", "QUARANTINE"])

print(f"✅ Firewall Results:")
print(f"   ALLOW:      {allowed_t1}/{len(decisions_t1)}")
print(f"   BLOCK/QUAR: {blocked_t1}/{len(decisions_t1)}")
print(f"   ✓ Correct: {allowed_t1 == len(decisions_t1)}")

# ---------------------
# TEST 2: Pure Malicious
# ---------------------
print(f"\n\n{'=' * 80}")
print("TEST 2️⃣  : PURE MALICIOUS EEG DATA (All attacks)")
print(f"{'=' * 80}")

df_malicious, is_mal_malicious = create_mixed_test_data(
    normal_samples=0,
    malicious_samples=40
)
print_test_summary(df_malicious, is_mal_malicious)

decisions_t2 = firewall_decision(df_malicious, session_id="TEST2_MALICIOUS")

allowed_t2 = sum(1 for d in decisions_t2 if d == "ALLOW")
blocked_t2 = sum(1 for d in decisions_t2 if d in ["BLOCK", "QUARANTINE"])

print(f"✅ Firewall Results:")
print(f"   ALLOW:      {allowed_t2}/{len(decisions_t2)}")
print(f"   BLOCK/QUAR: {blocked_t2}/{len(decisions_t2)}")
print(f"   ✓ Correct:  {blocked_t2 == len(decisions_t2)}")

# ---------------------
# TEST 3: REALISTIC MIXED (Most Important!)
# ---------------------
print(f"\n\n{'=' * 80}")
print("TEST 3️⃣  : REALISTIC MIXED DATA (70% Normal, 30% Attacks) 🎯")
print(f"{'=' * 80}")

df_mixed, is_mal_mixed = create_mixed_test_data(
    normal_samples=35,
    malicious_samples=15,
    random_seed=42
)
print_test_summary(df_mixed, is_mal_mixed)

decisions_t3 = firewall_decision(df_mixed, session_id="TEST3_MIXED_REALISTIC")

# Map decisions back to sample labels - note: fewer decisions than rows due to LSTM sequences
# Each decision corresponds to a 10-timestep sequence
results_detail = []
num_sequences = len(decisions_t3)

# Sample analysis showing every Nth packet for readability
for i in range(min(num_sequences, 20)):  # Show first 20 sequences max
    # For each sequence, the ground truth is the majority of the rows in that window
    window_start = i
    window_end = min(i + 10, len(is_mal_mixed))
    is_malicious_in_window = any(is_mal_mixed[window_start:window_end])
    
    expected = "BLOCK/QUARANTINE" if is_malicious_in_window else "ALLOW"
    actual = "BLOCK/QUARANTINE" if decisions_t3[i] in ["BLOCK", "QUARANTINE"] else "ALLOW"
    correct = expected == actual
    results_detail.append({
        "Sequence": i + 1,
        "Expected": expected,
        "Actual": actual,
        "Match": "✅" if correct else "❌"
    })

results_df = pd.DataFrame(results_detail)
print("\n📊 Detailed Results (Sequence Analysis):")
print(results_df.to_string(index=False))

# Verify accuracy
correct_detections = 0
num_sequences = len(decisions_t3)

for i in range(num_sequences):
    # Each sequence represents 10 timesteps
    window_start = i
    window_end = min(i + 10, len(is_mal_mixed))
    
    # Ground truth: is this window containing malicious data?
    is_malicious_in_window = any(is_mal_mixed[window_start:window_end])
    is_allowed = decisions_t3[i] == "ALLOW"
    is_normal = not is_malicious_in_window
    
    if is_allowed == is_normal:  # Matched expectations
        correct_detections += 1

accuracy_t3 = (correct_detections / num_sequences) * 100 if num_sequences > 0 else 0

allowed_t3 = sum(1 for d in decisions_t3 if d == "ALLOW")
blocked_t3 = sum(1 for d in decisions_t3 if d in ["BLOCK", "QUARANTINE"])

print(f"\n✅ Firewall Results:")
print(f"   ALLOW:      {allowed_t3}/{len(decisions_t3)}")
print(f"   BLOCK/QUAR: {blocked_t3}/{len(decisions_t3)}")
print(f"   👁️  Detection Accuracy: {accuracy_t3:.1f}% ({correct_detections}/{num_sequences})")

# ===== SUMMARY =====
print(f"\n\n{'=' * 80}")
print("📊 FINAL SUMMARY")
print(f"{'=' * 80}")

test_1_pass = allowed_t1 == len(decisions_t1)
test_2_pass = blocked_t2 == len(decisions_t2)
test_3_pass = accuracy_t3 >= 90  # At least 90% accuracy on mixed

print(f"\nTest 1 (Pure Normal):     {'✅ PASS' if test_1_pass else '❌ FAIL'}")
print(f"Test 2 (Pure Malicious):  {'✅ PASS' if test_2_pass else '❌ FAIL'}")
print(f"Test 3 (Mixed Realistic): {'✅ PASS' if test_3_pass else '❌ FAIL'} ({accuracy_t3:.1f}%)")

if all([test_1_pass, test_2_pass, test_3_pass]):
    print("\n🎉 ALL TESTS PASSED - FIREWALL WORKING PERFECTLY!")
else:
    print("\n⚠️  SOME TESTS FAILED - REVIEW RESULTS ABOVE")

print("=" * 80)
