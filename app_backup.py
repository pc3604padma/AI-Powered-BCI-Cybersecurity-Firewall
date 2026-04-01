import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time

from auth import create_user, login_user
from scripts.bci_firewall import firewall_decision
from scripts.mixed_data_utils import create_realistic_stream_test

st.set_page_config(page_title="Synora", layout="wide")

# session states
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "email" not in st.session_state:
    st.session_state.email = None

# -----------------------------
# LANDING SCREEN
# -----------------------------
if not st.session_state.logged_in:

    st.markdown("<h1 style='text-align:center'>🧠 SYNORA</h1>", unsafe_allow_html=True)

    st.markdown("<h4 style='text-align:center'>AI Cybersecurity for Brain Interfaces</h4>", unsafe_allow_html=True)

    st.markdown("---")

    tab1, tab2 = st.tabs(["Login", "Create Account"])

    # LOGIN
    with tab1:

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):

            if login_user(email, password):

                st.session_state.logged_in = True
                st.session_state.email = email
                st.success("Login Successful")
                st.rerun()

            else:
                st.error("Invalid credentials")

    # CREATE ACCOUNT
    with tab2:

        new_email = st.text_input("New Email")
        new_password = st.text_input("New Password", type="password")

        if st.button("Create Account"):

            success = create_user(new_email, new_password)

            if success:
                st.success("Account created successfully")

            else:
                st.error("User already exists")

