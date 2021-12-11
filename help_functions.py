import logging
from functools import wraps

from flask import request, current_app, session, redirect, url_for, abort
from flask_login.config import EXEMPT_METHODS


def breached(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif current_app.config.get('LOGIN_DISABLED'):
            return func(*args, **kwargs)
        elif 'breached' in session:
            return redirect(url_for('app_auth.set_new_password'))
        return func(*args, **kwargs)
    return decorated_view


def get_from_session(key, remote_addr):
    if key in session:
        return session[key]
    else:
        logger = logging.getLogger('web_logger')
        logger.warning('tried to access signup_mfa through an invalid path',
                       extra={'ip': remote_addr, 'user': 'anonym'})
        abort(404, description='you tried to access that page through an invalid path')