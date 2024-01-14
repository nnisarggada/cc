import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set a random seed for reproducibility
np.random.seed(42)

# Define the time range
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 12, 31)
date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

# Define product information
products = ['Product1', 'Product2', 'Product3', 'Product4', 'Product5']
categories = {'Product1': 'Category1', 'Product2': 'Category2', 'Product3': 'Category3', 'Product4': 'Category1', 'Product5': 'Category2'}

# Create a dictionary to store unique restock thresholds, shelf lives, and dynamic pricing for each product
restock_thresholds = {product: np.random.randint(10, 50) for product in products}
shelf_lives = {product: np.random.randint(30, 365) for product in products}
offsets = {product: np.random.uniform(0, 2 * np.pi) for product in products}

# Generate fixed base prices for each product
base_prices = {product: np.random.uniform(10.0, 50.0) for product in products}

data = []

# Generate data with trends and conditions
for date in date_range:
    for product in products:
        category = categories[product]

        # Generate periodic demand increase during the summer with an offset
        demand_increase = 20 * np.sin(2 * np.pi * date.timetuple().tm_yday / 365 + offsets[product])

        # Generate stock reduction during high demand periods
        base_stock = 70
        stock_noise = base_stock - demand_increase + np.random.normal(0, 5)

        # If stock goes below 0, set it to 0
        stock = max(0, int(stock_noise))

        # If stock is 0 for two consecutive days, restock on the next day
        if stock == 0:
            consecutive_zero_days = data[-2][0] if len(data) >= 2 and data[-1][2] == 0 else 0
            if consecutive_zero_days == date - timedelta(days=1):
                stock = restock_thresholds[product]  # Restock threshold

        # Calculate today's restock amount
        if len(data) > 0 and data[-1][0] == date - timedelta(days=1):
            yesterday_stock = data[-1][2]
            restock_amount = max(0, stock - yesterday_stock)
        else:
            restock_amount = 0

        # Restock only when the stock is significantly close to the restock threshold
        if stock < 0.2 * restock_thresholds[product]:
            restock_amount = max(restock_amount, np.random.randint(5, 20))

        # Calculate today's price based on yesterday's price and dynamic pricing
        if len(data) > 0 and data[-1][0] == date - timedelta(days=1):
            yesterday_price = data[-1][5]
            # Change price by 5% every 7 to 15 days
            if np.random.rand() < 0.1:  # 10% chance for a price change
                price = yesterday_price * np.random.uniform(0.95, 1.05)
            else:
                price = yesterday_price
        else:
            price = base_prices[product]

        data.append([date, product, stock, restock_thresholds[product], restock_amount, price, category, shelf_lives[product]])

# Create a DataFrame from the generated data
columns = ['date', 'product', 'stock', 'restock_threshold', 'restock_amount', 'price', 'category', 'shelf_life']
df = pd.DataFrame(data, columns=columns)

# Save the DataFrame to a CSV file
df.to_csv('product_data.csv', index=False)
