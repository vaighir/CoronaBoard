#!/usr/bin/env python3
from flask import (
    request, Blueprint, render_template, session, redirect,
    url_for, flash
    )
from werkzeug.security import check_password_hash, generate_password_hash
from . import db_user_helper, user
from mysql.connector import Error as mysql_error


bp = Blueprint('user_blueprint', __name__, url_prefix='/')


@bp.route('/users', methods=('GET', 'POST'))
def show_users():
    if request.method == 'POST':
        session['viewed_user_id'] = request.form['id']
        return redirect(url_for('user_blueprint.show_user'))
    users = db_user_helper.get_users()
    return render_template("user/users.html", users=users)


@bp.route('/user', methods=["GET"])
def show_user():

    if session.get('user_id'):
        logged_user_id = int(session['user_id'])
    else:
        return "You have to log in"

    if session.get('viewed_user_id'):
        viewed_user_id = int(session['viewed_user_id'])

        session.pop('viewed_user_id')
    else:
        viewed_user_id = logged_user_id

    user = db_user_helper.get_user_by_id(viewed_user_id)

    delete_rights = (logged_user_id == 1)
    edit_rights = (logged_user_id == 1 or logged_user_id == viewed_user_id)

    return render_template(
                            "user/user.html", user=user,
                            edit_rights=edit_rights,
                            delete_rights=delete_rights)


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not email:
            error = 'Email is required'
        # elif get user by username
        elif db_user_helper.get_user_by_username(username) is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            u = user.User()
            u.username = username
            u.password = (generate_password_hash(password))
            u.email = email

            try:
                db_user_helper.insert_user(u)
                # return redirect(url_for('user.login'))
                return "User created"
            except mysql_error:
                error = "A user with this email address is already registered."

        flash(error)

    return render_template("user/register.html")


@bp.route('/edituser', methods=('GET', 'POST'))
def edit():
    user = db_user_helper.get_user_by_id(2)
    return render_template("user/edit_user.html", user=user)


@bp.route('/deleteuser', methods=('GET', 'POST'))
def delete():
    yield


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
            #return redirect(url_for('index'))
            return "Logged in"

        flash(error)
    return render_template("user/login.html")


@bp.route('/logout')
def logout():
    session.clear()
    # return redirect(url_for('index'))
    return "Logged out"
