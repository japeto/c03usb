from flask import request, jsonify
from models import db, Orders

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

#Ver orden por ID
@app.route('/ordenes/<int:orden_id>', methods=['GET'])
def obtener_orden(orden_id):
    orden = Ordenes.query.get(orden_id)
    if orden:
        return jsonify(orden.serialize()), 200
    return jsonify({'message': 'Orden no encontrada'}), 404

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
