# login route for web interface
import pyotp
from flask_login import login_user, logout_user, current_user, login_required
from flask import Blueprint, render_template, session, abort, flash
from User import User, db
from flask import (request, url_for, make_response,
                   redirect, render_template, session)
import qrcode

app_mfa = Blueprint('app_mfa', __name__)


# MFA Zeugs ab hier
@app_mfa.route('/signup/mfa', methods=['GET'])
def signup_mfa():
    secret = pyotp.random_base32()
    qrCodeURI = pyotp.totp.TOTP(secret).provisioning_uri(name=current_user.username + ' bookandfly', issuer_name='Secure App')
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5)
    qr.add_data(qrCodeURI)
    qr.make(fit=True)
    imgQR = qr.make_image(fill='black', back_color='white')
    imgQR.save('static/qrcode.png', compress_level=1)

    return render_template('signup_mfa.html', secret=secret, imgQR=imgQR)


@app_mfa.route('/signup/mfa', methods=['POST'])
def signup_mfa_form():
    # getting fresh generated secret
    secret = request.form.get('secret')
    # getting OTP provided by user
    otp = int(request.form.get('otp'))

    # verifying submitted OTP with PyOTP
    if pyotp.TOTP(secret).verify(otp):
        # inform users if OTP is valid
        print('The TOTP 2FA token is valid', 'success')

        # TODO login_user() falls notwendig
        login_user()

        # safe secret in user data in database
        current_user.mfasecretkey = secret
        db.session.add(current_user)
        db.session.commit()

        return redirect(url_for('app_main.profile'))
    else:
        # inform users if OTP is invalid
        print('You have supplied an invalid 2FA token!', 'danger')
        flash('You have supplied an invalid 2FA token!', 'danger')
        return redirect(url_for('app_mfa.signup_mfa'))


@app_mfa.route('/login/mfa', methods=['GET'])
def login_mfa():
    secret = current_user.mfasecretkey
    return render_template('login_mfa.html', secret=secret)


@app_mfa.route('/login/mfa', methods=['POST'])
def login_mfa_form():
    # getting secret key used by user (loaded from user data in database)
    secret = request.form.get('secret')
    # getting OTP provided by user
    otp = int(request.form.get('otp'))

    # verifying submitted OTP with PyOTP
    if pyotp.TOTP(secret).verify(otp):
        # inform users if OTP is valid
        print('The TOTP 2FA token is valid', 'success')

        # TODO login_user()
        login_user()

        return redirect(url_for('app_main.profile'))
    else:
        # inform users if OTP is invalid
        flash('You have supplied an invalid 2FA token!', 'danger')
        return redirect(url_for('app_mfa.login_mfa'))

