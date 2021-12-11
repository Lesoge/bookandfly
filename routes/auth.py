# login route for web interface
import logging

from flask_login import login_user, logout_user, current_user, login_required
from flask import Blueprint, render_template, session, abort, flash
from flask_security import hash_password, password_breached_validator, password_length_validator
from flask_security import password_complexity_validator
from dbModel import User, db, db_commit, user_datastore, security
from flask import (request, url_for, make_response,
                   redirect, render_template, session, current_app)
from Forms import LogInForm, SignUpForm

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

    email = form.email.data
    password = form.password.data
    remember = True if form.remember.data else False

    user = User.query.filter_by(email=email).first()
    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not user.check_password(password):
        logger.info('tried to log in as'+ email, extra={'ip': request.remote_addr, 'user':'anonym'})
        flash('Please check your login details and try again.')
        return redirect(url_for('app_auth.login'))  # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    session['remember'] = remember
    session['user_id'] = user.id

    if user.mfasecretkey is None:
        return redirect(url_for('app_mfa.signup_mfa'))
    else:
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



    user = User.query.filter((User.email == email) | (User.username == username)).first() # if this returns a user, then the email already exists in database
    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        logger.info('tried to create a user with an  already existing email or username', extra={'ip': request.remote_addr, 'user': 'anonym'})
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
                extra={'ip': request.remote_addr, 'user':email})
    return redirect(url_for('app_mfa.signup_mfa'))


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
    if password_message:
        for message in password_message:
            text += message
            text += '\n' 
    return text


@app_auth.route('/web/logout')
@login_required
def logout():
    logout_user()
    logger.info('logged out',
                extra={'ip': request.remote_addr, 'user':current_user.email})
    return redirect(url_for('app_auth.login'))
