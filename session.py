from flask import session, abort
import logging
'''
Funktionen zum Session Managment
__author__ = L. F.
'''


def get_from_session(key, remote_addr):
    '''Funktion zum Abrufen eines Wertes in der Session, falls nicht vorhanden wird ein 404 error ausgegebn
    :param key wert der aus der session geholt werden soll
    :param remote_addr Ip-Adresse des Aufrufenden'''
    if key in session:
        return session[key]
    else:
        logger = logging.getLogger('web_logger')
        logger.warning('tried to access signup_mfa through an invalid path',
                       extra={'ip': remote_addr, 'user': 'anonym'})
        abort(404, description='you tried to access that page through an invalid path')