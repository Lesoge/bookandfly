from flask import session, abort
import logging


def get_from_session(key, remote_addr):
    if key in session:
        return session[key]
    else:
        logger = logging.getLogger('web_logger')
        logger.warning('tried to access signup_mfa through an invalid path',
                       extra={'ip': remote_addr, 'user': 'anonym'})
        abort(404, description='you tried to access that page through an invalid path')