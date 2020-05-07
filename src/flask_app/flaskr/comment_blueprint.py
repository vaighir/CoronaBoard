#!/usr/bin/env python3
from flask import (
    request, Blueprint, render_template, session, redirect,
    url_for, flash, g
    )
from . import db_comment_helper, comment
from mysql.connector import Error as mysql_error
import datetime


bp = Blueprint('comment_blueprint', __name__, url_prefix='/comment')


@bp.route('/show/<int:comment_id>', methods=('GET', 'POST'))
def show_post(comment_id):

    if session.get('user_id'):
        logged_user_id = int(session['user_id'])
    else:
        error = "You have to log in"
        flash(error)
        return redirect(url_for('index.index'))

    if request.method == 'POST':
        session['comment_to_delete'] = request.form['delete_id']
        return redirect(url_for('comment_blueprint.delete'))

    c = db_comment_helper.get_comment_by_id(comment_id)
    delete_rights = (logged_user_id == 1)

    return render_template(
                            "comment/comment.html", comment=c,
                            delete_rights=delete_rights)


@bp.route('/<int:post_id>/create', methods=('GET', 'POST'))
def create(post_id):

    if session.get('user_id'):
        logged_user_id = int(session['user_id'])
    else:
        error = "You have to log in"
        flash(error)
        return redirect(url_for('index.index'))

    if request.method == 'POST':
        description = request.form['description']
        error = None

        if not description:
            error = 'Description is required'

        if error is None:
            c = comment.Comment()
            c.author_id = logged_user_id
            c.post_id = post_id
            c.description = description
            c.created = datetime.datetime.now()

            try:
                db_comment_helper.insert_comment(c)
                return redirect(url_for('index.index'))
                message = "Comment created"
                flash(message)
            except mysql_error:
                error = "Oops, a database error occured :("

        flash(error)

    return render_template("comment/create_comment.html")


@bp.route('/delete', methods=('GET', 'POST'))
def delete():

    if session.get('user_id') == 1:
        pass
    else:
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
