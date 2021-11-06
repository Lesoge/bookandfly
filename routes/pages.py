from flask import Blueprint, render_template

app_pages = Blueprint('app_pages', __name__)


@app_pages.route("/", methods=['GET'])
def startpage():
    return render_template('/index.html')

