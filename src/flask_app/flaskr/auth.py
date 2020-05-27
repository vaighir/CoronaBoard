import functools

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from. import db_user_helper


bp = Blueprint("auth", __name__, url_prefix="/")


@bp.before_app_request
def load_logged_in_user():
    """This function is taken directly from Flask tutorial"""
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db_user_helper.get_user_by_id(user_id)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = db_user_helper.get_user_by_username(username)

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('index.index'))

        flash(error)
    return render_template("user/login.html")


@bp.route('/logout')
def logout():
    """This function is taken directly from Flask tutorial"""
    session.clear()
    return redirect(url_for('index.index'))


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            error = "You have to log in"
            flash(error)
            return redirect(url_for("index.index"))

        return view(**kwargs)

    return wrapped_view
