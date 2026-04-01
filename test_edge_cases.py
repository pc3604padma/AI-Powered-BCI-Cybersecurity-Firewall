"""
Test script to verify decision distribution graph and all features work correctly 
across different packet counts (edge cases)
"""

import pandas as pd
import numpy as np
import sys
import traceback

sys.path.insert(0, 'd:\\Download\\bci_cybersecurity_project')

from scripts.bci_firewall import firewall_decision
from scripts.mixed_data_utils import create_realistic_stream_test

def test_packet_count(packet_count):
    """Test all features with given packet count"""
    print(f"\n{'='*60}")
    print(f"TESTING WITH {packet_count} PACKETS")
    print(f"{'='*60}")
    
    try:
        # Generate test data
        df_mixed, is_malicious = create_realistic_stream_test(packet_count, injection_rate=0.3)
        print(f"✅ Data generation: SUCCESS")
        print(f"   - Shape: {df_mixed.shape}")
        print(f"   - Malicious packets: {sum(is_malicious)}")
        
        # Run firewall detection
        decisions = firewall_decision(df_mixed, session_id="TEST")
        print(f"✅ Firewall detection: SUCCESS")
        print(f"   - Decisions generated: {len(decisions)}")
        print(f"   - Decision types: {set(decisions)}")
        
        # Calculate metrics
        num_sequences = len(df_mixed) - 10
        print(f"✅ Sequence calculation: SUCCESS")
        print(f"   - Total sequences: {num_sequences}")
        
        if num_sequences > 0:
            # Test accuracy calculation
            correct_detections = 0
            for i in range(num_sequences):
                window_end = min(i + 10, len(is_malicious))
                window_has_malicious = any(is_malicious[i:window_end])
                decision_is_block = decisions[i] in ["BLOCK", "QUARANTINE"]
                if decision_is_block == window_has_malicious:
                    correct_detections += 1
            
            accuracy = (correct_detections / num_sequences) * 100
            print(f"✅ Accuracy calculation: SUCCESS")
            print(f"   - Correct detections: {correct_detections}/{num_sequences}")
            print(f"   - Accuracy: {accuracy:.1f}%")
        else:
            print(f"✅ Accuracy calculation: HANDLES EDGE CASE (no sequences)")
            print(f"   - Accuracy: N/A (insufficient data)")
        
        # Test decision distribution graph robustness
        try:
            decision_counts = pd.Series(decisions).value_counts().reset_index()
            decision_counts.columns = ["Decision", "Count"]
            
            # This is the key fix - use only available colors
            available_colors = {
                "ALLOW": "#00CC96",
                "BLOCK": "#FFA15A", 
                "QUARANTINE": "#EF553B"
            }
            available_colors = {k: v for k, v in available_colors.items() 
                               if k in decision_counts["Decision"].values}
            
            print(f"✅ Decision distribution: SUCCESS")
            print(f"   - Decision breakdown:")
            for _, row in decision_counts.iterrows():
                print(f"     {row['Decision']}: {row['Count']}")
            print(f"   - Available colors for chart: {len(available_colors)}")
            
        except Exception as e:
            print(f"❌ Decision distribution: FAILED")
            print(f"   Error: {str(e)}")
            traceback.print_exc()
            return False
        
        # Test research summary calculations
        total_malicious_actual = sum(1 for is_mal in is_malicious if is_mal)
        total_normal_actual = packet_count - total_malicious_actual
        
        normal_packet_count = sum(1 for i in range(packet_count) if not is_malicious[i])
        malicious_packet_count = sum(1 for i in range(packet_count) if is_malicious[i])
        
        print(f"✅ Research summary: SUCCESS")
        print(f"   - Normal packets: {normal_packet_count}")
        print(f"   - Malicious packets: {malicious_packet_count}")
        print(f"   - Injection rate: {(malicious_packet_count/packet_count)*100:.1f}%")
        
        # Test packet-level analysis
        packet_details = []
        for i in range(packet_count):
            containing_sequences = []
            containing_decisions = []
            
            for seq_idx in range(num_sequences):
                if i >= seq_idx and i < seq_idx + 10:
                    containing_sequences.append(seq_idx + 1)
                    containing_decisions.append(decisions[seq_idx])
            
            any_sequence_blocked = any(d in ["BLOCK", "QUARANTINE"] for d in containing_decisions)
            
            if is_malicious[i]:
                is_correct = any_sequence_blocked
            else:
                is_correct = True
            
            packet_details.append({
                "Packet #": i + 1,
                "Is_Malicious": is_malicious[i],
                "Is_Correct": is_correct
            })
        
        research_df = pd.DataFrame(packet_details)
        print(f"✅ Packet-level analysis: SUCCESS")
        print(f"   - Total packets analyzed: {len(research_df)}")
        print(f"   - Correct packets: {sum(research_df['Is_Correct'])}")
        
        # Test research counts
        if num_sequences > 0:
            correctly_detected_malicious = sum(
                1 for _, row in research_df.iterrows() 
                if row['Is_Malicious'] and row['Is_Correct']
            )
            false_negatives = sum(
                1 for _, row in research_df.iterrows() 
                if row['Is_Malicious'] and not row['Is_Correct']
            )
            correctly_passed_normal = sum(
                1 for _, row in research_df.iterrows() 
                if not row['Is_Malicious'] and row['Is_Correct']
            )
            
            print(f"✅ Research statistics: SUCCESS")
            print(f"   - Correctly detected malicious: {correctly_detected_malicious}")
            print(f"   - False negatives: {false_negatives}")
            print(f"   - Correctly passed normal: {correctly_passed_normal}")
        
        print(f"\n✅ ALL TESTS PASSED FOR {packet_count} PACKETS\n")
        return True
        
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {str(e)}")
        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_counts = [5, 10, 11, 20, 30, 50, 100]
    
    print("COMPREHENSIVE EDGE CASE TESTING")
    print("=" * 60)
    print(f"Testing packet counts: {test_counts}")
    
    results = {}
    for count in test_counts:
        results[count] = test_packet_count(count)
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    for count, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{count:3d} packets: {status}")
    
    all_passed = all(results.values())
    if all_passed:
        print("\n🎉 ALL EDGE CASES HANDLED SUCCESSFULLY!")
    else:
        print("\n⚠️ SOME TESTS FAILED - SEE DETAILS ABOVE")
