from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import *
from routes.auth import app_auth
from routes.main import app_main
from User import db, User
from flask_jwt_extended import (
    JWTManager
)

login_manager = LoginManager()


def create_app():
    main_app = Flask(__name__)
    main_app.register_blueprint(app_auth)
    main_app.register_blueprint(app_main)

    database_url = 'postgresql+psycopg2://' + dbuser + ':' + dbpassword + '@' + db_ip_and_port + '/' + dbname
    main_app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    main_app.config['SQLALCHEMY_ECHO'] = echomode
    main_app.config['SECRET_KEY'] = Secret_Key
    main_app.config['JWT_SECRET_KEY'] = JWT_Key

    db.init_app(main_app)
    login_manager.login_view = 'app_auth.login'
    login_manager.init_app(main_app)
    jwt = JWTManager(main_app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return main_app


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    create_app().run(debug=True)
