
import os
from flask_cors import CORS
app = Flask(__name__)
from models import db
from flask import Flask, request, jsonify, g
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from functools import wraps


basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] =\
  'sqlite:///' + os.path.join(basedir, 'database.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)
CORS(app)

with app.app_context():
   db.create_all()

app.config['JWT_SECRET_KEY'] = 'clave-123' 
jwt = JWTManager(app)


# Ruta para el registro de usuarios
@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Usuario registrado exitosamente'}), 201

# Ruta para el inicio de sesión
@app.route('/login', methods=['POST'])
def login_user():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and user.password == data['password']:
        access_token = create_access_token(identity=user.username)
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Credenciales inválidas'}), 401

# Middleware para obtener el usuario actualmente autenticado
@app.before_request
def before_request():
    g.user = get_jwt_identity()

# Middleware para autorización
def authorize(roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if g.user:
                user = User.query.filter_by(username=g.user).first()
                if user and user.role in roles:
                    return fn(*args, **kwargs)
            return jsonify({'message': 'Acceso no autorizado'}), 403
        return wrapper
    return decorator

# Ejemplo de ruta protegida (requiere autenticación y autorización)
@app.route('/protected', methods=['GET'])
@jwt_required()
@authorize(roles=['admin', 'user'])
def protected_route():
    return jsonify({'message': 'Ruta protegida'}), 200

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

#Crear nuevo producto    
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
