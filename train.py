import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

from data_loader import load_data
from inference import preprocess_data, create_sequences

def train_model(data, sequence_length=10, epochs=50, batch_size=64):
    scaled_data = preprocess_data(data)

    sequences = create_sequences(scaled_data, sequence_length)

    X_train, X_test, y_train, y_test = train_test_split(
        sequences[:, :-1], sequences[:, -1], test_size=0.2, random_state=42
    )

    model = Sequential()
    model.add(LSTM(50, activation="relu", input_shape=(X_train.shape[1], X_train.shape[2])))
    model.add(Dense(1))
    model.compile(optimizer="adam", loss="mse")

    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.1)

    loss = model.evaluate(X_test, y_test)
    print(f"Mean Squared Error on Test Set: {loss}")

    return model
