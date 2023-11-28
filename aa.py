# app.py

from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# User model for login management
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)


# Product model for the products database
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)


# Login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])


# Product form for adding/modifying products
class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    price = IntegerField('Product Price', validators=[DataRequired(), NumberRange(min=0)])


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
        if user:
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login failed. Check your username and password.', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/')
@login_required
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)


@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash('You do not have admin privileges.', 'danger')
        return redirect(url_for('index'))

    products = Product.query.all()
    return render_template('admin.html', products=products)


@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if not current_user.is_admin:
        flash('You do not have admin privileges.', 'danger')
        return redirect(url_for('index'))

    form = ProductForm()
    if form.validate_on_submit():
        new_product = Product(name=form.name.data, price=form.price.data)
        db.session.add(new_product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('admin'))
    return render_template('add_product.html', form=form)


@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    if not current_user.is_admin:
        flash('You do not have admin privileges.', 'danger')
        return redirect(url_for('index'))

    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('admin'))
    return render_template('edit_product.html', form=form, product=product)


@app.route('/delete_product/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    if not current_user.is_admin:
        flash('You do not have admin privileges.', 'danger')
        return redirect(url_for('index'))

    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('admin'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


<!-- login.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
</head>
<body>
    <h1>Login</h1>
    <form method="POST">
        {{ form.hidden_tag() }}
        <p>Username: {{ form.username }}</p>
        <p>Password: {{ form.password }}</p>
        <p><input type="submit" value="Login"></p>
    </form>
</body>
</html>
