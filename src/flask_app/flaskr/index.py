#!/usr/bin/env python3
from flask import (
    request, Blueprint, render_template, session, redirect,
    url_for, flash, g
    )
from . import db_post_helper

bp = Blueprint('index', __name__, url_prefix='/')


@bp.route('/', methods=('GET', 'POST'))
def index():

    posts = db_post_helper.get_posts()
    return render_template("index.html", posts=posts)


@bp.route('/posts', methods=('GET', 'POST'))
def show_posts_by_category():

    category = request.form['category']
    posts = db_post_helper.get_posts_by_category(category)
    return render_template("index.html", posts=posts)


@bp.route('/test', methods=["GET"])
def error404():
    return render_template("errors/404.html")
