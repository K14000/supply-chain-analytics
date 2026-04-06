import sqlite3

conn = sqlite3.connect("supply_chain.db")
cursor = conn.cursor()

cursor.executescript("""
    DROP TABLE IF EXISTS products;
    DROP TABLE IF EXISTS suppliers;
    DROP TABLE IF EXISTS orders;

    CREATE TABLE products (
        product_id INTEGER PRIMARY KEY,
        product_name TEXT,
        category TEXT,
        unit_price REAL,
        stock_quantity INTEGER
    );

    CREATE TABLE suppliers (
        supplier_id INTEGER PRIMARY KEY,
        supplier_name TEXT,
        country TEXT,
        lead_time_days INTEGER
    );

    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY,
        product_id INTEGER,
        supplier_id INTEGER,
        quantity INTEGER,
        order_date TEXT,
        status TEXT
    );

    INSERT INTO products VALUES
        (1, 'Laptop',        'Electronics', 850.00, 120),
        (2, 'Office Chair',  'Furniture',   220.00, 45),
        (3, 'Desk',          'Furniture',   350.00, 30),
        (4, 'Monitor',       'Electronics', 400.00, 80),
        (5, 'Keyboard',      'Electronics',  55.00, 200),
        (6, 'Notebook',      'Stationery',    3.50, 500),
        (7, 'Pen Pack',      'Stationery',    1.20, 1000),
        (8, 'Filing Cabinet','Furniture',   180.00, 25);

    INSERT INTO suppliers VALUES
        (1, 'TechSource Ltd',   'China',  14),
        (2, 'OfficePro',        'Germany', 7),
        (3, 'AfriSupply',       'Uganda',  3),
        (4, 'GlobalGoods',      'India',  10);

    INSERT INTO orders VALUES
        (1, 1, 1, 50,  '2024-01-10', 'Delivered'),
        (2, 2, 2, 20,  '2024-01-15', 'Delivered'),
        (3, 4, 1, 30,  '2024-02-01', 'Pending'),
        (4, 5, 3, 150, '2024-02-05', 'Delivered'),
        (5, 3, 2, 10,  '2024-02-10', 'Cancelled'),
        (6, 6, 4, 300, '2024-03-01', 'Delivered'),
        (7, 1, 1, 25,  '2024-03-15', 'Pending'),
        (8, 8, 2, 15,  '2024-03-20', 'Delivered');
""")

conn.commit()
print("Database created successfully!")

print("\n--- All Products ---")
cursor.execute("SELECT * FROM products")
for row in cursor.fetchall():
    print(row)

print("\n--- All Suppliers ---")
cursor.execute("SELECT * FROM suppliers")
for row in cursor.fetchall():
    print(row)

conn.close()