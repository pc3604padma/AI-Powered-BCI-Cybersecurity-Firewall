import streamlit as st
import pandas as pd
import time
import plotly.express as px
import plotly.graph_objects as go
import joblib
import numpy as np
from scripts.bci_firewall import firewall_decision

st.set_page_config(page_title="BCI Security Dashboard", layout="wide")

st.title("🧠 BCI Security Monitoring System")
st.markdown("Real-Time AI Firewall with Risk Intelligence")
st.markdown("---")

# Load dataset and model
df = pd.read_csv("data/processed/eeg_features_labeled.csv")
X = df.drop(columns=["label"])
model = joblib.load("models/isolation_forest.pkl")

# Sidebar
st.sidebar.header("System Controls")

num_packets = st.sidebar.slider(
    "EEG Packets",
    min_value=1,
    max_value=20,
    value=5
)

run = st.sidebar.button("🚀 Start Live Monitoring")

if run:

    results = []
    confidences = []

    progress = st.progress(0)

    for i in range(num_packets):

        packet = X.iloc[[i]]

        decision = firewall_decision(packet, session_id="UI_SESSION")[0]
        results.append(decision)

        # Model confidence score
        score = model.decision_function(packet)[0]
        confidences.append(score)

        progress.progress((i + 1) / num_packets)
        time.sleep(0.5)

    # Layout Columns
    col1, col2, col3 = st.columns(3)

    anomaly_count = results.count("BLOCK") + results.count("QUARANTINE")

    with col1:
        st.metric("Total Packets", num_packets)

    with col2:
        st.metric("Anomalies Detected", anomaly_count)

    with col3:
        avg_conf = round(np.mean(confidences), 4)
        st.metric("Avg Model Score", avg_conf)

    st.markdown("---")

    # Risk Indicator
    if anomaly_count == 0:
        st.success("🟢 SYSTEM STATUS: SAFE")
    elif anomaly_count < 3:
        st.warning("🟡 SYSTEM STATUS: CAUTION")
    else:
        st.error("🔴 SYSTEM STATUS: HIGH RISK")

    st.markdown("---")

    # Decision Pie Chart
    st.subheader("Firewall Decision Distribution")

    decision_counts = pd.Series(results).value_counts().reset_index()
    decision_counts.columns = ["Decision", "Count"]

    fig = px.pie(
        decision_counts,
        names="Decision",
        values="Count",
        hole=0.4
    )

    st.plotly_chart(fig, use_container_width=True)

    # EEG Feature Visualization (Alpha Band Example)
    st.subheader("EEG Feature Trend (Alpha Band)")

    alpha_values = df["alpha"].head(num_packets)

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        y=alpha_values,
        mode='lines+markers',
        name='Alpha Power'
    ))

    fig2.update_layout(
        xaxis_title="Packet Index",
        yaxis_title="Alpha Power"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # XAI-style Explanation (Top Feature Impact)
    st.subheader("AI Decision Insights")

    feature_importance = X.head(num_packets).mean().sort_values(ascending=False)
    top_features = feature_importance.head(5)

    fig3 = px.bar(
        x=top_features.values,
        y=top_features.index,
        orientation='h',
        title="Top Influential EEG Features"
    )

    st.plotly_chart(fig3, use_container_width=True)

    # Log Preview
    st.subheader("Recent Firewall Logs")

    try:
        with open("logs/firewall.log", "r") as f:
            logs = f.readlines()[-10:]
            for line in logs:
                st.text(line.strip())
    except:
        st.info("No logs available.")
