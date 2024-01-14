import pandas as pd
import matplotlib.pyplot as plt

# Read the generated CSV file
df = pd.read_csv('product_data.csv', parse_dates=['date'])

# Group the data by product
grouped_data = df.groupby('product')

# Plot stock vs. date for each product and save to a PNG file
for product, group in grouped_data:
    plt.figure(figsize=(10, 6))
    plt.plot(group['date'], group['stock'], label=f'{product} - {group["category"].iloc[0]}')
    plt.title(f'Stock vs. Date for {product}')
    plt.xlabel('Date')
    plt.ylabel('Stock')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'{product}_stock_plot.png')  # Save plot to PNG file
    plt.close()  # Close the plot to avoid the warning

print("Plots saved successfully.")

