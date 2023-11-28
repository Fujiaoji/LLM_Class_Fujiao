import sqlite3

# Database setup
def create_tables():
    conn = sqlite3.connect('ecommerce.db')
    cur = conn.cursor()

    # Create users table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            is_admin BOOLEAN NOT NULL DEFAULT FALSE
        )
    ''')

    # Create products table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL
        )
    ''')

    # Insert sample users
    cur.execute("INSERT OR IGNORE INTO users (username, is_admin) VALUES ('admin', TRUE)")
    cur.execute("INSERT OR IGNORE INTO users (username, is_admin) VALUES ('user', FALSE)")

    # Insert sample products
    cur.execute("INSERT OR IGNORE INTO products (name, description, price) VALUES ('Product 1', 'Description 1', 10.99)")
    cur.execute("INSERT OR IGNORE INTO products (name, description, price) VALUES ('Product 2', 'Description 2', 20.99)")

    conn.commit()
    conn.close()

# Check if a user is an admin
def is_admin(username):
    conn = sqlite3.connect('ecommerce.db')
    cur = conn.cursor()

    cur.execute("SELECT is_admin FROM users WHERE username = ?", (username,))
    result = cur.fetchone()
    conn.close()

    return result and result[0]

# Add a new product
def add_product(username, name, description, price):
    if not is_admin(username):
        return "Access Denied: User is not an admin."

    conn = sqlite3.connect('ecommerce.db')
    cur = conn.cursor()

    cur.execute("INSERT INTO products (name, description, price) VALUES (?, ?, ?)", (name, description, price))
    conn.commit()
    conn.close()
    return "Product added successfully."

# Modify an existing product
def modify_product(username, product_id, name, description, price):
    if not is_admin(username):
        return "Access Denied: User is not an admin."

    conn = sqlite3.connect('ecommerce.db')
    cur = conn.cursor()

    cur.execute("UPDATE products SET name = ?, description = ?, price = ? WHERE id = ?", (name, description, price, product_id))
    conn.commit()
    conn.close()
    return "Product modified successfully."

# Remove a product
def remove_product(username, product_id):
    if not is_admin(username):
        return "Access Denied: User is not an admin."

    conn = sqlite3.connect('ecommerce.db')
    cur = conn.cursor()

    cur.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()
    return "Product removed successfully."

# Initialize database and insert sample data
create_tables()

# Testing code
def test():
    # Test functions with sample data
    print(add_product('admin', 'New Product', 'New Description', 30.99))  # Should succeed
    print(add_product('user', 'Unauthorized Product', 'No Description', 40.99))  # Should fail
    print(modify_product('admin', 1, 'Updated Product 1', 'Updated Description 1', 15.99))  # Should succeed
    print(remove_product('user', 2))  # Should fail
    print(remove_product('admin', 2))  # Should succeed

test()
