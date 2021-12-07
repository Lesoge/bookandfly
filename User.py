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
    mfasecretkey = db.Column(db.String(1024), nullable=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    # relation booked flights
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


class Booking_address(db.Model):
    __tablename__ = 'bookingAdress'
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)
    first_name = db.Column(db.String(1024), nullable=False)
    last_name = db.Column(db.String(1024), nullable=False)
    street = db.Column(db.String(1024), nullable=False)
    street_number = db.Column(db.String(1024), nullable=False)
    town = db.Column(db.String(1024), nullable=False)
    zipcode = db.Column(db.Integer(), nullable=False)

    def __init__(self, first_name, last_name, street, street_number, town, zipcode):
        self.first_name = first_name
        self.last_name = last_name
        self.street = street
        self.street_number = street_number
        self.town = town
        self.zipcode = zipcode


class Payment_info(db.Model):
    __tablename__ = 'paymentInfo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    credit_card_number = db.Column(db.String(1024), nullable=False)
    name_on_card = db.Column(db.String(1024), nullable=False)
    expire_date = db.Column(db.String(5), nullable=False)
    security_code = db.Column(db.Integer, nullable=False)

    def __init__(self, cc_number, no_card, expire_date, security_code):
        self.credit_card_number = cc_number
        self.name_on_card = no_card
        self.expire_date = expire_date
        self.security_code = security_code


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

    # todo test function + available seats
    def check_if_full(self):
        return len(self.booking_list) >= self.plane.seats

    def available_seats(self, bookings):
        return self.plane.seats - bookings.filter(Booking.flight == self).count()


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
    booking_address_id = db.Column(db.Integer, db.ForeignKey('bookingAdress.id'))
    booking_address = db.relationship('Booking_address', backref='bookingList')
    payment_info_id = db.Column(db.Integer, db.ForeignKey('paymentInfo.id'))
    payment_info = db.relationship('Payment_info', backref='bookingList')
    payed = db.Column(db.Boolean, default=False)

    def __init__(self, user_id, flight_id, booking_address_id, payment_info_id):
        self.user_id = user_id
        self.flight_id = flight_id
        self.booking_address_id = booking_address_id
        self.payment_info_id = payment_info_id


def db_commit(*object_list):
    for object in object_list:
        if isinstance(object, db.Model):
            db.session.add(object)
    else:
        print('Error')
        # todo add log
    db.session.commit()
