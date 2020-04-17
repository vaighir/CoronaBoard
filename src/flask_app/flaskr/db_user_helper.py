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
