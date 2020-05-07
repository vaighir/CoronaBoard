#!/usr/bin/env python3
import datetime


class Comment:
    id = 0
    author_id = 0
    post_id = 0
    author = ""
    post_title = ""
    description = ""
    created = datetime.datetime(1900, 1, 1, 0, 0, 0)

    def __init__(self):
        self.created = datetime.datetime(1900, 1, 1, 0, 0, 0)
