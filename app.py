
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
from models import db, Product

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] =\
  'sqlite:///' + os.path.join(basedir, 'database.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)
CORS(app)

with app.app_context():
   db.create_all()


# Ver todos los productos (GET)
@app.route('/products', methods=['GET'])
def get_all_products():
    products = Product.query.all()
    serialized_products = [product.serialize() for product in products]
    return jsonify(serialized_products), 200


# Ver un producto por su id (GET)
@app.route('/product/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    product = Product.query.get(product_id)
    if product:
        serialized_product = product.serialize()
        return jsonify(serialized_product), 200
    else:
        return jsonify({'message': 'Product not found'}), 404


# Editar un producto por su id (PUT)
@app.route('/product/<int:product_id>', methods=['PUT'])
def edit_product_by_id(product_id):
    data = request.json
    try:
        product_to_edit = Product.query.get(product_id)
        if product_to_edit:
            product_to_edit.product_name = data.get('name', product_to_edit.product_name)
            product_to_edit.product_description = data.get('description', product_to_edit.product_description)
            product_to_edit.product_price = data.get('price', product_to_edit.product_price)
            product_to_edit.availability = data.get('availability', product_to_edit.availability)
            db.session.commit()
            return jsonify({'message': 'success'}), 200
        else:
            return jsonify({'message': 'Product not found'}), 404
    except Exception as ex:
        return jsonify({'message': str(ex)}), 400


# Borrar un producto por su id (DELETE)
@app.route('/product/<int:product_id>', methods=['DELETE'])
def delete_product_by_id(product_id):
    product_to_delete = Product.query.get(product_id)
    if product_to_delete:
        db.session.delete(product_to_delete)
        db.session.commit()
        return jsonify({'message': 'Product deleted'}), 200
    else:
        return jsonify({'message': 'Product not found'}), 404
    
    


@app.route("/product", methods=['POST'])
def newproduct():
    data = request.json
    try:
      a_product = Product(
           data['name'],
           data['description'],
           data['price'],
           data['availability']
      )
      db.session.add(a_product)
      db.session.commit()
      return jsonify({"message": "success", 'id':a_product.id}), 200
    except Exception as ex:
       return jsonify({"message": str(ex)}), 400

app.run(host="0.0.0.0", debug=True, port=9030)
