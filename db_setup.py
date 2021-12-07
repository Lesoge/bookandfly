import getpass

from flask_security.utils import hash_password

from app import create_app, user_datastore
from User import db


def create_standard_admin():
    app = create_app()
    app.app_context().push()
    db.create_all()
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='end-user', description='End user')
    print('Create Standard Admin')
    admin_username, admin_email, admin_password = get_admin_acc()
    admin_password = hash_password(admin_password)
    user_datastore.create_user(username=admin_username, email=admin_email, password=admin_password, roles= ['admin'])
    user_datastore.commit()


def get_admin_acc():
    print('Create Standard Admin')
    admin_username = input('Admin username:')
    admin_email = input('Admin email:')
    admin_password = getpass.getpass(prompt='Admin Password:', stream=None)
    return admin_username, admin_email, admin_password


if __name__ == '__main__':
    create_standard_admin()
