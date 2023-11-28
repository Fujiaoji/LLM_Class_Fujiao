from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Use SQLite for simplicity
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this to a secure secret key in a production environment
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Define User, Product, and Cart models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer, nullable=False)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)

# Create tables in the database
with app.app_context():
    db.create_all()

# Add sample users and products
sample_users = [
    {'username': 'john_doe', 'password': 'password1'},
    {'username': 'jane_smith', 'password': 'password2'}
]

sample_products = [
    Product(name='Product A', stock=10),
    Product(name='Product B', stock=5),
    Product(name='Product C', stock=8)
]

with app.app_context():
    for user_data in sample_users:
        existing_user = User.query.filter_by(username=user_data['username']).first()
        if not existing_user:
            new_user = User(username=user_data['username'], password=user_data['password'])
            db.session.add(new_user)

    db.session.bulk_save_objects(sample_products)
    db.session.commit()

# API endpoint for user registration
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Check if the username already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'error': 'Username already exists'}), 400

    # Create a new user
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'})

# API endpoint for user login and token generation
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Check if the user exists and the password is correct
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        # Generate an access token
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token)
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

# API endpoint to retrieve product information by product ID
@app.route('/api/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({'id': product.id, 'name': product.name, 'stock': product.stock})
    else:
        return jsonify({'error': 'Product not found'}), 404

# API endpoint to add products with stock to the user's cart
@app.route('/api/add_to_cart', methods=['POST'])
@jwt_required()
def add_to_cart():
    current_user_id = get_jwt_identity()
    data = request.get_json()

    product_id = data.get('product_id')

    # Check if the product is in stock
    product = Product.query.filter_by(id=product_id).first()
    if product and product.stock > 0:
        # Reduce the stock of the product
        product.stock -= 1
        db.session.commit()

        # Add the product to the user's cart
        cart_item = Cart(user_id=current_user_id, product_id=product_id)
        db.session.add(cart_item)
        db.session.commit()

        return jsonify({'message': 'Product added to cart successfully'})
    else:
        return jsonify({'error': 'Product not available or out of stock'}), 400

if __name__ == '__main__':
    app.run(debug=True)