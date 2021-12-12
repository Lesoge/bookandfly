from functools import wraps

from flask import request, current_app, session, redirect, url_for
from flask_login.config import EXEMPT_METHODS


def breached(func):
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


