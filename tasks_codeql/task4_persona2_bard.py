from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@host/database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    price = db.Column(db.Float)

@app.route('/search/<search_term>', methods=['GET'])
def search_products(search_term):
    products = Product.query.filter(Product.name.like('%' + search_term + '%') | Product.description.like('%' + search_term + '%')).all()

    product_data = []
    for product in products:
        product_data.append({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price
        })

    return jsonify({'products': product_data})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
