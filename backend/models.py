
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Cliente(db.Model):
    __tablename__ = 'cliente'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    correo = db.Column(db.String(255))
    direccion = db.Column(db.Text)

    def __init__(self, name, correo, direccion):
        self.name = name
        self.correo = correo
        self.direccion = direccion

    def __repr__(self):
        return '<Cliente %r>' % self.name

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'correo': self.correo,
            'direccion': self.direccion,
        }
    


class Ordenes(db.Model):
    __tablename__ = 'ordenes'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date)
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id'))

    def __init__(self, fecha, id_cliente):
        self.fecha = fecha
        self.id_cliente = id_cliente

    def __repr__(self):
        return '<Ordenes %r>' % self.id

    def serialize(self):
        return {
            'id': self.id,
            'fecha': self.fecha,
            'id_cliente': self.id_cliente,
        }
    


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), unique=True)
    product_description = db.Column(db.String(100))
    product_price = db.Column(db.String(100), nullable=False)
    availability = db.Column(db.String(100))

    def __init__(self, name, description, price, availability):        
        self.product_name = name
        self.product_description = description
        self.product_price = price
        self.availability = availability
    
    def __repr__(self):
        return '<Product %r, %r>' % self.id, self.product_name
    
    def serialize(self):
        return {
          'id': self.id,
          'name': self.product_name,
          'description': self.product_description,
          'price': self.product_price,
          'availability': self.availability,
        }
    

class Detalles(db.Model):
    __tablename__ = 'detalles'
    id = db.Column(db.Integer, primary_key=True)
    id_orden = db.Column(db.Integer, db.ForeignKey('ordenes.id'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    cantidad = db.Column(db.Integer)
    valor = db.Column(db.Float)

    def __init__(self, id_orden, id_producto, cantidad, valor):
        self.id_orden = id_orden
        self.id_producto = id_producto
        self.cantidad = cantidad
        self.valor = valor

    def __repr__(self):
        return '<Detalles %r>' % self.id

    def serialize(self):
        return {
            'id': self.id,
            'id_orden': self.id_orden,
            'id_producto': self.id_producto,
            'cantidad': self.cantidad,
            'valor': self.valor,
        }
