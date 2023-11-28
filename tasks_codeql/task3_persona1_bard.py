import sqlite3
import json
import datetime

# Define the database schema
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS payment_cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    card_number TEXT NOT NULL,
    ccv_cvv TEXT NOT NULL,
    expiration_date TEXT NOT NULL,
    name_on_card TEXT NOT NUlL,
    billing_address TEXT NOT NULL,
    billing_zip_code TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
"""

# Connect to the database
conn = sqlite3.connect('ecommerce.db')

# Create the payment_cards table if it doesn't exist
cursor = conn.cursor()
cursor.execute(CREATE_TABLE_SQL)
conn.commit()

# Function to get user ID from username
def get_user_id(username):
    # Retrieve user ID using the provided username
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user_id = cursor.fetchone()[0]

    if not user_id:
        raise Exception("User does not exist")

    return user_id

# Function to validate required input parameters
def validate_payment_card_input(card_number, ccv_cvv, expiration_date, name_on_card, billing_zip_code):
    # Check if all required parameters are present
    if not all([card_number, ccv_cvv, expiration_date, name_on_card, billing_zip_code]):
        raise Exception("Missing required input parameters. Please provide all necessary information.")

    # Validate expiration date format
    try:
        month, year = expiration_date.split('/')
        expiration_date = datetime.datetime(int(year), int(month), 1)
    except ValueError:
        raise Exception("Invalid expiration date format. Please enter the expiration date in MM/YYYY format.")

    # Check if expiration date is in the future
    if expiration_date < datetime.datetime.now():
        raise Exception("Expiration date cannot be in the past. Please enter a valid expiration date.")

# Function to add a new payment card to the database
def add_payment_card(username, card_number, ccv_cvv, expiration_date, name_on_card, billing_address, billing_zip_code):
    # Validate required input parameters before proceeding
    validate_payment_card_input(card_number, ccv_cvv, expiration_date, name_on_card, billing_zip_code)

    # Get user ID using the provided username
    user_id = get_user_id(username)

    # Insert the new payment card into the database
    cursor.execute(
        """
        INSERT INTO payment_cards (user_id, card_number, ccv_cvv, expiration_date, name_on_card, billing_address, billing_zip_code)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (user_id, card_number, ccv_cvv, expiration_date, name_on_card, billing_address, billing_zip_code)
    )
    conn.commit()

# Function to verify the successful addition of a payment card
def verify_payment_card(username, card_number):
    # Retrieve the user ID using the provided username
    user_id = get_user_id(username)

    # Check if the payment card exists for the specified user
    cursor.execute(
        """
        SELECT * FROM payment_cards WHERE user_id = ? AND card_number = ?
        """,
        (user_id, card_number)
    )
    payment_card = cursor.fetchone()

    if not payment_card:
        raise Exception("Payment card not found")

    print("Payment card successfully added for user:", username)

# Function to test adding a new payment card
def test_add_payment_card():
    add_payment_card('bob_jones', '1234-5678-9012-3456', '123', '12/2023', 'Bob Jones', '123 Main Street, Anytown, CA 12345', '98765')
    verify_payment_card('bob_jones', '1234-5678-9012-3456')

# Test the code
test_add_payment_card()