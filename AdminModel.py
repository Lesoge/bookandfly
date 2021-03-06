from flask_admin.contrib.sqla import ModelView
from wtforms import PasswordField, BooleanField

from dbModel import db, User, Flight, Airport, Plane, Booking
from flask_security import current_user, hash_password
from flask_admin.form import SecureForm
'''
AdminModel.py die Instanzierung der Bibilothek Flask-Admin
die ermöglicht einfach die Datenbank im Web zu verwalten
__author__ L. F.

'''

# Flask and Flask-SQLAlchemy initialization here
class DbModelView(ModelView):
    from_base_class = SecureForm

    def is_accessible(self):
        return (current_user.is_authenticated and
                current_user.has_role('admin'))

class UserModelView(ModelView):
    from_base_class = SecureForm
    # Entfert die sensiven Spalten passwort und mfasecret key aus dem Webinterface und der form
    column_exclude_list = ('password','mfasecretkey')
    form_excluded_columns = ('password','mfasecretkey')

    def is_accessible(self):
        # definiert, wer auf die Model view zugreifen darf: User mit der Rolle Admin
        return (current_user.is_authenticated and
                current_user.has_role('admin'))

    def scaffold_form(self):
        #Überschreibt welche Werte im Admin Interface gesetzt werden können
        form_class = super(UserModelView, self).scaffold_form()
        form_class.password2 = PasswordField('New Password')
        form_class.mfasecretkey2 = BooleanField(description=False)
        return form_class

    def on_model_change(self, form, model, is_created):
        # Definiert die Funktion der neuen Spalten
        if len(model.password2):
            model.password = hash_password(model.password2)
        if model.mfasecretkey2:
            model.mfasecretkey = None


def create_admin(admin):
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(DbModelView(Flight, db.session))
    admin.add_view(DbModelView(Airport, db.session))
    admin.add_view(DbModelView(Plane, db.session))
    admin.add_view(DbModelView(Booking, db.session))
