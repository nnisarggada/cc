import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# Sample Historical Data
np.random.seed(42)
date_rng = pd.date_range(start='2022-01-01', end='2022-12-31', freq='D')
inventory_levels = np.random.randint(50, 200, size=(len(date_rng)))
historical_data = pd.DataFrame(data={'Date': date_rng, 'Inventory': inventory_levels})


data = historical_data[['Inventory']].values.astype(float)
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data)

def create_sequences(data, sequence_length):
    sequences = []
    for i in range(len(data) - sequence_length):
        seq = data[i : (i + sequence_length)]
        sequences.append(seq)
    return np.array(sequences)

sequence_length = 10
batch_size = 64
epochs = 50

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

model.save("inventory_prediction_model.keras")

