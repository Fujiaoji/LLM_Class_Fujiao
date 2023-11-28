import sqlite3
import json

class Product:
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock

class CartItem:
    def __init__(self, product_id, quantity):
        self.product_id = product_id
        self.quantity = quantity

class User:
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username

class EcommerceAPI:
    def __init__(self):
        self.db_connection = sqlite3.connect('ecommerce.db')
        self.create_tables()

    def create_tables(self):
        cursor = self.db_connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS products (product_id INTEGER PRIMARY KEY, name TEXT, price REAL, stock INTEGER)')
        cursor.execute('CREATE TABLE IF NOT EXISTS cart (user_id INTEGER, product_id INTEGER, quantity INTEGER, FOREIGN KEY (user_id) REFERENCES users(user_id), FOREIGN KEY (product_id) REFERENCES products(product_id))')
        cursor.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, username TEXT)')
        self.db_connection.commit()

    def get_product_by_id(self, product_id):
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT * FROM products WHERE product_id = ?', (product_id,))
        product_row = cursor.fetchone()
        if product_row is None:
            return None
        else:
            product = Product(product_row[0], product_row[1], product_row[2], product_row[3])
            return product

    def add_product_to_cart(self, user_id, product_id, quantity):
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT stock FROM products WHERE product_id = ?', (product_id,))
        stock = cursor.fetchone()[0]
        if stock >= quantity:
            cursor.execute('INSERT INTO cart VALUES (?, ?, ?)', (user_id, product_id, quantity))
            self.db_connection.commit()
            return True
        else:
            return False

    def get_cart(self, user_id):
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT * FROM cart WHERE user_id = ?', (user_id,))
        cart_rows = cursor.fetchall()
        cart_items = []
        for cart_row in cart_rows:
            cart_item = CartItem(cart_row[1], cart_row[2])
            cart_items.append(cart_item)
        return cart_items

if __name__ == '__main__':
    api = EcommerceAPI()

    # Example usage
    product = api.get_product_by_id(1)
    if product is not None:
        print('Product:', product.name)
        print('Price:', product.price)
        print('Stock:', product.stock)

    user_id = 1
    product_id = 2
    quantity = 3
    if api.add_product_to_cart(user_id, product_id, quantity):
        print('Product added to cart')
    else:
        print('Product not added to cart')

    cart_items = api.get_cart(user_id)
    print('Cart:')
    for cart_item in cart_items:
        print('-', cart_item.product_id, cart_item.quantity)

