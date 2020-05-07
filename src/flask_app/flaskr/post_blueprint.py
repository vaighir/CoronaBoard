#!/usr/bin/env python3
from flask import (
    request, Blueprint, render_template, session, redirect,
    url_for, flash, g
    )
from . import db_post_helper, post
from mysql.connector import Error as mysql_error
import datetime


bp = Blueprint('post_blueprint', __name__, url_prefix='/post')


@bp.route('/<int:post_id>', methods=('GET', 'POST'))
def show_post(post_id):

    if session.get('user_id'):
        logged_user_id = int(session['user_id'])
    else:
        error = "You have to log in"
        flash(error)
        return redirect(url_for('index.index'))

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

    delete_rights = (logged_user_id == 1)
    edit_rights = (logged_user_id == 1 or logged_user_id == int(post.author_id))

    return render_template(
                            "post/post.html", post=post,
                            edit_rights=edit_rights,
                            delete_rights=delete_rights)


@bp.route('/create', methods=('GET', 'POST'))
def create():

    if session.get('user_id'):
        logged_user_id = int(session['user_id'])
    else:
        error = "You have to log in"
        flash(error)
        return redirect(url_for('index.index'))

    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        description = request.form['description']
        error = None

        if not title:
            error = 'Title is required.'
        elif not category:
            error = 'Category is required.'
        elif not description:
            error = 'Description is required'

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
                return redirect(url_for('index.index'))
                message = "Post created"
                flash(message)
            except mysql_error:
                error = "Oops, a database error occured :("

        flash(error)

    return render_template("post/create_post.html")


@bp.route('/edit', methods=('GET', 'POST'))
def edit():

    if session.get('user_id'):
        logged_user_id = int(session['user_id'])
    else:
        error = "You have to log in"
        flash(error)
        return redirect(url_for('index.index'))

    p = db_post_helper.get_post_by_id(session.get('post_to_edit'))

    if logged_user_id != 1 and logged_user_id != p.author_id:
        error = "You do not have rights to edit this user"
        flash(error)
        session.pop('user_to_edit')
        return redirect(url_for('index.index'))

    if request.method == 'POST':
        new_description = request.form['description']
        error = None
        message = None

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
def delete():

    if session.get('user_id') == 1:
        pass
    else:
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
