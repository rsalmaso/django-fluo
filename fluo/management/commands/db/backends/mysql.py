# -*- coding: utf-8 -*-

# Copyright (C) 2007-2010, Salmaso Raffaele <raffaele@salmaso.org>
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

import _mysql
from django.utils.translation import ugettext as _
from fluo.management.commands.db.backends import BaseDatabase

__all__ = ['Database']

class Database(BaseDatabase):
    def connect(self):
        self.connection = _mysql.connect(
            host=self.host,
            user=self.user,
            passwd=self.password,
        )
    def close(self):
        if self.connection:
            self.connection.close()
        self.connection = None
    def do_createdb(self):
        self.connection.query('CREATE DATABASE %s CHARACTER SET utf8 COLLATE utf8_general_ci' % self.name)
    def do_dropdb(self):
        self.connection.query("DROP DATABASE IF EXISTS %s" % self.name)

