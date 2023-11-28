from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Create SQLite database and table for card information
conn = sqlite3.connect('payment_cards.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS payment_cards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        card_token TEXT,
        expiration_date TEXT,
        cvv TEXT,
        billing_zip TEXT,
        cardholder_name TEXT
    )
''')
conn.commit()
conn.close()

def is_valid_expiration_date(expiration_date):
    try:
        exp_date = datetime.strptime(expiration_date, '%m/%Y')
        current_date = datetime.now()
        return exp_date > current_date
    except ValueError:
        return False

@app.route('/register_card', methods=['POST'])
def register_card():
    try:
        user_id = request.json['user_id']
        card_token = request.json['card_token']
        expiration_date = request.json['expiration_date']
        cvv = request.json['cvv']
        billing_zip = request.json['billing_zip']
        cardholder_name = request.json['cardholder_name']

        # Validate expiration date
        if not is_valid_expiration_date(expiration_date):
            return jsonify({'error': 'Invalid expiration date'}), 400

        # Store card information in the database
        conn = sqlite3.connect('payment_cards.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO payment_cards (user_id, card_token, expiration_date, cvv, billing_zip, cardholder_name)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, card_token, expiration_date, cvv, billing_zip, cardholder_name))
        conn.commit()
        conn.close()

        return jsonify({'message': 'Card registered successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
