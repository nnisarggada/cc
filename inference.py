import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model

def preprocess_data(data):
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data[['Inventory']].values.astype(float))
    return scaled_data

def create_sequences(data, sequence_length):
    sequences = []
    for i in range(len(data) - sequence_length):
        seq = data[i: (i + sequence_length)]
        sequences.append(seq)
    return np.array(sequences)

def make_predictions(model, scaled_data, sequence_length):
    sequences = create_sequences(scaled_data, sequence_length)
    predictions = model.predict(sequences[:, :-1])
    return predictions
