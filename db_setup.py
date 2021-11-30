from app import User, create_app
from User import db


def create_standard_admin():
    app = create_app()
    app.app_context().push()
    db.create_all()
    user = User('admin', "admin@admin.de", '1234')
    user.is_admin = True
    db.session.add(user)
    db.session.commit()


if __name__ == '__main__':

    create_standard_admin()