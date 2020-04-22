#!/usr/bin/env python3
from flask import request, Blueprint, jsonify, abort, current_app, render_template
from . import db_user_helper

bp = Blueprint('user_blueprint', __name__, url_prefix='/')


@bp.route('users', methods=["GET"])
def show_users():
    return "users"


@bp.route('user', methods=["GET"])
def show_user():
    # if user is the same as logged in user

    # else, if user id is not 1
    user = db_user_helper.get_user_by_id(1)
    # if user exists in database
    return render_template("user/user.html", user=user)
