#!/usr/bin/env python3
from . import db_connector
from . import user


def parse_mysql_response(mysql_response):
    u = user.User()
    u.id = mysql_response[0][0]
    u.username = mysql_response[0][1]
    u.email = mysql_response[0][2]
    u.role = mysql_response[0][3]
    u.password = mysql_response[0][4]
    return u


def get_users():
    mydb, cursor = db_connector.connect()
    query = """SELECT * FROM user"""
    cursor.execute(query)
    mysql_response = cursor.fetchall()
    cursor.close()
    mydb.close()
    users = set()
    for response in mysql_response():
        u = parse_mysql_response(response)
        users.add(u)
    return users


def get_user_by_username(username):
    mydb, cursor = db_connector.connect()
    query = """SELECT * FROM user where username = %s"""
    cursor.execute(query, (username,))
    mysql_response = cursor.fetchall()
    # if not mysql_response: // if mysql response is an empty list
    user = parse_mysql_response(mysql_response)
    cursor.close()
    mydb.close()
    return user


def get_user_by_id(user_id):
    mydb, cursor = db_connector.connect()
    query = """SELECT * FROM user where id = %s"""
    cursor.execute(query, (user_id,))
    mysql_response = cursor.fetchall()
    user = parse_mysql_response(mysql_response)
    cursor.close()
    mydb.close()
    return user


def insert_user(user):
    mydb, cursor = db_connector.connect()
    query = """INSERT INTO user (username, email, role, password)
               VALUES (%s,%s,%s,%s)"""
    cursor.execute(
                query, (user.username, user.email, user.role, user.password))
    mydb.commit()
    cursor.close()
    mydb.close()


def update_user_email(user):
    mydb, cursor = db_connector.connect()
    query = """UPDATE user set email = %s WHERE id = %s"""
    cursor.execute(query, (user.email, user.id))
    mydb.commit()
    cursor.close()
    mydb.close()


def update_user_password(user):
    mydb, cursor = db_connector.connect()
    query = """UPDATE user set password = %s WHERE id = %s"""
    cursor.execute(query, (user.password, user.id))
    mydb.commit()
    cursor.close()
    mydb.close()


def delete_user(user):
    mydb, cursor = db_connector.connect()
    query = """DELETE FROM user WHERE id = %s"""
    cursor.execute(
                query, (user.id,))
    mydb.commit()
    cursor.close()
    mydb.close()
