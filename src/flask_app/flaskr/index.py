#!/usr/bin/env python3
from flask import request, Blueprint, jsonify, abort, current_app, render_template

bp = Blueprint('index', __name__, url_prefix='/')


@bp.route('/', methods=["GET"])
def index():
    name = "Tester"
    posts = ["First", "Second", "Third", "Fourth"]
    return render_template("index.html", name=name, posts=posts)
