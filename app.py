from logging.config import dictConfig

from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

from AdminModel import create_admin
from routes.auth import app_auth
from routes.main import app_main
from routes.mfa import app_mfa
from routes.pay import app_pay
from dbModel import db, user_datastore, security
from flask_admin import Admin
from flask_sslify import SSLify
from config.loggerConfig import logger_config
from config.config import CERT_NAME, KEY_NAME, APP_IP
'''
Hier wird die Flask app erstellt.
__author__ = L. F.
'''

login_manager = LoginManager()
admin = Admin()
csrf = CSRFProtect()



def create_app(log_conf=logger_config, config_path='config/config.py', ssl=True):
    '''Funktion zum konfigurieren der app
    :param log_conf config des Logger
    :param config_path speicherort der config
    :param Booelan ob ssl benutzt werden soll'''
    main_app = Flask(__name__)
    csrf.init_app(main_app)
    if ssl:
        sslify = SSLify(main_app)
    main_app.register_blueprint(app_auth)
    main_app.register_blueprint(app_main)
    main_app.register_blueprint(app_mfa)
    main_app.register_blueprint(app_pay)
    main_app.config.from_pyfile(config_path)
    dictConfig(log_conf)
    admin.init_app(main_app)
    create_admin(admin)
    db.init_app(main_app)
    security.init_app(main_app, datastore=user_datastore)

    @main_app.after_request
    def apply_caching(response):
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Cache-Control'] = 'max-age=300'
        return response
    return main_app

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    create_app().run(ssl_context=(CERT_NAME, KEY_NAME), host=APP_IP)
