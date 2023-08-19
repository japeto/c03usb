
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Client(db.Model):
    __tablename__ = "clients"   

    id = db.Column(db.Integer,primary_key=True)
    client_name = db.Column(db.String(100),unique=True)
    client_email = db.Column(db.String(100),unique=True)
    client_address = db.Column(db.String(100),unique=True)

    def __init__ (self,name,email,address):
        self.client_name = name
        self.client_email = email
        self.client_address = address

    def __repr__(self):
        return '<Client %r, %r>' % self.id, self.client_name

    def serialize(self):
        return {
            'client_id' :   self.id,
            'client_name' : self.client_name,
            'client_email' :self.client_email,
            'client_address' : self.client_address,
        }

class Orders(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer,primary_key=True)
    order_date = db.Column(db.DateTime)
    client_id = db.Column(db.Integer,db.ForeignKey('clients.id'),nullable=False)
    client = relationship("Client", foreign_keys=[client_id])

    def __init__ (self,date,client_id):
        self.order_date = date
        self.client_id = client_id

    def __repr__(self):
        return '<Orders %r, %r, %r>' % self.id, self.order_date, self.client_id

    def serialize(self):
        return {
            'Order_id' :   self.id,
            'Order_date' : self.order_date,
            'client_id' :self.client_id,
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