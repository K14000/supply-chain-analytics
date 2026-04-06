import sqlite3

conn = sqlite3.connect("supply_chain.db")
cursor = conn.cursor()

# --- CASE: add a label based on a condition (like IF/ELSE) ---
print("--- Stock level status per product ---")
cursor.execute("""
    SELECT product_name,
           category,
           stock_quantity,
           unit_price,
           CASE
               WHEN stock_quantity >= 200 THEN 'Overstocked'
               WHEN stock_quantity BETWEEN 50 AND 199 THEN 'Healthy'
               WHEN stock_quantity BETWEEN 20 AND 49 THEN 'Low'
               ELSE 'Critical'
           END AS stock_status
    FROM products
    ORDER BY stock_quantity ASC
""")
for row in cursor.fetchall():
    print(row)

# --- SUBQUERY: use a query inside another query ---
print("\n--- Products with below average price ---")
cursor.execute("""
    SELECT product_name, unit_price
    FROM products
    WHERE unit_price < (SELECT AVG(unit_price) FROM products)
    ORDER BY unit_price DESC
""")
for row in cursor.fetchall():
    print(row)

# --- Full analyst report: combining everything ---
print("\n--- Full Supply Chain Performance Report ---")
cursor.execute("""
    SELECT 
        p.product_name,
        p.category,
        s.supplier_name,
        s.country,
        s.lead_time_days,
        o.quantity AS ordered_qty,
        p.unit_price,
        ROUND(o.quantity * p.unit_price, 2) AS order_value,
        o.status,
        CASE
            WHEN o.status = 'Delivered' THEN 'On Track'
            WHEN o.status = 'Pending'   THEN 'Monitor'
            ELSE 'Investigate'
        END AS action_required,
        CASE
            WHEN s.lead_time_days <= 5  THEN 'Fast'
            WHEN s.lead_time_days <= 10 THEN 'Standard'
            ELSE 'Slow'
        END AS supplier_speed
    FROM orders o
    INNER JOIN products p ON o.product_id = p.product_id
    INNER JOIN suppliers s ON o.supplier_id = s.supplier_id
    ORDER BY order_value DESC
""")

print(f"\n{'Product':<20} {'Supplier':<18} {'Country':<10} {'Lead':<6} {'Qty':<6} {'Value':<10} {'Status':<12} {'Action':<12} {'Speed'}")
print("-" * 110)
for row in cursor.fetchall():
    print(f"{row[0]:<20} {row[2]:<18} {row[3]:<10} {row[4]:<6} {row[5]:<6} ${row[7]:<10} {row[8]:<12} {row[9]:<12} {row[10]}")

# --- Summary stats at the bottom ---
print("\n--- Report Summary ---")
cursor.execute("""
    SELECT 
        COUNT(o.order_id) AS total_orders,
        ROUND(SUM(o.quantity * p.unit_price), 2) AS total_spend,
        ROUND(AVG(s.lead_time_days), 1) AS avg_lead_time,
        SUM(CASE WHEN o.status = 'Delivered' THEN 1 ELSE 0 END) AS delivered,
        SUM(CASE WHEN o.status = 'Pending'   THEN 1 ELSE 0 END) AS pending,
        SUM(CASE WHEN o.status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled
    FROM orders o
    INNER JOIN products p ON o.product_id = p.product_id
    INNER JOIN suppliers s ON o.supplier_id = s.supplier_id
""")
row = cursor.fetchone()
print(f"Total Orders   : {row[0]}")
print(f"Total Spend    : ${row[1]:,.2f}")
print(f"Avg Lead Time  : {row[2]} days")
print(f"Delivered      : {row[3]}")
print(f"Pending        : {row[4]}")
print(f"Cancelled      : {row[5]}")

conn.close()