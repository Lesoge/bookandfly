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
    email = db.Column(db.String(1024), nullable=True, unique=False)
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
    DepAirport = db.Column(db.String(1024), nullable=False, unique=True)
    ArrAirport = db.Column(db.String(1024), nullable=False, unique=True)
    # DepTime =
    # ArrTime =
    # Plane =

class Airport(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)


class Plane(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)


class Booking(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)
