#!/usr/bin/env python3
from flask import (
    request, Blueprint, render_template, session, redirect,
    url_for, flash, g
    )
from . import db_post_helper

bp = Blueprint('index', __name__, url_prefix='/')


@bp.route('/', methods=('GET', 'POST'))
def index():

    if request.method == 'POST':
        session['viewed_user_id'] = request.form['author_id']
        return redirect(url_for('user_blueprint.show_user'))

    posts = db_post_helper.get_posts()
    return render_template("index.html", posts=posts)


@bp.route('/test', methods=["GET"])
def error():
    return render_template("errors/404.html")
