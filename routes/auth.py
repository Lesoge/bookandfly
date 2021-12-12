# login route for web interface
import logging

from flask_login import login_user, logout_user, current_user, login_required
from flask import Blueprint, render_template, session, abort, flash
from flask_security import hash_password, password_breached_validator, password_length_validator
from flask_security import password_complexity_validator
from dbModel import User, db, db_commit, user_datastore, security
from session import get_from_session
from flask import (request, url_for, make_response,
                   redirect, render_template, session, current_app)
from Forms import LogInForm, SignUpForm, ResetPasswordForm

app_auth = Blueprint('app_auth', __name__)
logger = logging.getLogger('web_logger')


@app_auth.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app_auth.route('/login', methods=['POST'])
def login_post():
    form = LogInForm(request.form)
    if not form.validate():
        logger.info('invalid input in login form', extra={'ip': request.remote_addr, 'user': 'anonym'})
        flash('Invalid inputs')
        return redirect(url_for('app_auth.login'))

    user = User.query.filter_by(email=form.email.data).first()
    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    message = 'Please check your login details and try again. If you entered a wrong password 5 times your account may be locked'
    if not user:
        logger.info('tried to log in as an non existing user' + form.email.data, extra={'ip': request.remote_addr, 'user': 'anonym'})
        flash(message)
        return redirect(url_for('app_auth.login'))  # if the user doesn't exist or password is wrong, reload the page
    elif not user.check_password(form.password.data):
        flash(message)
        logger.info('entered wrong password' + form.email.data,
                    extra={'ip': request.remote_addr, 'user': 'anonym'})
        user.login_tries  = user.login_tries + 1
        db_commit(user)
        return redirect(url_for('app_auth.login'))
    elif user.login_locked():
        logger.info('user account locked because of too many false login attempts' + form.email.data, extra={'ip': request.remote_addr, 'user': 'anonym'})
        flash(message)
        return redirect(url_for('app_auth.login'))

    # if the user doesn't exist or password is wrong, reload the page
    # if the above check passes, then we know the user has the right credentials
    remember = True if form.remember.data else False
    session['remember'] = remember
    session['user_id'] = user.id

    if user.mfasecretkey is None:
        return redirect(url_for('app_mfa.signup_mfa'))
    else:
        if check_password_complexity(form.password.data) != '':
            session['breached'] = True
        logger.info('Successfully provided Login Data', extra={'ip': request.remote_addr, 'user': 'anonym'})
        return redirect(url_for('app_mfa.login_mfa'))


@app_auth.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')


@app_auth.route('/signup', methods=['POST'])
def signup_post():
    form = SignUpForm(request.form)
    if not form.validate():
        logger.info('invalid input in signup_form', extra={'ip': request.remote_addr, 'user': 'anonym'})
        flash('Invalid inputs')
        return redirect(url_for('app_auth.signup'))

    email = form.email.data
    username = form.username.data
    password = form.password.data

    user = User.query.filter((User.email == email) | (
            User.username == username)).first()  # if this returns a user, then the email already exists in database
    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        logger.info('tried to create a user with an  already existing email or username',
                    extra={'ip': request.remote_addr, 'user': 'anonym'})
        flash('Username or Email is already used')
        return redirect(url_for('app_auth.signup'))
    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    text = check_password_complexity(password)
    if text:
        logger.info('tried to create a user with an weak password',
                    extra={'ip': request.remote_addr, 'user': 'anonym'})
        flash(text)
        return redirect(url_for('app_auth.signup'))
    password = hash_password(password)
    new_user = user_datastore.create_user(username=username, email=email, password=password, roles=['end-user'])
    user_datastore.commit()
    session['user_id'] = new_user.id
    logger.info('user was created',
                extra={'ip': request.remote_addr, 'user': email})
    return redirect(url_for('app_mfa.signup_mfa'))


# todo add front end
@app_auth.route('/setpw', methods=['GET'])
@login_required
def set_new_password():
    if 'breached' not in session:
        return redirect(url_for('app_main.index'))
    return render_template('setpw.html')


@app_auth.route('/setpw', methods=['POST'])
@login_required
def set_new_password_post():
    if 'breached' not in session:
        return redirect(url_for('app_main.index'))
    form = ResetPasswordForm(request.form)
    password = form.password.data
    text = check_password_complexity(password)
    if text:
        logger.info('tried to create a user with an weak password',
                    extra={'ip': request.remote_addr, 'user': current_user.email})
        flash(text)
        return redirect(url_for('app_auth.set_new_password'))
    password = hash_password(password)
    current_user.password = password
    db_commit(current_user)
    session['breached'] = False
    return redirect(url_for('app_main.profile'))


@app_auth.route('/web/logout')
@login_required
def logout():
    logger.info('logged out',
                extra={'ip': request.remote_addr, 'user': current_user.email})
    logout_user()
    return redirect(url_for('app_auth.login'))


def check_password_complexity(password):
    password_message = []
    password_length_message = password_length_validator(password)
    if password_length_message:
        password_message += password_length_message
    password_complexity_message = password_complexity_validator(password, True)
    if password_complexity_message:
        password_message += password_complexity_message

    password_breached_message = password_breached_validator(password)
    if password_breached_message:
        password_message += password_breached_message
    text = ''
    for message in password_message:
        text += message
        text += '\n'
    return text
