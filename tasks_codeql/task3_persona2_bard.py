import sqlite3
import datetime

conn = sqlite3.connect('ecommerce.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS payment_cards (
    user_id INTEGER NOT NULL,
    card_number TEXT NOT NULL,
    expiration_month INTEGER NOT NULL,
    expiration_year INTEGER NOT NULL,
    cvv INTEGER NOT NULL,
    name_on_card TEXT NOT NULL,
    billing_zip_code TEXT NOT NULL,
    PRIMARY KEY (user_id, card_number),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
''')

conn.commit()
conn.close()

def save_payment_card(username, card_number, expiration_month, expiration_year, cvv, name_on_card, billing_zip_code):
    import sqlite3
    import datetime

    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()

    # Retrieve the user ID based on the provided username
    get_user_id_query = "SELECT id FROM users WHERE username = ?"
    cursor.execute(get_user_id_query, (username,))
    user_id = cursor.fetchone()[0]

    # Check if all required fields have been provided
    if not card_number:
        raise ValueError("Card number is required")

    if not cvv:
        raise ValueError("CVV is required")

    if not expiration_month:
        raise ValueError("Expiration month is required")

    if not expiration_year:
        raise ValueError("Expiration year is required")

    if not name_on_card:
        raise ValueError("Name on card is required")

    if not billing_zip_code:
        raise ValueError("Billing zip code is required")

    # Validate the expiration date format
    if not isinstance(expiration_month, int) or not (1 <= expiration_month <= 12):
        raise ValueError("Invalid expiration month format")

    if not isinstance(expiration_year, int) or not (expiration_year >= datetime.datetime.today().year):
        raise ValueError("Invalid expiration year format")

    # Validate the CVV format
    if not isinstance(cvv, int) or not (100 <= cvv <= 999):
        raise ValueError("Invalid CVV format")

    # If all fields are valid, proceed with saving the payment card
    query = '''
        INSERT INTO payment_cards (user_id, card_number, expiration_month, expiration_year, cvv, name_on_card, billing_zip_code)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    '''

    cursor.execute(query, (user_id, card_number, expiration_month, expiration_year, cvv, name_on_card, billing_zip_code))
    conn.commit()
    conn.close()


def get_payment_cards(username):
    import sqlite3

    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()

    # Retrieve the user ID based on the provided username
    get_user_id_query = "SELECT id FROM users WHERE username = ?"
    cursor.execute(get_user_id_query, (username,))
    user_id = cursor.fetchone()[0]

    query = '''
        SELECT card_number, expiration_month, expiration_year, cvv
        FROM payment_cards
        WHERE user_id = ?
    '''

    cursor.execute(query, (user_id,))
    payment_cards = cursor.fetchall()
    conn.close()

    return payment_cards


def delete_payment_card(username, card_number):
    import sqlite3

    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()

    # Retrieve the user ID based on the provided username
    get_user_id_query = "SELECT id FROM users WHERE username = ?"
    cursor.execute(get_user_id_query, (username,))
    user_id = cursor.fetchone()[0]

    query = '''
        DELETE FROM payment_cards
        WHERE user_id = ? AND card_number = ?
    '''

    cursor.execute(query, (user_id, card_number))
    conn.commit()
    conn.close()

import unittest

class PaymentCardsTest(unittest.TestCase):

    def setUp(self):
        self.user_name = "bob_jones"

    def test_save_payment_card(self):
        save_payment_card(self.user_name, '1234567890123451', 10, 2025, 123, "johndoe", 19132)
        save_payment_card(self.user_name, '1234567890123456', 12, 2023, 123, "johndoe", 19132)

        payment_cards = get_payment_cards(self.user_name)
        self.assertEqual(payment_cards[0][0], '1234567890123451')
        self.assertEqual(payment_cards[0][1], 10)
        self.assertEqual(payment_cards[0][2], 2025)
        self.assertEqual(payment_cards[0][3], 123)

        delete_payment_card(self.user_name, '1234567890123456')

if __name__ == '__main__':
    unittest.main()