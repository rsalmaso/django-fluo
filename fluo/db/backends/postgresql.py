# -*- coding: utf-8 -*-

# Copyright (C) 2007-2016, Raffaele Salmaso <raffaele@salmaso.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from __future__ import absolute_import, division, print_function, unicode_literals
import psycopg2
from .. import backend


__all__ = ['Backend']


class Backend(backend.Backend):
    def connect(self):
        if self.name == '':
            raise AssertionError("You must specify a value for database NAME in settings file.")
        if self.user == '':
            raise AssertionError("You must specify a value for database USER in settings file.")
        conn_string = ["dbname=postgres"]
        if self.user:
            conn_string.append("user=%s" % self.user)
        if self.password:
            conn_string.append("password='%s'" % self.password)
        if self.host:
            conn_string.append("host=%s" % self.host)
        if self.port:
            conn_string.append("port=%s" % self.port)

        self.connection = psycopg2.connect(' '.join(conn_string))
        try:
            self.connection.autocommit = True
        except Exception:
            self.connection.set_isolation_level(0)
        self.connection.set_client_encoding('UTF8')
        self.cursor = self.connection.cursor()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        self.connection = None
        self.cursor = None

    def createdb(self):
        self.cursor.execute("CREATE DATABASE %s OWNER %s ENCODING 'UTF8'" % (self.name, self.user,))

    def dropdb(self):
        self.cursor.execute("DROP DATABASE IF EXISTS %s" % (self.name,))
