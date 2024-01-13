import pandas as pd
import numpy as np

def generate_synthetic_data(start_date, end_date):
    np.random.seed(42)
    date_rng = pd.date_range(start=start_date, end=end_date, freq='D')
    inventory_levels = np.random.randint(50, 200, size=(len(date_rng)))
    synthetic_data = pd.DataFrame(data={'Date': date_rng, 'Inventory': inventory_levels})
    return synthetic_data
