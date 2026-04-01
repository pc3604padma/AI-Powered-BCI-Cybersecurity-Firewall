import numpy as np
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, RepeatVector, TimeDistributed, Dense

def build_lstm_autoencoder(timesteps, features):

    inputs = Input(shape=(timesteps, features))

    # Encoder
    encoded = LSTM(64, activation='relu')(inputs)

    # Repeat
    decoded = RepeatVector(timesteps)(encoded)

    # Decoder
    decoded = LSTM(64, activation='relu', return_sequences=True)(decoded)

    # 🔥 IMPORTANT FIX (match output to input features)
    outputs = TimeDistributed(Dense(features))(decoded)

    autoencoder = Model(inputs, outputs)
    autoencoder.compile(optimizer='adam', loss='mse')

    return autoencoder


def create_sequences(data, timesteps=10):
    sequences = []
    for i in range(len(data) - timesteps):
        sequences.append(data[i:i+timesteps])
    return np.array(sequences)