import sqlite3

conn = sqlite3.connect("supply_chain.db")
cursor = conn.cursor()

# --- SELECT specific columns (not always need all) ---
print("--- Product names and prices ---")
cursor.execute("SELECT product_name, unit_price FROM products")
for row in cursor.fetchall():
    print(row)

# --- WHERE: filter rows ---
print("\n--- Electronics only ---")
cursor.execute("SELECT product_name, stock_quantity FROM products WHERE category = 'Electronics'")
for row in cursor.fetchall():
    print(row)

# --- AND: multiple conditions ---
print("\n--- Electronics under $500 ---")
cursor.execute("""
    SELECT product_name, unit_price 
    FROM products 
    WHERE category = 'Electronics' AND unit_price < 500
""")
for row in cursor.fetchall():
    print(row)

# --- OR: either condition ---
print("\n--- Furniture or Stationery ---")
cursor.execute("""
    SELECT product_name, category 
    FROM products 
    WHERE category = 'Furniture' OR category = 'Stationery'
""")
for row in cursor.fetchall():
    print(row)

# --- ORDER BY: sort results ---
print("\n--- All products sorted by price (highest first) ---")
cursor.execute("SELECT product_name, unit_price FROM products ORDER BY unit_price DESC")
for row in cursor.fetchall():
    print(row)

# --- Combining everything ---
print("\n--- Pending or Cancelled orders, most recent first ---")
cursor.execute("""
    SELECT order_id, product_id, quantity, order_date, status
    FROM orders
    WHERE status = 'Pending' OR status = 'Cancelled'
    ORDER BY order_date DESC
""")
for row in cursor.fetchall():
    print(row)

conn.close()