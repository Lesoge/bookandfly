from flask import Blueprint, render_template

app_pay = Blueprint('app_pages', __name__)


@app_pay.route("/", methods=['GET'])
def pay():
    return render_template('/index.html')
