import pandas as pd

# Load data from CSV file
df = pd.read_csv('supply_chain.csv')

print("=" * 80)
print("ADVANCED SUPPLY CHAIN ANALYSIS")
print("=" * 80)

# 1. Show all data
print("\n1. ALL INVENTORY DATA:")
print(df.to_string(index=False))

# 2. Calculate key metrics
df['inventory_value'] = df['quantity_on_hand'] * df['unit_cost']
df['days_of_stock'] = df['quantity_on_hand'] / df['daily_demand']

print("\n" + "=" * 80)
print("2. PRODUCT ANALYSIS WITH CALCULATED METRICS:")
print("=" * 80)

for idx, row in df.iterrows():
    print(f"\n📦 {row['product_name']}")
    print(f"   Quantity: {row['quantity_on_hand']} units")
    print(f"   Daily Demand: {row['daily_demand']} units/day")
    print(f"   Days of Stock: {row['days_of_stock']:.1f} days")
    print(f"   Inventory Value: ${row['inventory_value']:,.0f}")
    print(f"   Supplier: {row['supplier']} (Delivery: {row['delivery_time_days']} days)")

# 3. Find critical products (less than 2 weeks of stock)
print("\n" + "=" * 80)
print("3. ⚠️  CRITICAL PRODUCTS (Less than 14 days of stock):")
print("=" * 80)

critical = df[df['days_of_stock'] < 14].sort_values('days_of_stock')
if len(critical) > 0:
    for idx, row in critical.iterrows():
        print(f"🔴 {row['product_name']:<20} | Only {row['days_of_stock']:.1f} days left!")
        print(f"   Action: Order from {row['supplier']} (takes {row['delivery_time_days']} days)")
else:
    print("✅ All products have sufficient stock!")

# 4. Total inventory statistics
print("\n" + "=" * 80)
print("4. SUMMARY STATISTICS:")
print("=" * 80)
print(f"Total Products: {len(df)}")
print(f"Total Inventory Value: ${df['inventory_value'].sum():,.0f}")
print(f"Average Days of Stock: {df['days_of_stock'].mean():.1f} days")
print(f"Highest Value Product: {df.loc[df['inventory_value'].idxmax(), 'product_name']} (${df['inventory_value'].max():,.0f})")
print(f"Fastest Moving Product: {df.loc[df['daily_demand'].idxmax(), 'product_name']} ({df['daily_demand'].max()} units/day)")

# 5. Supplier Analysis
print("\n" + "=" * 80)
print("5. SUPPLIER PERFORMANCE:")
print("=" * 80)

supplier_analysis = df.groupby('supplier').agg({
    'product_name': 'count',
    'inventory_value': 'sum',
    'daily_demand': 'sum',
    'delivery_time_days': 'mean'
}).rename(columns={
    'product_name': 'products',
    'inventory_value': 'total_value',
    'daily_demand': 'total_demand',
    'delivery_time_days': 'avg_delivery_days'
})

print(supplier_analysis.to_string())

print("\n" + "=" * 80)
print("✅ Analysis Complete! Ready for action.")
print("=" * 80)