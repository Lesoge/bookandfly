# login route for web interface
import pyotp
from flask_login import login_user, logout_user, current_user
from flask import Blueprint, render_template, session, abort, flash
from flask_security import hash_password, password_breached_validator
from flask_security import password_complexity_validator
from User import User, db, db_commit, user_datastore, security
from flask import (request, url_for, make_response,
                   redirect, render_template, session, current_app)

app_auth = Blueprint('app_auth', __name__)


@app_auth.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app_auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    user = User.query.filter_by(email=email).first()
    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not user.check_password(password):
        flash('Please check your login details and try again.')
        return redirect(url_for('app_auth.login'))  # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    session['remember'] = remember
    session['user_id'] = user.id
    if user.mfasecretkey is None:
        return redirect(url_for('app_mfa.signup_mfa'))
    else:
        return redirect(url_for('app_mfa.login_mfa'))

    # old redirect to profile page
    # return redirect(url_for('app_main.profile'))


@app_auth.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')


@app_auth.route('/signup', methods=['POST'])
def signup_post():
    # TODO ADD Input Validation
    email = request.form.get('email')
    username = request.form.get('name')

    password = request.form.get('password')
    user = User.query.filter((User.email == email) | (
                User.username == username)).first()  # if this returns a user, then the email already exists in database
    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Username or Email is already used')
        return redirect(url_for('app_auth.signup'))
    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    text = check_password_complexity(password)
    if text:
        flash(text)
        return redirect(url_for('app_auth.signup'))
    password = hash_password(password)
    new_user = user_datastore.create_user(username=username, email=email, password=password, roles=['end-user'])
    user_datastore.commit()
    session['user_id'] = new_user.id
    return redirect(url_for('app_mfa.signup_mfa'))


def check_password_complexity(password):
    password_message = []
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
def logout():
    logout_user()
    return redirect(url_for('app_auth.login'))
