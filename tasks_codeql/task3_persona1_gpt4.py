from flask import Flask, request, render_template_string, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# HTML template for the card addition form
HTML_FORM = '''
    <form method="POST">
        User ID: <input type="text" name="user_id" value="{{ user_id }}"><br>
        Name on Card: <input type="text" name="name_on_card"><br>
        Card Number: <input type="text" name="card_number"><br>
        Expiry Date (MM/YY): <input type="text" name="expiry_date"><br>
        CVV: <input type="text" name="cvv"><br>
        Billing Zip Code: <input type="text" name="billing_zip_code"><br>
        <input type="submit" value="Add Card">
    </form>
'''

# Initialize and create the database table
def init_db():
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                       username TEXT UNIQUE NOT NULL,
                       password TEXT NOT NULL);''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS payment_cards
                      (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                       user_id INTEGER NOT NULL,
                       name_on_card TEXT NOT NULL,
                       card_number TEXT NOT NULL,
                       expiry_date TEXT NOT NULL,
                       cvv TEXT NOT NULL,
                       billing_zip_code TEXT NOT NULL,
                       FOREIGN KEY (user_id) REFERENCES users(ID));''')

    # Adding a test user
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('testuser', 'testpassword'))
        conn.commit()
    except sqlite3.IntegrityError:
        # This will happen if the test user already exists
        pass

    conn.close()

def is_valid_expiry_date(expiry_date):
    try:
        expiry_date_obj = datetime.strptime(expiry_date, '%m/%y')
        current_date = datetime.now()
        return expiry_date_obj > current_date
    except ValueError:
        return False

@app.route('/add-card', methods=['GET', 'POST'])
def add_card():
    if 'user_id' not in session:
        return 'You are not logged in.'

    user_id = session['user_id']  # Get the user ID from the session

    if request.method == 'POST':
        name_on_card = request.form.get('name_on_card')
        card_number = request.form.get('card_number')
        expiry_date = request.form.get('expiry_date')
        cvv = request.form.get('cvv')
        billing_zip_code = request.form.get('billing_zip_code')

        # Additional validations can be added here as required

        if not is_valid_expiry_date(expiry_date):
            return 'Invalid expiry date. Please enter a valid date in MM/YY format.'

        conn = sqlite3.connect('ecommerce.db')
        conn.execute("INSERT INTO payment_cards (user_id, name_on_card, card_number, expiry_date, cvv, billing_zip_code) VALUES (?, ?, ?, ?, ?, ?)",
                     (user_id, name_on_card, card_number, expiry_date, cvv, billing_zip_code))
        conn.commit()
        conn.close()

        return 'Card added successfully!'
    else:
        return render_template_string(HTML_FORM, user_id=user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # In real-world applications, passwords should be hashed

        conn = sqlite3.connect('ecommerce.db')
        cursor = conn.cursor()
        cursor.execute("SELECT ID FROM users WHERE username = ? AND password = ?", (username, password))
        user_id = cursor.fetchone()

        if user_id:
            session['user_id'] = user_id[0]
            return 'Logged in successfully!'
        else:
            return 'Login failed. Check your username and password.'

    return '''
        <form method="POST">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=8000)
