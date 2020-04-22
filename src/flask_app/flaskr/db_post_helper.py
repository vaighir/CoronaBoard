#!/usr/bin/env python3
import db_connector


def get_posts():
    mydb, cursor = db_connector.connect()
    query = """SELECT * FROM post ORDER BY created DESC"""
    cursor.execute(query)
    users = cursor.fetchall()
    cursor.close()
    mydb.close()
    return users


def get_post_by_user_id(user_id):
    mydb, cursor = db_connector.connect()
    query = """SELECT * FROM post where user_id = %s"""
    cursor.execute(query, (user_id,))
    user = cursor.fetchall()
    cursor.close()
    mydb.close()
    return user


def get_post_by_id(post_id):
    mydb, cursor = db_connector.connect()
    query = """SELECT * FROM post where id = %s"""
    cursor.execute(query, (post_id,))
    user = cursor.fetchall()
    cursor.close()
    mydb.close()
    return user


def insert_post(post):
    mydb, cursor = db_connector.connect()
    query = """INSERT INTO user (user_id, title, category, description, created)
               VALUES (%s,%s,%s,%s,%s)"""
    cursor.execute(
                query, (post.user_id, post.title, post.category, post.description, post.created))
    mydb.commit()
    cursor.close()
    mydb.close()


def update_post(post):
    mydb, cursor = db_connector.connect()
    query = """UPDATE post set description = %s WHERE id = %s"""
    cursor.execute(query, (post.description, post.id))
    mydb.commit()
    query = """UPDATE post set edited = %s WHERE id = %s"""
    cursor.execute(query, (post.edited, post.id))
    mydb.commit()
    cursor.close()
    mydb.close()


def delete_post(post):
    mydb, cursor = db_connector.connect()
    query = """DELETE FROM post WHERE id = %s"""
    cursor.execute(
                query, (post.id,))
    mydb.commit()
    cursor.close()
    mydb.close()
