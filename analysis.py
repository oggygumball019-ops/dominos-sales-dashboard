import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import json

# Set seed for reproducible sales data
np.random.seed(42)
n_orders = 5000
start_date = datetime(2026, 1, 1)

# List of Chennai Delivery Areas
chennai_areas = ['Velachery', 'Anna Nagar', 'T. Nagar', 'OMR (Kandanchavadi)', 'Adyar', 'Nungambakkam', 'Tambaram']

# Domino's India INR Pricing
pizza_catalog = {
    'peppy_paneer': {'name': 'Peppy Paneer', 'category': 'Veggie', 'S': 259.0, 'M': 459.0, 'L': 699.0},
    'farmhouse': {'name': 'Farmhouse', 'category': 'Veggie', 'S': 239.0, 'M': 419.0, 'L': 629.0},
    'non_veg_supreme': {'name': 'Non-Veg Supreme', 'category': 'Chicken', 'S': 319.0, 'M': 579.0, 'L': 839.0},
    'chicken_dominator': {'name': 'Chicken Dominator', 'category': 'Chicken', 'S': 359.0, 'M': 629.0, 'L': 919.0},
    'margherita': {'name': 'Margherita', 'category': 'Classic', 'S': 109.0, 'M': 239.0, 'L': 399.0}
}

data = []
order_id = 1000

for _ in range(n_orders):
    day_offset = random.randint(0, 180)
    hour = np.random.choice([11, 12, 13, 14, 17, 18, 19, 20, 21, 22], p=[0.05, 0.15, 0.15, 0.05, 0.05, 0.20, 0.20, 0.10, 0.03, 0.02])
    minute = random.randint(0, 59)
    order_time = start_date + timedelta(days=day_offset, hours=int(hour), minutes=minute)
    
    area = random.choice(chennai_areas)
    n_items = random.choices([1, 2, 3], weights=[0.6, 0.3, 0.1])[0]
    
    for _ in range(n_items):
        p_code = random.choice(list(pizza_catalog.keys()))
        p_info = pizza_catalog[p_code]
        size = random.choice(['S', 'M', 'L'])
        quantity = random.choices([1, 2], weights=[0.85, 0.15])[0]
        unit_price = p_info[size]
        
        data.append({
            'order_id': order_id,
            'order_date': order_time.strftime('%Y-%m-%d'),
            'order_time': order_time.strftime('%H:%M:%S'),
            'hour': int(hour),
            'area': area,
            'pizza_name': p_info['name'],
            'category': p_info['category'],
            'size': size,
            'quantity': quantity,
            'unit_price': unit_price,
            'price': round(quantity * unit_price, 2)
        })
    order_id += 1

df = pd.DataFrame(data)

# Save updated CSV
df.to_csv('dominos_sales.csv', index=False)

# Export updated JavaScript data file
json_records = df[['order_id', 'hour', 'area', 'category', 'size', 'price']].to_dict(orient='records')
with open('data.js', 'w') as f:
    f.write(f"const rawSalesData = {json.dumps(json_records)};")

print("✅ Updated data.js with Indian Rupee (₹) pricing successfully!")