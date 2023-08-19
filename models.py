
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

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
          'product_name': self.product_name,
          'product_description': self.product_description,
          'product_price': self.product_price,
          'availability': self.availability,
        }