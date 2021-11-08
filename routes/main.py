from flask import Blueprint, render_template
from flask_login import login_required, current_user

app_main = Blueprint('app_main', __name__)


@app_main.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app_main.route('/profile', methods=['GET'])
@login_required
def profile():
    return render_template('profile.html', name=current_user.username)
