
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)

class Orders(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    client = relationship("Client", foreign_keys=[client_id])

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