# -*- coding: utf8 -*-
#user:gzf

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
# db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    CarId = db.Column(db.String(20), nullable=True, primary_key=True)
    FlightNum = db.Column(db.String(20), nullable=True)
    FlyDate = db.Column(db.DateTime, nullable=True)
    ArriveTime = db.Column(db.String(20))
    ParkDate = db.Column(db.DateTime)
    Phone = db.Column(db.String(20), nullable=True)
    ParkPlace = db.Column(db.String(20), nullable=True)
    BackPersons = db.Column(db.String(20), default=1)
    BoxNum = db.Column(db.String(10))
    Fee = db.Column(db.Integer)



class OldUser(db.Model):
    __tablename__ = 'olduser'
    CarId = db.Column(db.String(20), nullable=True, primary_key=True)
    FlightNum = db.Column(db.String(20), nullable=True)
    FlyDate = db.Column(db.DateTime, nullable=True)
    ArriveTime = db.Column(db.String(20))
    ParkDate = db.Column(db.DateTime)
    Phone = db.Column(db.String(20), nullable=True)
    ParkPlace = db.Column(db.String(20), nullable=True)
    BackPersons = db.Column(db.String(20), default=1)
    BoxNum = db.Column(db.String(10))
    Fee = db.Column(db.Integer)
    LeaveDate = db.Column(db.DateTime)

class Parker(db.Model):
    __tablename__ = 'parker'
    account = db.Column(db.String(20), nullable=True, primary_key=True)
    password_hash = db.Column(db.String(128), nullable=True)
    token = db.Column(db.String(50))

    def __init__(self, **kwargs):
        super(Parker, self).__init__(**kwargs)
        self.account = kwargs.get('account')
        self.password = kwargs.get('password')
        self.token = kwargs.get('token')


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def varify_password(self, password):
        return check_password_hash(self.password_hash, password)
