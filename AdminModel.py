from flask_admin.contrib.sqla import ModelView
from User import db, User, Flight, Airport, Plane, Booking
from flask_security import current_user
from flask_admin.form import SecureForm


# Flask and Flask-SQLAlchemy initialization here
class AdminModelView(ModelView):
    from_base_class = SecureForm

    def is_accessible(self):
        return (current_user.is_authenticated and
                current_user.has_role('admin'))


def create_admin(admin):
    admin.add_view(AdminModelView(User, db.session))
    admin.add_view(AdminModelView(Flight, db.session))
    admin.add_view(AdminModelView(Airport, db.session))
    admin.add_view(AdminModelView(Plane, db.session))
    admin.add_view(AdminModelView(Booking, db.session))
