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

from optparse import make_option
from django.core.management.base import BaseCommand

__all__ = ['DatabaseCommand']

class DatabaseCommand(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--noinput', action='store_false',
            dest='interactive', default=True,
            help='Tells Django to NOT prompt the user for input of any kind.'),
        make_option('--no-utf8', action='store_true',
            dest='no_utf8_support', default=False,
            help='Tells Django to not create a UTF-8 charset database'),
        make_option('-U', '--user', action='store',
            dest='user', default=None,
            help='Use another user for the database then defined in settings.py'),
        make_option('-P', '--password', action='store',
            dest='password', default=None,
            help='Use another password for the database then defined in settings.py'),
        make_option('-D', '--dbname', action='store',
            dest='dbname', default=None,
            help='Use another database name then defined in settings.py (For PostgreSQL this defaults to "template1")'),
    )
    requires_model_validation = False
