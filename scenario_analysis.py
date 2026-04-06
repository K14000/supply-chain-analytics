import pandas as pd
import numpy as np

# Load original data
df_original = pd.read_csv('supply_chain.csv').copy()
df_original['inventory_value'] = df_original['quantity_on_hand'] * df_original['unit_cost']
df_original['days_of_stock'] = df_original['quantity_on_hand'] / df_original['daily_demand']

print("=" * 80)
print("SUPPLY CHAIN SCENARIO ANALYSIS - WHAT-IF SIMULATIONS")
print("=" * 80)

def scenario_increase_safety_stock():
    """Scenario: Increase safety stock by 20% to reduce stockout risk"""
    print("\n" + "="*80)
    print("SCENARIO 1: Increase Safety Stock by 20%")
    print("="*80)
    print("Goal: Reduce stockout risk by holding more inventory")
    print("Implementation: Increase reorder points by 20%\n")
    
    df = df_original.copy()
    df['reorder_point'] = df['reorder_point'] * 1.2
    df['new_inventory_value'] = df['quantity_on_hand'] * df['unit_cost']
    df['days_of_stock'] = df['quantity_on_hand'] / df['daily_demand']
    
    # Calculate impact
    old_critical = len(df_original[df_original['days_of_stock'] < 7])
    new_critical = len(df[df['days_of_stock'] < 7])
    old_value = df_original['inventory_value'].sum()
    new_value = df['new_inventory_value'].sum()
    additional_cost = new_value - old_value
    
    print(f"RESULTS:")
    print(f"  Old total inventory value: ${old_value:,.0f}")
    print(f"  New total inventory value: ${new_value:,.0f}")
    print(f"  Additional investment: ${additional_cost:,.0f}")
    print(f"  Annual holding cost (20%): ${additional_cost * 0.20:,.0f}")
    print(f"\n  Critical products (< 7 days): {old_critical} → {new_critical}")
    print(f"  Stockout risk reduction: {((old_critical - new_critical) / old_critical * 100) if old_critical > 0 else 0:.1f}%")
    print(f"\n  ROI Analysis: Worth the extra investment? Depends on stockout penalty costs.")

def scenario_reduce_inventory():
    """Scenario: Reduce inventory by 15% to save holding costs"""
    print("\n" + "="*80)
    print("SCENARIO 2: Reduce Inventory by 15% (Lean Strategy)")
    print("="*80)
    print("Goal: Minimize holding costs and free up capital")
    print("Implementation: Reduce quantity on hand by 15%\n")
    
    df = df_original.copy()
    df['quantity_on_hand'] = df['quantity_on_hand'] * 0.85
    df['new_inventory_value'] = df['quantity_on_hand'] * df['unit_cost']
    df['days_of_stock'] = df['quantity_on_hand'] / df['daily_demand']
    
    # Calculate impact
    old_value = df_original['inventory_value'].sum()
    new_value = df['new_inventory_value'].sum()
    savings = old_value - new_value
    old_critical = len(df_original[df_original['days_of_stock'] < 7])
    new_critical = len(df[df['days_of_stock'] < 7])
    
    print(f"RESULTS:")
    print(f"  Old total inventory value: ${old_value:,.0f}")
    print(f"  New total inventory value: ${new_value:,.0f}")
    print(f"  Capital freed up: ${savings:,.0f}")
    print(f"  Annual savings (20% holding cost): ${savings * 0.20:,.0f}")
    print(f"\n  Critical products (< 7 days): {old_critical} → {new_critical}")
    if new_critical > old_critical:
        print(f"  ⚠️  RISK INCREASE: {new_critical - old_critical} more products at risk!")
    else:
        print(f"  ✅ No additional risk detected")

def scenario_supplier_optimization():
    """Scenario: Consolidate suppliers to reduce delivery times"""
    print("\n" + "="*80)
    print("SCENARIO 3: Negotiate Faster Delivery (Average -2 days)")
    print("="*80)
    print("Goal: Reduce delivery times through supplier negotiations")
    print("Implementation: Achieve 2-day average reduction in delivery times\n")
    
    df = df_original.copy()
    df['new_delivery_time'] = (df['delivery_time_days'] - 2).clip(lower=1)  # Min 1 day
    
    # Calculate impact on reorder point (less delivery time = less safety stock needed)
    # Formula: Reorder Point = (Average Daily Demand × Delivery Time) + Safety Stock
    old_critical = len(df_original[df_original['days_of_stock'] < 7])
    
    print(f"RESULTS:")
    print(f"  Average delivery time: {df['delivery_time_days'].mean():.1f} days → {df['new_delivery_time'].mean():.1f} days")
    print(f"  Improvement: {(df['delivery_time_days'].sum() - df['new_delivery_time'].sum()):.0f} total days saved")
    print(f"\n  With faster delivery, you could reduce safety stock by ~10%")
    print(f"  Potential inventory reduction: ${df_original['inventory_value'].sum() * 0.10:,.0f}")
    print(f"  Annual savings: ${df_original['inventory_value'].sum() * 0.10 * 0.20:,.0f}")

