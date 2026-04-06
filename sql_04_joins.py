import sqlite3

conn = sqlite3.connect("supply_chain.db")
cursor = conn.cursor()

# --- INNER JOIN: only rows that match in BOTH tables ---
print("--- Orders with product names ---")
cursor.execute("""
    SELECT o.order_id,
           p.product_name,
           o.quantity,
           o.status
    FROM orders o
    INNER JOIN products p ON o.product_id = p.product_id
""")
for row in cursor.fetchall():
    print(row)

# --- Joining 3 tables: orders + products + suppliers ---
print("\n--- Full order report ---")
cursor.execute("""
    SELECT o.order_id,
           p.product_name,
           s.supplier_name,
           s.country,
           o.quantity,
           o.order_date,
           o.status
    FROM orders o
    INNER JOIN products p ON o.product_id = p.product_id
    INNER JOIN suppliers s ON o.supplier_id = s.supplier_id
    ORDER BY o.order_date
""")
for row in cursor.fetchall():
    print(row)

# --- Real analyst query: total spend per supplier ---
print("\n--- Total spend per supplier ---")
cursor.execute("""
    SELECT s.supplier_name,
           s.country,
           COUNT(o.order_id) AS total_orders,
           SUM(o.quantity * p.unit_price) AS total_spend
    FROM orders o
    INNER JOIN products p ON o.product_id = p.product_id
    INNER JOIN suppliers s ON o.supplier_id = s.supplier_id
    GROUP BY s.supplier_name
    ORDER BY total_spend DESC
""")
for row in cursor.fetchall():
    print(row)

# --- Real analyst query: delivered orders only with lead time ---
print("\n--- Delivered orders with supplier lead time ---")
cursor.execute("""
    SELECT p.product_name,
           s.supplier_name,
           s.lead_time_days,
           o.quantity,
           o.order_date
    FROM orders o
    INNER JOIN products p ON o.product_id = p.product_id
    INNER JOIN suppliers s ON o.supplier_id = s.supplier_id
    WHERE o.status = 'Delivered'
    ORDER BY s.lead_time_days ASC
""")
for row in cursor.fetchall():
    print(row)

conn.close()