#!/usr/bin/env python3
import datetime
from flask import (
    request, Blueprint, render_template, session, redirect,
    url_for, flash, g
    )
from mysql.connector import Error as mysql_error
from werkzeug import exceptions as request_error
from . import db_comment_helper, comment
from. import auth


bp = Blueprint('comment_blueprint', __name__, url_prefix='/comment')


@bp.route('/show/<int:comment_id>', methods=('GET', 'POST'))
@auth.login_required
def show_comment(comment_id):

    logged_user_id = g.user.id

    if request.method == 'POST':
        session['comment_to_delete'] = request.form['delete_id']
        return redirect(url_for('comment_blueprint.delete'))

    c = db_comment_helper.get_comment_by_id(comment_id)
    delete_rights = (logged_user_id == 1)

    return render_template(
                            "comment/comment.html", comment=c,
                            delete_rights=delete_rights)


@bp.route('/<int:post_id>/create', methods=('GET', 'POST'))
@auth.login_required
def create(post_id):

    logged_user_id = g.user.id

    if request.method == 'POST':
        error = None

        try:
            description = request.form['description']
            description = description.replace('\n', '<br>')
            description = description.strip()
        except request_error.BadRequestKeyError:
            error = 'Description is required'

        if not description:
            error = 'Commet cannot be empty'

        if error is None:
            c = comment.Comment()
            c.author_id = logged_user_id
            c.post_id = post_id
            c.description = description
            c.created = datetime.datetime.now()

            try:
                db_comment_helper.insert_comment(c)
                message = "Comment created"
                flash(message)
                return redirect(url_for('index.index'))
            except mysql_error:
                error = "Oops, a database error occured :("

        flash(error)

    return render_template("comment/create_comment.html")


@bp.route('/delete', methods=('GET', 'POST'))
@auth.login_required
def delete():

    if g.user.role != "admin":
        error = "Only the admin can delete posts"
        flash(error)
        return redirect(url_for('index.index'))

    if request.method == 'POST':
        c = db_comment_helper.get_comment_by_id(request.form['delete_id'])

        try:
            db_comment_helper.delete_comment(c)
            session.pop('comment_to_delete')
            message = "Comment deleted"
            flash(message)
        except mysql_error:
            session.pop('comment_to_delete')
            error = "Oops, something went wrong with the database request"
            flash(error)

        return redirect(url_for('index.index'))

    c = db_comment_helper.get_comment_by_id(session.get('comment_to_delete'))

    return render_template("comment/delete_comment.html", comment=c)
