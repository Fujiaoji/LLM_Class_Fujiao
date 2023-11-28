import sqlite3

# Step 1: Database Setup
def setup_database():
    conn = sqlite3.connect(':memory:')  # Using in-memory database for simplicity
    cursor = conn.cursor()

    # Create the products table
    cursor.execute('''
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT NOT NULL
        )
    ''')

    # Step 2: Inserting Sample Data
    sample_data = [
        (1, 'Red T-Shirt', 'Comfortable cotton t-shirt in red'),
        (2, 'Blue Jeans', 'Stylish blue jeans with a modern fit'),
        (3, 'Running Shoes', 'Lightweight running shoes for everyday use'),
        (4, 'T-Shirt with Print', 'Graphic T-shirt in various colors')
    ]

    cursor.executemany('INSERT INTO products VALUES (?, ?, ?)', sample_data)
    conn.commit()
    return conn

# Step 3: Implementing Search Functionality
def search_products(conn, query):
    # Validate input
    if not query:
        return "Search query is required"

    cursor = conn.cursor()
    query = f'%{query}%'
    cursor.execute('''
        SELECT *,
               MIN(INSTR(name, ?), INSTR(description, ?)) AS relevance
        FROM products
        WHERE name LIKE ? OR description LIKE ?
        ORDER BY relevance
    ''', (query.strip('%'), query.strip('%'), query, query))
    results = cursor.fetchall()

    if len(results) == 0:
        return "No results found"
    else:
        return results

# Step 4: Testing Functionality
def test_search():
    conn = setup_database()
    print("Search results for 'shirt':", search_products(conn, 'shirt'))
    print("Search results for 'blue':", search_products(conn, 'blue'))
    print("Search results for '':", search_products(conn, ''))  # Expected to show "Search query is required"
    print("Search results for 'xyz':", search_products(conn, 'xyz'))  # Expected to show "No results found"

test_search()
