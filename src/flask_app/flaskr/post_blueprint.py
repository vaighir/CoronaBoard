#!/usr/bin/env python3
import datetime
from flask import (
    request, Blueprint, render_template, session, redirect,
    url_for, flash, g
    )
from mysql.connector import Error as mysql_error
from werkzeug import exceptions as request_error
from . import db_post_helper, post
from . import db_comment_helper
from . import auth


bp = Blueprint('post_blueprint', __name__, url_prefix='/post')


@bp.route('/<int:post_id>', methods=('GET', 'POST'))
@auth.login_required
def show_post(post_id):

    logged_user_id = g.user.id

    if request.method == 'POST':
        post_to_delete = int(request.form['delete_id'])
        post_to_edit = int(request.form['edit_id'])
        if post_to_delete != 0:
            session['post_to_delete'] = post_to_delete
            return redirect(url_for('post_blueprint.delete'))
        if post_to_edit != 0:
            session['post_to_edit'] = post_to_edit
            return redirect(url_for('post_blueprint.edit'))

    post = db_post_helper.get_post_by_id(post_id)
    comments = db_comment_helper.get_comments_by_post_id(post_id)

    delete_rights = (logged_user_id == 1)
    edit_rights = (logged_user_id == 1 or logged_user_id == int(post.author_id))

    return render_template(
                            "post/post.html", post=post, comments=comments,
                            edit_rights=edit_rights,
                            delete_rights=delete_rights)


@bp.route('/create', methods=('GET', 'POST'))
@auth.login_required
def create():

    logged_user_id = g.user.id

    if request.method == 'POST':
        error = None

        try:
            title = request.form['title']
            title = title.strip()
        except request_error.BadRequestKeyError:
            error = 'Title is required.'

        if not title:
            error = "Title cannot be empty"

        try:
            category = request.form['category']
        except request_error.BadRequestKeyError:
            error = 'Category is required.'

        try:
            description = request.form['description']
            description = description.replace('\n', '<br>')
            description = description.strip()
        except request_error.BadRequestKeyError:
            error = 'Description is required'

        if not description:
            error = "Description cannot be empty"

        if error is None:
            p = post.Post()
            p.author_id = logged_user_id
            p.title = title
            p.category = category
            p.description = description
            p.created = datetime.datetime.now()
            p.edited = False

            try:
                db_post_helper.insert_post(p)
                message = "Post created"
                flash(message)
                return redirect(url_for('index.index'))
            except mysql_error:
                error = "Oops, a database error occured :("

        flash(error)

    return render_template("post/create_post.html")


@bp.route('/edit', methods=('GET', 'POST'))
@auth.login_required
def edit():

    logged_user_id = g.user.id

    p = db_post_helper.get_post_by_id(session.get('post_to_edit'))
    old_description = p.description
    old_description = old_description.replace('<br>', '\n')
    p.description = old_description

    if logged_user_id != 1 and logged_user_id != p.author_id:
        error = "You do not have rights to edit this post"
        flash(error)
        session.pop('post_to_edit')
        return redirect(url_for('index.index'))

    if request.method == 'POST':
        error = None
        message = None

        try:
            new_description = request.form['description']
            new_description = new_description.replace('\n', '<br>')
            new_description = new_description.strip()
        except request_error.BadRequestKeyError:
            error = 'Description cannot be empty'

        p.description = new_description

        try:
            db_post_helper.update_post(p)
            message = "Post updated!"
        except mysql_error:
            error = "Oops, something went wrong with the database :("

        if error:
            flash(error)
        elif message:
            flash(message)

        return redirect(url_for("index.index"))

    return render_template("post/edit_post.html", post=p)


@bp.route('/delete', methods=('GET', 'POST'))
@auth.login_required
def delete():

    if g.user.role != "admin":
        error = "Only the admin can delete posts"
        flash(error)
        return redirect(url_for('index.index'))

    if request.method == 'POST':
        p = db_post_helper.get_post_by_id(request.form['delete_id'])

        try:
            db_post_helper.delete_post(p)
            session.pop('post_to_delete')
            message = "Post deleted"
            flash(message)
        except mysql_error:
            session.pop('post_to_delete')
            error = "Oops, something went wrong with the database request"
            flash(error)

        return redirect(url_for('index.index'))

    p = db_post_helper.get_post_by_id(session.get('post_to_delete'))

    return render_template("post/delete_post.html", post=p)


def clean_up_session():
    if session.get('post_to_edit'):
        session.pop('post_to_edit')
    elif session.get('post_to_delete'):
        session.pop('post_to_delete')
