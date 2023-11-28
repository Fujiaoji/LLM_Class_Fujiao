import sqlite3

# Connect to the user database
user_db = sqlite3.connect('users.db')
user_cursor = user_db.cursor()

# Create the 'users' table if it doesn't already exist
user_db.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    admin INTEGER NOT NULL DEFAULT 0
)
""")
user_db.commit()

# Connect to the products database
products_db = sqlite3.connect('products.db')
products_cursor = products_db.cursor()

# Function to check if the user is an admin
def is_admin(user_id):
    # Query the user database to check if the user has admin privileges
    user_cursor.execute('SELECT admin FROM users WHERE id = ?', (user_id,))
    user_info = user_cursor.fetchone()

    # Return True if the user is an admin, False otherwise
    return user_info[0] == 1

# Function to modify product details
def modify_product(product_id, new_name, new_price, new_description):
    # Check if the user has admin privileges
    if not is_admin(current_user_id):
        print('You are not authorized to modify product details.')
        return

    # Update the product details in the products database
    products_cursor.execute('UPDATE products SET name = ?, price = ?, description = ? WHERE id = ?', (new_name, new_price, new_description, product_id))
    products_db.commit()

    # Print a success message
    print('Product details updated successfully.')

# Function to add a new product
def add_product(name, price, description):
    # Check if the user has admin privileges
    if not is_admin(current_user_id):
        print('You are not authorized to add new products.')
        return

    # Insert the new product into the products database
    products_cursor.execute('INSERT INTO products (name, price, description) VALUES (?, ?, ?)', (name, price, description))
    products_db.commit()

    # Print a success message
    print('Product added successfully.')

# Function to remove a product
def remove_product(product_id):
    # Check if the user has admin privileges
    if not is_admin(current_user_id):
        print('You are not authorized to remove products.')
        return

    # Delete the product from the products database
    products_cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
    products_db.commit()

    # Print a success message
    print('Product removed successfully.')

# Test the functionality
current_user_id = 1  # Replace with the actual user ID

# Modify product details
modify_product(1, 'New Product Name', 100.00, 'New product description')

# Add a new product
add_product('Another Product', 50.00, 'Another great product')

# Remove a product
remove_product(2)

