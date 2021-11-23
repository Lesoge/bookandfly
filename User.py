import pyotp
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)
    username = db.Column(db.String(1024), nullable=False, unique=True)
    password = db.Column(db.String(1024), nullable=False)
    email = db.Column(db.String(1024), nullable=True, unique=True)
    mfasecretkey = db.Column(db.String(1024), nullable=True, unique=False)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = db.relationship('Role', backref=db.backref('user_list'))
    # relation booked flights
    # first_name = db.Column(db.String(1024), nullable=False)
    # last_name = db.Column(db.String(1024), nullable=False)
    # role_id = db.Column(UUID(as_uuid=True), db.ForeignKey('roles.id'))
    # role = db.relationship('Role', backref='user_list')

    def __repr__(self):
        return '<User %r>' % self.username

    def __init__(self, username, email, password):
        self.email = email
        self.username = username
        self.password = generate_password_hash(
            password,
            method='sha256',
        )

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def check_otp(self, otp):
        return pyotp.TOTP(self.mfasecretkey).verify(otp)

    def generate_otp(self):
        self.mfasecretkey = pyotp.random_base32()

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)
    name = db.Column(db.String(80), unique=True)

    def __str__(self):
        return self.name




class Flight(db.Model):
    __tablename__ = 'flights'
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)
    depAirport_id = db.Column(db.Integer, db.ForeignKey('airports.id'))
    arrAirport_id = db.Column(db.Integer, db.ForeignKey('airports.id'))
    depAirport = db.relationship('Airport', foreign_keys=[depAirport_id], backref='flightdeplist')
    arrAirport = db.relationship('Airport', foreign_keys=[arrAirport_id], backref='flightarrlist')
    depTime = db.Column(db.DateTime, nullable=False)
    arrTime = db.Column(db.DateTime, nullable=False)
    plane_id = db.Column(db.Integer, db.ForeignKey('planes.id'))
    plane = db.relationship('Plane', backref='flightlist')


class Airport(db.Model):
    __tablename__ = 'airports'
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)
    town = db.Column(db.String(1024), nullable=False)
    country = db.Column(db.String(1024), nullable=False)
    name = db.Column(db.String(1024), nullable=False, unique=True)
    iata = db.Column(db.String(3), nullable=False, unique=True)


class Plane(db.Model):
    __tablename__ = 'planes'
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)
    planename = db.Column(db.String(100), nullable=False, unique=True)
    seats = db.Column(db.Integer, nullable=False)


class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='bookinglist')
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'))
    flight = db.relationship('Flight', backref='bookinglist')


