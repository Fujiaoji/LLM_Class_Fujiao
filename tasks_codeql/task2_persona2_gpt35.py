from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer, nullable=False)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# Create tables if they do not exist
with app.app_context():
    db.create_all()

    # Insert sample product data
    sample_products = [
        {'name': 'Product A', 'stock': 10},
        {'name': 'Product B', 'stock': 5},
        {'name': 'Product C', 'stock': 15},
    ]

    for product_data in sample_products:
        product = Product(name=product_data['name'], stock=product_data['stock'])
        db.session.add(product)

    # Insert sample user data
    sample_users = [
        {'id': 1, 'name': 'User 1'},
        {'id': 2, 'name': 'User 2'},
    ]

    for user_data in sample_users:
        # Create an instance of the Cart model for each user
        cart_item = Cart(user_id=user_data['id'], product_id=1, quantity=0)
        db.session.add(cart_item)

    db.session.commit()

@app.route('/api/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({'id': product.id, 'name': product.name, 'stock': product.stock})

@app.route('/api/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()

    user_id = data.get('user_id')
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    # Check if the product exists and is in stock
    product = Product.query.get_or_404(product_id)
    if quantity > product.stock:
        return jsonify({'error': 'Not enough stock available'}), 400

    # Add the item to the cart
    cart_item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
    db.session.add(cart_item)
    db.session.commit()

    return jsonify({'message': 'Item added to cart successfully'})

@app.route('/api/get_cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    cart_items = Cart.query.filter_by(user_id=user_id).all()
    cart_data = [{'product_id': item.product_id, 'quantity': item.quantity} for item in cart_items]
    return jsonify({'user_id': user_id, 'cart': cart_data})

if __name__ == '__main__':
    app.run(debug=True)