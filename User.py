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
            method='sha256'
        )

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Flight(db.Model):
    __tablename__ = 'flights'
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)
    depAirport_id = db.Column(db.Integer, db.ForeignKey('airports.id'))
    arrAirport_id = db.Column(db.Integer, db.ForeignKey('airports.id'))
    depAirport = db.relationship('Airport', backref='flightdeplist')
    arrAirport = db.relationship('Airport', backref='flightarrlist')
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
    flight = db.relationship('User', backref='bookinglist')


