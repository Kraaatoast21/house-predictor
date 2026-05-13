import pandas as pd
import numpy as np
import os

def generate_mock_data():
    np.random.seed(42)
    n_samples = 1000
    
    # Subdivisions in the Philippines
    subdivisions = ['Ayala Alabang', 'Forbes Park', 'Dasmarinas Village', 'Bel-Air', 'BF Homes', 'Loyola Grand Villas']
    
    data = {
        'bedrooms': np.random.randint(1, 7, n_samples),
        'bathrooms': np.random.randint(1, 5, n_samples),
        'floor_area': np.random.uniform(50, 500, n_samples),
        'land_size': np.random.uniform(100, 1000, n_samples),
        'subdivision': np.random.choice(subdivisions, n_samples),
        'build_year': np.random.randint(1990, 2024, n_samples),
    }
    
    df = pd.DataFrame(data)
    
    # Base price calculation
    base_price = 2_000_000
    df['price'] = base_price + \
                  (df['bedrooms'] * 500_000) + \
                  (df['bathrooms'] * 300_000) + \
                  (df['floor_area'] * 30_000) + \
                  (df['land_size'] * 15_000)
                  
    # Subdivision multipliers
    sub_mult = {
        'Forbes Park': 5.0,
        'Dasmarinas Village': 4.5,
        'Ayala Alabang': 3.0,
        'Bel-Air': 2.5,
        'Loyola Grand Villas': 1.8,
        'BF Homes': 1.2
    }
    
    df['price'] = df.apply(lambda row: row['price'] * sub_mult[row['subdivision']], axis=1)
    
    # Add some noise
    noise = np.random.normal(0, 0.1, n_samples)
    df['price'] = df['price'] * (1 + noise)
    
    # Ensure no negative prices and round to integers
    df['price'] = df['price'].clip(lower=1_000_000).astype(int)
    
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/housing_data.csv', index=False)
    print("Mock data generated successfully at data/housing_data.csv")

if __name__ == '__main__':
    generate_mock_data()
