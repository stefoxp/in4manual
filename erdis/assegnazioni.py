from flask import (
    Blueprint, flash, redirect, render_template, request, make_response
)
from library import pandas_days_for_month

bp = Blueprint('assegnazioni', __name__)

ALLOWED_EXTENSIONS = {'csv'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/assegnazioni', methods=['GET', 'POST'])
def assegnazioni():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('Nessun file selezionato')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            result = pandas_days_for_month.main(file)
            response = make_response(result)
            response.headers["Content-Disposition"] = "attachment; filename=CALCOLATO_" + file.filename + ""
            return response

    return render_template("assegnazioni.html")
