"""
🔥 LSTM Threshold Calibration Tool
Calculates the optimal anomaly detection threshold from normal data only
"""

import pandas as pd
import numpy as np
from models.lstm_autoencoder import create_sequences
from tensorflow.keras.models import load_model

# Load model
model = load_model("models/lstm_autoencoder.h5", compile=False)

# Load dataset
df = pd.read_csv("data/processed/eeg_features_labeled.csv")

print("=" * 60)
print("🔍 LSTM ANOMALY DETECTION THRESHOLD CALIBRATION")
print("=" * 60)

# Extract NORMAL data only (label == 0)
normal_df = df[df["label"] == 0].drop(columns=["label"])
malicious_df = df[df["label"] == 1].drop(columns=["label"])

print(f"\n📊 Dataset Composition:")
print(f"   Normal samples: {len(normal_df)}")
print(f"   Malicious samples: {len(malicious_df)}")

# Calculate loss for NORMAL data
print(f"\n⚙️  Computing reconstruction loss for NORMAL data...")
normal_sequences = create_sequences(normal_df.values, timesteps=10)
normal_reconstructions = model.predict(normal_sequences, verbose=0)
normal_loss = np.mean(np.square(normal_sequences - normal_reconstructions), axis=(1, 2))

# Calculate loss for MALICIOUS data
print(f"⚙️  Computing reconstruction loss for MALICIOUS data...")
malicious_sequences = create_sequences(malicious_df.values, timesteps=10)
malicious_reconstructions = model.predict(malicious_sequences, verbose=0)
malicious_loss = np.mean(np.square(malicious_sequences - malicious_reconstructions), axis=(1, 2))

# Analysis
print(f"\n📈 NORMAL DATA LOSS Statistics:")
print(f"   Mean:     {np.mean(normal_loss):.6f}")
print(f"   Std Dev:  {np.std(normal_loss):.6f}")
print(f"   Min:      {np.min(normal_loss):.6f}")
print(f"   Max:      {np.max(normal_loss):.6f}")
print(f"   Median:   {np.median(normal_loss):.6f}")

print(f"\n📈 MALICIOUS DATA LOSS Statistics:")
print(f"   Mean:     {np.mean(malicious_loss):.6f}")
print(f"   Std Dev:  {np.std(malicious_loss):.6f}")
print(f"   Min:      {np.min(malicious_loss):.6f}")
print(f"   Max:      {np.max(malicious_loss):.6f}")
print(f"   Median:   {np.median(malicious_loss):.6f}")

# Calculate optimal threshold
threshold_mean_2std = np.mean(normal_loss) + 2 * np.std(normal_loss)
threshold_mean_3std = np.mean(normal_loss) + 3 * np.std(normal_loss)
threshold_median = np.median(normal_loss)
threshold_max = np.max(normal_loss)

print(f"\n🎯 RECOMMENDED THRESHOLDS:")
print(f"   Mean + 2×Std (Balanced):         {threshold_mean_2std:.6f}")
print(f"   Mean + 3×Std (Conservative):    {threshold_mean_3std:.6f}")
print(f"   Max of Normal (Aggressive):     {threshold_max:.6f}")

# Test detection accuracy
print(f"\n✅ TESTING DETECTION ACCURACY:")

def test_threshold(threshold, name):
    # Count correct detections
    normal_detected_as_normal = np.sum(normal_loss < threshold)
    malicious_detected_as_anomaly = np.sum(malicious_loss >= threshold)
    
    normal_accuracy = (normal_detected_as_normal / len(normal_loss)) * 100
    malicious_accuracy = (malicious_detected_as_anomaly / len(malicious_loss)) * 100
    overall_accuracy = ((normal_detected_as_normal + malicious_detected_as_anomaly) / 
                        (len(normal_loss) + len(malicious_loss))) * 100
    
    print(f"\n   Threshold: {threshold:.6f} ({name})")
    print(f"   ✓ Normal detection rate:    {normal_accuracy:.1f}%")
    print(f"   ✓ Malicious detection rate: {malicious_accuracy:.1f}%")
    print(f"   ✓ Overall accuracy:         {overall_accuracy:.1f}%")
    
    return overall_accuracy

acc1 = test_threshold(threshold_mean_2std, "Mean+2Std")
acc2 = test_threshold(threshold_mean_3std, "Mean+3Std")
acc3 = test_threshold(threshold_max, "Max Normal")

print("\n" + "=" * 60)
print("🎓 RECOMMENDATION:")
print("=" * 60)

best_threshold = threshold_mean_2std  # Default to balanced approach
print(f"\nBest threshold: {best_threshold:.6f}")
print(f"\n✏️  Update 'scripts/lstm_detector.py' with:")
print(f"   THRESHOLD = {best_threshold:.6f}")
print("=" * 60)
