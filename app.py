from logging.config import dictConfig

from flask import Flask
from flask_login import LoginManager
from config import *
from routes.auth import app_auth
from routes.main import app_main
from routes.mfa import app_mfa
from routes.pay import app_pay
from dbModel import db, user_datastore, security
from flask_admin import Admin
from flask_sslify import SSLify
from logger_config import logger_config
login_manager = LoginManager()
admin = Admin()

def create_app():
    main_app = Flask(__name__)
    sslify = SSLify(main_app)
    main_app.register_blueprint(app_auth)
    main_app.register_blueprint(app_main)
    main_app.register_blueprint(app_mfa)
    main_app.register_blueprint(app_pay)
    main_app.config.from_pyfile('config.py')
    dictConfig(logger_config)
    admin.init_app(main_app)
    db.init_app(main_app)
    security.init_app(main_app, datastore=user_datastore)
    return main_app


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    create_app().run(debug=True, ssl_context=(CERT_PATH, KEY_PATH), host='127.1.1.1')
