#!/usr/bin/env python3
import db_connector


def get_users():
    mydb, cursor = db_connector.connect()
    query = """SELECT * FROM user"""
    cursor.execute(query)
    users = cursor.fetchall()
    cursor.close()
    mydb.close()
    return users


def get_user_by_username(username):
    mydb, cursor = db_connector.connect()
    query = """SELECT * FROM user where username = %s"""
    cursor.execute(query, (username,))
    user = cursor.fetchall()
    cursor.close()
    mydb.close()
    return user


def get_user_by_id(user_id):
    mydb, cursor = db_connector.connect()
    query = """SELECT * FROM user where id = %s"""
    cursor.execute(query, (user_id,))
    user = cursor.fetchall()
    cursor.close()
    mydb.close()
    return user


def create_user(user):
    yield


def update_user(user):
    yield


def delete_user(user):
    yield
