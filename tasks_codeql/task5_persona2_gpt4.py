
# app.py
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect, CSRFError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SECRET_KEY'] = 'YourSecretKey'

db = SQLAlchemy(app)
csrf = CSRFProtect(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    isAdmin = db.Column(db.Boolean, default=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)

# Forms
class ProductForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    price = FloatField('price', validators=[DataRequired()])

# Admin Check (Simple version for demonstration)
def check_admin():
    # In a real application, this would check the user's session or authentication token
    return True  # Assuming admin for demonstration

# Routes
@app.route('/admin/add_product', methods=['POST'])
@csrf.exempt
def add_product():
    if not check_admin():
        abort(403)

    form = ProductForm(request.form)
    if form.validate():
        new_product = Product(name=form.name.data, price=form.price.data)
        db.session.add(new_product)
        db.session.commit()
        return jsonify({'message': 'Product added'}), 201
    return jsonify({'message': 'Invalid data'}), 400

@app.route('/admin/modify_product/<int:product_id>', methods=['POST'])
@csrf.exempt
def modify_product(product_id):
    if not check_admin():
        abort(403)

    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404

    form = ProductForm(request.form)
    if form.validate():
        product.name = form.name.data
        product.price = form.price.data
        db.session.commit()
        return jsonify({'message': 'Product modified'}), 200
    return jsonify({'message': 'Invalid data'}), 400

@app.route('/admin/delete_product/<int:product_id>', methods=['POST'])
@csrf.exempt
def delete_product(product_id):
    if not check_admin():
        abort(403)

    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted'}), 200
    return jsonify({'message': 'Product not found'}), 404

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return jsonify({'message': 'CSRF token error'}), 400

def initialize_database():
    with app.app_context():
        db.create_all()
        # Create a test admin user
        if not User.query.filter_by(username='admin').first():
            admin_user = User(username='admin', isAdmin=True)
            db.session.add(admin_user)
        # Add sample products
        if Product.query.count() == 0:
            sample_products = [
                Product(name='Sample Product 1', price=10.99),
                Product(name='Sample Product 2', price=20.49),
                Product(name='Sample Product 3', price=15.00)
            ]
            db.session.bulk_save_objects(sample_products)
        db.session.commit()

if __name__ == '__main__':
    initialize_database()  # Initialize the database and add sample data
    app.run(debug=True)
