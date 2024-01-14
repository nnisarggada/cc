import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
from tensorflow.keras import layers


def train_or_load_model(X_train_scaled, y_train):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    model_file_path = os.path.join(current_directory, 'models', 'reorder_quantity_model.h5')

    if os.path.exists(model_file_path):
        # Load the saved model
        model = keras.models.load_model(model_file_path)
        print('Using pre-trained model.')
    else:
        # Train and save the model
        model = keras.Sequential([
            layers.Dense(128, activation='relu', input_shape=(X_train_scaled.shape[1],)),
            layers.Dropout(0.3),
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.3),
            layers.Dense(1, activation='linear')
        ])
        model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])
        model.fit(X_train_scaled, y_train, epochs=100, batch_size=32, validation_split=0.2, verbose=2)
        
        # Save the trained model
        model.save(model_file_path)

    return model


def predict_reorder_quantity(user_input):
    # return (user_input)
    current_directory = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(current_directory, 'product_data.csv')
    df = pd.read_csv(csv_file_path)

    X = df.drop(['date', 'product', 'restock_amount'], axis=1)
    y = df['restock_amount']
    X = pd.get_dummies(X, columns=['category'])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    # Train or load the model
    model = train_or_load_model(X_train_scaled, y_train)

    # Create a DataFrame with a single row using user input
    user_input_df = pd.DataFrame({
        'product': [user_input['product']],
        'date': [user_input['date']],
        'stock': [user_input['stock']],
        'restock_threshold': [user_input['restock_threshold']],
        'price': [user_input['price']],
        'category': [user_input['category']],
        'shelf_life': [user_input['shelf_life']]
    })

    user_input_df['price'] = user_input_df['price'].astype('float32')

    user_input_df = pd.get_dummies(user_input_df, columns=['category'])

    # Ensure that the user input has the same columns as the training data
    missing_cols = set(X.columns) - set(user_input_df.columns)
    for col in missing_cols:
        user_input_df[col] = 0
    
    user_input_df = user_input_df.reindex(columns=X.columns, fill_value=0)
    user_input_scaled = scaler.transform(user_input_df)

    # Ensure that the user input has the same number of features as the training data
    if user_input_scaled.shape[1] != model.input_shape[1]:
        raise ValueError(f"The user input has {user_input_scaled.shape[1]} features, but the model expects {model.input_shape[1]} features.")

    prediction = model.predict(user_input_scaled)

    return max(0, int(prediction[0]))
