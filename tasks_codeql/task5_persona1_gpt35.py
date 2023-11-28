from flask import Flask, render_template, request

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# Define the User and Product models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

# Create tables
with app.app_context():
    db.create_all()

# Sample data for testing
with app.app_context():
    # Check if the admin user already exists
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        admin_user = User(username='admin', is_admin=True)
        db.session.add(admin_user)
        db.session.commit()

    # Check if the sample products already exist
    sample_products = Product.query.all()
    if not sample_products:
        sample_products = [
            Product(name='Product 1', price=19.99),
            Product(name='Product 2', price=29.99),
            Product(name='Product 3', price=39.99),
        ]
        db.session.add_all(sample_products)
        db.session.commit()

# Route to manage products (only accessible by admin users)
@app.route('/admin/manage-products', methods=['GET', 'POST'])
def manage_products():
    # Check if the current user has admin privileges
    username = "admin"  # Replace with the actual username of the logged-in user
    current_user = User.query.filter_by(username=username).first()

    if current_user and current_user.is_admin:
        if request.method == 'POST':
            # Handle form submission for adding a new product
            if 'add_product' in request.form:
                product_name = request.form.get('name')
                product_price = float(request.form.get('price'))

                new_product = Product(name=product_name, price=product_price)
                db.session.add(new_product)
                db.session.commit()

            # Handle form submission for modifying a product
            elif 'modify_product' in request.form:
                product_id = int(request.form.get('product_id'))
                updated_name = request.form.get('updated_name')
                updated_price = float(request.form.get('updated_price'))

                product = Product.query.get(product_id)
                if product:
                    product.name = updated_name
                    product.price = updated_price
                    db.session.commit()

            # Handle form submission for removing a product
            elif 'remove_product' in request.form:
                product_id = int(request.form.get('product_id'))

                product = Product.query.get(product_id)
                if product:
                    db.session.delete(product)
                    db.session.commit()

        # Fetch all products from the database
        products = Product.query.all()

        return render_template('manage_products.html', products=products)
    else:
        return "You do not have admin privileges."

if __name__ == '__main__':
    app.run(debug=True)