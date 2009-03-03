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
from django.core.management import call_command
from django.conf import settings
from fluo.management import DatabaseCommand
from fluo.management.commands.db import connection, CreateDBError, DropDBError
INSTALLED_APPS = settings.INSTALLED_APPS

class Command(DatabaseCommand):
    help = "(Re)create and initialize database with common data"

    def handle(self, *args, **options):
        if options.get('interactive'):
            confirm = raw_input("""
You have requested a database reset.
This will IRREVERSIBLY DESTROY
ALL data in the database "%s".
Are you sure you want to do this?

Type 'yes' to continue, or 'no' to cancel: """ % (settings.DATABASE_NAME,))
        else:
            confirm = 'yes'

        if confirm != 'yes':
            print "Reset cancelled."
            return

        try:
            connection.dropdb()
        except DropDBError, e:
            print e
            call_command('resetdb')
        else:
            try:
                connection.createdb()
            except CreateDBError, e:
                print e
        connection.close()

        call_command('syncdb', interactive=False)
        call_command('load_admin_data')

