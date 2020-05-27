#!/usr/bin/env python3
from . import db_connector
from . import post
from . import db_user_helper


def parse_mysql_response(mysql_response):
    p = post.Post()
    p.id = mysql_response[0]
    p.author_id = mysql_response[1]
    p.author = db_user_helper.get_user_by_id(mysql_response[1])
    p.title = mysql_response[2]
    p.category = mysql_response[3]
    p.description = mysql_response[4]
    p.created = mysql_response[5]
    p.edited = mysql_response[6]
    return p


def get_posts():
    mydb, cursor = db_connector.connect()
    query = """SELECT * FROM post"""
    cursor.execute(query)
    posts = []
    mysql_response = cursor.fetchone()
    while mysql_response:
        p = parse_mysql_response(mysql_response)
        posts.append(p)
        mysql_response = cursor.fetchone()
    cursor.close()
    mydb.close()
    return posts


def get_posts_by_category(category):
    mydb, cursor = db_connector.connect()
    query = """SELECT * FROM post where category = %s"""
    cursor.execute(query, (category,))
    posts = []
    mysql_response = cursor.fetchone()
    while mysql_response:
        p = parse_mysql_response(mysql_response)
        posts.append(p)
        mysql_response = cursor.fetchone()
    cursor.close()
    mydb.close()
    return posts


def get_post_by_id(post_id):
    mydb, cursor = db_connector.connect()
    query = """SELECT * FROM post where id = %s"""
    cursor.execute(query, (post_id,))
    mysql_response = cursor.fetchone()
    if not mysql_response:
        return None
    post = parse_mysql_response(mysql_response)
    cursor.close()
    mydb.close()
    return post


def get_posts_by_user_id(user_id):
    mydb, cursor = db_connector.connect()
    query = """SELECT * FROM post WHERE user_id = %s"""
    cursor.execute(query, (user_id,))
    posts = []
    mysql_response = cursor.fetchone()
    while mysql_response:
        p = parse_mysql_response(mysql_response)
        posts.append(p)
        mysql_response = cursor.fetchone()
    cursor.close()
    mydb.close()
    return posts


def insert_post(post):
    mydb, cursor = db_connector.connect()
    query = """INSERT INTO post (user_id, title, category, description, created)
               VALUES (%s,%s,%s,%s, %s)"""
    cursor.execute(
                query,
                (post.author_id, post.title, post.category, post.description, post.created.strftime('%Y-%m-%d %H:%M:%S')))
    mydb.commit()
    cursor.close()
    mydb.close()


def update_post(post):
    mydb, cursor = db_connector.connect()
    query = """UPDATE post set description = %s WHERE id = %s"""
    cursor.execute(query, (post.description, post.id))
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
