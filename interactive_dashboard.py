import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Load data
df = pd.read_csv('supply_chain.csv')

# Calculate metrics
df['inventory_value'] = df['quantity_on_hand'] * df['unit_cost']
df['days_of_stock'] = df['quantity_on_hand'] / df['daily_demand']
df['reorder_cost'] = df['unit_cost'] * df['reorder_point']
df['stockout_risk'] = df['daily_demand'] / df['quantity_on_hand']

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (16, 12)

# Create comprehensive dashboard
fig = plt.figure(figsize=(16, 12))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# Main title with timestamp
fig.suptitle(f'Supply Chain Intelligence Dashboard - {datetime.now().strftime("%Y-%m-%d %H:%M")}', 
             fontsize=18, fontweight='bold', y=0.98)

# 1. INVENTORY VALUE (larger plot, top-left)
ax1 = fig.add_subplot(gs[0, :2])
df_sorted = df.sort_values('inventory_value', ascending=True)
colors = ['#d62728' if x < 20000 else '#2ca02c' for x in df_sorted['inventory_value']]
bars = ax1.barh(df_sorted['product_name'], df_sorted['inventory_value'], color=colors)
ax1.set_xlabel('Inventory Value ($)', fontsize=11, fontweight='bold')
ax1.set_title('💰 Inventory Value by Product', fontsize=13, fontweight='bold')
for i, v in enumerate(df_sorted['inventory_value']):
    ax1.text(v, i, f' ${v:,.0f}', va='center', fontsize=9, fontweight='bold')
ax1.axvline(x=df_sorted['inventory_value'].mean(), color='orange', linestyle='--', 
            linewidth=2, label=f'Average: ${df_sorted["inventory_value"].mean():,.0f}')
ax1.legend()

# 2. KEY METRICS (top-right)
ax2 = fig.add_subplot(gs[0, 2])
ax2.axis('off')
metrics_text = f"""
SUPPLY CHAIN METRICS

📊 Total Inventory Value
${df['inventory_value'].sum():,.0f}

⏰ Average Days of Stock
{df['days_of_stock'].mean():.1f} days

📦 Total Daily Demand
{df['daily_demand'].sum():.1f} units/day

🏢 Number of Suppliers
{df['supplier'].nunique()}

⚠️ Critical Products
{len(df[df['days_of_stock'] < 14])} products
"""
ax2.text(0.1, 0.95, metrics_text, transform=ax2.transAxes, fontsize=10,
         verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))

# 3. CRITICAL ALERTS (large, middle-left)
ax3 = fig.add_subplot(gs[1, :2])
critical = df[df['days_of_stock'] < 14].sort_values('days_of_stock')
if len(critical) > 0:
    colors_alert = ['#d62728' if x < 7 else '#ff7f0e' for x in critical['days_of_stock']]
    bars = ax3.barh(critical['product_name'], critical['days_of_stock'], color=colors_alert)
    ax3.axvline(x=7, color='darkred', linestyle='--', linewidth=2, label='CRITICAL (7 days)')
    ax3.axvline(x=14, color='orange', linestyle='--', linewidth=2, label='WARNING (14 days)')
    ax3.set_xlabel('Days of Stock Remaining', fontsize=11, fontweight='bold')
    ax3.set_title('🔴 URGENT: Products Needing Reorder', fontsize=13, fontweight='bold')
    for i, v in enumerate(critical['days_of_stock']):
        ax3.text(v, i, f' {v:.1f} days', va='center', fontsize=9, fontweight='bold')
    ax3.legend()
else:
    ax3.text(0.5, 0.5, '✅ All products well-stocked!', 
            transform=ax3.transAxes, ha='center', va='center',
            fontsize=14, fontweight='bold', color='green')
    ax3.axis('off')

# 4. REORDER RECOMMENDATIONS (middle-right)
ax4 = fig.add_subplot(gs[1, 2])
reorder_needed = df[df['quantity_on_hand'] < df['reorder_point']].copy()
if len(reorder_needed) > 0:
    reorder_text = "🛒 IMMEDIATE REORDERS:\n\n"
    for idx, row in reorder_needed.iterrows():
        shortage = row['reorder_point'] - row['quantity_on_hand']
        reorder_text += f"• {row['product_name']}\n"
        reorder_text += f"  Order: {shortage:.0f} units\n"
        reorder_text += f"  From: {row['supplier']}\n"
        reorder_text += f"  Est. Arrival: {row['delivery_time_days']} days\n\n"
else:
    reorder_text = "✅ No immediate reorders needed"

ax4.axis('off')
ax4.text(0.05, 0.95, reorder_text, transform=ax4.transAxes, fontsize=9,
         verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))

