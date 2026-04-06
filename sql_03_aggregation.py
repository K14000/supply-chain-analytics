import sqlite3

conn = sqlite3.connect("supply_chain.db")
cursor = conn.cursor()

# --- COUNT: how many rows ---
print("--- Total number of products ---")
cursor.execute("SELECT COUNT(*) FROM products")
print(cursor.fetchone())

# --- SUM: total value ---
print("\n--- Total stock value (price x quantity) ---")
cursor.execute("SELECT SUM(unit_price * stock_quantity) FROM products")
print(cursor.fetchone())

# --- AVG: average value ---
print("\n--- Average product price ---")
cursor.execute("SELECT ROUND(AVG(unit_price), 2) FROM products")
print(cursor.fetchone())

# --- MIN and MAX ---
print("\n--- Cheapest and most expensive product ---")
cursor.execute("SELECT MIN(unit_price), MAX(unit_price) FROM products")
print(cursor.fetchone())

# --- GROUP BY: aggregate per category ---
print("\n--- Total stock value per category ---")
cursor.execute("""
    SELECT category, 
           COUNT(*) AS num_products,
           ROUND(AVG(unit_price), 2) AS avg_price,
           SUM(unit_price * stock_quantity) AS total_stock_value
    FROM products
    GROUP BY category
    ORDER BY total_stock_value DESC
""")
for row in cursor.fetchall():
    print(row)

# --- HAVING: filter after grouping (like WHERE but for groups) ---
print("\n--- Categories with average price above $100 ---")
cursor.execute("""
    SELECT category, ROUND(AVG(unit_price), 2) AS avg_price
    FROM products
    GROUP BY category
    HAVING avg_price > 100
    ORDER BY avg_price DESC
""")
for row in cursor.fetchall():
    print(row)

# --- Real analyst question: which supplier has the most orders? ---
print("\n--- Orders per supplier ---")
cursor.execute("""
    SELECT supplier_id,
           COUNT(*) AS total_orders,
           SUM(quantity) AS total_units_ordered
    FROM orders
    GROUP BY supplier_id
    ORDER BY total_orders DESC
""")
for row in cursor.fetchall():
    print(row)

conn.close()