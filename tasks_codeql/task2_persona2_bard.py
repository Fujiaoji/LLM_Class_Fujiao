import sqlite3
import json

# Database connection
conn = sqlite3.connect('ecommerce.db')
cursor = conn.cursor()

# Table creation (if not exists)
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    product_description TEXT,
    product_price REAL NOT NULL,
    stock_quantity INTEGER NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS cart (
    cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
""")

conn.commit()

# Function to retrieve product information by product ID
def get_product_info(product_id):
    # Parameter sanitization against SQL injection
    product_id = int(product_id)

    # Query the database
    cursor.execute("SELECT * FROM products WHERE product_id = ?", (product_id,))
    product_data = cursor.fetchone()

    # Check if product exists
    if not product_data:
        return None

    # Return product information
    return {
        'product_id': product_data[0],
        'product_name': product_data[1],
        'product_description': product_data[2],
        'product_price': product_data[3],
        'stock_quantity': product_data[4]
    }

# Function to add product to cart
def add_product_to_cart(user_id, product_id, quantity):
    # Parameter sanitization against SQL injection
    user_id = int(user_id)
    product_id = int(product_id)
    quantity = int(quantity)

    # Check if product has enough stock
    product_info = get_product_info(product_id)
    if not product_info or product_info['stock_quantity'] < quantity:
        return False

    # Insert cart item into the database
    cursor.execute("INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)", (user_id, product_id, quantity))
    conn.commit()

    # Update product stock quantity
    cursor.execute("UPDATE products SET stock_quantity = stock_quantity - ? WHERE product_id = ?", (quantity, product_id))
    conn.commit()

    return True

# Function to save cart information to the database
def save_cart_to_db(cart_data):
    # Parameter sanitization against SQL injection
    cart_data = json.loads(cart_data)

    # Add each cart item to the database
    for item in cart_data:
        add_product_to_cart(item['user_id'], item['product_id'], item['quantity'])

    return True

# Function to test the API
def test_api():
    # Get product information
    product_info = get_product_info(1)
    print(product_info)

    # Add product to cart
    add_product_to_cart(1, 1, 2)

    # Save cart information to database
    cart_data = '[{"user_id": 1,"product_id": 1,"quantity": 2}]'

    save_cart_to_db(cart_data)

test_api()

