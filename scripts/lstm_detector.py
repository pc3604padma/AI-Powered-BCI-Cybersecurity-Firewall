import numpy as np
import streamlit as st
from tensorflow.keras.models import load_model
from models.lstm_autoencoder import create_sequences

# 🔥 LAZY LOAD: Only load model when needed (cached)
@st.cache_resource
def get_model():
    """Load model once and cache it across app reruns"""
    return load_model("models/lstm_autoencoder.h5", compile=False)

# Threshold (CALIBRATED from normal data only)
# Calculated by: calibrate_threshold.py
# Normal loss:    0.000589
# Malicious loss: 0.184-0.391
THRESHOLD = 0.000589  # 🔥 OPTIMAL THRESHOLD


# 🔥 IMPORTANT: This function calculates proper threshold from NORMAL data only
def get_optimal_threshold(df_with_labels):
    """
    Calculate threshold using ONLY normal data (label=0)
    This ensures the model's reconstruction baseline is set correctly
    """
    model = get_model()
    from models.lstm_autoencoder import create_sequences
    
    # Extract ONLY normal data
    normal_data = df_with_labels[df_with_labels["label"] == 0].drop(columns=["label"]).values
    
    if len(normal_data) < 15:
        raise ValueError("Not enough normal data samples for threshold calculation")
    
    sequences = create_sequences(normal_data, timesteps=10)
    reconstructions = model.predict(sequences, verbose=0)
    loss = np.mean(np.square(sequences - reconstructions), axis=(1, 2))
    
    # Set threshold at mean + 2*stddev of NORMAL data loss
    threshold = np.mean(loss) + 2 * np.std(loss)
    
    print(f"📊 Threshold Calculation (from normal data only):")
    print(f"   Mean loss: {np.mean(loss):.6f}")
    print(f"   Std dev: {np.std(loss):.6f}")
    print(f"   Optimal threshold: {threshold:.6f}")
    
    return threshold


# -----------------------------
# Anomaly Detection Function
# -----------------------------
def detect_anomaly(data):
    model = get_model()
    sequences = create_sequences(data, timesteps=10)

    if len(sequences) == 0:
        return ["NORMAL"], [0.0]

    reconstructions = model.predict(sequences, verbose=0)

    loss = np.mean(np.square(sequences - reconstructions), axis=(1,2))

    # 🔥 DEBUG PRINT
    print("LOSS VALUES:", loss[:5])
    print(f"THRESHOLD: {THRESHOLD}")


    results = []

    for l in loss:
        if l > THRESHOLD:  # 🔥 HIGH loss = ANOMALY detected
            results.append("ANOMALY")
        else:
            results.append("NORMAL")

    return results, loss
# -----------------------------
# Threshold Calculation (DEPRECATED - use get_optimal_threshold instead)
# ⚠️  This function uses mixed data (normal + malicious). Use get_optimal_threshold()
def calculate_threshold(data):
    model = get_model()
    sequences = create_sequences(data, timesteps=10)

    # 🔥 FIX FOR YOUR ERROR
    if len(sequences) == 0:
        raise ValueError("Not enough data to form sequences (need at least 10 rows)")

    reconstructions = model.predict(sequences, verbose=0)

    loss = np.mean(np.square(sequences - reconstructions), axis=(1, 2))

    threshold = np.mean(loss) + 2 * np.std(loss)
    
    print("⚠️  WARNING: calculate_threshold() uses mixed data (normal+malicious).")
    print("            Use get_optimal_threshold() for better results!")

    return threshold, loss