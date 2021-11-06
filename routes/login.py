# login route for web interface
from flask_login import login_user, logout_user
from flask import Blueprint, render_template, session, abort
from User import User
from flask import (request, url_for, make_response,
                   redirect, render_template, session)

app_login = Blueprint('app_login', __name__)


@app_login.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if not user:
            return "Wrong Credentials"
        if not user.check_password(password):
            return "Wrong Credentials"
        login_user(user)
        return redirect(url_for('car'))
    return render_template('login.html')


@app_login.route('/web/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
