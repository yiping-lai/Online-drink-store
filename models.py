from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
import os


database_path = os.environ['DATABASE_URL']
db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.create_all()


'''
Drink
'''


class Drink(db.Model):
    __tablename__ = 'drinks'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    quantity = Column(Integer)
    transactions = db.relationship('Transaction', backref='drink', lazy=True)

    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'quantity': self.quantity}


'''
Transaction
'''


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    drink_id = Column(Integer, db.ForeignKey('drinks.id'), nullable=False)
    quantity = Column(Integer)
    created_at = db.Column(db.DateTime)

    def __init__(self, drink_id, quantity, created_at):
        self.drink_id = drink_id
        self.quantity = quantity
        self.created_at = created_at

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'drink_id': self.drink_id,
            'quantity': self.quantity,
            'created_at': self.created_at
        }
