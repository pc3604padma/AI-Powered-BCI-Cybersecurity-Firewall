import pandas as pd
import numpy as np
from scripts.lstm_detector import model, create_sequences

df = pd.read_csv("data/processed/eeg_features_labeled.csv")

# 🔥 ONLY NORMAL
X = df[df["label"] == 0].drop(columns=["label"]).values

sequences = create_sequences(X, timesteps=10)

recon = model.predict(sequences, verbose=0)

loss = np.mean(np.square(sequences - recon), axis=(1,2))

threshold = np.mean(loss) + 2 * np.std(loss)

print("FINAL THRESHOLD:", threshold)