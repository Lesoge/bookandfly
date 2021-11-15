# login route for web interface
import pyotp
from flask_login import login_user, logout_user, current_user
from flask import Blueprint, render_template, session, abort, flash
from User import User, db
from flask import (request, url_for, make_response,
                   redirect, render_template, session)

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
    if not user or user.check_password(password):
        flash('Please check your login details and try again.')
        return redirect(url_for('app_auth.login'))  # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)

    # TODO Sicherheitscheck laut flask login doc:
    # @app.route('/login', methods=['GET', 'POST'])
    # def login():
    #     # Here we use a class of some kind to represent and validate our
    #     # client-side form data. For example, WTForms is a library that will
    #     # handle this for us, and we use a custom LoginForm to validate.
    #     form = LoginForm()
    #     if form.validate_on_submit():
    #         # Login and validate the user.
    #         # user should be an instance of your `User` class
    #         login_user(user)
    #
    #         flask.flash('Logged in successfully.')
    #
    #         next = flask.request.args.get('next')
    #         # is_safe_url should check if the url is safe for redirects.
    #         # See http://flask.pocoo.org/snippets/62/ for an example.
    #         if not is_safe_url(next):
    #             return flask.abort(400)
    #
    #         return flask.redirect(next or flask.url_for('index'))
    #     return flask.render_template('login.html', form=form)

    # TODO redirect to mfa page
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
    name = request.form.get('name')
    password = request.form.get('password')
    user = User.query.filter_by(
        email=email).first()  # if this returns a user, then the email already exists in database
    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        return redirect(url_for('app_auth.signup'))
    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(username=name, email=email, password=password)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('app_auth.login'))


@app_auth.route('/web/logout')
def logout():
    logout_user()
    return redirect(url_for('app_auth.login'))
