#!/usr/bin/env python3
from flask import (
    request, Blueprint, render_template, session, redirect,
    url_for, flash, g
    )
from werkzeug import exceptions as request_error
from . import db_post_helper

bp = Blueprint('index', __name__, url_prefix='/')


@bp.route('/', methods=('GET', 'POST'))
def index():

    posts = db_post_helper.get_posts()
    return render_template("index.html", posts=posts)


@bp.route('/posts', methods=('GET', 'POST'))
def show_posts_by_category():

    error = None

    try:
        category = request.form['category']
    except request_error.BadRequestKeyError:
        error = 'Category is required.'

    if error is None:

        posts = db_post_helper.get_posts_by_category(category)
        return render_template("index.html", posts=posts)

    posts = db_post_helper.get_posts()
    flash(error)
    return render_template("index.html", posts=posts)
