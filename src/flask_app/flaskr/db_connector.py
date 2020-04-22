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
