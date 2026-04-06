import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('supply_chain.csv')

# Calculate metrics
df['inventory_value'] = df['quantity_on_hand'] * df['unit_cost']
df['days_of_stock'] = df['quantity_on_hand'] / df['daily_demand']

# Set style for better-looking charts
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 10)

# Create a figure with 4 subplots
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Supply Chain Analytics Dashboard', fontsize=16, fontweight='bold')

# Chart 1: Inventory Value by Product
ax1 = axes[0, 0]
df_sorted = df.sort_values('inventory_value', ascending=True)
ax1.barh(df_sorted['product_name'], df_sorted['inventory_value'], color='steelblue')
ax1.set_xlabel('Inventory Value ($)')
ax1.set_title('💰 Inventory Value by Product')
for i, v in enumerate(df_sorted['inventory_value']):
    ax1.text(v, i, f' ${v:,.0f}', va='center')

# Chart 2: Days of Stock (Alert if < 14 days)
ax2 = axes[0, 1]
colors = ['red' if x < 14 else 'green' for x in df['days_of_stock']]
df_stock = df.sort_values('days_of_stock')
ax2.barh(df_stock['product_name'], df_stock['days_of_stock'], color=colors)
ax2.axvline(x=14, color='orange', linestyle='--', linewidth=2, label='Warning Level (14 days)')
ax2.set_xlabel('Days of Stock')
ax2.set_title('⏰ Days of Stock (When will we run out?)')
ax2.legend()

# Chart 3: Daily Demand
ax3 = axes[1, 0]
df_demand = df.sort_values('daily_demand', ascending=True)
ax3.barh(df_demand['product_name'], df_demand['daily_demand'], color='coral')
ax3.set_xlabel('Daily Demand (units/day)')
ax3.set_title('📦 Daily Demand by Product')
for i, v in enumerate(df_demand['daily_demand']):
    ax3.text(v, i, f' {v:.1f}', va='center')

# Chart 4: Supplier Value Analysis
ax4 = axes[1, 1]
supplier_value = df.groupby('supplier')['inventory_value'].sum().sort_values(ascending=True)
ax4.barh(supplier_value.index, supplier_value.values, color='lightgreen')
ax4.set_xlabel('Total Inventory Value ($)')
ax4.set_title('🏢 Inventory Value by Supplier')
for i, v in enumerate(supplier_value.values):
    ax4.text(v, i, f' ${v:,.0f}', va='center')

# Adjust layout and show
plt.tight_layout()
plt.savefig('supply_chain_dashboard.png', dpi=300, bbox_inches='tight')
print("✅ Dashboard saved as 'supply_chain_dashboard.png'")
plt.show()

# Print summary
print("\n" + "=" * 80)
print("SUPPLY CHAIN INSIGHTS SUMMARY")
print("=" * 80)
print(f"\n🔴 CRITICAL ALERT:")
critical = df[df['days_of_stock'] < 14].sort_values('days_of_stock')
if len(critical) > 0:
    for idx, row in critical.iterrows():
        print(f"   {row['product_name']}: Only {row['days_of_stock']:.1f} days left!")
else:
    print("   ✅ All products have sufficient stock")

print(f"\n💰 Top 3 Most Valuable Products:")
top_value = df.nlargest(3, 'inventory_value')[['product_name', 'inventory_value']]
for idx, (i, row) in enumerate(top_value.iterrows(), 1):
    print(f"   {idx}. {row['product_name']}: ${row['inventory_value']:,.0f}")

print(f"\n📦 Top 3 Highest Demand Products:")
top_demand = df.nlargest(3, 'daily_demand')[['product_name', 'daily_demand']]
for idx, (i, row) in enumerate(top_demand.iterrows(), 1):
    print(f"   {idx}. {row['product_name']}: {row['daily_demand']:.1f} units/day")

print(f"\n🏢 Most Critical Supplier:")
supplier_value = df.groupby('supplier')['inventory_value'].sum().sort_values(ascending=False)
print(f"   {supplier_value.index[0]}: ${supplier_value.values[0]:,.0f} ({supplier_value.values[0]/df['inventory_value'].sum()*100:.1f}% of total)")

print("\n" + "=" * 80)