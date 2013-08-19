# -*- coding: utf-8 -*-

# Copyright (C) 2007-2013, Raffaele Salmaso <raffaele@salmaso.org>
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
from django.utils.translation import ugettext as _
from django.core.exceptions import ImproperlyConfigured

__all__ = ['BaseDatabase', 'ConnectionError', 'CreateDBError', 'DropDBError', 'ImproperlyConfigured']

class ConnectionError(Exception):
    pass

class CreateDBError(Exception):
    pass

class DropDBError(Exception):
    pass

class BaseDatabase(object):
    def __init__(self, name, host, port, password, user, db_dict):
        self.host = host
        self.port = port
        self.password = password
        self.name = name
        self.user = user
        self.db_dict = db_dict
        self.connect()
    def connect(self):
        raise ImproperlyConfigured('connect is not implemented.')
    def close(self):
        raise ImproperlyConfigured('close is not implemented.')

    def do_createdb(self):
        raise ImproperlyConfigured('do_createdb is not implemented.')
    def createdb(self):
        try:
            print(_(u"Creating database %(database)s...") % self.db_dict)
            self.do_createdb()
            print(_(u"done"))
        except Exception, e:
            raise CreateDBError(_(u'Cannot create db: %(exception)s') % {'exception': e})

    def do_dropdb(self):
        raise ImproperlyConfigured('do_dropdb is not implemented.')
    def dropdb(self):
        try:
            print(_(u"Dropping database %(database)s...") % self.db_dict)
            self.do_dropdb()
            print(_(u"done"))
        except Exception, e:
            raise DropDBError(_(u'Cannot drop db: %(exception)s') % {'exception': e})

