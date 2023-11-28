import sqlite3
import re

def create_table():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT NOT NULL
    )''')

    conn.commit()
    conn.close()

def add_product(name, description):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO products (name, description) VALUES (?, ?)''', (name, description))

    conn.commit()
    conn.close()

def search_products(query):
    if not query:
        return "Missing search query parameter."

    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    words = re.split(' ', query)
    for word in words:
        cursor.execute('''SELECT * FROM products WHERE name LIKE ? OR description LIKE ?''', ('%' + word + '%', '%' + word + '%'))

    results = cursor.fetchall()

    if not results:
        message = "No results found for query: " + query
        return message

    conn.close()
    return results


def test_search_function():
    create_table()

    add_product('Laptop', 'A powerful laptop with a long battery life.')
    add_product('Phone', 'A smartphone with a high-resolution camera.')
    add_product('Tablet', 'A tablet with a large display and a powerful processor.')

    query = 'laptop'
    results = search_products(query)
    print(results)

    query = 'phone camera'
    results = search_products(query)
    print(results)

    query = ''
    results = search_products(query)
    print(results)

if __name__ == '__main__':
    test_search_function()
