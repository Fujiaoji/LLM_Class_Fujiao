from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Float, nullable=False)
    sales_count = db.Column(db.Integer, default=0)  # Tracks number of sales

    def __repr__(self):
        return f'<Product {self.name}>'

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/add_product', methods=['POST'])
def add_product():
    try:
        data = request.get_json()
        new_product = Product(
            name=data['name'],
            description=data['description'],
            price=data['price'],
            sales_count=data['sales_count']
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify({'message': 'Product added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    search_type = request.args.get('type')  # 'name', 'description', or 'price'
    results = []
    if search_type == 'name':
        results = Product.query.filter(Product.name.contains(query)).order_by(Product.sales_count.desc()).all()
    elif search_type == 'description':
        results = Product.query.filter(Product.description.contains(query)).order_by(Product.sales_count.desc()).all()
    elif search_type == 'price':
        try:
            price = float(query)
            results = Product.query.filter(Product.price <= price).order_by(Product.sales_count.desc()).all()
        except ValueError:
            pass

    if not results:
        return jsonify({'message': 'No results found'})
    else:
        return jsonify([{'name': product.name, 'sales_count': product.sales_count} for product in results])

if __name__ == '__main__':
    app.run(debug=True)
