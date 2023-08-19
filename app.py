
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

@app.route("/ping", methods=['GET'])
def pong():
    return jsonify({
        "message":"pong"
    }), 200

@app.route("/products", methods=['POST'])
def new_product():
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
    
@app.route("/products", methods=['GET'])
def products():
   return jsonify([
      a_product.serialize() for a_product in Product.query.all()
   ])

@app.route("/products/<int:id>", methods=['GET'])
def get_product(id):
   a_product = Product.query.get_or_404(id)
   return jsonify(a_product.serialize())

@app.route("/products/<int:id>", methods=['PUT'])
def edit_product(id):
   a_product = Product.query.get_or_404(id)
   data = request.json
   try:
      a_product.product_name = data['name']
      a_product.product_description = data['description']
      a_product.product_price = data['price']
      a_product.availability = data['availability']
      db.session.commit()
      return jsonify(a_product.serialize())
   except Exception as ex:
      return jsonify({"message": str(ex)}), 400

@app.route("/products/<int:id>", methods=['DELETE'])
def delete_product(id):
   a_product = Product.query.get_or_404(id)
   a_product.availability = 0
   db.session.commit()
   return jsonify(a_product.serialize())


app.run(host="0.0.0.0", debug=True, port=9030)
