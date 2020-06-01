#!/usr/bin/env python3
from flask import (
    Blueprint, render_template, redirect, url_for, flash
    )
import subprocess
import json


bp = Blueprint('covid_blueprint', __name__, url_prefix='/covid')


@bp.route('/', methods=('GET', 'POST'))
def show_stats():
    error = None
    url = 'https://api.covid19api.com/summary'
    response = subprocess.run(
        ['curl', '--location', '--request', 'GET', url], stdout=subprocess.PIPE
    ).stdout

    try:
        response_as_dictionary = json.loads(response)
        global_cases = response_as_dictionary['Global']
    except ValueError:
        error = """You cannot get covid info so often.
                Wait a moment before trying again."""

    if error is None:
        return render_template(
                            "covid_info.html",
                            global_cases=global_cases)

    else:
        flash(error)
        return redirect(url_for('index.index'))
