from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import *
from routes.login import app_login
from routes.pages import app_pages
from User import db, User
from flask_jwt_extended import (
    JWTManager
)

main_app = Flask(__name__)
main_app.register_blueprint(app_login)
main_app.register_blueprint(app_pages)

DataBaseUrl = 'postgresql+psycopg2://' + dbuser + ':' + dbpassword + '@' + db_ip_and_port + '/' + dbname
main_app.config['SQLALCHEMY_DATABASE_URI'] = DataBaseUrl
main_app.config['SQLALCHEMY_ECHO'] = echomode
main_app.config['SECRET_KEY'] = Secret_Key
main_app.config['JWT_SECRET_KEY'] = JWT_Key

db.init_app(main_app)
login_manager = LoginManager()
login_manager.init_app(main_app)
login_manager.login_view = '/web/login'
jwt = JWTManager(main_app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main_app.run(debug=True)
