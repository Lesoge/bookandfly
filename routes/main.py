from flask import Blueprint, render_template
from flask_login import login_required, current_user

from User import Flight

app_main = Blueprint('app_main', __name__)


@app_main.route('/', methods=['GET'])
def index():
    flights = Flight.query
    return render_template('index.html', flights=flights)


@app_main.route('/profile', methods=['GET'])
@login_required
def profile():
    return render_template('profile.html', user=current_user)
