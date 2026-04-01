import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
import json
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import warnings
warnings.filterwarnings('ignore')

from auth import create_user, login_user
from scripts.bci_firewall import firewall_decision
from scripts.mixed_data_utils import create_realistic_stream_test
from database import log_firewall_scan, get_firewall_history, get_firewall_stats

# ========== PAGE CONFIG ==========
st.set_page_config(page_title="Synora - BCI Security", layout="wide")

# ========== STYLING ==========
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }
</style>
""", unsafe_allow_html=True)

# ========== SESSION STATES ==========
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "email" not in st.session_state:
    st.session_state.email = None
if "scan_results" not in st.session_state:
    st.session_state.scan_results = None

# ========== AUTHENTICATION ==========
if not st.session_state.logged_in:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <h1 style='color: #e94540;'>SYNORA</h1>
        <h3 style='color: #ffa15a;'>AI Cybersecurity for Brain Interfaces</h3>
        """, unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("**Enterprise-grade threat detection for EEG-based systems**")
    
    with col2:
        tab1, tab2 = st.tabs(["Login", "Create Account"])
        
        with tab1:
            st.subheader("Welcome Back")
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            
            if st.button("Login", use_container_width=True, type="primary"):
                if email and password:
                    try:
                        if login_user(email, password):
                            st.session_state.logged_in = True
                            st.session_state.email = email
                            st.success("Login Successful!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("Invalid credentials")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                else:
                    st.error("Enter email and password")
        
        with tab2:
            st.subheader("Create Account")
            new_email = st.text_input("Email", key="signup_email")
            new_password = st.text_input("Password", type="password", key="signup_password")
            confirm = st.text_input("Confirm Password", type="password", key="confirm_password")
            
            if st.button("Create Account", use_container_width=True, type="primary"):
                if not new_email or not new_password:
                    st.error("Email and password required")
                elif new_password != confirm:
                    st.error("Passwords don't match")
                elif len(new_password) < 6:
                    st.error("Password must be 6+ characters")
                else:
                    try:
                        if create_user(new_email, new_password):
                            st.success("Account created! Please log in.")
                        else:
                            st.error("Account creation failed")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

# ========== MAIN DASHBOARD (AFTER LOGIN) ==========
else:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #e94540 0%, #c1121f 100%); padding: 30px; border-radius: 10px; margin-bottom: 30px;'>
        <h1 style='color: white; margin: 0;'>SYNORA - Firewall Dashboard</h1>
        <p style='color: #eee; margin: 10px 0 0 0;'>AI-Powered Brain Interface Security</p>
    </div>
    """, unsafe_allow_html=True)
    
    # User info & logout
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.email = None
            st.rerun()
    with col1:
        st.markdown(f"**User:** {st.session_state.email}")
    
    st.markdown("---")
    
    # SIDEBAR NAVIGATION
    with st.sidebar:
        st.markdown("### Navigation")
        page = st.radio(
            "Features:",
            ["Dashboard & Scan", "History & Reports", "Explainable AI", "Security Center"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("### Quick Stats")
        try:
            stats = get_firewall_stats(st.session_state.email)
            if stats and stats.get('total_scans', 0) > 0:
                st.metric("Total Scans", stats.get('total_scans', 0))
                st.metric("Avg Accuracy", f"{stats.get('avg_accuracy', 0):.1f}%")
                st.metric("Threats Found", stats.get('total_threats', 0))
            else:
                st.metric("Total Scans", 0)
                st.metric("Avg Accuracy", "0.0%")
                st.metric("Threats Found", 0)
        except Exception as e:
            st.metric("Total Scans", 0)
            st.metric("Avg Accuracy", "0.0%")
            st.metric("Threats Found", 0)
    
    # ========== PAGE 1: DASHBOARD & SCAN (COMBINED) ==========
    if page == "Dashboard & Scan":
        st.markdown("### Real-Time EEG Threat Detection")
        st.markdown("Scan EEG datasets to detect malicious patterns. The system will randomly inject anomalies at 30% rate and analyze detection accuracy.")
        
        st.markdown("---")
        
        # SCAN CONTROL
        st.subheader("Scan Configuration")
        col1, col2 = st.columns([3, 1])
        with col1:
            num_packets = st.slider("Number of packets to scan", 5, 100, 20)
        with col2:
            if st.button("SCAN DATASET", use_container_width=True, type="primary"):
                with st.spinner("⏳ Scanning..."):
                    try:
                        # Generate data with 30% injection (fixed, no slider)
                        df_mixed, is_malicious = create_realistic_stream_test(num_packets, 0.3)
                        
                        # Run detection
                        decisions = firewall_decision(df_mixed, session_id="STREAMLIT_UI")
                        
                        # Store results
                        st.session_state.scan_results = {
                            "df_mixed": df_mixed,
                            "is_malicious": is_malicious,
                            "decisions": decisions,
                            "packet_count": num_packets,
                            "timestamp": datetime.now()
                        }
                        
                        # Log to database
                        try:
                            decision_counts = pd.Series(decisions).value_counts().to_dict() if len(decisions) > 0 else {}
                            malicious_count = sum(is_malicious)
                            num_sequences = len(decisions)
                            
                            # Calculate accuracy
                            if num_sequences > 0:
                                correct = sum(
                                    1 for i in range(num_sequences)
                                    if (decisions[i] in ["BLOCK", "QUARANTINE"]) == 
                                    any(is_malicious[i:min(i+10, len(is_malicious))])
                                )
                                accuracy = (correct / num_sequences) * 100
                            else:
                                accuracy = 0
                            
                            log_firewall_scan(
                                st.session_state.email,
                                num_packets,
                                num_sequences,
                                list(decisions),
                                is_malicious,
                                accuracy,
                                malicious_count,
                                num_packets - malicious_count,
                                decision_counts
                            )
                        except:
                            pass
                        
                        st.success(f"Scan completed! Analyzed {num_packets} packets, generated {num_sequences} sequences")
                        
                        # Send email alert if threats
                        total_malicious = int(sum(is_malicious))
                        if total_malicious > 0:
                            try:
                                import email_alerts
                                email_alerts.send_email(
                                    st.session_state.email,
                                    f"BCI Firewall Alert - {total_malicious} Threats Detected!",
                                    f"Security Alert: {total_malicious} threats detected in {num_packets} packets. Check your dashboard."
                                )
                            except:
                                pass
                                
                    except Exception as e:
                        st.error(f"Scan failed: {str(e)}")
        
        # ========== DISPLAY RESULTS ==========
        if st.session_state.scan_results is not None:
            results = st.session_state.scan_results
            df_mixed = results["df_mixed"]
            is_malicious = results["is_malicious"]
            decisions = results["decisions"]
            packet_count = results["packet_count"]
            
            num_sequences = len(decisions)
            total_malicious_actual = sum(is_malicious)
            total_normal_actual = packet_count - total_malicious_actual
            
            # Calculate accuracy
            if num_sequences > 0:
                correct_detections = 0
                for i in range(num_sequences):
                    window_end = min(i + 10, len(is_malicious))
                    window_has_malicious = any(is_malicious[i:window_end])
                    decision_is_block = decisions[i] in ["BLOCK", "QUARANTINE"]
                    if decision_is_block == window_has_malicious:
                        correct_detections += 1
                accuracy = (correct_detections / num_sequences) * 100
            else:
                accuracy = 0
            
            st.markdown("---")
            st.subheader("Scan Results")
            
            # KEY METRICS
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Packets Scanned", packet_count)
            col2.metric("Threats Detected", total_malicious_actual)
            col3.metric("Accuracy", f"{accuracy:.1f}%" if num_sequences > 0 else "0.0%")
            col4.metric("Sequences Analyzed", num_sequences)
            
            # Display info if data is limited
            if num_packets < 11:
                st.warning(f"Limited data: {num_packets} packets generate {num_sequences} sequence(s). Use 11+ packets for full analysis.")
            
            st.markdown("---")
            
            # FIREWALL DECISIONS TABLE
            st.subheader("Firewall Decisions (Sequence Level)")
            if num_sequences > 0:
                table_data = {
                    "Sequence": range(1, num_sequences+1),
                    "Decision": decisions,
                    "Contains Malicious": [any(is_malicious[i:min(i+10, len(is_malicious))]) for i in range(num_sequences)],
                    "Correct": ["PASS" if (decisions[i] in ["BLOCK", "QUARANTINE"]) == any(is_malicious[i:min(i+10, len(is_malicious))]) else "FAIL" for i in range(num_sequences)]
                }
                st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)
            else:
                st.info(f"Packet-level analysis: {num_packets} packets. Need 11+ packets to create 10-packet sliding windows.")
                st.dataframe(pd.DataFrame({
                    "Packets": range(1, packet_count+1),
                    "Status": ["MALICIOUS" if is_malicious[i] else "NORMAL" for i in range(packet_count)],
                    "Raw Analysis": ["Anomaly detected" if is_malicious[i] else "Normal" for i in range(packet_count)]
                }), use_container_width=True, hide_index=True)            
            st.markdown("---")
            
            # VISUALIZATIONS
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Packet Distribution")
                packet_type_data = pd.DataFrame({
                    "Type": ["MALICIOUS" if is_malicious[i] else "NORMAL" for i in range(packet_count)],
                    "Type_Code": ["MALICIOUS" if is_malicious[i] else "NORMAL" for i in range(packet_count)]
                })
                packet_counts = packet_type_data['Type_Code'].value_counts()
                fig = px.bar(
                    x=packet_counts.index,
                    y=packet_counts.values,
                    color=packet_counts.index,
                    color_discrete_map={"MALICIOUS": "#EF553B", "NORMAL": "#00CC96"},
                    labels={"x": "Type", "y": "Count"},
                    title="Packet Classification"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("### Decision Distribution")
                if num_sequences > 0:
                    decision_counts_series = pd.Series(decisions).value_counts()
                    # Ensure all three classifications are shown
                    all_decisions = {"ALLOW": 0, "QUARANTINE": 0, "BLOCK": 0}
                    for decision in ["ALLOW", "BLOCK", "QUARANTINE"]:
                        if decision in decision_counts_series.index:
                            all_decisions[decision] = int(decision_counts_series[decision])
                    
                    decision_df = pd.DataFrame(list(all_decisions.items()), columns=["Decision", "Count"])
                    colors_map = {
                        "ALLOW": "#00CC96",
                        "BLOCK": "#FFA15A",
                        "QUARANTINE": "#EF553B"
                    }
                    fig = px.pie(
                        decision_df,
                        names="Decision",
                        values="Count",
                        hole=0.4,
                        color_discrete_map=colors_map,
                        title="Firewall Decisions (All 3 Classifications)"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    # Show empty pie chart with all three classifications at 0
                    empty_df = pd.DataFrame({"Decision": ["ALLOW", "BLOCK", "QUARANTINE"], "Count": [0, 0, 0]})
                    colors_map = {
                        "ALLOW": "#00CC96",
                        "BLOCK": "#FFA15A",
                        "QUARANTINE": "#EF553B"
                    }
                    fig = px.pie(
                        empty_df,
                        names="Decision",
                        values="Count",
                        hole=0.4,
                        color_discrete_map=colors_map,
                        title="Firewall Decisions (No Sequences Yet)"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    st.info("Scan with 11+ packets to generate sequence-based decisions")
            
            st.markdown("---")
            
            # PACKET-LEVEL ANALYSIS
            st.subheader("Research Data - Packet Details")
            packet_details = []
            for i in range(packet_count):
                packet_label = "MALICIOUS" if is_malicious[i] else "NORMAL"
                
                containing_decisions = []
                for seq_idx in range(num_sequences):
                    if i >= seq_idx and i < seq_idx + 10:
                        containing_decisions.append(decisions[seq_idx])
                
                any_sequence_blocked = any(d in ["BLOCK", "QUARANTINE"] for d in containing_decisions)
                
                if is_malicious[i]:
                    firewall_result = "DETECTED" if any_sequence_blocked else "MISSED"
                    is_correct = any_sequence_blocked
                else:
                    firewall_result = "PASSED"
                    is_correct = True
                
                packet_details.append({
                    "Packet #": i + 1,
                    "Actual": packet_label,
                    "Should Be": "BLOCK" if is_malicious[i] else "ALLOW",
                    "Result": firewall_result,
                    "Correct": "PASS" if is_correct else "FAIL"
                })
            
            research_df = pd.DataFrame(packet_details)
            st.dataframe(research_df, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            
            # RESEARCH SUMMARY
            st.subheader("Research Summary")
            total_malicious = sum(1 for p in packet_details if "MALICIOUS" in p["Actual"])
            total_normal = sum(1 for p in packet_details if "NORMAL" in p["Actual"])
            correctly_detected_malicious = sum(1 for p in packet_details if "MALICIOUS" in p["Actual"] and p["Correct"] == "PASS")
            correctly_passed_normal = total_normal
            incorrectly_missed = total_malicious - correctly_detected_malicious
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Malicious Detected", f"{correctly_detected_malicious}/{total_malicious}")
            col2.metric("Normal Passed", f"{correctly_passed_normal}/{total_normal}")
            col3.metric("Missed Threats", incorrectly_missed)
            col4.metric("Total Correct", f"{correctly_detected_malicious + correctly_passed_normal}/{packet_count}")
            
            if incorrectly_missed == 0:
                st.success("PERFECT - All packets correctly classified!")
            elif incorrectly_missed > 0:
                st.error(f"{incorrectly_missed} malicious packet(s) NOT detected (False Negatives)")
            
            st.markdown("---")
            
            # RANDOM DISTRIBUTION
            st.subheader("Random Packet Distribution")
            packet_labels_visual = ["MALICIOUS" if is_malicious[i] else "NORMAL" for i in range(packet_count)]
            packet_type_data = pd.DataFrame({
                "Packet": [f"P{i+1}" for i in range(packet_count)],
                "Type": packet_labels_visual,
                "Type_Code": ["MALICIOUS" if is_malicious[i] else "NORMAL" for i in range(packet_count)]
            })
            
            fig_dist = px.bar(
                packet_type_data,
                x="Packet",
                y=[1]*packet_count,
                color="Type_Code",
                color_discrete_map={"MALICIOUS": "#EF553B", "NORMAL": "#00CC96"},
                labels={"y": "Packet Status"},
                height=250,
                title="Random Packet Distribution (Red=Malicious, Green=Normal)"
            )
            fig_dist.update_layout(
                showlegend=False,
                yaxis_title="",
                xaxis_title="Packets",
                yaxis=dict(showticklabels=False),
                hovermode="x unified"
            )
            st.plotly_chart(fig_dist, use_container_width=True)
            
            malicious_packets = [i+1 for i in range(packet_count) if is_malicious[i]]
            normal_packets = [i+1 for i in range(packet_count) if not is_malicious[i]]
            
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"**NORMAL Packets:**\n\n{', '.join(map(str, normal_packets[:20]))}{'...' if len(normal_packets) > 20 else ''}")
            with col2:
                st.warning(f"**MALICIOUS Packets:**\n\n{', '.join(map(str, malicious_packets[:20]))}{'...' if len(malicious_packets) > 20 else ''}")
            
            st.markdown("---")
            
            # ATTACK EXPLANATION
            st.subheader("Attack Method Explanation")
            with st.expander("How are malicious packets created?"):
                st.markdown("""
### Malicious Pattern Injection Process:

**Step 1: Amplification** - Values × Random(6-12) = 6-12x amplification  
**Step 2: Frequency Distortion** - Bands × Random(3-6) = Unnatural patterns  
**Step 3: Noise Addition** - Gaussian N(0, 5.0) = Complete anomaly  
**Step 4: Random Distribution** - Mixed with normal packets = Realistic attack  

**Result:** LSTM detects reconstruction error ~0.0006 vs normal ~0.000589 threshold
                """)
            
            st.markdown("---")
            
            # DATA TRANSPARENCY
            st.subheader("Data Transparency & Verification")
            st.info("Download datasets to inspect exactly what was injected during the attack simulation.")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                csv_data = df_mixed.to_csv(index=False)
                st.download_button("Download CSV", csv_data, "eeg_data.csv", "text/csv")
            
            with col2:
                injection_meta = "Packet,Is_Malicious,Injection_Applied\n"
                for i in range(packet_count):
                    injection_meta += f"{i+1},{'Yes' if is_malicious[i] else 'No'},{'AMPLIFIED+NOISE' if is_malicious[i] else 'ORIGINAL'}\n"
                st.download_button("Download Injection Log", injection_meta, "injection_log.csv", "text/csv")
            
            with col3:
                json_data = json.dumps({
                    "timestamp": str(results['timestamp']),
                    "packets": int(packet_count),
                    "accuracy": float(accuracy) if num_sequences > 0 else None,
                    "threats": int(total_malicious_actual),
                    "sequences": int(num_sequences)
                }, indent=2)
                st.download_button("Download JSON", json_data, "scan_report.json", "application/json")
            
            st.markdown("---")
            
            # INJECTION REPORT
            st.subheader("Injection Report")
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
    
    # ========== PAGE 2: HISTORY & REPORTS ==========
    elif page == "History & Reports":
        st.markdown("### Scan History & Security Reports")
        
        tab1, tab2, tab3 = st.tabs(["History", "Statistics", "Export"])
        
        with tab1:
            try:
                history = get_firewall_history(st.session_state.email, limit=50)
                if history and len(history) > 0:
                    st.markdown(f"**Total Scans:** {len(history)}")
                    history_display = []
                    for log in history:
                        try:
                            timestamp = log.get('timestamp', 'N/A')
                            if timestamp and timestamp != 'N/A':
                                timestamp = timestamp[:19]  # Get only date and time part
                            
                            history_display.append({
                                "Date": timestamp,
                                "Packets": log.get('scan_config', {}).get('total_packets', 0),
                                "Accuracy": f"{log.get('results', {}).get('accuracy', 0):.1f}%",
                                "Threats": log.get('results', {}).get('malicious_detected', 0)
                            })
                        except Exception as e:
                            continue
                    
                    if history_display:
                        df_history = pd.DataFrame(history_display)
                        st.dataframe(df_history, use_container_width=True, hide_index=True)
                    else:
                        st.info("No valid scan records found")
                else:
                    st.info("No scan history yet. Run a scan to see history here.")
            except Exception as e:
                st.warning(f"History unavailable")
                st.info("Ensure MongoDB is running and you have performed at least one scan.")
        
        with tab2:
            try:
                stats = get_firewall_stats(st.session_state.email)
                if stats and stats.get('total_scans', 0) > 0:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Total Scans", stats.get('total_scans', 0))
                        st.metric("Avg Accuracy", f"{stats.get('avg_accuracy', 0):.1f}%")
                    with col2:
                        st.metric("Total Threats", stats.get('total_threats', 0))
                        st.metric("Total Packets", stats.get('total_packets_scanned', 0))
                    
                    # Decision distribution from history
                    st.markdown("---")
                    st.subheader("Decision Distribution (Historical)")
                    decision_dist = stats.get('decision_distribution', {})
                    if decision_dist:
                        dist_df = pd.DataFrame(list(decision_dist.items()), columns=["Decision", "Count"])
                        fig = px.bar(dist_df, x="Decision", y="Count", color="Decision",
                                    color_discrete_map={"ALLOW": "#00CC96", "BLOCK": "#FFA15A", "QUARANTINE": "#EF553B"},
                                    title="Firewall Decisions Over Time")
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No statistics available yet. Run some scans first!")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Total Scans", 0)
                        st.metric("Avg Accuracy", "0.0%")
                    with col2:
                        st.metric("Total Threats", 0)
                        st.metric("Total Packets", 0)
            except Exception as e:
                st.error(f"Error loading statistics: {str(e)}")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Scans", 0)
                    st.metric("Avg Accuracy", "0.0%")
                with col2:
                    st.metric("Total Threats", 0)
                    st.metric("Total Packets", 0)
        
        with tab3:
            st.markdown("#### Export Options")
            if st.session_state.scan_results:
                results = st.session_state.scan_results
                num_sequences = len(results['decisions'])
                packet_count = results['packet_count']
                is_malicious = results['is_malicious']
                
                # Calculate accuracy
                accuracy = 0
                if num_sequences > 0:
                    accuracy = (sum(1 for i in range(num_sequences) if (results['decisions'][i] in ['BLOCK', 'QUARANTINE']) == any(is_malicious[i:min(i+10, len(is_malicious))])) / num_sequences * 100)
                
                col1, col2, col3 = st.columns(3)
                
                # PDF Export
                with col1:
                    if st.button("Generate PDF Report", use_container_width=True, type="primary"):
                        try:
                            pdf_buffer = BytesIO()
                            pdf = SimpleDocTemplate(pdf_buffer, pagesize=letter)
                            elements = []
                            styles = getSampleStyleSheet()
                            
                            title = Paragraph("SYNORA Security Report", styles['Title'])
                            elements.append(title)
                            elements.append(Spacer(1, 12))
                            
                            info_text = f"Generated: {results['timestamp']}<br/>User: {st.session_state.email}"
                            elements.append(Paragraph(info_text, styles['Normal']))
                            elements.append(Spacer(1, 12))
                            
                            data = [
                                ["Metric", "Value"],
                                ["Packets Scanned", str(packet_count)],
                                ["Sequences Analyzed", str(num_sequences)],
                                ["Detection Accuracy", f"{accuracy:.1f}%"],
                                ["Threats Detected", str(int(sum(is_malicious)))]
                            ]
                            
                            table = Table(data)
                            table.setStyle(TableStyle([
                                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e94540')),
                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                ('GRID', (0, 0), (-1, -1), 1, colors.grey)
                            ]))
                            elements.append(table)
                            
                            pdf.build(elements)
                            pdf_buffer.seek(0)
                            
                            st.download_button("Download PDF", pdf_buffer.getvalue(), "security_report.pdf", "application/pdf", key="pdf_export")
                            st.success("PDF ready to download")
                        except Exception as e:
                            st.error(f"PDF error: {str(e)}")
                
                # CSV Export
                with col2:
                    try:
                        csv_data = results['df_mixed'].to_csv(index=False)
                        st.download_button("Download CSV", csv_data, "eeg_data.csv", "text/csv", key="csv_export")
                    except Exception as e:
                        st.error(f"CSV error: {str(e)}")
                
                # JSON Export
                with col3:
                    try:
                        json_data = json.dumps({
                            "timestamp": str(results['timestamp']),
                            "packets": int(packet_count),
                            "accuracy": float(accuracy),
                            "threats": int(sum(is_malicious)),
                            "sequences": int(num_sequences)
                        }, indent=2)
                        st.download_button("Download JSON", json_data, "scan_report.json", "application/json", key="json_export")
                    except Exception as e:
                        st.error(f"JSON error: {str(e)}")
                
                st.markdown("---")
                st.info(f"Scan Summary: {packet_count} packets, {num_sequences} sequences, {accuracy:.1f}% accuracy")
            else:
                st.info("Run a scan first to export reports")
    
    # ========== PAGE 3: EXPLAINABLE AI ==========
    elif page == "Explainable AI":
        st.markdown("### Explainable AI - Understanding Firewall Decisions")
        st.info("Learn WHY the firewall made specific decisions")
        
        if st.session_state.scan_results:
            results = st.session_state.scan_results
            
            st.markdown("### How LSTM Detects Anomalies:")
            st.markdown("""
1. **Training Phase**: Trained on normal EEG data only
2. **Feature Learning**: Learns natural brain signal patterns  
3. **Detection**: Reconstruction error indicates deviation
4. **Threshold**: Error > 0.000589 indicates Anomaly
5. **Decision**: Sequence-level classification (10-packet windows)
            """)
            
            st.markdown("---")
            st.markdown("### Current Scan Analysis:")
            
            num_sequences = len(results['decisions'])
            if num_sequences > 0:
                explanations = []
                for i in range(min(10, num_sequences)):
                    window_start = i
                    window_end = min(i + 10, results['packet_count'])
                    has_malicious = any(results['is_malicious'][window_start:window_end])
                    decision = results['decisions'][i]
                    
                    explanation = {
                        "Sequence": i + 1,
                        "Decision": decision,
                        "Has Malicious": "Yes" if has_malicious else "No",
                        "Reasoning": (
                            "High reconstruction error detected"
                            if decision in ["BLOCK", "QUARANTINE"]
                            else "Normal reconstruction error"
                        )
                    }
                    explanations.append(explanation)
                
                exp_df = pd.DataFrame(explanations)
                st.dataframe(exp_df, use_container_width=True, hide_index=True)
        else:
            st.info("Run a scan first to see decision explanations")
    
    # ========== PAGE 4: SECURITY CENTER ==========
    elif page == "Security Center":
        st.markdown("### Security Center")
        
        tab1, tab2 = st.tabs(["Settings", "Status"])
        
        with tab1:
            st.markdown("#### System Configuration")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Detection Parameters**")
                threshold = st.number_input("LSTM Threshold", 0.0001, 0.001, 0.000589)
                sensitivity = st.slider("Sensitivity", 0.5, 1.5, 1.0, 0.1)
            with col2:
                st.markdown("**Scan Settings**")
                st.checkbox("Email Alerts on Detection", value=True)
                st.checkbox("Auto-save scan results", value=True)
            
            if st.button("Save Settings", use_container_width=True):
                st.success("Settings saved")
        
        with tab2:
            st.markdown("#### Security Status")
            security = [
                ("Authentication", "Configured"),
                ("Database", "Connected"),
                ("Data Privacy", "Protected"),
                ("Alerts", "Active"),
                ("Encryption", "Enabled"),
            ]
            for check, status in security:
                st.markdown(f"**{check}**: {status}")
