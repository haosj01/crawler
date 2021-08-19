#!/usr/bin/python
# -*- coding: UTF-8 -*-

class DatabaseIndexException(Exception):

    def __init__(self, err='database index must be unique'):
        Exception.__init__(self, err)
