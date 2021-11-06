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

    first_name = db.Column(db.String(1024), nullable=False)
    last_name = db.Column(db.String(1024), nullable=False)
    username = db.Column(db.String(1024), nullable=False, unique=True)
    password = db.Column(db.String(1024), nullable=False)

    #  role_id = db.Column(UUID(as_uuid=True), db.ForeignKey('roles.id'))
    #  role = db.relationship('Role', backref='user_list')

    def __repr__(self):
        return '<User %r>' % self.username

    def __init__(self, first_name, last_name, username, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = generate_password_hash(
            password,
            method='sha256'
        )

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)
    role_name = db.Column(
        db.String(1024),
        nullable=False,
        unique=True
    )

    def __repr__(self):
        return '<Role %r>' % self.role_name


# To user Flask login we need to tell flask how to load our users
