import pandas as pd
from datetime import datetime
 
# Load and prepare data
df = pd.read_csv('supply_chain.csv')
df['inventory_value'] = df['quantity_on_hand'] * df['unit_cost']
df['days_of_stock'] = df['quantity_on_hand'] / df['daily_demand']
 
# Create Excel writer
filename = f"supply_chain_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
writer = pd.ExcelWriter(filename, engine='openpyxl')
 
# Sheet 1: Full Inventory
df.to_excel(writer, sheet_name='Inventory', index=False)
 
# Sheet 2: Critical Items (that need reordering)
critical = df[df['quantity_on_hand'] < df['reorder_point']].copy()
critical['shortage'] = critical['reorder_point'] - critical['quantity_on_hand']
critical = critical[['product_name', 'quantity_on_hand', 'reorder_point', 'shortage', 'supplier', 'delivery_time_days']]
critical.to_excel(writer, sheet_name='Critical - Reorder Now', index=False)
 
# Sheet 3: Low Stock Warning (< 14 days)
low_stock = df[df['days_of_stock'] < 14].copy().sort_values('days_of_stock')
low_stock = low_stock[['product_name', 'quantity_on_hand', 'daily_demand', 'days_of_stock', 'supplier']]
low_stock.to_excel(writer, sheet_name='Warning - Low Stock', index=False)
 
# Sheet 4: Supplier Summary
supplier_summary = df.groupby('supplier').agg({
    'product_name': 'count',
    'quantity_on_hand': 'sum',
    'inventory_value': 'sum',
    'delivery_time_days': 'mean'
}).rename(columns={
    'product_name': 'products_supplied',
    'quantity_on_hand': 'total_units',
    'inventory_value': 'total_value',
    'delivery_time_days': 'avg_delivery_days'
})
supplier_summary['% of total inventory'] = (supplier_summary['total_value'] / supplier_summary['total_value'].sum() * 100).round(1)
supplier_summary.to_excel(writer, sheet_name='Supplier Analysis')
 
# Sheet 5: Analysis Summary
summary_data = {
    'Metric': [
        'Total Inventory Value',
        'Number of Products',
        'Number of Suppliers',
        'Average Days of Stock',
        'Products Below Reorder Point',
        'Products with <14 Days Stock',
        'Highest Value Product',
        'Highest Demand Product',
        'Total Daily Demand'
    ],
    'Value': [
        f"${df['inventory_value'].sum():,.0f}",
        str(len(df)),
        str(df['supplier'].nunique()),
        f"{df['days_of_stock'].mean():.1f} days",
        str(len(df[df['quantity_on_hand'] < df['reorder_point']])),
        str(len(df[df['days_of_stock'] < 14])),
        f"{df.loc[df['inventory_value'].idxmax(), 'product_name']} (${df['inventory_value'].max():,.0f})",
        f"{df.loc[df['daily_demand'].idxmax(), 'product_name']} ({df['daily_demand'].max():.1f} units/day)",
        f"{df['daily_demand'].sum():.1f} units/day"
    ]
}
summary_df = pd.DataFrame(summary_data)
summary_df.to_excel(writer, sheet_name='Summary', index=False)
 
# Save the file
writer.close()
 
print("✅ Excel report generated successfully!")
print(f"📄 File saved as: {filename}")
print("\n📊 Sheets included:")
print("  1. Inventory - All products with full details")
print("  2. Critical - Reorder Now - Products below reorder point")
print("  3. Warning - Low Stock - Products with <14 days supply")
print("  4. Supplier Analysis - Supplier performance metrics")
print("  5. Summary - Key metrics and insights")
print("\n💡 Open this file in Excel to share with your team!")