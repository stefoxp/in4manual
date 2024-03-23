from flask import (
    Blueprint, render_template
)

bp = Blueprint('home', __name__)

@bp.route('/', methods=['GET'])
def home():
    return render_template("home.html")
