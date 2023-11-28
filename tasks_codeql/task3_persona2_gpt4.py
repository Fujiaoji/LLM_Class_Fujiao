from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///payment.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

class PaymentCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    card_token = db.Column(db.String(80), nullable=False)
    card_name = db.Column(db.String(100), nullable=False)
    expiration_date = db.Column(db.String(10), nullable=False)
    cvv = db.Column(db.String(5), nullable=False)
    billing_zip = db.Column(db.String(20), nullable=False)

def initialize_database():
    with app.app_context():
        db.create_all()
        # Create a default user if not already present
        if User.query.count() == 0:
            default_user = User(name="John Doe", email="johndoe@example.com")
            db.session.add(default_user)
            db.session.commit()

initialize_database()

@app.route('/add_card', methods=['POST'])
def add_card():
    data = request.json
    user_id = data.get('user_id')
    card_token = data.get('card_token')
    card_name = data.get('card_name')
    expiration_date = data.get('expiration_date')
    cvv = data.get('cvv')
    billing_zip = data.get('billing_zip')

    if not all([user_id, card_token, card_name, expiration_date, cvv, billing_zip]):
        return jsonify({"error": "Missing fields"}), 400

    if not re.match(r"^\d{3,4}$", cvv):
        return jsonify({"error": "Invalid CVV"}), 400
    try:
        exp_date = datetime.strptime(expiration_date, '%m/%y')
        if exp_date < datetime.now():
            return jsonify({"error": "Card expired"}), 400
    except ValueError:
        return jsonify({"error": "Invalid expiration date"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    new_card = PaymentCard(user_id=user_id, card_token=card_token, card_name=card_name,
                           expiration_date=expiration_date, cvv=cvv, billing_zip=billing_zip)
    db.session.add(new_card)
    db.session.commit()

    return jsonify({"message": "Card added successfully", "card_id": new_card.id}), 201


@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


if __name__ == '__main__':
    app.run(debug=True, port=8000)
