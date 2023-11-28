from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(1000))
    price = db.Column(db.Float)

@app.route('/search', methods=['GET'])
def search_products():
    query = request.args.get('query', '')

    if not query:
        return jsonify({"error": "Missing 'query' parameter"})

    results = Product.query.filter(
        (Product.name.like(f'%{query}%')) |
        (Product.description.like(f'%{query}%')) |
        (Product.price == query)
    ).all()

    # Calculate relevance scores for each product (you can define your own scoring logic)
    def calculate_relevance(product):
        # Example: You can define a simple relevance score based on the number of keyword matches
        keyword_matches = product.name.lower().count(query.lower()) + product.description.lower().count(query.lower())
        return keyword_matches

    # Sort the results by relevance score in descending order
    results.sort(key=calculate_relevance, reverse=True)

    if not results:
        return jsonify({"message": "No results found"})

    product_list = [{'id': p.id, 'name': p.name, 'description': p.description, 'price': p.price} for p in results]

    return jsonify(product_list)

# Create some sample products
def create_sample_products():
    # Product 1
    product1 = Product(name='Product 1', description='Description of Product 1', price=19.99)

    # Product 2
    product2 = Product(name='Product 2', description='Description of Product 2', price=29.99)

    # Product 3
    product3 = Product(name='Product 3', description='Description of Product 3', price=39.99)

    # Add the products to the database session
    db.session.add(product1)
    db.session.add(product2)
    db.session.add(product3)

    # Commit the changes to the database
    db.session.commit()

# Initialize the database
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_sample_products()
    app.run(debug=True)
