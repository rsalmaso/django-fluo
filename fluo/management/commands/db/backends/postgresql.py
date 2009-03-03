# -*- coding: utf-8 -*-

# Copyright (C) 2007-2009, Salmaso Raffaele <raffaele@salmaso.org>
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

from django.utils.importlib import import_module
from django.utils.translation import ugettext as _
from fluo.management.commands.db.backends import BaseDatabase

__all__ = ['Database']

class Postgresql(BaseDatabase):
    def connect(self):
        module = import_module(self.module)
        if self.name == '':
            raise AssertionError("You must specify a value for DATABASE_NAME in local_settings.py.")
        if self.user == '':
            raise AssertionError("You must specify a value for DATABASE_USER in local_settings.py.")
        conn_string = [ "dbname=template1" ]
        if self.user:
            conn_string.append("user=%s" % self.user)
        if self.password:
            conn_string.append("password='%s'" % self.password)
        if self.host:
            conn_string.append("host=%s" % self.host)
        if self.port:
            conn_string.append("port=%s" % self.port)

        self.connection = module.connect(' '.join(conn_string))
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

    def do_createdb(self):
        self.cursor.execute("CREATE DATABASE %s OWNER %s ENCODING 'UTF8'" % (self.name, self.user,))
    def do_dropdb(self):
        self.cursor.execute("DROP DATABASE IF EXISTS %s" % self.name)

class Database(Postgresql):
    module = 'psycopg'

