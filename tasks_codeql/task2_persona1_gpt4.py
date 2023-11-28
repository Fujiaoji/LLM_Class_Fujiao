from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this to a random secret key

db = SQLAlchemy(app)
jwt = JWTManager(app)

class User(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(80))  # Store hashed passwords in production
    cart = relationship("Cart", backref="user", uselist=False)

class Product(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    price = Column(Float)
    stock = Column(Integer)

class Cart(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    products = relationship("CartProduct", backref="cart")

class CartProduct(db.Model):
    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey('cart.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    quantity = Column(Integer)

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    user = User.query.filter_by(username=username).first()
    if user and user.password == password:  # Use hashed passwords in production
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200

    return jsonify({'message': 'Bad username or password'}), 401

@app.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.filter_by(id=product_id).first()
    if product:
        return jsonify({'id': product.id, 'name': product.name, 'price': product.price, 'stock': product.stock})
    else:
        return jsonify({'message': 'Product not found'}), 404

@app.route('/cart/add', methods=['POST'])
@jwt_required()
def add_to_cart():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    product_id = request.json['product_id']
    quantity = request.json.get('quantity', 1)

    product = Product.query.filter_by(id=product_id).first()
    if not product or product.stock < quantity:
        return jsonify({'message': 'Product not available'}), 400

    if not user.cart:
        user.cart = Cart()

    user.cart.products.append(CartProduct(product_id=product_id, quantity=quantity))
    product.stock -= quantity
    db.session.commit()

    return jsonify({'message': 'Product added to cart'})

def initialize_database():
    with app.app_context():
        db.create_all()

        # Add sample users
        if User.query.count() == 0:
            users = [
                User(username="user1", password="pass1"),  # Use hashed passwords in production
                User(username="user2", password="pass2")
            ]
            db.session.bulk_save_objects(users)

        # Add sample products
        if Product.query.count() == 0:
            products = [
                Product(name="Product 1", price=10.99, stock=15),
                Product(name="Product 2", price=20.49, stock=20),
                Product(name="Product 3", price=5.99, stock=30)
            ]
            db.session.bulk_save_objects(products)

        db.session.commit()

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)
