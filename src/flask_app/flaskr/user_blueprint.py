#!/usr/bin/env python3
from flask import (
    request, Blueprint, render_template, session, redirect,
    url_for, flash, g
    )
from werkzeug.security import check_password_hash, generate_password_hash
from . import db_user_helper, user
from . import db_post_helper, post
from mysql.connector import Error as mysql_error


bp = Blueprint('user_blueprint', __name__, url_prefix='/')


@bp.route('/users', methods=('GET', 'POST'))
def show_users():

    if not session.get('user_id'):
        error = "You have to log in"
        flash(error)
        return redirect(url_for('index.index'))

    if request.method == 'POST':
        session['viewed_user_id'] = request.form['id']
        return redirect(url_for('user_blueprint.show_user'))

    users = db_user_helper.get_users()
    return render_template("user/users.html", users=users)


@bp.route('/user', methods=('GET', 'POST'))
def show_user():

    if session.get('user_id'):
        logged_user_id = int(session['user_id'])
    else:
        error = "You have to log in"
        flash(error)
        return redirect(url_for('index.index'))

    if request.method == 'POST':
        user_to_delete = int(request.form['delete_id'])
        user_to_edit = int(request.form['edit_id'])
        if user_to_delete != 0:
            session['user_to_delete'] = user_to_delete
            return redirect(url_for('user_blueprint.delete'))
        if user_to_edit != 0:
            session['user_to_edit'] = user_to_edit
            return redirect(url_for('user_blueprint.edit'))

    if session.get('viewed_user_id'):
        viewed_user_id = int(session['viewed_user_id'])

        session.pop('viewed_user_id')
    else:
        viewed_user_id = logged_user_id

    user = db_user_helper.get_user_by_id(viewed_user_id)

    posts = db_post_helper.get_posts_by_user_id(viewed_user_id)

    delete_rights = (logged_user_id == 1)
    edit_rights = (logged_user_id == 1 or logged_user_id == viewed_user_id)

    return render_template(
                            "user/user.html", user=user, posts=posts,
                            edit_rights=edit_rights,
                            delete_rights=delete_rights)


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        email = request.form['email']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif password != password2:
            error = "Passwords must match"
        elif not email:
            error = 'Email is required'
        elif db_user_helper.get_user_by_username(username) is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            u = user.User()
            u.username = username
            u.password = (generate_password_hash(password))
            u.email = email

            try:
                db_user_helper.insert_user(u)
                return redirect(url_for('user_blueprint.login'))
            except mysql_error:
                error = "A user with this email address is already registered."

        flash(error)

    return render_template("user/register.html")


@bp.route('/edituser', methods=('GET', 'POST'))
def edit():

    if session.get('user_id'):
        logged_user_id = int(session['user_id'])
    else:
        error = "You have to log in"
        flash(error)
        return redirect(url_for('index.index'))

    edit_user_id = int(session.get('user_to_edit'))

    if logged_user_id != 1 and logged_user_id != edit_user_id:
        error = "You do not have rights to edit this user"
        flash(error)
        session.pop('user_to_edit')
        return redirect(url_for('index.index'))

    u = db_user_helper.get_user_by_id(edit_user_id)

    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        new_password2 = request.form['new_password2']
        email = request.form['email']
        error = None
        message = None

        if not check_password_hash(u.password, old_password):
            error = 'Incorrect password.'
            flash(error)
            return redirect(url_for("user_blueprint.edit", user=u))

        if new_password:
            if new_password == old_password:
                error = 'New password has to be new'
            elif new_password != new_password2:
                error = 'Passwords must match'
            else:
                u.password = (generate_password_hash(new_password))
                message = "User updated!"
                try:
                    db_user_helper.update_user_password(u)
                except mysql_error:
                    error = "Oops, something went wrong with the database"

        if email:
            u.email = email
            try:
                db_user_helper.update_user_email(u)
                message = "User updated!"
            except mysql_error:
                error = "A user with this email already exists in our database"

        if error:
            flash(error)
        elif message:
            flash(message)

        return redirect(url_for("index.index"))

    return render_template("user/edit_user.html", user=u)


@bp.route('/deleteuser', methods=('GET', 'POST'))
def delete():

    if session.get('user_id') == 1:
        pass
    else:
        error = "You have to log in"
        flash(error)
        return redirect(url_for('index.index'))

    if request.method == 'POST':
        uid = request.form['delete_id']
        u = db_user_helper.get_user_by_id(uid)

        try:
            db_user_helper.delete_user(u)
            session.pop('user_to_delete')
            message = "User deleted"
            flash(message)
        except mysql_error:
            session.pop('user_to_delete')
            error = "Oops, something went wrong with the database request"
            flash(error)

        return redirect(url_for('index.index'))

    delete_user_id = session.get('user_to_delete')
    u = db_user_helper.get_user_by_id(delete_user_id)

    return render_template("user/delete_user.html", user=u)


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
    session.clear()
    return redirect(url_for('index.index'))


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db_user_helper.get_user_by_id(user_id)