# 5. DEMAND ANALYSIS (bottom-left)
ax5 = fig.add_subplot(gs[2, 0])
df_demand = df.nlargest(10, 'daily_demand').sort_values('daily_demand')
ax5.barh(df_demand['product_name'], df_demand['daily_demand'], color='coral')
ax5.set_xlabel('Daily Demand (units/day)', fontsize=10, fontweight='bold')
ax5.set_title('📦 Top Demand Products', fontsize=12, fontweight='bold')
for i, v in enumerate(df_demand['daily_demand']):
    ax5.text(v, i, f' {v:.1f}', va='center', fontsize=8)

# 6. SUPPLIER ANALYSIS (bottom-middle)
ax6 = fig.add_subplot(gs[2, 1])
supplier_metrics = df.groupby('supplier').agg({
    'inventory_value': 'sum',
    'delivery_time_days': 'mean'
})
supplier_metrics = supplier_metrics.sort_values('inventory_value', ascending=True)
ax6.barh(supplier_metrics.index, supplier_metrics['inventory_value'], color='lightgreen')
ax6.set_xlabel('Total Inventory Value ($)', fontsize=10, fontweight='bold')
ax6.set_title('🏢 Supplier Importance', fontsize=12, fontweight='bold')
for i, v in enumerate(supplier_metrics['inventory_value']):
    pct = v / df['inventory_value'].sum() * 100
    ax6.text(v, i, f' ${v:,.0f} ({pct:.1f}%)', va='center', fontsize=8)

# 7. STOCKOUT RISK (bottom-right)
ax7 = fig.add_subplot(gs[2, 2])
df_risk = df.sort_values('stockout_risk', ascending=False).head(8)
colors_risk = ['#d62728' if x > 0.1 else '#ff7f0e' if x > 0.05 else '#2ca02c' for x in df_risk['stockout_risk']]
ax7.barh(df_risk['product_name'], df_risk['stockout_risk'], color=colors_risk)
ax7.set_xlabel('Stockout Risk Score', fontsize=10, fontweight='bold')
ax7.set_title('⚠️ Stockout Risk Analysis', fontsize=12, fontweight='bold')
ax7.axvline(x=0.1, color='red', linestyle='--', linewidth=1, alpha=0.5)
for i, v in enumerate(df_risk['stockout_risk']):
    ax7.text(v, i, f' {v:.3f}', va='center', fontsize=8)

# Save dashboard
plt.savefig('supply_chain_advanced_dashboard.png', dpi=300, bbox_inches='tight')
print("✅ Advanced dashboard saved as 'supply_chain_advanced_dashboard.png'")
plt.show()

# GENERATE EXECUTIVE SUMMARY REPORT
print("\n" + "=" * 80)
print("EXECUTIVE SUMMARY REPORT")
print("=" * 80)
print(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Critical Issues
print("🔴 CRITICAL ISSUES:")
print("-" * 80)
critical_products = df[df['days_of_stock'] < 7]
if len(critical_products) > 0:
    for idx, row in critical_products.iterrows():
        shortage = row['reorder_point'] - row['quantity_on_hand']
        days_left = row['days_of_stock']
        print(f"URGENT: {row['product_name']}")
        print(f"  • Stock runs out in: {days_left:.1f} days")
        print(f"  • Reorder immediately: {shortage:.0f} units from {row['supplier']}")
        print(f"  • Delivery time: {row['delivery_time_days']} days")
        print(f"  • Annual impact: ${row['inventory_value'] * 365:,.0f}")
else:
    print("✅ No critical stockout risks detected")

# Warnings
print("\n⚠️  WARNINGS (7-14 days of stock):")
print("-" * 80)
warnings = df[(df['days_of_stock'] >= 7) & (df['days_of_stock'] < 14)]
if len(warnings) > 0:
    for idx, row in warnings.iterrows():
        print(f"  • {row['product_name']}: {row['days_of_stock']:.1f} days of stock")
else:
    print("✅ No warning-level issues")

# Top opportunities
print("\n💡 TOP OPPORTUNITIES FOR COST SAVINGS:")
print("-" * 80)
top_value = df.nlargest(3, 'inventory_value')
for rank, (idx, row) in enumerate(top_value.iterrows(), 1):
    holding_cost = row['inventory_value'] * 0.20  # Assume 20% annual holding cost
    print(f"{rank}. {row['product_name']}: Reduce inventory by 10% = Save ${holding_cost/10:,.0f}/year")

# Supplier performance
print("\n🏢 SUPPLIER PERFORMANCE RANKING:")
print("-" * 80)
supplier_perf = df.groupby('supplier').agg({
    'product_name': 'count',
    'inventory_value': 'sum',
    'delivery_time_days': 'mean'
}).sort_values('inventory_value', ascending=False)
supplier_perf.columns = ['Products Supplied', 'Total Value', 'Avg Delivery (days)']

for rank, (supplier, row) in enumerate(supplier_perf.iterrows(), 1):
    pct = row['Total Value'] / df['inventory_value'].sum() * 100
    print(f"{rank}. {supplier}: ${row['Total Value']:,.0f} ({pct:.1f}%) - {row['Avg Delivery (days)']:.1f} day delivery")

print("\n" + "=" * 80)
print("END OF REPORT")
print("=" * 80)