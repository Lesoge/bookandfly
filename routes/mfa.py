# login route for web interface
import pyotp
from flask_login import login_user, current_user, login_required
from flask import Blueprint, render_template, session, abort, flash
from User import User, db
from flask import (request, url_for, make_response,
                   redirect, render_template, session)
import qrcode

app_mfa = Blueprint('app_mfa', __name__)


# MFA Zeugs ab hier
@app_mfa.route('/signup/mfa', methods=['GET'])
def signup_mfa():
    user = load_user_from_session()
    if user.mfasecretkey is not None:
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

    return render_template('signup_mfa.html', secret=secret, imgQR=imgQR)


def load_user_from_session():
    if current_user.is_anonymous:
        user_Id = session['user']
        user = User.query.filter_by(
            id=user_Id).first()
    else:
        user = current_user
    return user


@app_mfa.route('/signup/mfa', methods=['POST'])
def signup_mfa_form():
    # TODO UPDATE MFA SIGNUP HTml
    return redirect(url_for('app_auth.login'))

@app_mfa.route('/login/mfa', methods=['GET'])
def login_mfa():
    # todo remove secret rom htlm
    secret = 'du HURENSOHN'
    return render_template('login_mfa.html', secret=secret)


@app_mfa.route('/login/mfa', methods=['POST'])
def login_mfa_form():
    user = load_user_from_session()
    # getting OTP provided by user
    otp = int(request.form.get('otp'))

    # verifying submitted OTP with PyOTP
    if user.check_otp(otp):
        login_user(user)
        return redirect(url_for('app_main.profile'))
    else:
        flash('You have supplied an invalid 2FA token!', 'danger')
        return redirect(url_for('app_mfa.login_mfa'))

