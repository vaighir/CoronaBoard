#!/usr/bin/env python3
import os
import mysql.connector

db_name = os.environ["MYSQL_DATABASE"]
db_user = os.environ["MYSQL_USER"]
db_pwd = os.environ["MYSQL_PASSWORD"]
db_hostname = os.environ["MYSQL_HOSTNAME"]
db_port = os.environ["MYSQL_PORT"]


def connect():
    mydb = mysql.connector.connect(
        host=db_hostname, user=db_user, passwd=db_pwd, port=db_port,
        database=db_name)
    cursor = mydb.cursor(prepared=True)
    return mydb, cursor


def get_posts():
    yield


def get_post_by_id(post_id):
    yield


def get_posts_by_user_id(user_id):
    yield


def create_post(post):
    yield


def update_post(post):
    yield


def delete_post(post):
    yield


def get_comments_by_post_id(post_id):
    yield


def create_comment(comment):
    yield


def delete_comment(comment):
    yield
