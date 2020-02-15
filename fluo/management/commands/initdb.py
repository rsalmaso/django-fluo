# Copyright (C) 2007-2020, Raffaele Salmaso <raffaele@salmaso.org>
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

from django.core.management import call_command

from ..database import DatabaseCommand


class Command(DatabaseCommand):
    help = "(Re)create and initialize database with common data"
    message = """You have requested to create "%(name)s" database.
This will IRREVERSIBLY DELETE all data currently in the "%(name)s" database if already exists,
and then will create a new database.
Are you sure you want to do this?"""
    error_message = """Database %(name)s couldn't be dropped. Possible reasons:
  * The database isn't running or isn't configured correctly.
  * The database is in use by another user.
The full error: %(error)s"""

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            '--noadmin',
            action='store_false',
            dest='noadmin',
            default=True,
            help='Tells Django to NOT create a default admin user.',
        )

    def execute_sql(self, backend, **options):
        backend.dropdb()
        backend.createdb()

    def migrate(self):
        call_command('migrate')

    def post_execute(self, **options):
        self.migrate()
        if options.get('noadmin'):
            call_command('load_admin_data')
