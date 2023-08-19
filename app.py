
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
from models import db, Product, Cliente, Ordenes

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] =\
  'sqlite:///' + os.path.join(basedir, 'database.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)
CORS(app)

with app.app_context():
   db.create_all()

#Ver todos los clientes
@app.route('/clientes', methods=['GET'])
def obtener_todos_los_clientes():
    clientes = Cliente.query.all()
    clientes_serializados = [cliente.serialize() for cliente in clientes]
    return jsonify(clientes_serializados), 200

#Editar cliente
@app.route('/clientes/<int:cliente_id>', methods=['PUT'])
def editar_cliente(cliente_id):
    cliente = Cliente.query.get(cliente_id)
    if not cliente:
        return jsonify({'message': 'Cliente no encontrado'}), 404
    data = request.json
    cliente.name = data['name']
    cliente.correo = data['correo']
    cliente.direccion = data['direccion']
    db.session.commit()
    return jsonify({'message': 'Cliente editado exitosamente'}), 200

#Eliminar cliente
@app.route('/clientes/<int:cliente_id>', methods=['DELETE'])
def eliminar_cliente(cliente_id):
    cliente = Cliente.query.get(cliente_id)
    if cliente:
        db.session.delete(cliente)
        db.session.commit()
        return jsonify({'message': 'Cliente eliminado exitosamente'}), 200
    return jsonify({'message': 'Cliente no encontrado'}), 404

#Crear nuevo cliente
@app.route('/clientes', methods=['POST'])
def crear_cliente():
    data = request.json
    nuevo_cliente = Cliente(name=data['name'], correo=data['correo'], direccion=data['direccion'])
    db.session.add(nuevo_cliente)
    db.session.commit()
    return jsonify({'message': 'Cliente creado exitosamente'}), 201

#Obtener cliente por ID
@app.route('/clientes/<int:cliente_id>', methods=['GET'])
def obtener_cliente(cliente_id):
    cliente = Cliente.query.get(cliente_id)
    if cliente:
        return jsonify(cliente.serialize()), 200
    return jsonify({'message': 'Cliente no encontrado'}), 404

#Crear nueva orden
@app.route('/ordenes', methods=['POST'])
def crear_orden():
    data = request.json
    cliente_existente = Cliente.query.get(data['cliente_id'])
    if not cliente_existente:
        return jsonify({'message': 'Cliente no encontrado'}), 404
    nueva_orden = Ordenes(fecha=data['fecha'], total=data['total'], cliente=cliente_existente)
    db.session.add(nueva_orden)
    db.session.commit()
    return jsonify({'message': 'Orden creada exitosamente'}), 201

#Eliminar orden por ID
@app.route('/ordenes/<int:orden_id>', methods=['DELETE'])
def eliminar_orden(orden_id):
    orden = Ordenes.query.get(orden_id)
    if orden:
        db.session.delete(orden)
        db.session.commit()
        return jsonify({'message': 'Orden eliminada exitosamente'}), 200
    return jsonify({'message': 'Orden no encontrada'}), 404

#Ver todas las ordenes
@app.route('/ordenes', methods=['GET'])
def obtener_todas_las_ordenes():
    ordenes = Ordenes.query.all()
    ordenes_serializadas = [orden.serialize() for orden in ordenes]
    return jsonify(ordenes_serializadas), 200

#Editar orden
@app.route('/ordenes/<int:orden_id>', methods=['PUT'])
def editar_orden(orden_id):
    orden = Ordenes.query.get(orden_id)
    if not orden:
        return jsonify({'message': 'Orden no encontrada'}), 404
    data = request.json
    orden.fecha = data['fecha']
    orden.total = data['total']
    db.session.commit()
    return jsonify({'message': 'Orden editada exitosamente'}), 200

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
