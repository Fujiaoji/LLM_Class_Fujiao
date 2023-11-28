import sqlite3

def connect_db():
    connection = sqlite3.connect('products.db')
    return connection

def create_tables():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            image_url TEXT
        )
    """)

    connection.commit()
    connection.close()

def add_product(name, description, price, image_url):
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO products (name, description, price, image_url)
        VALUES (?, ?, ?, ?)
    """, (name, description, price, image_url))

    connection.commit()
    connection.close()

def modify_product(product_id, name, description, price, image_url):
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE products
        SET name = ?, description = ?, price = ?, image_url = ?
        WHERE id = ?
    """, (name, description, price, image_url, product_id))

    connection.commit()
    connection.close()

def remove_product(product_id):
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM products
        WHERE id = ?
    """, (product_id,))

    connection.commit()
    connection.close()

def get_all_products():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM products
    """)

    products = cursor.fetchall()
    connection.close()

    return products

def get_product_by_id(product_id):
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM products
        WHERE id = ?
    """, (product_id,))

    product = cursor.fetchone()
    connection.close()

    return product

def is_admin(user_id):
    # Implement logic to check if the user with the given ID has admin privileges
    pass

# Test the functionality
if __name__ == '__main__':
    create_tables()

    # Add a product
    add_product('Laptop', 'A powerful laptop for gaming and productivity.', 1200.00, 'https://example.com/laptop.jpg')

    # Modify a product
    modify_product(1, 'High-Performance Laptop', 'An upgraded version of the Laptop with enhanced performance.', 1500.00, 'https://example.com/laptop-pro.jpg')

    # Remove a product
    remove_product(2)

    # Get all products
    products = get_all_products()
    print('All products:')
    for product in products:
        print(product)

    # Get a product by ID
    product = get_product_by_id(1)
    print('Product with ID 1:')
    print(product)

    # Check if a user is an admin
    is_admin_user = is_admin(12345)
    print('Is user 12345 an admin?', is_admin_user)

