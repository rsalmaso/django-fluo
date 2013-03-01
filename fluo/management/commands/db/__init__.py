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

import os
from django.utils.importlib import import_module
from django.core.exceptions import ImproperlyConfigured
from fluo.management.commands.db.backends import ConnectionError, CreateDBError, DropDBError

__all__ = ['get_connection', 'ImproperlyConfigured', 'CreateDBError', 'DropDBError', 'ConnectionError']

def get_connection(database):
    engine = database['ENGINE'].split('.')[-1]
    options = {
        'host': database['HOST'],
        'port': database['PORT'],
        'password': database['PASSWORD'],
        'name': database['NAME'],
        'user': database['USER'],
        'db_dict': {'database': database['NAME']},
    }
    try:
        module = import_module('fluo.management.commands.db.backends.%s' % engine)
    except ImportError, e:
        try:
            module = import_module('.db_commands', engine)
        except ImportError, e_user:
            # The database backend wasn't found. Display a helpful error message
            # listing all possible (built-in) database backends.
            backend_dir = os.path.join(__path__[0], 'backends')
            try:
                available_backends = [f for f in os.listdir(backend_dir)
                        if os.path.isdir(os.path.join(backend_dir, f))
                        and not f.startswith('.')]
            except EnvironmentError:
                available_backends = []
            available_backends.sort()
            if engine not in available_backends:
                error_msg = "%r isn't an available database backend. Available options are: %s\nError was: %s" % \
                    (engine, ", ".join(map(repr, available_backends)), e_user)
                raise ImproperlyConfigured(error_msg)
            else:
                raise # If there's some other error, this must be an error in Django itself.
    try:
        return module.Database(**options)
    except Exception, e:
        print e
        raise ConnectionError('Cannot connect to database %(name)s' % options)

