import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Create database and tables if they don't exist
def create_tables():
    connection = sqlite3.connect('ecom.db')
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT UNIQUE,
        password TEXT
    )''')

    connection.commit()
    connection.close()

create_tables()

# User registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if username or email already exists
        connection = sqlite3.connect('ecom.db')
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM users WHERE username=? OR email=?', (username, email))
        user = cursor.fetchone()

        if user:
            error = 'Username or email already exists'
            return render_template('register.html', error=error)

        # Register user if username and email are unique
        cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, password))
        connection.commit()
        connection.close()

        success = 'Registration successful. Please login to continue.'
        return render_template('register.html', success=success)

    return render_template('register.html')

# User login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validate user credentials
        connection = sqlite3.connect('ecom.db')
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        user = cursor.fetchone()

        if user:
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid username or password'
            return render_template('login.html', error=error)

    return render_template('login.html')

# Dashboard route for logged-in users
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
