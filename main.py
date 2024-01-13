from data_generator import generate_synthetic_data
from data_loader import load_data
from train import train_model
from inference import preprocess_data, make_predictions

# Generate synthetic data
start_date = '2022-01-01'
end_date = '2022-12-31'
synthetic_data = generate_synthetic_data(start_date, end_date)

# Save synthetic data to CSV
synthetic_data.to_csv('synthetic_data.csv', index=False)

# Load synthetic data
loaded_data = load_data('synthetic_data.csv')

# Train the model
trained_model = train_model(loaded_data)

# Preprocess data for inference
scaled_data = preprocess_data(loaded_data)

# Make predictions using the trained model
predictions = make_predictions(trained_model, scaled_data, sequence_length=10)

# Display predictions (replace this with your actual use case)
print(predictions)
