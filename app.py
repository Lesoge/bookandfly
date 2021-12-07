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

    database_url = 'postgresql+psycopg2://' + dbuser + ':' + dbpassword + '@' + db_ip_and_port + '/' + dbname
    main_app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    main_app.config['SQLALCHEMY_ECHO'] = echomode
    main_app.config['SECRET_KEY'] = Secret_Key
    main_app.config['JWT_SECRET_KEY'] = JWT_Key
    main_app.config['SECURITY_LOGIN_USER_TEMPLATE'] = 'templates/login.html'
    main_app.config['SECURITY_PASSWORD_HASH'] = 'sha512_crypt'
    # Replace this with your own salt.
    main_app.config['SECURITY_PASSWORD_SALT'] = 'test'

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
    create_app().run(debug=True)
