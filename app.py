
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
