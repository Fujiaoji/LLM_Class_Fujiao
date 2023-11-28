from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import re
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure value

# Create a SQLite database and table to store card information
def create_db():
    conn = sqlite3.connect('payment_cards.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS cards (
                      id INTEGER PRIMARY KEY,
                      user_id INTEGER,
                      user_name TEXT,
                      card_number TEXT,
                      expiration_date TEXT,
                      cvv TEXT,
                      zip_code TEXT)''')
    conn.commit()
    conn.close()

create_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_card', methods=['POST'])
def add_card():
    if request.method == 'POST':
        user_id = 1  # Replace with your user authentication logic
        user_name = request.form['user_name']
        card_number = request.form['card_number']
        expiration_date = request.form['expiration_date']
        cvv = request.form['cvv']
        zip_code = request.form['zip_code']

        # Validate the expiration date format (MM/YYYY)
        if not re.match(r'^(0[1-9]|1[0-2])\/[0-9]{4}$', expiration_date):
            flash('Invalid expiration date format (MM/YYYY)', 'error')
            return redirect(url_for('index'))

        # Check if the expiration date is in the future
        exp_month, exp_year = map(int, expiration_date.split('/'))
        current_month, current_year = datetime.datetime.now().month, datetime.datetime.now().year
        if exp_year < current_year or (exp_year == current_year and exp_month < current_month):
            flash('Card has already expired', 'error')
            return redirect(url_for('index'))

        # You can add more detailed validation for the card number and zip code here.

        conn = sqlite3.connect('payment_cards.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO cards (user_id, user_name, card_number, expiration_date, cvv, zip_code) VALUES (?, ?, ?, ?, ?, ?)',
                       (user_id, user_name, card_number, expiration_date, cvv, zip_code))
        conn.commit()
        conn.close()

        flash('Payment card added successfully', 'success')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
