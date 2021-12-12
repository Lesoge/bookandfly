# login route for web interface
import logging

import pyotp
from flask_security import current_user, login_required
from flask_security.utils import login_user
from flask import Blueprint, render_template, session, abort, flash
from dbModel import User, db, security
from session import get_from_session
from flask import (request, url_for, make_response,
                   redirect, render_template, session)
from Forms import MfaForm
import qrcode

app_mfa = Blueprint('app_mfa', __name__)

logger = logging.getLogger('web_logger')


@app_mfa.route('/signup/mfa', methods=['GET'])
def signup_mfa():
    user_id = get_from_session('user_id', request.remote_addr)
    user = User.query.get_or_404(user_id)
    if user.mfasecretkey is not None:
        logger.warning('tried to access signup_mfa despite having an mfa key',
                       extra={'ip': request.remote_addr, 'user':user.id})
        return redirect(url_for('app_auth.login'))
    user.generate_otp()
    db.session.add(user)
    db.session.commit()
    secret = user.mfasecretkey
    qrCodeURI = pyotp.totp.TOTP(secret).provisioning_uri(name=user.username + ' bookandfly', issuer_name='Secure App')
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5)
    qr.add_data(qrCodeURI)
    qr.make(fit=True)
    imgQR = qr.make_image(fill='black', back_color='white')
    imgQR.save('static/qrcode.png', compress_level=1)
    logger.info('created mfa key',
                   extra={'ip': request.remote_addr, 'user': user.id})
    return render_template('signup_mfa.html', secret=secret, imgQR=imgQR)





@app_mfa.route('/signup/mfa', methods=['POST'])
def signup_mfa_form():
    return redirect(url_for('app_auth.login'))


@app_mfa.route('/login/mfa', methods=['GET'])
def login_mfa():
    return render_template('login_mfa.html')


@app_mfa.route('/login/mfa', methods=['POST'])
def login_mfa_form():
    user_id = get_from_session('user_id', request.remote_addr)
    user = User.query.get_or_404(user_id)
    form = MfaForm(request.form)
    if not form.validate():
        logger.info('invalid input in mfa_form',
                       extra={'ip': request.remote_addr, 'user': user.id})
        flash('You have supplied an invalid 2FA token!', 'danger')
        return redirect(url_for('app_mfa.login_mfa'))
    otp = form.otp.data

    if 'remember' in session:
        remember = session['remember']
    else:
        remember = False
    # verifying submitted OTP with PyOTP
    if user.check_otp(otp):
        login_user(user, remember)
        logger.info('logged_in',
                       extra={'ip': request.remote_addr, 'user': user.id})
        if 'breached' in session:
            pass
            #return redirect(url_for('app_auth.set_new_password'))
        return redirect(url_for('app_main.profile'))
    else:
        logger.info('invalid mfa token',
                    extra={'ip': request.remote_addr, 'user': user.id})
        flash('You have supplied an invalid 2FA token!', 'danger')
        return redirect(url_for('app_mfa.login_mfa'))
