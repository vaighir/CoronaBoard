#!/usr/bin/env python3
from . import db_connector
from . import comment
from . import db_user_helper
from . import db_post_helper


def parse_mysql_response(mysql_response):
    c = comment.Comment()
    c.id = mysql_response[0]
    c.author_id = mysql_response[1]
    c.author = db_user_helper.get_user_by_id(mysql_response[1])
    c.post_id = mysql_response[2]
    c.post_title = db_post_helper.get_post_by_id(mysql_response[2]).title
    c.description = mysql_response[3]
    c.created = mysql_response[4]
    return c


def get_comment_by_id(comment_id):
    mydb, cursor = db_connector.connect()
    query = """SELECT * FROM comment where id = %s"""
    cursor.execute(query, (comment_id,))
    mysql_response = cursor.fetchone()
    if not mysql_response:
        return None
    comment = parse_mysql_response(mysql_response)
    cursor.close()
    mydb.close()
    return comment


def get_comments_by_post_id(post_id):
    mydb, cursor = db_connector.connect()
    query = """SELECT * FROM comment WHERE post_id = %s
               ORDER BY created DESC"""
    cursor.execute(query, (post_id,))
    comments = []
    mysql_response = cursor.fetchone()
    while mysql_response:
        c = parse_mysql_response(mysql_response)
        comments.append(c)
        mysql_response = cursor.fetchone()
    cursor.close()
    mydb.close()
    return comments


def insert_comment(comment):
    mydb, cursor = db_connector.connect()
    query = """INSERT INTO comment (user_id, post_id, description, created)
               VALUES (%s,%s,%s,%s)"""
    cursor.execute(
                query,
                (comment.author_id, comment.post_id, comment.description, comment.created.strftime('%Y-%m-%d %H:%M:%S')))
    mydb.commit()
    cursor.close()
    mydb.close()


def delete_comment(comment):
    mydb, cursor = db_connector.connect()
    query = """DELETE FROM comment WHERE id = %s"""
    cursor.execute(
                query, (comment.id,))
    mydb.commit()
    cursor.close()
    mydb.close()
