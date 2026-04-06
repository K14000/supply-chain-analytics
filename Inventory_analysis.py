import pandas as pd

# Create supply chain data
data = {
    'product_name': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'USB Cable', 
                     'Desk Chair', 'Standing Desk', 'Webcam', 'Monitor Stand', 'Headset'],
    'quantity_on_hand': [45, 150, 120, 75, 500, 30, 20, 80, 60, 40],
    'unit_cost': [800, 25, 60, 300, 5, 150, 400, 70, 35, 90],
    'reorder_point': [30, 50, 40, 20, 100, 15, 10, 30, 20, 20],
    'supplier': ['TechSupply Co', 'ElectroMart', 'ElectroMart', 'ScreenWorld', 'ChargeTech',
                 'FurniturePro', 'FurniturePro', 'TechSupply Co', 'AccessoryHub', 'AudioGear'],
    'delivery_time_days': [5, 3, 3, 7, 2, 10, 10, 5, 4, 6]
}

# Convert to DataFrame (like a spreadsheet)
df = pd.DataFrame(data)

print("=" * 70)
print("SUPPLY CHAIN INVENTORY ANALYSIS")
print("=" * 70)

# 1. Show the data
print("\n1. INVENTORY DATA:")
print(df.to_string(index=False))

# 2. Calculate inventory value
df['inventory_value'] = df['quantity_on_hand'] * df['unit_cost']

print("\n" + "=" * 70)
print("2. INVENTORY VALUE BY PRODUCT:")
print("=" * 70)
for idx, row in df.iterrows():
    print(f"{row['product_name']:<20} | Value: ${row['inventory_value']:>10,.0f}")

# 3. Total inventory value
total_value = df['inventory_value'].sum()
print(f"\nTOTAL INVENTORY VALUE: ${total_value:,.0f}")

# 4. Identify products that need reordering
print("\n" + "=" * 70)
print("3. PRODUCTS NEEDING REORDER (Below reorder point):")
print("=" * 70)
low_stock = df[df['quantity_on_hand'] < df['reorder_point']]
if len(low_stock) > 0:
    for idx, row in low_stock.iterrows():
        shortage = row['reorder_point'] - row['quantity_on_hand']
        print(f"🔴 {row['product_name']:<20} | Current: {row['quantity_on_hand']} | Need: +{shortage} units")
else:
    print("✅ All products are well-stocked!")

# 5. Calculate supplier statistics
print("\n" + "=" * 70)
print("4. SUPPLIER SUMMARY:")
print("=" * 70)
supplier_stats = df.groupby('supplier').agg({
    'product_name': 'count',
    'quantity_on_hand': 'sum',
    'inventory_value': 'sum'
}).rename(columns={
    'product_name': 'products_supplied',
    'quantity_on_hand': 'total_units',
    'inventory_value': 'total_value'
})

print(supplier_stats.to_string())

print("\n" + "=" * 70)
print("✅ Analysis complete! You just performed supply chain analytics!")
print("=" * 70)