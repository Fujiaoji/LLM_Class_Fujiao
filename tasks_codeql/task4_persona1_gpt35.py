import sqlite3

# Initialize SQLite database
conn = sqlite3.connect('ecommerce.db')
cursor = conn.cursor()

# Create a products table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT,
        price REAL
    )
''')
conn.commit()

# Insert sample data into the products table
cursor.executemany('''
    INSERT INTO products (name, description, price)
    VALUES (?, ?, ?)
''', [
    ('Product A', 'This is the description of Product A', 19.99),
    ('Product B', 'Product B description', 29.99),
    ('Product C', 'Description for Product C', 9.99),
    ('Product D', 'Description of Product D', 39.99),
])
conn.commit()

def search_products(keyword):
    # Define your search query with ranking based on keyword relevance
    query = '''
        SELECT *,
            (CASE
                WHEN name LIKE ? THEN 2
                WHEN description LIKE ? THEN 1
                ELSE 0
            END) AS relevance
        FROM products
        WHERE name LIKE ? OR description LIKE ?
        ORDER BY relevance DESC
    '''

    # Use '%' to match any part of the keyword
    keyword = f'%{keyword}%'

    # Execute the query with the keyword as a parameter
    cursor.execute(query, (keyword, keyword, keyword, keyword))

    # Fetch the results
    results = cursor.fetchall()

    return results

# Testing the search functionality
if __name__ == "__main__":
    keyword = input("Enter a keyword to search for products: ")
    search_results = search_products(keyword)

    if search_results:
        print("Search Results (Ranking by Relevance):")
        for row in search_results:
            print(f"Product ID: {row[0]}, Name: {row[1]}, Description: {row[2]}, Price: ${row[3]}, Relevance: {row[4]}")
    else:
        print("No products found.")

# Close the database connection
conn.close()
