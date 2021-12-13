from functools import wraps

from flask import request, current_app, session, redirect, url_for
from flask_login.config import EXEMPT_METHODS

'''
Decorators die benötigt werden
__author__ = L. F.
'''


def breached(func):
    '''Falls das Passwort des Nutzer gebrochen wurde verhindert der Decorator Zugriff
    auf geschütze Seiten'''
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif current_app.config.get('LOGIN_DISABLED'):
            return func(*args, **kwargs)
        elif 'breached' in session and session['breached']:
            return redirect(url_for('app_auth.set_new_password'))
        return func(*args, **kwargs)
    return decorated_view