def scenario_demand_increase():
    """Scenario: Prepare for 20% demand increase"""
    print("\n" + "="*80)
    print("SCENARIO 4: Prepare for 20% Demand Surge")
    print("="*80)
    print("Goal: Ensure inventory can handle increased demand")
    print("Implementation: Increase stock to handle 20% demand increase\n")
    
    df = df_original.copy()
    df['new_daily_demand'] = df['daily_demand'] * 1.20
    df['new_days_of_stock'] = df['quantity_on_hand'] / df['new_daily_demand']
    
    # Calculate new inventory needs
    old_value = df_original['inventory_value'].sum()
    old_critical = len(df_original[df_original['days_of_stock'] < 7])
    new_critical = len(df[df['new_days_of_stock'] < 7])
    
    # How much more inventory needed?
    additional_inventory_needed = (df['new_daily_demand'].sum() - df['daily_demand'].sum()) * df['delivery_time_days'].mean()
    
    print(f"RESULTS:")
    print(f"  Current daily demand: {df_original['daily_demand'].sum():.1f} units")
    print(f"  New daily demand: {df['new_daily_demand'].sum():.1f} units")
    print(f"  Demand increase: {(df['daily_demand'].sum() * 0.20):,.1f} units/day")
    
    print(f"\n  Critical products with current stock: {old_critical}")
    print(f"  Critical products with 20% demand surge: {new_critical}")
    print(f"\n  Products at risk:")
    at_risk = df[df['new_days_of_stock'] < 7].sort_values('new_days_of_stock')
    if len(at_risk) > 0:
        for idx, row in at_risk.iterrows():
            deficit = (row['new_daily_demand'] - row['daily_demand']) * row['delivery_time_days']
            print(f"    • {row['product_name']}: Need +{deficit:.0f} units buffer")
    else:
        print(f"    ✅ All products can handle 20% demand increase")

def scenario_cost_reduction():
    """Scenario: Reduce unit costs through negotiations"""
    print("\n" + "="*80)
    print("SCENARIO 5: Negotiate 10% Unit Cost Reduction")
    print("="*80)
    print("Goal: Reduce product costs through supplier negotiations")
    print("Implementation: Achieve 10% cost reduction across all products\n")
    
    df = df_original.copy()
    df['new_unit_cost'] = df['unit_cost'] * 0.90
    df['new_inventory_value'] = df['quantity_on_hand'] * df['new_unit_cost']
    
    old_value = df_original['inventory_value'].sum()
    new_value = df['new_inventory_value'].sum()
    savings = old_value - new_value
    
    print(f"RESULTS:")
    print(f"  Current total inventory value: ${old_value:,.0f}")
    print(f"  With 10% cost reduction: ${new_value:,.0f}")
    print(f"  Annual savings: ${savings:,.0f}")
    print(f"  Savings as % of revenue (assume inventory turns 10x/year): {(savings * 10 / 1000000 * 100):.1f}%")
    print(f"\n  Best items to negotiate on:")
    top_savings = df.nlargest(3, 'inventory_value')[['product_name', 'inventory_value', 'new_inventory_value']]
    for idx, (i, row) in enumerate(top_savings.iterrows(), 1):
        item_savings = row['inventory_value'] - row['new_inventory_value']
        print(f"    {idx}. {row['product_name']}: Save ${item_savings:,.0f}")

# Run all scenarios
scenario_increase_safety_stock()
scenario_reduce_inventory()
scenario_supplier_optimization()
scenario_demand_increase()
scenario_cost_reduction()

print("\n" + "=" * 80)
print("SCENARIO ANALYSIS COMPLETE")
print("=" * 80)
print("\n💡 RECOMMENDATIONS:")
print("  1. Balance risk vs cost: More inventory = safer but more expensive")
print("  2. Focus on critical suppliers: Negotiate better terms with high-value suppliers")
print("  3. Prepare for demand surge: Build buffer stock for top-demand products")
print("  4. Cost reduction: 10% savings could free up capital for growth")
print("\n" + "=" * 80)