"""
⚡ QUICK BCI FIREWALL TEST - Fast version for rapid validation
"""

import pandas as pd
import numpy as np
from scripts.bci_firewall import firewall_decision
from scripts.mixed_data_utils import create_mixed_test_data, print_test_summary

print("\n" + "=" * 80)
print("⚡ QUICK FIREWALL TEST (Optimized)")
print("=" * 80)

# TEST 1: Pure Normal (Smaller dataset for speed)
print(f"\n{'=' * 80}")
print("TEST 1: PURE NORMAL EEG (20 samples)")
print(f"{'=' * 80}")

df_normal, _ = create_mixed_test_data(normal_samples=20, malicious_samples=0)
decisions_1 = firewall_decision(df_normal, session_id="TEST1")

blocked_1 = sum(1 for d in decisions_1 if d in ["BLOCK", "QUARANTINE"])
pass_1 = blocked_1 == 0

print(f"Total decisions: {len(decisions_1)}")
print(f"BLOCK/QUARANTINE: {blocked_1}")
print(f"Result: {'✅ PASS' if pass_1 else '❌ FAIL'} (Expected: All ALLOW)")

# TEST 2: Pure Malicious
print(f"\n{'=' * 80}")
print("TEST 2: PURE MALICIOUS EEG (20 samples)")
print(f"{'=' * 80}")

df_malicious, _ = create_mixed_test_data(normal_samples=0, malicious_samples=20)
decisions_2 = firewall_decision(df_malicious, session_id="TEST2")

allowed_2 = sum(1 for d in decisions_2 if d == "ALLOW")
pass_2 = allowed_2 == 0

print(f"Total decisions: {len(decisions_2)}")
print(f"ALLOW: {allowed_2}")
print(f"Result: {'✅ PASS' if pass_2 else '❌ FAIL'} (Expected: All BLOCK/QUARANTINE)")

# TEST 3: Mixed Realistic
print(f"\n{'=' * 80}")
print("TEST 3: MIXED REALISTIC (14 normal + 6 malicious = 20 samples)")
print(f"{'=' * 80}")

df_mixed, is_mal = create_mixed_test_data(normal_samples=14, malicious_samples=6, random_seed=42)
decisions_3 = firewall_decision(df_mixed, session_id="TEST3")

print(f"Total decisions: {len(decisions_3)}")
print(f"BLOCK/QUARANTINE: {sum(1 for d in decisions_3 if d in ['BLOCK', 'QUARANTINE'])}")
print(f"ALLOW: {sum(1 for d in decisions_3 if d == 'ALLOW')}")

# Analyze detection accuracy
correct = 0
for i in range(len(decisions_3)):
    window_has_malicious = any(is_mal[i:min(i+10, len(is_mal))])
    is_blocked = decisions_3[i] in ["BLOCK", "QUARANTINE"]
    if is_blocked == window_has_malicious:
        correct += 1

accuracy = (correct / len(decisions_3)) * 100 if len(decisions_3) > 0 else 0
pass_3 = accuracy >= 80

print(f"Detection accuracy: {accuracy:.1f}%")
print(f"Result: {'✅ PASS' if pass_3 else '⚠️ WARN'} (Expected: >= 80%)")

# SUMMARY
print(f"\n{'=' * 80}")
print("📊 FINAL SUMMARY")
print(f"{'=' * 80}")

print(f"\n✅ Test 1 (Pure Normal):    {'PASS' if pass_1 else 'FAIL'}")
print(f"✅ Test 2 (Pure Malicious): {'PASS' if pass_2 else 'FAIL'}")
print(f"✅ Test 3 (Mixed Data):     {'PASS' if pass_3 else 'WARN'} ({accuracy:.0f}% accuracy)")

if all([pass_1, pass_2, pass_3]):
    print("\n🎉 ALL TESTS PASSED!")
elif pass_1 and pass_2:
    print("\n✅ Core detection working (normal/malicious separation OK)")
else:
    print("\n⚠️  Review test results above")

print("=" * 80 + "\n")
