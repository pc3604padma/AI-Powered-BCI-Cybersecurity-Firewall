import pandas as pd
import numpy as np
from models.lstm_autoencoder import build_lstm_autoencoder, create_sequences
import joblib

# Load dataset
df = pd.read_csv("data/processed/eeg_features_labeled.csv")

# 🔥 ONLY NORMAL DATA
X = df[df["label"] == 0].drop(columns=["label"]).values
# Create sequences
timesteps = 10
X_seq = create_sequences(X, timesteps)

# Build model
model = build_lstm_autoencoder(timesteps, X.shape[1])

# Train ONLY on normal data
model.fit(
    X_seq,
    X_seq,
    epochs=20,
    batch_size=32,
    validation_split=0.1
)

# Save model
model.save("models/lstm_autoencoder.h5")

print("Model trained and saved!")