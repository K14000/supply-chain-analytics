import sqlite3
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

conn = sqlite3.connect("supply_chain.db")
cursor = conn.cursor()

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Supply Chain SQL Dashboard", fontsize=16, fontweight="bold", y=1.01)

# --- Chart 1: Total spend per supplier ---
cursor.execute("""
    SELECT s.supplier_name, ROUND(SUM(o.quantity * p.unit_price), 2)
    FROM orders o
    INNER JOIN products p ON o.product_id = p.product_id
    INNER JOIN suppliers s ON o.supplier_id = s.supplier_id
    GROUP BY s.supplier_name
    ORDER BY SUM(o.quantity * p.unit_price) DESC
""")
data = cursor.fetchall()
suppliers = [row[0] for row in data]
spend = [row[1] for row in data]

axes[0, 0].barh(suppliers, spend, color=["#378ADD", "#1D9E75", "#BA7517", "#D4537E"])
axes[0, 0].set_title("Total Spend per Supplier", fontweight="bold")
axes[0, 0].set_xlabel("USD ($)")
for i, v in enumerate(spend):
    axes[0, 0].text(v + 200, i, f"${v:,.0f}", va="center", fontsize=9)

# --- Chart 2: Stock status breakdown ---
cursor.execute("""
    SELECT 
        CASE
            WHEN stock_quantity >= 200 THEN 'Overstocked'
            WHEN stock_quantity BETWEEN 50 AND 199 THEN 'Healthy'
            WHEN stock_quantity BETWEEN 20 AND 49 THEN 'Low'
            ELSE 'Critical'
        END AS stock_status,
        COUNT(*) AS count
    FROM products
    GROUP BY stock_status
""")
data = cursor.fetchall()
statuses = [row[0] for row in data]
counts = [row[1] for row in data]
colors = {"Overstocked": "#378ADD", "Healthy": "#1D9E75", "Low": "#EF9F27", "Critical": "#E24B4A"}
bar_colors = [colors.get(s, "#888780") for s in statuses]

axes[0, 1].bar(statuses, counts, color=bar_colors)
axes[0, 1].set_title("Stock Status Breakdown", fontweight="bold")
axes[0, 1].set_ylabel("Number of Products")
for i, v in enumerate(counts):
    axes[0, 1].text(i, v + 0.05, str(v), ha="center", fontweight="bold")

# --- Chart 3: Order value by status ---
cursor.execute("""
    SELECT o.status, ROUND(SUM(o.quantity * p.unit_price), 2)
    FROM orders o
    INNER JOIN products p ON o.product_id = p.product_id
    GROUP BY o.status
""")
data = cursor.fetchall()
statuses = [row[0] for row in data]
values = [row[1] for row in data]
pie_colors = ["#1D9E75", "#EF9F27", "#E24B4A"]

axes[1, 0].pie(values, labels=statuses, colors=pie_colors,
               autopct="%1.1f%%", startangle=90)
axes[1, 0].set_title("Order Value by Status", fontweight="bold")

# --- Chart 4: Lead time vs total spend per supplier ---
cursor.execute("""
    SELECT s.supplier_name, s.lead_time_days, 
           ROUND(SUM(o.quantity * p.unit_price), 2) AS total_spend,
           COUNT(o.order_id) AS total_orders
    FROM orders o
    INNER JOIN products p ON o.product_id = p.product_id
    INNER JOIN suppliers s ON o.supplier_id = s.supplier_id
    GROUP BY s.supplier_name
""")
data = cursor.fetchall()
names = [row[0] for row in data]
lead_times = [row[1] for row in data]
spend = [row[2] for row in data]
orders = [row[3] for row in data]

scatter = axes[1, 1].scatter(lead_times, spend, 
                              s=[o * 200 for o in orders],
                              color=["#378ADD", "#1D9E75", "#BA7517", "#D4537E"],
                              alpha=0.8)
for i, name in enumerate(names):
    axes[1, 1].annotate(name, (lead_times[i], spend[i]),
                        textcoords="offset points", xytext=(8, 4), fontsize=8)
axes[1, 1].set_title("Lead Time vs Spend (bubble = order count)", fontweight="bold")
axes[1, 1].set_xlabel("Lead Time (days)")
axes[1, 1].set_ylabel("Total Spend ($)")

plt.tight_layout()
plt.savefig("sql_dashboard.png", dpi=150, bbox_inches="tight")
plt.show()
print("Dashboard saved as sql_dashboard.png")

conn.close()