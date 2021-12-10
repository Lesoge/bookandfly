from flask import Flask, render_template
from flask_login import LoginManager
from flask_security import Security
from flask_sqlalchemy import SQLAlchemy
from config import *
from routes.auth import app_auth
from routes.main import app_main
from routes.mfa import app_mfa
from routes.pay import app_pay
from User import db, User, user_datastore, security
from flask_admin import Admin
from AdminModel import create_admin
from OpenSSL import SSL
login_manager = LoginManager()
admin = Admin()


def create_app():
    main_app = Flask(__name__)
    main_app.register_blueprint(app_auth)
    main_app.register_blueprint(app_main)
    main_app.register_blueprint(app_mfa)
    main_app.register_blueprint(app_pay)
    main_app.config.from_pyfile('config.py')
    admin.init_app(main_app)
    create_admin(admin)
    db.init_app(main_app)
    security.init_app(main_app, datastore=user_datastore)

    return main_app
#
# def create_context():
#     context = SSL.Context(SSL.TLSv1_2_METHOD)
#     context.use_certificate('certfile')
#     context.use_privatekey('privkey')
#


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    create_app().run(debug=True, ssl_context=('cert.pem', 'ca-key.pem'), host='127.1.1.1')