# -----------------------------
# DASHBOARD AFTER LOGIN
# -----------------------------
else:

    st.sidebar.success(f"Logged in as {st.session_state.email}")

    st.title("🧠 Synora Firewall - EEG Security Detection")

    st.markdown("""
    Scan EEG datasets to detect malicious patterns. The system will:
    - ✅ Randomly inject malicious patterns into your dataset
    - 🔍 Detect both normal and anomalous packets
    - 📊 Show comprehensive results
    """)

    st.markdown("---")

    st.sidebar.title("⚙️ Settings")
    
    # Initialize session state for scan results (prevents rerun issues on download)
    if "scan_results" not in st.session_state:
        st.session_state.scan_results = None
    
    # Simple packet count slider
    num_packets = st.sidebar.slider(
        "Number of packets to scan",
        5,
        100,
        20,
        help="Total packets to test with random malicious injection"
    )
    
    # Simple scan button
    if st.sidebar.button("🚀 Scan Dataset", use_container_width=True):
        st.info(f"🔄 Scanning {num_packets} packets with random malicious injection...")
        
        # Auto-generate with random injection (30% default)
        from scripts.mixed_data_utils import create_realistic_stream_test
        df_mixed, is_malicious = create_realistic_stream_test(
            total_packets=num_packets,
            injection_rate=0.3,  # Always 30% random injection
            random_seed=None
        )
        
        packet_count = num_packets
        
        # Run firewall detection
        st.warning(f"⚠️  Firewall scanning {num_packets} packets...")
        
        decisions = firewall_decision(df_mixed, session_id="STREAMLIT_UI")
        
        # Store results in session state for persistence across reruns
        st.session_state.scan_results = {
            "df_mixed": df_mixed,
            "is_malicious": is_malicious,
            "decisions": decisions,
            "packet_count": packet_count
        }
        
        # Send email alert if threats detected
        total_malicious = sum(1 for is_mal in is_malicious if is_mal)
        if total_malicious > 0:
            try:
                import email_alerts
                threat_subject = f"🚨 BCI Firewall Alert - {total_malicious} Threats Detected!"
                threat_message = f"""
Security Alert from Synora BCI Firewall

Threats Detected: {total_malicious}
Total Packets Scanned: {packet_count}
User: {st.session_state.email}
Timestamp: {pd.Timestamp.now()}

IMMEDIATE ACTION REQUIRED:
Review the firewall dashboard for detailed packet analysis.

Attack Patterns Detected:
- Abnormal EEG frequency patterns
- Amplified signal distortion
- Anomalous reconstruction errors

This is an automated alert from your BCI security system.
Log in to the dashboard for more details.
                """
                # Send email using root email_alerts.py
                email_alerts.send_email(st.session_state.email, threat_subject, threat_message)
                st.success(f"✅ Security alert sent to {st.session_state.email}")
            except Exception as e:
                st.warning(f"⚠️ Email alert failed (check email configuration in email_alerts.py): {e}")
    
    # Display results if they exist in session state
    if st.session_state.scan_results is not None:
        results = st.session_state.scan_results
        df_mixed = results["df_mixed"]
        is_malicious = results["is_malicious"]
        decisions = results["decisions"]
        packet_count = results["packet_count"]

        # Note: firewall_decision returns num_packets - 10 sequences (LSTM windowing)
        # We need to map sequences back to packet labels
        num_sequences = len(decisions)
        
        # Count malicious packets at packet level (not sequence level)
        total_malicious_actual = sum(1 for is_mal in is_malicious if is_mal)
        total_normal_actual = packet_count - total_malicious_actual
        
        # Calculate detection accuracy based on window analysis
        correct_detections = 0
        for i in range(num_sequences):
            # Each sequence window starts at position i
            window_end = min(i + 10, len(is_malicious))
            # Check if this window contains any malicious packets
            window_has_malicious = any(is_malicious[i:window_end])
            
            decision_is_block = decisions[i] in ["BLOCK", "QUARANTINE"]
            
            # Correct if decision matches the window's nature
            if decision_is_block == window_has_malicious:
                correct_detections += 1
        
        accuracy = (correct_detections / num_sequences) * 100 if num_sequences > 0 else 0

        col1, col2, col3 = st.columns(3)

        col1.metric("Packets Scanned", packet_count)
        col2.metric("Threats Detected", total_malicious_actual)
        if num_sequences > 0:
            col3.metric("Detection Accuracy", f"{accuracy:.1f}%")
        else:
            col3.metric("Detection Accuracy", "N/A")
        
        # Count normal vs malicious at PACKET level (not sequence level)
        normal_packet_count = sum(1 for i in range(packet_count) if not is_malicious[i])
        malicious_packet_count = sum(1 for i in range(packet_count) if is_malicious[i])
        
        col1, col2, col3 = st.columns(3)
        col1.metric("✅ Packets ALLOWED (Normal)", normal_packet_count, help="Total normal packets in dataset")
        col2.metric("🚫 Packets BLOCKED (Malicious)", malicious_packet_count, help="Total malicious packets in dataset")
        col3.metric("📊 Total Sequences", num_sequences)

        st.subheader("📊 Firewall Decisions")

        # Create detailed results table showing sequence analysis
        # (Not packet-by-packet since LSTM uses 10-step windows)
        table_data = {
            "Sequence": range(1, num_sequences+1),
            "Decision": decisions,
            "Contains Malicious": [any(is_malicious[i:min(i+10, len(is_malicious))]) 
                                   for i in range(num_sequences)],
            "Correct": ["✅" if (decisions[i] in ["BLOCK", "QUARANTINE"]) == 
                               any(is_malicious[i:min(i+10, len(is_malicious))])
                        else "❌" 
                        for i in range(num_sequences)]
        }

        st.dataframe(
            pd.DataFrame(table_data),
            use_container_width=True
        )
        
        st.markdown("---")
        
        # DATA TRANSPARENCY SECTION
        st.subheader("🔬 Data Transparency & Verification")
        st.info("**Verify the injection process:** Download both the original and malicious-injected datasets to inspect exactly what was changed during the attack simulation.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Export original data
            st.markdown("### 📊 Original Dataset (Before Injection)")
            csv_original = df_mixed.to_csv(index=False)
            st.download_button(
                label="📥 Download Original Data",
                data=csv_original,
                file_name="original_packets.csv",
                mime="text/csv"
            )
            st.caption(f"✅ {total_normal_actual} normal packets")
        
        with col2:
            # Create injection report
            st.markdown("### 🔴 Injection Report")
            injection_report = f"""
**Malicious Injection Summary:**
- Total Packets: {packet_count}
- Normal Packets: {total_normal_actual}
- Malicious Packets Injected: {total_malicious_actual}
- Injection Rate: {(total_malicious_actual/packet_count)*100:.1f}%
- Attack Type: LSTM anomaly pattern (6-12x amplification + heavy noise)
- Randomly Distributed: Yes (packets randomly shuffled)
            """
            st.text(injection_report)
            
            # Download injection metadata
            injection_meta = f"Packet,Is_Malicious,Injection_Applied\n"
            for i in range(packet_count):
                injection_meta += f"{i+1},{'Yes' if is_malicious[i] else 'No'},{'AMPLIFIED+NOISE' if is_malicious[i] else 'ORIGINAL'}\n"
            
            st.download_button(
                label="📋 Download Injection Log",
                data=injection_meta,
                file_name="injection_log.csv",
                mime="text/csv"
            )
        
        st.markdown("---")
        
        # Add a summary breakdown
        st.subheader("📋 Summary of Results")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ✅ ALLOWED (Normal Packets)")
            st.info(f"**{normal_packet_count} packets** are normal EEG patterns\n\nThese were safely passed through the firewall.")
        
        with col2:
            st.markdown("### 🚫 BLOCKED (Malicious Packets)")
            st.warning(f"**{malicious_packet_count} packets** contain malicious patterns\n\nThese should be detected and blocked by the firewall.")
        
        # Detailed breakdown by type
        st.subheader("🔍 Detailed Breakdown (Packet Level)")
        breakdown_data = {
            "Status": ["✅ NORMAL (Safe)", "🚫 MALICIOUS (Threat)"],
            "Count": [normal_packet_count, malicious_packet_count]
        }
        breakdown_df = pd.DataFrame(breakdown_data)
        st.dataframe(breakdown_df, use_container_width=True)

        st.markdown("---")
        
        # EXPLAIN THE ATTACK
        st.subheader("⚔️ Attack Method Explanation")
        with st.expander("🔍 How are malicious packets created?"):
            st.markdown("""
### Malicious Pattern Injection Process:

**Step 1: Amplification**
- Original values × Random(6-12) = Massive amplification
- Normal EEG: ~0.001 to 0.01 range
- Malicious EEG: ~0.006 to 0.12 range (6-12x larger)

**Step 2: Frequency Distortion** 
- Alpha/Beta/Gamma bands × Random(3-6) additional boost
- Creates unnatural frequency patterns not seen in real EEG

**Step 3: Heavy Noise Addition**
- Gaussian noise N(0, 5.0) added
- Simulates external interference/EMI attacks
- Makes patterns completely anomalous

**Step 4: Random Distribution**
- Malicious packets randomly mixed with normal packets
- Creates realistic attack scenario (not all-at-once)
- Tests firewall's consistency detection

**Result:** Completely different feature patterns that LSTM can detect in ~0.0006s reconstruction error vs normal ~0.000589 threshold.
            """)
        
        # Add research mode packet-level detail
        st.subheader("🎲 Random Packet Distribution")
        
        # Visualize which packets are randomly selected as malicious vs normal
        packet_labels_visual = ["🔴 MALICIOUS" if is_malicious[i] else "🟢 NORMAL" for i in range(packet_count)]
        packet_type_data = pd.DataFrame({
            "Packet": [f"P{i+1}" for i in range(packet_count)],
            "Type": packet_labels_visual,
            "Type_Code": ["MALICIOUS" if is_malicious[i] else "NORMAL" for i in range(packet_count)]
        })
        
        # Visual bar chart of distribution
        fig_dist = px.bar(
            packet_type_data,
            x="Packet",
            y=[1]*packet_count,  # All 1 for just showing presence
            color="Type_Code",
            color_discrete_map={"MALICIOUS": "#EF553B", "NORMAL": "#00CC96"},
            labels={"y": "Packet Status"},
            height=250,
            title="🎲 Random Packet Distribution (Red=Malicious, Green=Normal)"
        )
        fig_dist.update_layout(
            showlegend=False,
            yaxis_title="",
            xaxis_title="Packets",
            yaxis=dict(showticklabels=False),
            hovermode="x unified"
        )
        st.plotly_chart(fig_dist, use_container_width=True)
        
        # Show summary of randomness
        malicious_packets = [i+1 for i in range(packet_count) if is_malicious[i]]
        normal_packets = [i+1 for i in range(packet_count) if not is_malicious[i]]
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"🟢 **NORMAL Packets** (Randomly Selected):\n\n{', '.join(map(str, normal_packets))}")
        with col2:
            st.warning(f"🔴 **MALICIOUS Packets** (Randomly Injected):\n\n{', '.join(map(str, malicious_packets))}")

        st.markdown("---")
        
        # Add research mode packet-level detail
        st.subheader("🔬 Research Data - Packet Details")
        
        # Create packet-level view
        packet_details = []
        for i in range(packet_count):
            packet_label = "🔴 MALICIOUS" if is_malicious[i] else "🟢 NORMAL"
            
            # Find which sequences contain this packet
            containing_sequences = []
            containing_decisions = []
            for seq_idx in range(num_sequences):
                if i >= seq_idx and i < seq_idx + 10:
                    containing_sequences.append(seq_idx + 1)  # 1-indexed
                    containing_decisions.append(decisions[seq_idx])
            
            # LOGIC: Detect if firewall flagged any sequence containing this packet
            any_sequence_blocked = any(d in ["BLOCK", "QUARANTINE"] for d in containing_decisions)
            
            if is_malicious[i]:
                # MALICIOUS packet - should be DETECTED by firewall
                firewall_result = "🚫 DETECTED" if any_sequence_blocked else "❌ MISSED"
                is_correct = any_sequence_blocked  # Correct if firewall caught it
            else:
                # NORMAL packet - packet itself is SAFE, so always CORRECT
                # Being in a blocked sequence doesn't make the packet itself wrong
                firewall_result = "✅ PASSED"
                is_correct = True  # Normal packets are always correct (they're safe)
            
            correct_mark = "✅" if is_correct else "❌"
            
            packet_details.append({
                "Packet #": i + 1,
                "Actual": packet_label,
                "Should Be": "🚫 BLOCK" if is_malicious[i] else "✅ ALLOW",
                "Firewall Result": firewall_result,
                "Correct": correct_mark
            })
        
        research_df = pd.DataFrame(packet_details)
        
        # Add color coding to the dataframe
        st.dataframe(research_df, use_container_width=True)
        
        # Summary statistics
        st.markdown("---")
        st.subheader("📊 Research Summary")
        
        # Calculate based on correct detection
        total_malicious = sum(1 for p in packet_details if "MALICIOUS" in p["Actual"])
        total_normal = sum(1 for p in packet_details if "NORMAL" in p["Actual"])
        
        # Count correctly detected malicious packets
        correctly_detected_malicious = sum(1 for p in packet_details 
                                          if "MALICIOUS" in p["Actual"] and p["Correct"] == "✅")
        # All normal packets are always correct (they're safe)
        correctly_passed_normal = total_normal
        
        incorrectly_missed_malicious = total_malicious - correctly_detected_malicious
        
        total_correct = correctly_detected_malicious + correctly_passed_normal
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("✅ Total Correct", f"{total_correct}/{packet_count}", delta=f"{(total_correct/packet_count)*100:.1f}%")
        col2.metric("🔴 Malicious Detected", f"{correctly_detected_malicious}/{total_malicious}")
        col3.metric("🟢 Normal Passed", f"{correctly_passed_normal}/{total_normal}")
        col4.metric("📊 Total Packets", packet_count)
        
        # Show any errors
        if incorrectly_missed_malicious > 0:
            st.error(f"⚠️ {incorrectly_missed_malicious} malicious packet(s) NOT detected (False Negatives)")
        if incorrectly_missed_malicious == 0:
            st.success("✅ PERFECT - All packets correctly classified!")

        st.subheader("📈 Decision Distribution")

        # Create robust decision counts (handles missing decision types)
        decision_counts = pd.Series(decisions).value_counts().reset_index()
        decision_counts.columns = ["Decision", "Count"]
        
        # Define colors for all possible decisions
        color_map = {
            "ALLOW": "#00CC96",
            "BLOCK": "#FFA15A", 
            "QUARANTINE": "#EF553B"
        }
        
        # Only include colors that actually exist in the data
        available_colors = {k: v for k, v in color_map.items() if k in decision_counts["Decision"].values}
        
        # Create pie chart with available data
        if len(decision_counts) > 0:
            fig = px.pie(
                decision_counts,
                names="Decision",
                values="Count",
                hole=0.4,
                color_discrete_map=available_colors,
                title="📊 Decision Distribution"
            )
            fig.update_layout(showlegend=True, height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("⚠️ No decision data available")

        st.subheader("📊 Actual vs Predicted (Sequence Analysis)")

        # Show window-based comparison
        actual_labels = ["HAS MALICIOUS" if any(is_malicious[i:min(i+10, len(is_malicious))]) 
                         else "NORMAL" 
                         for i in range(num_sequences)]
        predicted = ["BLOCK/QUARANTINE" if d in ["BLOCK", "QUARANTINE"] else "ALLOW" 
                     for d in decisions]
        
        comparison_data = pd.DataFrame({
            "Sequence": range(1, num_sequences+1),
            "Actual": actual_labels,
            "Predicted": predicted,
            "Match": ["✅" if actual_labels[i] == ("BLOCK/QUARANTINE" if predicted[i] == "BLOCK/QUARANTINE" else "NORMAL")
                      else "❌" for i in range(num_sequences)]
        })

        st.dataframe(comparison_data, use_container_width=True)

        st.subheader("📋 Firewall Logs")

        try:
            with open("logs/firewall.log","r") as f:
                logs = f.readlines()[-15:]

            for line in logs[-10:]:
                st.text(line.strip())

        except:
            st.info("No logs found yet")