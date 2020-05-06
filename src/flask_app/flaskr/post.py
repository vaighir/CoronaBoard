#!/usr/bin/env python3
import datetime


class Post:
    id = 0
    author_id = 0
    author = ""
    title = ""
    category = ""
    description = ""
    created = datetime.datetime(1900, 1, 1, 0, 0, 0)
    edited = False

    def __init__(self):
        self.edited = False
