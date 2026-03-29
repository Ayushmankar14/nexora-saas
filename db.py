import sqlite3

conn = sqlite3.connect("orders.db", check_same_thread=False)
c = conn.cursor()

# USERS
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT,
    is_paid INTEGER DEFAULT 0
)
''')

# PRODUCTS
c.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    seller_id INTEGER,
    name TEXT,
    price INTEGER
)
''')

# ORDERS
c.execute('''
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    seller_id INTEGER,
    customer_id INTEGER,
    product TEXT,
    price INTEGER,
    qty INTEGER,
    total INTEGER,
    status TEXT DEFAULT 'Pending'
)
''')

# ---------- USERS ----------
def create_user(username, password, role):
    try:
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                  (username, password, role))
        conn.commit()
        return True, "Success"
    except sqlite3.IntegrityError:
        return False, "Username already exists"

def login_user(username, password):
    return c.execute("SELECT * FROM users WHERE username=? AND password=?",
                     (username, password)).fetchone()

def activate_subscription(user_id):
    c.execute("UPDATE users SET is_paid=1 WHERE id=?", (user_id,))
    conn.commit()

# ---------- PRODUCTS ----------
def add_product(seller_id, name, price):
    c.execute("INSERT INTO products (seller_id, name, price) VALUES (?, ?, ?)",
              (seller_id, name, price))
    conn.commit()

def get_products():
    return c.execute("SELECT * FROM products").fetchall()

def delete_product(product_id):
    c.execute("DELETE FROM products WHERE id=?", (product_id,))
    conn.commit()

# ---------- ORDERS ----------
def save_order(customer_id, seller_id, product, price, qty):
    total = price * qty
    c.execute("""
        INSERT INTO orders (seller_id, customer_id, product, price, qty, total)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (seller_id, customer_id, product, price, qty, total))
    conn.commit()

def get_orders_seller(seller_id):
    return c.execute("SELECT * FROM orders WHERE seller_id=?", (seller_id,)).fetchall()

def get_orders_customer(customer_id):
    return c.execute("SELECT * FROM orders WHERE customer_id=?", (customer_id,)).fetchall()

def update_status(order_id, status):
    c.execute("UPDATE orders SET status=? WHERE id=?", (status, order_id))
    conn.commit()